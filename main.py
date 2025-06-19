import streamlit as st
from .student_mode import summarizer
from utils.video_utils import download_audio_from_youtube, convert_to_wav
from student_mode import flashcards, quiz_generator
from creators_mode import clip_detector, viral_scorer, timestamp_extractor
from clipper import create_clip
from transcriber import transcribe_audio  # To get segments
from gdrive_uploader import upload_to_drive

st.set_page_config(page_title="ClipWhiz.AI", layout="centered")
st.title("🎬 ClipWhiz.AI")

mode = st.radio("Choose your mode:", ["🎓 Student Mode", "🎥 Creator Mode"])
style = st.selectbox("🎨 Choose subtitle style", ["MrBeast", "TikTok", "ASMR"])
temp_file_path = f"temp_{create_clip.name}"

yt_link = st.text_input("Paste a YouTube link:")

if yt_link:
    with st.spinner("Downloading audio..."):
        mp3_path = download_audio_from_youtube(yt_link)
        wav_path = convert_to_wav(mp3_path)
        transcript, segments = transcribe_audio(wav_path)
    st.success("Audio ready!")

    if mode == "🎓 Student Mode":
        st.header("📚 Study Tools")
        summary = summarizer.generate_summary("Pretend transcript here")
        st.subheader("📝 Summary")
        st.markdown(summary)

        st.subheader("🎯 Quiz Generator")
        st.markdown(quiz_generator.generate_quiz("Pretend transcript here"))

        st.subheader("🧠 Flashcards")
        flashcards.show_flashcards(["Gemini", "LLM", "YouTube Summary"])

    elif mode == "🎥 Creator Mode":
        st.header("📸 Clip & Viral Tools")
        st.subheader("📌 Clip Detection")
        st.markdown(clip_detector.detect_clips("Pretend transcript"))

        st.subheader("🔥 Viral Score")
        st.markdown(viral_scorer.score_clip("Pretend transcript"))

        st.subheader("⏱️ Timestamps")
        st.markdown(timestamp_extractor.extract_timestamps("Pretend transcript"))
        st.subheader("🎨 Choose Subtitle Style")
        subtitle_style = st.selectbox("Style:", ["MrBeast", "TikTok Gaming", "ASMR Chill"])
        [
  {"start": 0.0, "end": 5.0, "text": "Hi everyone, welcome to the video."},
  {"start": 5.0, "end": 10.0, "text": "Today we'll learn AI-powered content."}
]

         # Upload B-roll
    style = st.selectbox("🎨 Choose subtitle style", ["MrBeast", "TikTok", "ASMR"])

# Upload B-roll
st.subheader("🎮 Optional B-Roll (e.g., Subway Surfer, ASMR video)")
b_roll_file = st.file_uploader("Upload B-Roll (mp4)", type=["mp4"])

# Export Short Toggle
export_short = st.checkbox("📲 Export as 9:16 Reel/Short format?", value=True)

if st.button("🚀 Generate Viral Clips Now!"):
    for idx, seg in enumerate(segments[:3]):
        start = max(seg['start'] - 1, 0)
        end = seg['end'] + 1
        subtitle = seg['text']
        
        b_roll_path = None
        if b_roll_file:
            b_roll_path = f"broll_{b_roll_file.name}"
            with open(b_roll_path, "wb") as f:
                f.write(b_roll_file.read())

        with st.spinner(f"🎬 Rendering Clip {idx+1}..."):
            out_path = create_clip(
                video_path=temp_file_path,
                start=start,
                end=end,
                subtitles=subtitle,
                style=style.lower(),
                b_roll_path=b_roll_path,
                export_short=export_short
            )
            st.video(out_path)
            with open(out_path, "rb") as f:
                st.download_button(f"Download Clip {idx+1}", f, file_name=out_path)
upload_to_drive(out_path)

