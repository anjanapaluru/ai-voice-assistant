import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class LLMEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment or passed as argument.")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash') # Using flash for speed

    def generate_response(self, prompt, history=None, resume_text=""):
        """
        Generates a response from the LLM based on history and resume context.
        """
        system_instruction = f"""
        You are an AI digital clone of the candidate. Your task is to answer interview and personality questions exactly like the candidate would respond in real life.
        
        Candidate Resume Context:
        {resume_text}
        
        Guidelines:
        1. Use the provided resume to answer technical and professional questions.
        2. Be authentic, confident, concise, and human-like.
        3. Respond in the first person ("I", "my").
        4. If a question is about something not in your resume, infer a polite and professional answer that aligns with your persona.
        5. Keep responses conversational and suitable for voice output (avoid long lists or complex markdown).
        """
        
        chat = self.model.start_chat(history=history or [])
        
        # Combine system instruction with the prompt for a single turn if no history, 
        # or just send the prompt if history exists (Gemini handles context)
        # Note: In a real app, you might want to prepend the system instruction once.
        
        full_prompt = f"{system_instruction}\n\nUser Question: {prompt}" if not history else prompt
        
        response = chat.send_message(full_prompt)
        return response.text

if __name__ == "__main__":
    # Test
    # engine = LLMEngine()
    # print(engine.generate_response("Tell me about yourself.", resume_text="Experienced Python Developer."))
    pass
