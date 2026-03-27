from app.plugins.base import BasePlugin

class SecurityPlugin(BasePlugin):

    name = "security"

    def generate(self, example):
        return [
            {"payload": "' OR 1=1 --"},
            {"payload": "<script>alert(1)</script>"}
        ]

    def validate(self, payload, response):
        if "sql" in response.lower():
            return {"valid": False, "reason": "Possible SQL injection leak"}

        return {"valid": True}