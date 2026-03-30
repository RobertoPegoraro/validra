from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.openapi.docs import get_swagger_ui_html

from app.plugins.fuzz.fuzz import FuzzPlugin
from app.plugins.security.security import SecurityPlugin
from app.plugins.pen.pen import PenTestPlugin
from app.engine.executor import Executor
from app.engine.orchestrator import Orchestrator
from app.model.TestRequest import TestRequest
from app.plugins.validator.validator import LLMValidatorPlugin
from app.model.ValidateRequest import ValidateRequest

app = FastAPI(
    title="Validra",
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
    docs_url=None,
    redoc_url=None
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

PLUGINS = {
    "FUZZ": FuzzPlugin(),
    "AUTH": SecurityPlugin(),
    "PEN" : PenTestPlugin()
}

executor = Executor()
validator = LLMValidatorPlugin()

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title="Validra",
        swagger_favicon_url="/favicon.ico",
        swagger_ui_parameters={
            "defaultModelsExpandDepth": -1,
            "defaultModelExpandDepth": -1 
        }
    )

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("app/static/favicon.ico")

@app.post("/validate", summary='Validate Response from /generateAndRun', tags=["Validation"])
def validate(request: ValidateRequest):
    try:
        result = validator.validate_with_llm(
            test=request.test,
            response=request.response,
            meta=request.meta or {}
        )
        return {
            "validation": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Validation error: {str(e)}"
        )

@app.post("/generateAndRun", summary='Generates Test Cases and Run', tags=["Execution"])
def generate_and_run(request: TestRequest):

    """
    Generate and execute automated API tests.

    This endpoint is responsible for:
    1. Generating test cases based on the provided payload.
    2. Executing those tests against the target endpoint.
    3. Returning both the generated tests and their execution results.

    ## Test Types

    ### 1. FUZZY
    - Focuses on input validation and robustness.
    - Generates invalid, unexpected, or edge-case payloads.
    - Helps identify crashes, validation issues, and improper error handling.

    ### 2. AUTH
    - Focuses on authentication and authorization scenarios.
    - Validates access control mechanisms.
    - Examples include missing tokens, invalid tokens, expired credentials.
    - Try to gain access/explore vunerabilities.

    ### 3. PEN (Penetration Testing)
    - Focuses on security vulnerabilities.
    - Attempts to identify common security flaws such as:
      - Injection attacks (SQL, NoSQL, etc.)
      - Improper input sanitization
      - Security misconfigurations
    - Simulates malicious behavior to evaluate system resilience.

    ## Response
    - `tests`: The list of generated test cases.
    - `results`: The execution results for each test case.

    ## Example Flow

    1. Client sends a request with an API payload.
    2. System generates FUZZY, AUTH, or PEN test cases.
    3. System executes each test against the target endpoint.
    4. System returns structured results for analysis.

    """

    plugin = PLUGINS.get(request.test_type.upper())

    if not plugin:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported test type: {request.test_type}"
        )

    orchestrator = Orchestrator(plugin, executor)

    safe_input = {
        "payload": request.payload,
        "headers": request.headers,
        "meta": request.payload_meta or {}
    }

    try:
        tests = orchestrator.generate(safe_input, request.max_cases)
        tests = tests[:request.max_cases]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating test cases: {str(e)}"
        )

    if not tests:
        raise HTTPException(
            status_code=500,
            detail="No test cases were generated. LLM may be unavailable or returned invalid output."
        )
    
    try:
        safe_request = {
            "endpoint": request.endpoint,
            "method": request.method,
            "headers": request.headers
        }
        results = orchestrator.run(safe_request, tests)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error executing test cases: {str(e)}"
        )

    return results