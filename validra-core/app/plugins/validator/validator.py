from app.providers.ollama_provider import call_llm
import json
import re


class LLMValidatorPlugin:

    def validate_with_llm(self, test, response, meta=None):
        meta = meta or {}

        prompt = f"""
You are an expert API test validator.

Your job is to determine if the API response satisfies the intent of the test case.

---

TEST DESCRIPTION:
{test.get("description")}

TEST PAYLOAD:
{json.dumps(test.get("payload", {}), indent=2)}

META CONSTRAINTS (for context only):
{json.dumps(meta, indent=2)}

API RESPONSE:
{json.dumps(response, indent=2)}

---

EVALUATION INSTRUCTIONS:

- Use the test description as the primary source of intent.
- Evaluate whether the API behaved correctly.
- Consider:
  - Whether invalid inputs were rejected
  - Whether valid inputs were accepted
  - Whether the response matches expected behavior
  - Whether errors are appropriate or unexpected
- Meta constraints are additional context to guide your reasoning.

---

OUTPUT FORMAT (STRICT JSON ONLY):

- Output MUST be a single JSON object
- No explanations outside JSON
- No markdown or code blocks
- The response must start with {{ and end with }}
- Keep the "reason" field concise (1–3 sentences)

Return:

{{
  "dstatus": "PASS | FAIL | WARN",
  "reason": "Brief explanation",
  "confidence": 0.0
}}
"""

        try:
            raw = call_llm(prompt)
            result = self.extract_json(raw)
            return result

        except Exception as e:
            return {
                "dstatus": "WARN",
                "reason": f"LLM validation failed: {str(e)}",
                "confidence": 0.0
            }

    def extract_json(self, raw):
        if not raw:
            raise ValueError("Empty LLM response")

        # If already parsed dict
        if isinstance(raw, dict):
            return raw

        if isinstance(raw, str):
            raw = raw.strip()

            # Remove markdown code blocks if present
            if "```" in raw:
                parts = raw.split("```")
                for part in parts:
                    part = part.strip()
                    if part.startswith("json"):
                        part = part[4:].strip()
                    if part.startswith("{"):
                        raw = part
                        break

            # Extract JSON object (non-greedy)
            match = re.search(r"\{[\s\S]*?\}", raw)
            if not match:
                raise ValueError(f"No JSON found in LLM output: {raw}")

            json_str = match.group()

            # Try parsing
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                # Fallback: attempt to recover truncated JSON
                last_brace = json_str.rfind("}")
                if last_brace != -1:
                    json_str = json_str[:last_brace + 1]
                    return json.loads(json_str)

                raise ValueError(f"Invalid JSON: {json_str}")

        raise ValueError(f"Unsupported LLM output type: {type(raw)}")