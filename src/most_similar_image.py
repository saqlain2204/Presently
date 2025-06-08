import google.generativeai as genai
from dotenv import load_dotenv
import os
import shutil
from google import genai

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
def find_best_matching_image(images_dir, text_query):
    best_image_path = None
    best_score = -float('inf') 
    
    print(f"Finding best image match for text: '{text_query}'")
    
    for img_name in os.listdir(images_dir):
        if img_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            try:
                img_path = os.path.join(images_dir, img_name)                      
                my_file = client.files.upload(file=img_path)
                
                logo_check_prompt = f"""
                Analyze this image and determine if it's a company logo.
                
                A company logo typically:
                - Contains a brand name or recognizable symbol
                - Has clean, simplified graphics
                - Often uses specific brand colors
                - Is designed for brand recognition
                
                If this is clearly a company logo, respond with exactly "COMPANY_LOGO".
                If this is NOT a company logo, respond with exactly "NOT_LOGO".
                """
                
                logo_response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=[my_file, logo_check_prompt],
                )
                
                logo_result = logo_response.text.strip()
                print(f"Logo check for {img_name}: {logo_result}")

                if "COMPANY_LOGO" in logo_result:
                    print(f"Detected company logo: {img_name}")
                    
                    logos_dir = os.path.join(os.path.dirname(images_dir), "logos")
                    os.makedirs(logos_dir, exist_ok=True)
                    
                    logo_destination = os.path.join(logos_dir, img_name)
                    try:
                        shutil.move(img_path, logo_destination)
                        print(f"Moved company logo to: {logo_destination}")
                    except Exception as e:

                        print(f"Failed to move logo, removing instead: {e}")
                        try:
                            os.remove(img_path)
                            print(f"Removed company logo: {img_name}")
                        except:
                            pass
                    
                    continue
                
                my_file = client.files.upload(file=img_path)
                
                prompt = f"""
                Analyze this image and score how well it matches the following text. Be very precise in your evaluation.

                Text to match: "{text_query}"

                Scoring guidelines (0-10 scale):
                - For text about a person (bio, profile, resume):
                  * Score 8-10 if this is clearly a photo of that specific person
                  * Score 6-7 if this is a relevant photo but not necessarily of that person
                  * Look for name matches between the filename and any names in the text
                  
                - For text about companies/organizations:
                  * Score 8-10 if this is the company's logo or directly related image
                  * Score 5-7 if this shows products or services of that company
                
                - For text about topics/concepts:
                  * Score 8-10 if this directly illustrates the main concept
                  * Score 5-7 if this relates to secondary aspects mentioned
                
                The filename '{img_name}' may provide hints about the image content.
                
                Return ONLY a single number from 0 to 10, with no other text.
                """
                
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
    
    print(f"Best matching image score: {best_score:.1f}")
    
    if best_score:
        return best_image_path
    return None