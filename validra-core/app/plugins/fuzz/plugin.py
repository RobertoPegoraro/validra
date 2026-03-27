from app.plugins.base import BasePlugin
from app.providers.ollama_provider import call_llm
import json
import re


class FuzzPlugin(BasePlugin):
    name = "fuzz"

    def _extract_json(self, text: str):
        """
        Extract the first valid JSON array from LLM output.
        Cleans common prefixes like 'FINAL TEXT:' and ignores extra text.
        """
        try:
            # Remove common prefixes
            text = re.sub(r"(?i)final text:\s*", "", text)

            # Locate JSON array boundaries
            start = text.find("[")
            end = text.rfind("]")

            if start == -1 or end == -1:
                raise ValueError("No JSON array found in response")

            json_str = text[start:end + 1]

            return json.loads(json_str)

        except Exception as e:
            raise ValueError(f"Failed to parse JSON: {e}")

    def generate(self, example, previous_cases=None, max_cases=10):
        """
        Generate negative/fuzz test cases with simple and robust parsing.
        """

        if previous_cases is None:
            previous_cases = []

        all_cases = previous_cases.copy()
        batch_size = min(5, max_cases)

        prompt = f"""
You are a senior QA engineer specialized in API testing.

TASK:
Generate up to {batch_size} diverse negative and edge test cases.

STRICT OUTPUT RULES:
- Return ONLY a valid JSON array
- Do NOT include any extra text, prefixes, or explanations
- Do NOT include "FINAL TEXT" or similar labels
- Output must start with [ and end with ]
- Use only valid JSON types
- Do not suggest any attacks, credentials, tokens, or anything that could be interpreted as a security test.
- Do NOT include: 
    - JavaScript expressions 
    - functions 
    - constructors (e.g., new String) 
    - comments 
    - pseudo-code 
- All values must be literal JSON types: 
    - string 
    - number 
    - boolean 
    - null 
    - object 
    - array Never use expressions like: new String(), repeat(), fill(), or any computed values.

VALID EXAMPLE:
[
    {{
        "description": "...",
        "payload": {{}}
    }}
]

IMPORTANT:
- Do NOT repeat previous cases
- Focus on invalid, edge, and malformed inputs
- Keep cases diverse

Previous cases:
{json.dumps(all_cases, indent=2)}

INPUT PAYLOAD:
{json.dumps(example, indent=2)}
"""

        try:
            raw = call_llm(prompt)

            new_cases = self._extract_json(raw)

            if isinstance(new_cases, list):
                for case in new_cases:
                    if not isinstance(case, dict):
                        continue

                    if "description" not in case or "payload" not in case:
                        continue

                    if case not in all_cases:
                        all_cases.append(case)
            else:
                print("Unexpected format from LLM:", new_cases)

        except Exception as e:
            print("Error generating cases:", e)

        return all_cases