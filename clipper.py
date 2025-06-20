import os
from moviepy import VideoFileClip, TextClip, CompositeVideoClip


def create_clip(video_path, start, end, subtitles, style="mrbeast", b_roll_path=None, export_short=False):
    print("[🎞️] Loading main video...")
    clip = VideoFileClip(video_path).subclip(start, end)

    # Optional B-roll background
    if b_roll_path:
        print("[🎮] Adding b-roll overlay...")
        b_roll = VideoFileClip(b_roll_path).subclip(0, clip.duration).resize(clip.size)
        clip = CompositeVideoClip([b_roll.set_opacity(0.6), clip])

    # Subtitles styling
    if style.lower() == "mrbeast":
        subtitle = TextClip(subtitles, fontsize=48, font='Arial-Bold', color='yellow', bg_color='black')
    elif style.lower() == "asmr":
        subtitle = TextClip(subtitles, fontsize=28, font='Arial', color='white')
    else:
        subtitle = TextClip(subtitles, fontsize=36, font='Arial', color='cyan')

    subtitle = subtitle.set_duration(clip.duration).set_position(('center', 'bottom'))
    final = CompositeVideoClip([clip, subtitle])

    # Export as vertical for Shorts/Reels
    if export_short:
        print("[📲] Resizing for 9:16 vertical format...")
        final = final.resize(height=1280).resize(width=720)

    output_path = f"clip_{int(start)}_{int(end)}.mp4"
    final.write_videofile(output_path, codec="libx264", audio_codec="aac")

    print("[✅] Clip ready at:", output_path)
    return output_path

