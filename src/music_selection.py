"""
Select the most appropriate background music for a presentation based on content.
"""
from dotenv import load_dotenv
import os
from google import genai
import shutil
from terminal_utils import print_info, print_success

# Load environment variables
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def select_best_music(workspace_root, content_text):
    
    music_dir = os.path.join(workspace_root, "assets", "music")
    print_info(f"Searching for appropriate music in: {music_dir}")
    
    temp_dir = os.path.join(workspace_root, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    best_music_path = None
    best_score = -float('inf')
    
    try:
        keyword_prompt = (
            f"Extract 5-7 keywords from this text that describe its mood, tone, and subject matter. "
            f"Do not include common words. Include only what is necessary."
            f"Return ONLY keywords separated by commas, no explanations: \"{content_text[:500]}\""
        )
        
        keyword_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[keyword_prompt]
        )
        
        keywords = keyword_response.text.strip()
        print_info(f"Extracted keywords: {keywords}")
    except Exception as e:
        print(f"Failed to extract keywords: {e}")
        keywords = "professional, informative" 

    if not os.path.exists(music_dir):
        print_info("Music directory not found, trying alternate location")
        music_dir = os.path.join(workspace_root, "assets")
        if not os.path.exists(music_dir):
            raise FileNotFoundError(f"Neither assets/music nor assets directory found")
            
    music_files = [f for f in os.listdir(music_dir) 
                  if f.lower().endswith(('.mp3', '.wav', '.ogg', '.flac'))]
    
    if not music_files:
        raise FileNotFoundError(f"No music files found in {music_dir}")
    
    print_info(f"Found {len(music_files)} music files")

    for music_file in music_files:
        music_path = os.path.join(music_dir, music_file)
        try:
            music_name = os.path.splitext(music_file)[0]
            
            prompt = (
                f"On a scale from 0 to 10, how well would a music track titled '{music_name}' "
                f"match content with these keywords: {keywords}? "
                f"Consider the name: '{music_name}' would enhance a presentation about these topics. "
                f"Be very accurate in scoring the files. Your score is to be based on the majority of the keywords."
                f"Please respond with only a number from 0 to 10."
            )

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt]
            )

            score_text = response.text.strip()
            
            import re
            score_match = re.search(r'\b([0-9]|10)(\.[0-9]+)?\b', score_text)
            
            if score_match:
                score = float(score_match.group(0))
            else:
                score = 5.0 
                
            print_info(f"Music: {music_file}, Score: {score}/10")

            if score > best_score:
                best_score = score
                best_music_path = music_path

        except Exception as e:
            print(f"Failed processing {music_file}: {e}")

    if best_music_path is None:
        raise FileNotFoundError("No suitable music file found.")

    ext = os.path.splitext(best_music_path)[1]
    selected_music_path = os.path.join(temp_dir, f"selected_music{ext}")
    shutil.copy(best_music_path, selected_music_path)

    print_success(f"✓ Selected music: {os.path.basename(best_music_path)} with score {best_score:.2f}/10")
    return selected_music_path

