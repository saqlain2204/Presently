import cv2
import easyocr
import os

reader = easyocr.Reader(['en'])

# Added class 5 for Figure
label_map = {
    0: "Title",
    1: "Paragraph",
    2: "List",
    3: "Table",
    4: "Subtitle",
    5: "Figure"  # assuming 5 is the class ID for figures
}

def to_markdown(text, label):
    if label == "Title":
        return f"# {text}\n\n"
    elif label == "Subtitle":
        return f"## {text}\n\n"
    elif label == "List":
        lines = text.split('\n')
        bullets = "\n".join([f"- {line.strip()}" for line in lines if line.strip()])
        return f"{bullets}\n\n"
    elif label == "Table":
        return f"{text}\n\n"
    else:
        return f"{text}\n\n"

def extract_text_and_convert_to_markdown(image_path, det_res):
    image = cv2.imread(image_path)
    markdown = ""

    boxes = det_res[0].boxes.xyxy.cpu().numpy()
    classes = det_res[0].boxes.cls.cpu().numpy()

    # Combine boxes and classes into one list of tuples for sorting
    items = []
    for box, cls in zip(boxes, classes):
        x_min, y_min, x_max, y_max = box.astype(int)
        items.append((x_min, y_min, x_max, y_max, cls))

    # Sort by top-left corner for reading order
    items.sort(key=lambda x: (x[1], x[0]))

    # Create folder to save figure crops
    os.makedirs("./temp/extracted_figures", exist_ok=True)

    for idx, (x_min, y_min, x_max, y_max, cls) in enumerate(items):
        crop = image[y_min:y_max, x_min:x_max]
        crop_rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)

        label = label_map.get(cls, "Paragraph")

        if label == "Figure":
            # Save cropped figure image
            figure_path = f"./temp/extracted_figures/figure_{idx+1}.jpg"
            cv2.imwrite(figure_path, crop)
            # Insert markdown image link
            markdown += f"\n\n![Figure {idx+1}]({figure_path})\n\n"
        else:
            # OCR for text-based classes
            text_lines = reader.readtext(crop_rgb, detail=0)
            text = " ".join(text_lines).strip()
            markdown += to_markdown(text, label)

    return markdown
