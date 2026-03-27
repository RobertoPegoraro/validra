from fastapi import FastAPI
from app.engine.orchestrator import Orchestrator

app = FastAPI()
orchestrator = Orchestrator()

@app.post("/run")
def run_test(request: dict):
    return orchestrator.run(request)