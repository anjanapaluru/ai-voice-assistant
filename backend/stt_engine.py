import whisper
import os

class STTEngine:
    def __init__(self, model_name="base"):
        # "tiny", "base", "small", "medium", "large"
        print(f"Loading Whisper model: {model_name}...")
        self.model = whisper.load_model(model_name)

    def transcribe(self, audio_path):
        """
        Transcribes audio file to text.
        """
        if not os.path.exists(audio_path):
            return "Audio file not found."
        
        try:
            result = self.model.transcribe(audio_path)
            return result["text"].strip()
        except Exception as e:
            return f"Error transcribing audio: {str(e)}"

if __name__ == "__main__":
    # Test
    # engine = STTEngine()
    # print(engine.transcribe("path/to/audiooda.wav"))
    pass
