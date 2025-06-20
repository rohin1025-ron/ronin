from utils.video_utils import download_audio_from_youtube
from pytube import YouTube
import os

def download_audio_from_youtube(url, output_path="downloads", filename="audio"):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    file_path = audio_stream.download(output_path=output_path, filename=filename)
    return file_path
