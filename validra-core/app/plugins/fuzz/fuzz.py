import json
from app.plugins.llm_base_plugin import LLMBasePlugin


class FuzzPlugin(LLMBasePlugin):
    name = "fuzz"

    def _is_valid_case(self, case):
        return (
            isinstance(case, dict)
            and "description" in case
            and "payload" in case
        )

    def _build_prompt(self, example, previous_cases, batch_size):
        return f"""
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
- DO NOT generate or modify headers
- ONLY generate payload variations
- Ignore any headers in the input

Previous cases:
{json.dumps(previous_cases, indent=2)}

INPUT PAYLOAD:
{json.dumps(example, indent=2)}
"""