class BasePlugin:

    name = "base"

    def generate(self, example: dict):
        raise NotImplementedError
