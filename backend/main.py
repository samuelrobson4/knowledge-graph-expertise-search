"""FastAPI application for Knowledge Graph API."""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from backend.config import settings
from backend.services.neo4j_client import test_connection

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="API for knowledge graph extraction and search",
    version="0.1.0"
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Knowledge Graph API",
        "version": "0.1.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint.

    Verifies:
    - API is running
    - Neo4j connection is working
    - Environment variables are loaded
    """
    # Test Neo4j connection
    neo4j_ok = test_connection()

    # Check if API key is configured
    api_key_configured = bool(settings.anthropic_api_key)

    # Overall health status
    healthy = neo4j_ok and api_key_configured

    status = {
        "status": "healthy" if healthy else "unhealthy",
        "checks": {
            "neo4j": "connected" if neo4j_ok else "disconnected",
            "anthropic_api_key": "configured" if api_key_configured else "missing"
        }
    }

    status_code = 200 if healthy else 503
    return JSONResponse(content=status, status_code=status_code)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    from backend.services.neo4j_client import Neo4jClient
    Neo4jClient.close_driver()
