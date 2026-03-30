from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class TestRequest(BaseModel):
    endpoint: str
    method: str
    headers: dict = {}
    payload: dict
    payload_meta: Optional[Dict[str, Any]] = None
    test_type: str
    max_cases: int = Field(
        default=10,
        ge=3,
        le=100,
        description="Maximum number of test cases to generate(3-100)"
    )
    validate: bool = True   

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "endpoint": "https://jsonplaceholder.typicode.com/posts",
                    "method": "POST",
                    "headers": {
                        "Content-Type": "application/json",
                        "Authorization": "Bearer your-token-here"
                    },
                    "payload": {
                        "title": "Validra Test",
                        "body": "Testing fuzzy payload generation",
                        "userId": 30
                    },
                    "payload_meta": {
                        "body": "required, alphanumeric [1-50]",
                        "title": "optional, alphanumeric [1-50]",
                        "userId": "numeric [1-999]"
                    },
                    "test_type": "FUZZ",
                    "max_cases": 10,
                    "validate": True
                }
            ]
        }
    }