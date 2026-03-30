from app.plugins.base import BasePlugin
from app.providers.ollama_provider import call_llm
import json
import re


class LLMBasePlugin(BasePlugin):

    def _extract_json(self, response):
        try:
            if isinstance(response, list):
                return response

            if not isinstance(response, str):
                raise ValueError(f"Unexpected response type: {type(response)}")

            response = re.sub(r"(?i)final text:\s*", "", response)

            start = response.find("[")
            end = response.rfind("]")

            if start == -1 or end == -1:
                raise ValueError("No JSON array found")

            json_str = response[start:end + 1]

            # 🚨 HARD SANITIZATION RULES

            # Replace JS constructors like new Array(...)
            json_str = re.sub(r'new\s+Array\(\d+\)\.fill\([^\)]*\)\.join\([^\)]*\)', '"INVALID_STRING"', json_str)

            # Replace any remaining JS-like patterns
            json_str = re.sub(r'new\s+\w+\(.*?\)', '"INVALID_STRING"', json_str)

            # Remove trailing .repeat() or similar
            json_str = re.sub(r'\.repeat\(\d+\)', '', json_str)

            # Fix undefined
            json_str = re.sub(r'\bundefined\b', 'null', json_str)

            return json.loads(json_str)

        except Exception as e:
            raise ValueError(f"Failed to parse JSON: {e}")

    def _build_prompt(self, example, previous_cases, batch_size, meta=None):
        raise NotImplementedError

    def _is_valid_case(self, case):
        raise NotImplementedError

    def generate(self, example, previous_cases=None, max_cases=10, meta=None):

        if previous_cases is None:
            previous_cases = []

        all_cases = previous_cases.copy()

        while len(all_cases) < max_cases:

            remaining = max_cases - len(all_cases)
            batch_size = min(3, remaining)

            prompt = self._build_prompt(example, all_cases, batch_size, meta)

            try:
                raw = call_llm(prompt)
                print("RAW LLM OUTPUT:\n", raw)

                new_cases = self._extract_json(raw)
                print("PARSED CASES:\n", new_cases)

                if isinstance(new_cases, list):
                    added_any = False

                    for case in new_cases:
                        if len(all_cases) >= max_cases:
                            break
                        if not isinstance(case, dict):
                            continue
                        if not self._is_valid_case(case):
                            continue
                        if case not in all_cases:
                            all_cases.append(case)
                            added_any = True

                    if not added_any:
                        break
                else:
                    print("Unexpected format from LLM:", new_cases)

            except Exception as e:
                raise RuntimeError(f"{str(e)}")

        return all_cases[:max_cases]