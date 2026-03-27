class BasePlugin:

    name = "base"

    def generate(self, example: dict):
        raise NotImplementedError

    def validate(self, payload: dict, response: str):
        raise NotImplementedError