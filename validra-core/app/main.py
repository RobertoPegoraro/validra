from fastapi import FastAPI, Body
from app.plugins.fuzz.plugin import FuzzPlugin
from app.engine.executor import Executor
from app.engine.orchestrator import Orchestrator
from app.model.TestRequest import TestRequest

app = FastAPI(
    title="Validra",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1}
)

plugin = FuzzPlugin()
executor = Executor()
orchestrator = Orchestrator(plugin, executor)

@app.post("/run")
def run_test(request: TestRequest):
    return orchestrator.run(request.model_dump())