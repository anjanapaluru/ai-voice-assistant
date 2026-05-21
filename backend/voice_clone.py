import asyncio
import edge_tts
import os
import uuid

class VoiceCloneEngine:
    def __init__(self):
        print("Using Edge-TTS (Fallback) for compatibility...")

    def generate_voice(self, text, speaker_wav=None, output_dir="generated_audio"):
        """
        Generates voice using Edge-TTS. 
        Note: speaker_wav is ignored in this fallback mode.
        """
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        output_filename = f"response_{uuid.uuid4().hex}.mp3"
        output_path = os.path.join(output_dir, output_filename)
        
        try:
            # Select a default voice (e.g., en-US-GuyNeural or en-US-JennyNeural)
            # You can change the voice to match the gender if needed.
            voice = "en-US-GuyNeural" 
            
            async def _save():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(output_path)
            
            asyncio.run(_save())
            return output_path
        except Exception as e:
            print(f"Error generating voice: {str(e)}")
            return None

if __name__ == "__main__":
    # Test
    # engine = VoiceCloneEngine()
    # engine.generate_voice("Hello, this is my cloned voice.", "path/to/sample.wav")
    pass
