import requests
from bs4 import BeautifulSoup
import os
import re
import urllib.parse
from urllib.request import urlretrieve
from pathlib import Path
import hashlib

def scrape_website(url):
    """
    Scrape content from a website, extracting text and images.
    
    Args:
        url (str): URL of the website to scrape
        
    Returns:
        tuple: (text content as dict, list of image paths)
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.extract()
        
        content_dict = extract_text_content(soup)
        
        workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        images_dir = os.path.join(workspace_root, "temp", "images")
        os.makedirs(images_dir, exist_ok=True)
        
        image_paths = download_images(soup, url, images_dir)
        markdown_content = convert_to_markdown(content_dict, image_paths, url)
        
        markdown_file_path = os.path.join(workspace_root, "temp", "output.md")
        with open(markdown_file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        return soup, content_dict, image_paths, markdown_file_path, workspace_root, url
    
    except Exception as e:
        print(f"Error scraping website {url}: {e}")
        return {}, [], url

def extract_text_content(soup):
    """
    Extract headings and paragraphs from the soup object.
    
    Args:
        soup (BeautifulSoup): Parsed HTML content
        
    Returns:
        dict: Dictionary of content sections with their content
    """
    content_dict = {
        'title': '',
        'sections': []
    }
    
    title_tag = soup.find('title')
    if title_tag:
        content_dict['title'] = title_tag.get_text().strip()
    
    main_content = soup.find('main') or soup.find('article') or soup.find('body')
    
    current_heading = None
    current_text = []
    
    for element in main_content.find_all(['h1', 'h2', 'h3', 'p']):
        tag_name = element.name
        text = element.get_text().strip()
        
        if not text:
            continue
            
        if tag_name in ['h1', 'h2', 'h3']:
            if current_heading and current_text:
                content_dict['sections'].append({
                    'heading': current_heading,
                    'content': '\n\n'.join(current_text)
                })
                current_text = []
            
            current_heading = text
        
        elif tag_name == 'p' and len(text) > 15: 
            current_text.append(text)
    
    if current_heading and current_text:
        content_dict['sections'].append({
            'heading': current_heading,
            'content': '\n\n'.join(current_text)
        })
    
    return content_dict


def download_images(soup, base_url, images_dir):
    """
    Download images from the website.
    
    Args:
        soup (BeautifulSoup): Parsed HTML content
        base_url (str): Base URL of the website
        images_dir (str or Path): Directory to save images
        
    Returns:
        list: List of paths to downloaded images
    """
    image_paths = []
    
    images_dir = Path(images_dir)
    images_dir.mkdir(parents=True, exist_ok=True) 
    
    img_elements = soup.find_all('img')
    for i, img in enumerate(img_elements):
        img_url = img.get('src')
        if not img_url:
            continue
        
        if not img_url.startswith(('http://', 'https://')):
            img_url = urllib.parse.urljoin(base_url, img_url)
        
        try:
            file_extension = os.path.splitext(img_url)[1]
            if not file_extension:
                file_extension = '.jpg'
            
            # Try to get alt text for the image
            alt_text = img.get('alt')
            
            if alt_text and alt_text.strip():
                # Clean the alt text to make it a valid filename
                safe_alt_text = re.sub(r'[\\/*?:"<>|]', '', alt_text)  # Remove invalid filename chars
                safe_alt_text = re.sub(r'\s+', '_', safe_alt_text)     # Replace spaces with underscores
                safe_alt_text = safe_alt_text[:50]                     # Limit length
                img_filename = f"{safe_alt_text}{file_extension}"
            else:
                # Fall back to the original naming scheme
                img_hash = hashlib.md5(img_url.encode()).hexdigest()
                img_filename = f"image_{i+1}_{img_hash[:8]}{file_extension}"
            
            # Handle duplicate filenames by appending a counter if needed
            base_filename = os.path.splitext(img_filename)[0]
            counter = 0
            while (images_dir / img_filename).exists():
                counter += 1
                img_filename = f"{base_filename}_{counter}{file_extension}"
            
            img_path = images_dir / img_filename
            
            if img_path.exists():
                image_paths.append(str(img_path))
                continue
                
            urlretrieve(img_url, str(img_path))
            image_paths.append(str(img_path))
            print(f"Downloaded image: {img_path}")
            
        except Exception as e:
            print(f"Error downloading image {img_url}: {e}")
    
    return image_paths



def convert_to_markdown(content_dict, image_paths, source_url):
    """
    Convert the scraped content to markdown format.
    
    Args:
        content_dict (dict): Dictionary of content sections
        image_paths (list): List of paths to downloaded images
        source_url (str): Source URL of the content
        
    Returns:
        str: Markdown formatted text
    """
    markdown = f"# {content_dict['title']}\n\n"
    
    markdown += f"Source: [{source_url}]({source_url})\n\n"
    
    for section in content_dict['sections']:
        markdown += f"## {section['heading']}\n\n"
        markdown += f"{section['content']}\n\n"
    
    if image_paths:
        markdown += "## Images\n\n"
        for i, img_path in enumerate(image_paths):
            img_filename = os.path.basename(img_path)
            relative_path = os.path.join("temp", "images", img_filename)
            markdown += f"![Image {i+1}]({relative_path.replace(os.sep, '/')})\n\n"
    
    return markdown
