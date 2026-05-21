# AI Voice Clone Interview Bot

This is a beginner-friendly Streamlit application that uses AI to clone your voice and conduct an interview based on your resume.

## Features
- **Resume Parsing**: Analyzes your PDF resume to understand your background.
- **Speech-to-Text**: Uses OpenAI Whisper to transcribe your questions.
- **LLM Engine**: Uses Google Gemini to generate personalized responses.
- **Voice Cloning**: Uses Coqui XTTS-v2 to speak back in your own voice.
- **Memory**: Remembers the conversation context.

## Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd ai-voice-interview-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file from `.env.example` and add your `GOOGLE_API_KEY`.

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

## Requirements
- Python 3.9+
- FFmpeg (for audio processing)
- GPU recommended (for faster voice cloning)
