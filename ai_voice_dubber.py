import pyttsx3

def generate_ai_voice(text, output_path="ai_voice.mp3"):
    engine = pyttsx3.init()
    engine.setProperty("rate", 165)
    engine.setProperty("volume", 1.0)

    engine.save_to_file(text, output_path)
    engine.runAndWait()

    print("✅ AI voice saved to", output_path)
    return output_path
