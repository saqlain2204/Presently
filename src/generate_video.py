import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip, afx, concatenate_audioclips

def create_presentation_video(workspace_root):
    slide_images_folder = os.path.join(workspace_root, "temp", "slide_images")
    audio_folder = os.path.join(workspace_root, "temp", "audio")
    background_music_path = os.path.join(workspace_root, "temp", "selected_music.mp3")
    output_path = os.path.join(workspace_root, "temp", "presentation_video.mp4")

    slide_images = sorted([f for f in os.listdir(slide_images_folder) if f.endswith('.png')])
    audio_files = sorted([f for f in os.listdir(audio_folder) if f.endswith(('.mp3', '.wav'))])

    clips = []

    for i, slide_img in enumerate(slide_images):
        slide_path = os.path.join(slide_images_folder, slide_img)
        if i == 0 or i == len(slide_images) - 1:
            duration = 3
            clip = ImageClip(slide_path).set_duration(duration)
        else:
            try:
                audio_path = os.path.join(audio_folder, audio_files[i-1])
                audio_clip = AudioFileClip(audio_path)
                duration = audio_clip.duration
                clip = ImageClip(slide_path).set_duration(duration).set_audio(audio_clip)
            except:
                continue
        clips.append(clip)

    final_video = concatenate_videoclips(clips, method="compose")

    total_duration = final_video.duration
    bg_music_clip = AudioFileClip(background_music_path)
    bg_music_clip = concatenate_audioclips([bg_music_clip.subclip(0, bg_music_clip.duration-10), bg_music_clip.subclip(5, bg_music_clip.duration-10)])
    if bg_music_clip.duration < total_duration:
        loops_needed = int(total_duration // bg_music_clip.duration) + 1
        bg_music_clip = concatenate_audioclips([bg_music_clip] * loops_needed)
    bg_music_clip = bg_music_clip.subclip(0, total_duration)

    fade_duration = 3
    bg_music_clip = bg_music_clip.volumex(0.1).fx(afx.audio_fadein, fade_duration).fx(afx.audio_fadeout, fade_duration)

    if final_video.audio:
        combined_audio = CompositeAudioClip([final_video.audio.volumex(1.0), bg_music_clip])
    else:
        combined_audio = bg_music_clip

    final_video = final_video.set_audio(combined_audio)

    final_video.write_videofile(output_path, fps=24)
    print(f"Video saved to: {output_path}")
