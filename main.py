from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.agent_routes import router as agent_router
from app.api.audit_routes import router as audit_router
from app.api.email_routes import router as email_router
from app.api.mock_provider_routes import router as mock_provider_router
from app.api.page_routes import router as page_router


app = FastAPI(
    title="CSP Email AI Agent",
    description="Internal Email AI Agent for CSP Solutions",
    version="1.0.0",
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

app.include_router(page_router)
app.include_router(agent_router)
app.include_router(email_router)
app.include_router(audit_router)
app.include_router(mock_provider_router)


@app.get("/health")
def health_check():
    """
    Basic health check endpoint.
    """

    return {
        "status": "ok",
        "service": "CSP Email AI Agent",
    }