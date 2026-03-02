from __future__ import annotations

from app.config import Settings


class LLMClient:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings()

    def is_available(self) -> bool:
        return bool(self.settings.openai_api_key or self.settings.anthropic_api_key)

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        if self.settings.openai_api_key:
            return self._chat_openai(system_prompt, user_prompt)
        if self.settings.anthropic_api_key:
            return self._chat_anthropic(system_prompt, user_prompt)
        raise RuntimeError("No LLM provider configured")

    def _chat_openai(self, system_prompt: str, user_prompt: str) -> str:
        from openai import OpenAI

        client = OpenAI(api_key=self.settings.openai_api_key)
        response = client.chat.completions.create(
            model=self.settings.openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content or ""

    def _chat_anthropic(self, system_prompt: str, user_prompt: str) -> str:
        from anthropic import Anthropic

        client = Anthropic(api_key=self.settings.anthropic_api_key)
        response = client.messages.create(
            model=self.settings.anthropic_model,
            max_tokens=500,
            temperature=0.7,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        chunks = [b.text for b in response.content if getattr(b, "type", "") == "text"]
        return "".join(chunks).strip()
