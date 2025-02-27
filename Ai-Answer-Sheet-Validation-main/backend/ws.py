import asyncio
import os
import uuid,json, threading, re, requests
from aiohttp import web
from main import process_data
from utils import *
from pyppeteer import launch


# Store active WebSocket connections and their session IDs
connections = {}

IMG_API = "cad83bb4de3a9abbb44cd84beab8a19f"

async def upload_image_to_firebase(image_path: str, folder_path) -> str:
    url = f"https://api.imgbb.com/1/upload?&key={IMG_API}"
    with open(image_path, "rb") as image_file:
        files = {"image": image_file}
        response = requests.post(url, files=files)

    if response.status_code == 200:
        data = response.json()
        if data.get("success"):
            return data["data"]["url"]
        else:
            print(f"Error: {data.get('error', {}).get('message', 'Unknown error')}")
    else:
        print(f"HTTP Error: {response.status_code} - {response.text}")

    if os.path.exists(image_path):
        os.remove(image_path)
    return None

EDGE_EXECUTABLE_PATH = "/usr/bin/google-chrome"

async def intercept_requests(image_path):

    browser = await launch(
        headless=True, 
        executablePath=EDGE_EXECUTABLE_PATH,
        args=["--no-sandbox", "--disable-setuid-sandbox"]
    )
    page = await browser.newPage()
    extracted_text_t = ""
    for i in image_path:
        d_url = await upload_image_to_firebase(i,None)
        lens_url = f"https://lens.google.com/uploadbyurl?url={d_url}"
        
        extracted_text = None  # Store extracted text

        async def intercept_response(response):
            nonlocal extracted_text,extracted_text_t  # Allow modification of extracted_text within this function
            url = response.url
            if "https://lens.google.com/qfmetadata" in url:
                try:
                    print("yes")
                    content_type = response.headers.get("content-type", "")
                    if "application/json" in content_type:
                        json_data = await response.text()
                        cleaned_text = json_data.lstrip(")]}'\n")  # Remove unwanted prefix
                        json_data = json.loads(cleaned_text)
                        
                        regex_pattern = r"None,\s*'(\w+)'"
                        matches = re.findall(regex_pattern, str(json_data))
                        for i in matches:
                            if i.startswith("text:0:"):
                                print(i)
                                matches.remove(i)
                        extracted_text = " ".join(matches)  # Store result
                        print(extracted_text)
                        extracted_text_t = extracted_text_t + extracted_text
                    else:
                        print("Intercepted Non-JSON Response:", await response.text())
                except Exception as e:
                    print(f"Error parsing JSON from {url}: {e}")

        page.on("response", lambda response: asyncio.create_task(intercept_response(response)))

        try:
            await page.goto(lens_url, {'timeout': 60000})
        except Exception as e:
            print(f"Page navigation failed: {e}")

    await browser.close()
    data = {"text":extracted_text_t}
    return web.json_response(data, status=200)

# WebSocket handler
async def echo_handler(request):
    ws = web.WebSocketResponse(max_msg_size=100 * 1024 * 1024)
    await ws.prepare(request)

    # Generate a unique session ID and send it to the client
    session_id = str(uuid.uuid4())
    connections[session_id] = ws
    email = None
    try:
        async for message in ws:
            if message.type == web.WSMsgType.TEXT:
                data = json.loads(message.data)
                command = data["command"]
                if command == 'set_user':
                    email = data["email"]
                elif command == 'register':
                    status = await handle_register(data)
                    await ws.send_json({"command":"register_response","status":status})
                elif command == 'login':
                    status,token = await handle_login(data)
                    await ws.send_json({"command":"login_response","status":status,"token":token})
                elif command == 'add_subject':
                    status = await handle_add_subject(data,email)
                    await ws.send_json({"command":"add_subject_response","status":status})
                elif command == 'request_subjects':
                    subjects = await handle_request_subjects(email)
                    await ws.send_json({"command":"request_subjects_response","data":subjects})
                elif command == 'add_answersheet':
                    threading.Thread(target=process_data,args=(data,email,)).start()
                elif command == 'view_result':
                    ans_data = await handle_view_result(data)
                    await ws.send_json({"command": "view_result_response","data": ans_data})
            elif message.type == web.WSMsgType.ERROR:
                print(f"WebSocket connection closed with exception: {ws.exception()}")
    except Exception as e:
        print(f"WebSocket error with session {session_id}: {e}")
    finally:
        # Remove the connection on close
        if session_id in connections:
            del connections[session_id]
        print(f"WebSocket connection closed for session {session_id}")
    return ws

# HTTP handler
async def http_handler(request):
    port = int(os.getenv("PORT", 8765))
    return web.Response(text=f"WebSocket server is running on port {port}!", content_type="text/html")

# Main function to start the HTTP and WebSocket servers
async def main():
    # Environment-based port (default: 8765)
    port = int(os.getenv("PORT", 7860))

    # Create aiohttp app
    app = web.Application()
    app.router.add_get("/", http_handler)
    app.router.add_post("/ocr", intercept_requests)
    app.router.add_get("/ws", echo_handler)

    # Start HTTP server
    runner = web.AppRunner(app)
    await runner.setup()
    http_site = web.TCPSite(runner, "0.0.0.0", port)
    await http_site.start()
    print(f"HTTP and WebSocket server running on http://0.0.0.0:{port}")

    # Keep running
    await asyncio.Future()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user")
