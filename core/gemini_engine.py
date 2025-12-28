# gemini_engine.py
from google import genai
from google.genai import types  # optional, for structured/chat inputs
import logging

logger = logging.getLogger(__name__)

class GeminiEngine:
    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        """
        Simple text usage: pass 'contents' as a string (SDK converts it)
        """
        try:
            resp = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
            )
            return getattr(resp, "text", None) or str(resp)
        except Exception as e:
            logger.exception("Gemini generate failed")
            # Check if it's a RESOURCE_EXHAUSTED error
            error_msg = str(e)
            if "RESOURCE_EXHAUSTED" in error_msg:
                return (
                    "⚠️ Gemini API quota exceeded. "
                    "You've reached your daily limit for this model. "
                    "Please check your plan or try again later."
                )
            # Generic fallback for other errors
            return f"⚠️ Gemini API error: {error_msg}"

    def generate_chat(self, contents_list):
        """
        Example for structured/chat usage. `contents_list` can be:
        - a single string
        - a list of strings
        - a types.Content (or list of types.Content) for roles/parts
        """
        try:
            resp = self.client.models.generate_content(
                model=self.model,
                contents=contents_list,
            )
            return getattr(resp, "text", None) or str(resp)
        except Exception as e:
            logger.exception("Gemini generate_chat failed")
            return f"[Gemini Error] {e}"
