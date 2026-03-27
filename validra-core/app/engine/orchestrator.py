from app.plugins.fuzz.plugin import FuzzPlugin
from app.plugins.security.plugin import SecurityPlugin

PLUGINS = {
    "fuzz": FuzzPlugin(),
    "security": SecurityPlugin()
}

class Orchestrator:

    def __init__(self, plugin, executor):
        self.plugin = plugin
        self.executor = executor

    def run(self, request):

        tests = self.plugin.generate(request["payload"])

        results = []

        for test in tests:
            description = test.get("description", "generated")
            payload = test.get("payload", {})

            print(payload)

            response = self.executor.execute(request, payload)

            result = {
                "description": description,
                "request": payload,
                "response": response
            }

            print("TEST RESULT:", result)  # 👈 debug

            results.append(result)

        return results