from predict_and_save import predict_and_save
from ocr_to_markdown import extract_text_and_convert_to_markdown

def main(image_paths):
    det_res = predict_and_save(image_paths)

    for i, img_path in enumerate(image_paths):
        md = extract_text_and_convert_to_markdown(img_path, det_res)
        md_path = f"./temp/page_{i+1}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"Saved markdown: {md_path}")

if __name__ == "__main__":
    # Replace with your actual images
    image_files = [r"C:\Users\saqla\Downloads\Mohammed_Saqlain_Resume_with_photo_page-0001.jpg"]
    main(image_files)
