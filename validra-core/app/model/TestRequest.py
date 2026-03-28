from pydantic import BaseModel, Field

class TestRequest(BaseModel):
    endpoint: str
    method: str
    headers: dict = {}
    payload: dict
    test_type: str
    max_cases: int = Field(
        default=10,
        ge=3,
        le=100,
        description="Maximum number of test cases to generate(3-100)"
    )

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
                    "test_type": "FUZZ",
                    "max_cases": 10
                }
            ]
        }
    }