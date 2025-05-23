import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_content(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    prompt = (
        "You are given the content of a markdown file. Your task is to extract the most important "
        "information from the markdown in minimum of 5 headings and a maximum of 10 headings. The headings should start with # and the content should be in points. "
        "A minimum and maximum of 5 points for each heading. This is your text:\n\n"
        f"{text}\n\n"
        "Your main task is to create a presentation of the text. So you are supposed to be on point and clear. Always give positive statements and speak as if you are pitching it. Give summaries such that everyone can understand."
        "Every slide contains one heading. Under each heading, include 5 points.\n\n"
        "Format strictly like this:\n"
        "Give me the Title of the presentation that starts with ##.\n"
        "Then give me the headings and points in this format:\n"
        "# Heading\n"
        "- Point 1\n"
        "- Point 2\n"
        "- Point 3\n"
        "- Point 4\n"
        "- Point 5\n\n"
        "Return only markdown. Do not add any other explanations or summaries."
        "Strictly maintain the format. Do not Alter it.\n"
    )

    # Use Gemini Pro
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)

    return response.text

