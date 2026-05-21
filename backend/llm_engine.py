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
        # We will try these models in order if one fails
        self.model_names = [
            'gemini-1.5-flash',
            'models/gemini-1.5-flash',
            'gemini-2.5-flash',
            'gemini-1.5-pro',
            'gemini-pro'
        ]
        self.current_model_index = 0
        self.model = genai.GenerativeModel(self.model_names[self.current_model_index])

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
        
        full_prompt = f"{system_instruction}\n\nUser Question: {prompt}" if not history else prompt

        # Attempt generation with model fallback
        last_error = None
        for i in range(self.current_model_index, len(self.model_names)):
            model_name = self.model_names[i]
            try:
                print(f"Attempting response generation with: {model_name}...")
                model = genai.GenerativeModel(model_name)
                chat = model.start_chat(history=history or [])
                response = chat.send_message(full_prompt)
                
                # Remember the successful model index for subsequent calls
                self.current_model_index = i
                self.model = model
                return response.text
            except Exception as e:
                print(f"Model {model_name} failed: {str(e)}")
                last_error = e
                continue
                
        # If all models failed, raise the last exception
        raise last_error

if __name__ == "__main__":
    # Test
    # engine = LLMEngine()
    # print(engine.generate_response("Tell me about yourself.", resume_text="Experienced Python Developer."))
    pass
