class BasePlugin:

    name = "base"

    def generate(self, example: dict, meta: dict):
        raise NotImplementedError
