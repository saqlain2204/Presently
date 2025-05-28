from web_scraper import scrape_website, convert_to_markdown
from convert_to_ppt import parse_markdown, add_title_slide, add_content_slide, markdown_to_ppt
import content_generator
import os
from text_to_audio import generate_audio_from_markdown
from convert_to_images import ppt_to_images
from generate_video import create_presentation_video
from terminal_utils import print_success, print_info, print_header
from music_selection import select_best_music
import time


def main():
    print_header("Welcome to Presently")
    url_input = input("Enter the URL of the webpage: ")

    print_info("Scraping website content...")
    _, content_dict, image_paths, markdown_path, workspace_root, url = scrape_website(url_input)
    markdown_content = convert_to_markdown(content_dict, image_paths, url)
    print_success("✓ Website content successfully scraped and converted to markdown")
    
    print_info("Generating presentation content...")
    presentation_content = content_generator.generate_content(markdown_path)
    presentation_content_path = os.path.join(workspace_root, "temp", "presentation.md")
    with open(presentation_content_path, 'w', encoding='utf-8') as f:
        f.write(presentation_content)
    print_success("✓ Presentation content successfully generated")
    
    print_info("Converting markdown to PowerPoint...")
    markdown_to_ppt(workspace_root, output_file=os.path.join(workspace_root, "temp", "presentation.ppt"))
    print_success("✓ PowerPoint presentation successfully created")
    
    print_info("Selecting appropriate background music")
    select_best_music(workspace_root, presentation_content)
    
    print_info("Generating audio narration...")
    time.sleep(6)
    generate_audio_from_markdown(presentation_content, os.path.join(workspace_root, "temp", "audio"))
    print_success("✓ Audio narration successfully generated")
    
    print_info("Converting presentation to images...")
    ppt_to_images_path = ppt_to_images(workspace_root=workspace_root)
    print_success("✓ Slide images successfully created")
    
    print_info("Creating final presentation video...")
    presentation_video_path = create_presentation_video(workspace_root=workspace_root)
    print_success(f"✓ Video successfully generated and stored.")
    
    
    
    
    
if __name__ == "__main__":
    main()

