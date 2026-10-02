from groq import Groq
from apis.base_generation_api import BaseGenerationAPIClient


# Ordered list of fallback models — tries each until one works
GROQ_FALLBACK_MODELS = [
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
]


class GroqAPIClient(BaseGenerationAPIClient):
    def __init__(self, api_key, model):
        super().__init__(api_key, model)
        self.client = Groq(api_key=api_key)

    def _get_available_model(self):
        """
        Returns the first model from GROQ_FALLBACK_MODELS that is available
        on this account, falling back gracefully if none match.
        """
        try:
            available_ids = {m.id for m in self.client.models.list().data}
            for candidate in GROQ_FALLBACK_MODELS:
                if candidate in available_ids:
                    print(f"[Groq] Using model: {candidate}")
                    return candidate
            # If none matched exactly, just try them in order at call time
            print("[Groq] No exact match found in available models — will try fallback list at call time.")
        except Exception as e:
            print(f"[Groq] Could not fetch model list: {e}")
        return GROQ_FALLBACK_MODELS[0]

    def generate(self, prompt) -> str:
        """
        Sends a prompt to Groq. If a model is explicitly set, use it.
        Otherwise auto-detect the best available model and try fallbacks.
        """
        if self.model:
            models_to_try = [self.model]
        else:
            try:
                models_to_try = [self._get_available_model()]
            except Exception:
                models_to_try = GROQ_FALLBACK_MODELS

        last_error = None
        for model_id in models_to_try:
            try:
                response = self.client.chat.completions.create(
                    model=model_id,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates structured slide content."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.4
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"[Groq] Model {model_id} failed: {e}")
                last_error = e

        raise RuntimeError(f"All Groq models failed. Last error: {last_error}")
