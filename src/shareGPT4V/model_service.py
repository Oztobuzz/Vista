import google.generativeai as genai
import time

api_key = "YOUR_API_KEY"

class GeminiService:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def query(self, query, max_output_tokens=16000, temperature=0.5):
        system_message = ""
        system_message += query
        chat = self.model.start_chat(history=[])
        try:
            response = chat.send_message(
                system_message, 
                safety_settings={
                    'HARM_CATEGORY_HARASSMENT': 'block_none',
                    'HARM_CATEGORY_HATE_SPEECH': 'block_none',
                    'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'block_none',
                    'HARM_CATEGORY_DANGEROUS_CONTENT': 'block_none'
                }, 
                generation_config=genai.types.GenerationConfig(
                candidate_count=1,
                max_output_tokens=max_output_tokens,
                temperature=temperature)
            )
        except Exception as e:
            print(e)
            time.sleep(10)
        return response.text

GeminiClient = GeminiService(api_key=api_key)