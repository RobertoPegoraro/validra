from app.plugins.fuzz.fuzz import FuzzPlugin
from app.plugins.security.security import SecurityPlugin
import time

PLUGINS = {
    "FUZZ": FuzzPlugin(),
    "AUTH": SecurityPlugin()
}

class Orchestrator:

    def __init__(self, plugin, executor):
        self.plugin = plugin
        self.executor = executor

    def generate(self, payload, max_cases):
        return self.plugin.generate(payload, max_cases=max_cases)

    def run(self, request, tests):
        enriched_tests = []
        success_count = 0

        for idx, test in enumerate(tests, start=1):
            payload = test.get("payload", {})
            test_headers = test.get("headers")

            start = time.time()
            response = self.executor.execute(request, payload, headers=test_headers)
            duration = int((time.time() - start) * 1000)

            success = 200 <= response.get("status_code", 500) < 300

            if success:
                success_count += 1

            enriched_tests.append({
                "id": f"tc-{idx:03}",
                "description": test.get("description"),
                "request": {
                    "payload": payload,
                    "headers": test_headers if test_headers is not None else request.get("headers", {})
                },
                "response": response,
                "success": success,
                "duration_ms": duration
            })

        return {
            "tests": enriched_tests,
            "summary": {
                "total": len(enriched_tests),
                "success": success_count,
                "failed": len(enriched_tests) - success_count
            }
        }