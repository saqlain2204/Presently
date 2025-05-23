import os
import wave
from google import genai
from google.genai import types

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def generate_audio(text, file_name):
    response = client.models.generate_content(
        model="gemini-2.5-flash-preview-tts",
        contents=text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name='Kore',
                    )
                )
            ),
        )
    )
    data = response.candidates[0].content.parts[0].inline_data.data
    wave_file(file_name, data)

def generate_audio_from_markdown(markdown_text, audio_folder):
    # Create folder if not exists
    os.makedirs(audio_folder, exist_ok=True)
    
    lines = markdown_text.splitlines()
    slide_title = None
    slide_points = []
    slide_count = 0
    
    for line in lines + ["# END"]:  # add a dummy header to flush last slide
        line = line.strip()
        if line.startswith("# "):  # New slide start
            if slide_title:  # save previous slide audio
                slide_count += 1
                text_to_speak = slide_title + ". " + " ".join(slide_points)
                safe_title = slide_title.replace(' ', '_').replace('/', '_')
                audio_path = os.path.join(audio_folder, f"{slide_count:02d}_{safe_title}.mp3")
                print(f"Generating audio for slide '{slide_title}'...")
                generate_audio(text_to_speak, audio_path)
            # start new slide
            slide_title = line[2:].strip()
            slide_points = []
        elif line.startswith("- "):
            slide_points.append(line[2:].strip())
    
    print(f"Generated {slide_count} audio files in folder '{audio_folder}'.")

