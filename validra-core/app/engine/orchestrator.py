from app.plugins.fuzz.plugin import FuzzPlugin
from app.plugins.security.plugin import SecurityPlugin

PLUGINS = {
    "fuzz": FuzzPlugin(),
    "security": SecurityPlugin()
}

class Orchestrator:

    def run(self, request):

        plugin = PLUGINS.get(request["type"], FuzzPlugin())

        payloads = plugin.generate(request["examplePayload"])

        results = []

        for payload in payloads:
            results.append({
                "payload": payload,
                "status": "pending"
            })

        return results