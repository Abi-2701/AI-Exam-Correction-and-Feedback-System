import requests
import asyncio
import re
import ast
from PIL import Image
from io import BytesIO


def upload_images_and_extract_text(image_paths, endpoint_url='https://lens.google.com/v3/upload'):
    data = requests.post("http://localhost:7860/ocr",json={"images_path":image_paths})
    d = data.json()
    return [d["text"]]
