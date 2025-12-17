from typing import List, Dict, Optional
import os
from anthropic import Anthropic
import openai

class LLMClient:
    def __init__(self, provider: str = "anthropic"):
        self.provider = provider
        if provider == "anthropic":
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            self.model = "claude-3-5-sonnet-20241022"
        elif provider == "openai":
            openai.api_key = os.getenv("OPENAI_API_KEY")
            self.model = "gpt-4-turbo-preview"

    def generate(self, messages: List[Dict], system: Optional[str] = None, temperature: float = 0.7, max_tokens: int = 4096) -> str:
        if self.provider == "anthropic":
            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages
            }
            if system:
                kwargs["system"] = system

            response = self.client.messages.create(**kwargs)
            return response.content[0].text

        elif self.provider == "openai":
            if system:
                messages = [{"role": "system", "content": system}] + messages

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content

    def generate_with_tools(self, messages: List[Dict], tools: List[Dict], system: Optional[str] = None) -> Dict:
        if self.provider == "anthropic":
            kwargs = {
                "model": self.model,
                "max_tokens": 4096,
                "messages": messages,
                "tools": tools
            }
            if system:
                kwargs["system"] = system

            response = self.client.messages.create(**kwargs)

            result = {
                "content": [],
                "stop_reason": response.stop_reason,
                "tool_calls": []
            }

            for block in response.content:
                if block.type == "text":
                    result["content"].append({"type": "text", "text": block.text})
                elif block.type == "tool_use":
                    result["tool_calls"].append({
                        "id": block.id,
                        "name": block.name,
                        "input": block.input
                    })

            return result

        return {"content": [{"type": "text", "text": "Tool use not implemented for this provider"}], "tool_calls": []}
