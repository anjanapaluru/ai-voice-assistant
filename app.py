import streamlit as st
import os
import shutil
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder

# Import backend modules
from backend.resume_parser import parse_resume
from backend.llm_engine import LLMEngine
from backend.memory import Memory
from backend.stt_engine import STTEngine
from backend.voice_clone import VoiceCloneEngine

load_dotenv()

# --- Page Configuration ---
st.set_page_config(page_title="AI Voice Clone Interview Bot", page_icon="🎙️", layout="wide")

# --- Custom Styling ---
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stFileUploader {
        border: 1px dashed #4CAF50;
        padding: 10px;
        border-radius: 10px;
    }
    .chat-bubble {
        padding: 15px;
        border-radius: 15px;
        margin-bottom: 10px;
    }
    .user-bubble {
        background-color: #262730;
        text-align: right;
    }
    .bot-bubble {
        background-color: #1a1c24;
        border-left: 5px solid #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

# --- Initialization ---
if 'memory' not in st.session_state:
    st.session_state.memory = Memory()
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""
if 'stt_engine' not in st.session_state:
    with st.spinner("Initializing Speech-to-Text..."):
        st.session_state.stt_engine = STTEngine()
if 'voice_engine' not in st.session_state:
    with st.spinner("Initializing Voice Clone Engine (this may take a minute)..."):
        st.session_state.voice_engine = VoiceCloneEngine()
if 'llm_engine' not in st.session_state:
    st.session_state.llm_engine = None

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = st.text_input("Google API Key", type="password", value=os.getenv("GOOGLE_API_KEY", ""))
    
    if api_key:
        st.session_state.llm_engine = LLMEngine(api_key=api_key)
        st.success("API Key set!")
    
    st.divider()
    
    st.subheader("📄 Step 1: Upload Resume")
    resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    if resume_file:
        save_path = os.path.join("uploaded_resume", resume_file.name)
        with open(save_path, "wb") as f:
            f.write(resume_file.getbuffer())
        st.session_state.resume_text = parse_resume(save_path)
        st.success("Resume parsed successfully!")

    st.subheader("🎤 Step 2: Upload Voice Samples")
    voice_samples = st.file_uploader("Upload 1-3 voice samples (WAV/MP3)", type=["wav", "mp3"], accept_multiple_files=True)
    sample_paths = []
    if voice_samples:
        for i, sample in enumerate(voice_samples):
            path = os.path.join("uploaded_audio", f"sample_{i}.wav")
            with open(path, "wb") as f:
                f.write(sample.getbuffer())
            sample_paths.append(path)
        st.success(f"{len(voice_samples)} samples uploaded!")

# --- Main Interface ---
st.title("🎙️ AI Voice Clone Interview Bot")
st.write("Interview your digital twin. Upload your resume and voice samples to start!")

# Display Conversation History
chat_container = st.container()
with chat_container:
    for msg in st.session_state.memory.get_history():
        role = "You" if msg["role"] == "user" else "AI Clone"
        bubble_class = "user-bubble" if msg["role"] == "user" else "bot-bubble"
        content = msg["parts"][0]
        st.markdown(f'<div class="chat-bubble {bubble_class}"><b>{role}:</b><br>{content}</div>', unsafe_allow_html=True)

# Audio Input
st.divider()
st.subheader("💬 Ask a Question")
audio_bytes = audio_recorder(text="Click to Record your question", icon_size="2x")

if audio_bytes:
    if not st.session_state.llm_engine:
        st.error("Please provide a Google API Key in the sidebar.")
    elif not st.session_state.resume_text:
        st.warning("Please upload a resume first to give the bot context.")
    elif not voice_samples:
        st.warning("Please upload at least one voice sample for cloning.")
    else:
        # 1. Save recorded audio
        question_audio_path = os.path.join("uploaded_audio", "current_question.wav")
        with open(question_audio_path, "wb") as f:
            f.write(audio_bytes)
        
        # 2. Transcription
        with st.status("Transcribing question...", expanded=True) as status:
            question_text = st.session_state.stt_engine.transcribe(question_audio_path)
            st.write(f"Question: {question_text}")
            
            # 3. LLM Response
            status.update(label="Thinking like you...", state="running")
            # Using only the first sample for cloning in this version for simplicity, 
            # but ideally XTTS can use multiple or we can pick the best one.
            response_text = st.session_state.llm_engine.generate_response(
                question_text, 
                history=st.session_state.memory.get_history(),
                resume_text=st.session_state.resume_text
            )
            st.write(f"Response Generated.")
            
            # 4. Voice Cloning
            status.update(label="Generating cloned voice...", state="running")
            # Pick first sample
            ref_wav = os.path.join("uploaded_audio", "sample_0.wav")
            audio_response_path = st.session_state.voice_engine.generate_voice(
                response_text, 
                speaker_wav=ref_wav
            )
            
            status.update(label="Done!", state="complete", expanded=False)

        # 5. Update Memory and Session
        st.session_state.memory.add_user_message(question_text)
        st.session_state.memory.add_ai_message(response_text)
        
        # 6. Playback and Display
        if audio_response_path:
            st.audio(audio_response_path, format="audio/wav")
            with open(audio_response_path, "rb") as file:
                st.download_button(
                    label="Download Response Audio",
                    data=file,
                    file_name="cloned_response.wav",
                    mime="audio/wav"
                )
        
        # Rerun to refresh chat history display
        st.rerun()

# --- Footer ---
st.divider()
st.caption("Built with ❤️ using Streamlit, Gemini, Whisper, and Coqui XTTS.")
