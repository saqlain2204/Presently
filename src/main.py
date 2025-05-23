from web_scraper import scrape_website, convert_to_markdown
from convert_to_ppt import parse_markdown, add_title_slide, add_content_slide, markdown_to_ppt
import content_generator
import os
from text_to_audio import generate_audio_from_markdown


def main():
    url_input = input("Enter the URL of the webpage: ")
    _, content_dict, image_paths, markdown_path, workspace_root, url = scrape_website(url_input)
    markdown_content = convert_to_markdown(content_dict, image_paths, url)
    
    presentation_content = content_generator.generate_content(markdown_path)
    presentation_content_path = os.path.join(workspace_root, "temp", "presentation.md")
    with open(presentation_content_path, 'w', encoding='utf-8') as f:
        f.write(presentation_content)
    print(workspace_root)
    markdown_to_ppt(workspace_root, output_file=os.path.join(workspace_root, "temp", "presentation.pptx"))
    generate_audio_from_markdown(presentation_content, os.path.join(workspace_root, "temp", "audio"))

    
    
    
    
if __name__ == "__main__":
    main()

