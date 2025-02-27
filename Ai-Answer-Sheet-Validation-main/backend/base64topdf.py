import base64

def base64_to_pdf(data_uri, output_file):
    try:
        if data_uri.startswith("data:application/pdf;base64,"):
            base64_string = data_uri.split(",")[1]
        else:
            raise ValueError("The provided string is not a valid PDF Base64 data URI.")
        pdf_data = base64.b64decode(base64_string)
        with open(output_file, 'wb') as pdf_file:
            pdf_file.write(pdf_data)
        return True
    except Exception as e:
        return False
