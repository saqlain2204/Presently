import subprocess
import os
from pdf2image import convert_from_path

def ppt_to_images(workspace_root):
    ppt_file = os.path.join(workspace_root, "temp", "presentation.ppt")
    pdf_file = os.path.join(workspace_root, "temp", "presentation.pdf")
    output_folder = os.path.join(workspace_root, "temp", "slide_images")

    # Convert PPT to PDF using LibreOffice
    command = [
        "soffice",
        "--headless",
        "--convert-to", "pdf",
        "--outdir", os.path.dirname(pdf_file),
        ppt_file
    ]
    subprocess.run(command, check=True)

    # Convert PDF pages to images
    os.makedirs(output_folder, exist_ok=True)
    images = convert_from_path(pdf_file)
    image_paths = []
    for i, img in enumerate(images):
        img_path = os.path.join(output_folder, f"slide_{i+1}.png")
        img.save(img_path, "PNG")
        image_paths.append(img_path)

    return image_paths
