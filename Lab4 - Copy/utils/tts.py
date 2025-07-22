from gtts import gTTS
import os

def speak(text, lang='en', filename='output.mp3'):
    """Convert text to speech and save as file (for Streamlit compatibility)"""
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filename)
        return filename
    except Exception as e:
        print(f"Error in text-to-speech: {e}")
        return None
