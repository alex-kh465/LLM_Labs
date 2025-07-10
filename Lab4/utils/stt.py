import whisper

def transcribe_audio(audio_path):
    """Transcribe audio file using Whisper"""
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result['text']
