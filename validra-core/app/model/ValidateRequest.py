from pydantic import BaseModel
from typing import Dict, Any, Optional

class ValidateRequest(BaseModel):
    test: Dict[str, Any]
    response: Dict[str, Any]
    meta: Optional[Dict[str, Any]] = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "test": {
                        "id": "tc-001",
                        "description": "Body too long",
                        "payload": {
                            "title": "Validra Test",
                            "body": "Testing fuzzy payload generation",
                            "userId": 30
                        }
                    },
                    "response": {
                        "status_code": 201,
                        "body": {
                            "id": 101
                        }
                    },
                    "meta": {
                        "body": "required, alphanumeric [1-50]",
                        "title": "optional, alphanumeric [1-50]",
                        "userId": "numeric [1-999]"
                    }
                }
            ]
        }
    }