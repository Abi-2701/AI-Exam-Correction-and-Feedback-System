import fitz
import random
import string
import os

def filename(length=7):
    characters = string.ascii_letters + string.digits
    if length > len(characters):
        raise ValueError("Length cannot exceed the number of available characters")
    return ''.join(random.sample(characters, length))

def pdf_to_images(pdf_path, output_folder="output_images", dpi=150):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    doc = fitz.open(pdf_path)
    image_paths = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(dpi=dpi)
        name = filename()
        image_path = os.path.join(output_folder, f"page_{name}.png")
        pix.save(image_path)
        image_paths.append(image_path)

    return image_paths