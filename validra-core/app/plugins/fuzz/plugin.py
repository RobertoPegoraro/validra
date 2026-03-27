from app.plugins.base import BasePlugin
from app.providers.ollama_provider import call_llm

import json

class FuzzPlugin(BasePlugin):

    name = "fuzz"

    def generate(self, example):

        prompt = f"""
        Given this valid JSON:
        {json.dumps(example)}

        Generate 10 fuzzy variations.
        Return ONLY JSON array.
        """

        return json.loads(call_llm(prompt))


    def validate(self, payload, response):

        prompt = f"""
        Payload:
        {json.dumps(payload)}

        Response:
        {response}

        Is this correct?

        Return JSON:
        {{
          "valid": true/false,
          "reason": "..."
        }}
        """

        return json.loads(call_llm(prompt))