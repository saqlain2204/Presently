import os
import cv2
import torch
from model_loader import load_model

device = "cuda" if torch.cuda.is_available() else "cpu"

def predict_and_save(image_paths):
    model = load_model()

    if not os.path.exists("./temp/"):
        os.makedirs("./temp/")

    for i, img_path in enumerate(image_paths):
        det_res = model.predict(
            img_path,
            imgsz=1024,
            conf=0.2,
            device=device,
        )
        annotated_frame = det_res[0].plot(pil=True, line_width=5, font_size=20)
        output_path = f"./temp/result_page_{i+1}.jpg"
        cv2.imwrite(output_path, annotated_frame)
        print(f"Saved annotated image: {output_path}")

    return det_res  # Return last detection results if needed
