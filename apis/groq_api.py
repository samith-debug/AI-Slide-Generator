from groq import Groq
from apis.base_generation_api import BaseGenerationAPIClient


class GroqAPIClient(BaseGenerationAPIClient):
    def __init__(self, api_key, model):
        super().__init__(api_key, model)

        
        self.client = Groq(api_key=api_key)

        
        self.default_model = "llama-3.3-70b-versatile"

    def generate(self, prompt) -> str:
        """
        Sends a prompt to Groq using a supported model.
        Automatically falls back to default model if needed.
        """

        model_to_use = self.model or self.default_model

        
        response = self.client.chat.completions.create(
            model=model_to_use,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates structured slide content."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )

        
        return response.choices[0].message.content.strip()
