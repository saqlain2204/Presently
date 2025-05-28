import google.generativeai as genai
from dotenv import load_dotenv
import os
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
def find_best_matching_image(images_dir, text_query):
    best_image_path = None
    best_score = -float('inf') 
    
    for img_name in os.listdir(images_dir):
        if img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            img_path = os.path.join(images_dir, img_name)
            try:
                my_file = client.files.upload(file=img_path)
                
                prompt = f"How well does this image match this text? \"{text_query}\" Rate from 0 to 10. Only return the number. Nothing else. If the text matches the image little also its fine, give a good score"
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[my_file, prompt],
                )
                
                response_text = response.text.strip()
                print(f"Image: {img_name}, Response: {response_text}")
                
                try:
                    score = float(response_text.split()[0]) 
                except Exception:
                    score = 0
                
                if score > best_score:
                    best_score = score
                    best_image_path = img_path
            
            except Exception as e:
                print(f"Error processing {img_name}: {e}")
    
    return best_image_path