from app.plugins.base import BasePlugin
from app.providers.ollama_provider import call_llm
import json
import re


class FuzzPlugin(BasePlugin):
    name = "fuzz"

    def _extract_json(self, response):
        """
        Accepts either a raw string or already-parsed JSON (list).
        """

        try:
            # Se já vier como lista, retorna direto
            if isinstance(response, list):
                return response

            if not isinstance(response, str):
                raise ValueError(f"Unexpected response type: {type(response)}")

            # Remove prefixos comuns
            response = re.sub(r"(?i)final text:\s*", "", response)

            # Extrai bloco JSON
            start = response.find("[")
            end = response.rfind("]")

            if start == -1 or end == -1:
                raise ValueError("No JSON array found")

            json_str = response[start:end + 1]

            json_str = re.sub(r'\bundefined\b', 'null', json_str)

            return json.loads(json_str)

        except Exception as e:
            raise ValueError(f"Failed to parse JSON: {e}")

    def generate(self, example, previous_cases=None, max_cases=35):
        """
        Generate negative/fuzz test cases with simple and robust parsing.
        """

        if previous_cases is None:
            previous_cases = []

        all_cases = previous_cases.copy()

        while len(all_cases) < max_cases:

            remaining = max_cases - len(all_cases)
            batch_size = min(5, remaining)

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
    - undefined, NaN, Infinity or any other JSON non-valid
- All values must be literal JSON types: 
    - string 
    - number 
    - boolean (true/false)
    - null 
    - object 
    - array Never use expressions like: new String(), repeat(), fill(), or any computed values.
    - Do not use any non-JSON literals or language-specific values.

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
                    added_any = False

                    for case in new_cases:
                        if not isinstance(case, dict):
                            continue

                        if "description" not in case or "payload" not in case:
                            continue

                        if case not in all_cases:
                            all_cases.append(case)
                            added_any = True

                    # evita loop infinito caso não venha nada novo
                    if not added_any:
                        break

                else:
                    print("Unexpected format from LLM:", new_cases)
                    break

            except Exception as e:
                print("Error generating cases:", e)
                break

        return all_cases