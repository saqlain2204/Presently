import os
from spire.presentation import *

# Paths
PPTX_PATH = r"D:/Saqlain/Personal Projects/PPT-to-presentation-video/temp/presentation.pptx"
SLIDES_DIR = r"D:/Saqlain/Personal Projects/PPT-to-presentation-video/output/slides"

# Create the output directory if it doesn't exist
os.makedirs(SLIDES_DIR, exist_ok=True)

# Load presentation
presentation = Presentation()
presentation.LoadFromFile(PPTX_PATH)

# Convert slides to images
for i, slide in enumerate(presentation.Slides):
    image_path = os.path.join(SLIDES_DIR, f"slide_{i + 1}.png")
    image = slide.SaveAsImage()
    image.Save(image_path)
    image.Dispose()

presentation.Dispose()
print("Slides exported as images successfully!")
