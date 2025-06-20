import streamlit as st
from student_mode import flashcards, quiz_generator, summarizer
from creators_mode import clip_detector, viral_scorer, timestamp_extractor
from utils.video_utils import download_audio_from_youtube, convert_to_wav
from clipper import create_clip
from transcriber import transcribe_audio

import os
from datetime import datetime

st.set_page_config(page_title="ClipWhiz.AI", layout="centered")
st.title("🎬 ClipWhiz.AI")

# Step 1: UI — Mode + Style
mode = st.radio("Choose your mode:", ["🎓 Student Mode", "🎥 Creator Mode"])
style = st.selectbox("🎨 Choose subtitle style", ["MrBeast", "TikTok", "ASMR"])

# Step 2: YouTube URL Input
yt_link = st.text_input("Paste a YouTube link:")

# Step 3: If YouTube Link Provided
if yt_link:
    with st.spinner("📥 Downloading audio..."):
        mp3_path = download_audio_from_youtube(yt_link)
        wav_path = convert_to_wav(mp3_path)
        transcript, segments = transcribe_audio(wav_path)

    st.success("✅ Audio downloaded and transcript generated.")

    # STUDENT MODE ======================================
    if mode == "🎓 Student Mode":
        st.header("📚 Study Tools")
        
        st.subheader("📝 Summary")
        summary = summarizer.generate_summary(transcript)
        st.markdown(summary)

        st.subheader("🎯 Quiz Generator")
        quiz = quiz_generator.generate_quiz(transcript)
        st.markdown(quiz)

        st.subheader("🧠 Flashcards")
        flashcards_data = ["Gemini", "LLM", "YouTube Summary"]
        flashcards.show_flashcards(flashcards_data)

    # CREATOR MODE =======================================
    elif mode == "🎥 Creator Mode":
        st.header("📸 Clip & Viral Tools")

        st.subheader("📌 Clip Detection")
        st.markdown(clip_detector.detect_clips(transcript))

        st.subheader("🔥 Viral Score")
        st.markdown(viral_scorer.score_clip(transcript))

        st.subheader("⏱️ Timestamps")
        st.markdown(timestamp_extractor.extract_timestamps(transcript))

        st.markdown("---")
        st.subheader("🎮 Optional B-Roll (e.g., Subway Surfer, ASMR)")
        b_roll_file = st.file_uploader("Upload B-Roll (mp4)", type=["mp4"])

        st.subheader("📲 Export Format")
        export_short = st.checkbox("Export as 9:16 Reel/Short format?", value=True)

        # Generate temporary filename for output clip
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_file_path = f"clip_{timestamp}.mp4"

        # Final Button
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
                        video_path=mp3_path,  # Or full video path if used
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
from assets.gdrive_uploader import upload_to_drive

# Inside the st.button clip loop:
with open(out_path, "rb") as f:
    st.download_button(f"Download Clip {idx+1}", f, file_name=out_path)

# ✅ Upload to Google Drive
with st.spinner("📤 Uploading to Google Drive..."):
    gdrive_url = upload_to_drive(out_path)
    st.success("📁 File uploaded to Google Drive!")
    st.markdown(f"[🔗 View on Google Drive]({gdrive_url})")
from ai_voice_dubber import generate_ai_voice

st.subheader("🗣️ AI Voice Summary (Optional)")
if st.button("🎙️ Generate AI Voiceover"):
    voice_path = generate_ai_voice(summary)
    st.audio(voice_path, format="audio/mp3")
    st.success("🎧 Voiceover ready!")
