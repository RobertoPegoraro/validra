from pydantic import BaseModel

class TestRequest(BaseModel):
    endpoint: str
    method: str
    payload: dict
    type: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "endpoint": "https://jsonplaceholder.typicode.com/posts",
                    "method": "POST",
                    "payload": {
                        "title": "Validra Test",
                        "body": "Testing fuzzy payload generation",
                        "userId": 30
                    },
                    "type": "fuzz"
                }
            ]
        }
    }