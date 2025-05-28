import os
from google import genai
from google.genai import types
import wave

# Initialize client
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def wave_file(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

def generate_audio(text, file_name):
    print(f"\n🔊 Requesting audio for text: {text[:50]}...") 
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
    
    if not response.candidates:
        print("No candidates received from API.")
        return
    
    parts = response.candidates[0].content.parts
    if not parts or not hasattr(parts[0], "inline_data") or not parts[0].inline_data.data:
        print("No audio data found in response.")
        return
    
    data = parts[0].inline_data.data
    print(f"Received {len(data)} bytes of audio data.")
    wave_file(file_name, data)
    print(f"Audio written to {file_name}")

def generate_audio_from_markdown(markdown_text, audio_folder):
    os.makedirs(audio_folder, exist_ok=True)
    
    print("Warming up API with a test request...")
    warmup_path = os.path.join(audio_folder, "warmup.mp3")
    generate_audio("This is a warm-up test.", warmup_path)
    if os.path.exists(warmup_path):
        os.remove(warmup_path)
    print("Warm-up done!\n")

    lines = markdown_text.splitlines()
    slide_title = None
    slide_points = []
    slide_count = 0
    
    for line in lines + ["# END"]: 
        line = line.strip()
        if line.startswith("# "):
            if slide_title: 
                slide_count += 1
                text_to_speak = slide_title + ". " + " ".join(slide_points)
                safe_title = slide_title.replace(' ', '_').replace('/', '_')
                audio_path = os.path.join(audio_folder, f"{slide_count:02d}_{safe_title}.mp3")
                print(f"\n🎙️ Generating audio for slide '{slide_title}'...")
                print(f"Text: {text_to_speak}")
                generate_audio(text_to_speak, audio_path)
            slide_title = line[2:].strip()
            slide_points = []
        elif line.startswith("- "):
            slide_points.append(line[2:].strip())
    
    print(f"\n✅ Generated {slide_count} audio files in folder '{audio_folder}'.")
