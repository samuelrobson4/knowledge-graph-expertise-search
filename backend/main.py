"""FastAPI application for Knowledge Graph API."""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from backend.config import settings
from backend.services.neo4j_client import test_connection
from backend.services.document_processor import extract_text
from backend.services.entity_extractor import extract_entities_with_claude
from backend.validation import validate_entities

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


@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and process a document.

    Extracts text, then extracts entities using Claude API.

    Args:
        file: Document file to process (.pdf, .docx, .txt)

    Returns:
        JSON with extracted entities (people, projects, relationships) and metadata
    """
    # Validate file was provided
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # Step 1: Extract text
    text = await extract_text(file)

    # Step 2: Extract entities using Claude API
    try:
        entities = await extract_entities_with_claude(text)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Entity extraction failed: {str(e)}"
        )

    # Step 3: Validate entities
    valid, errors = validate_entities(entities)
    if not valid:
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Extracted entities failed validation",
                "errors": errors,
                "entities": entities
            }
        )

    # Return extracted entities with metadata
    return {
        "filename": file.filename,
        "text_length": len(text),
        "entities": entities,
        "summary": {
            "people_count": len(entities.get("people", [])),
            "projects_count": len(entities.get("projects", [])),
            "relationships_count": len(entities.get("relationships", []))
        }
    }


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    from backend.services.neo4j_client import Neo4jClient
    Neo4jClient.close_driver()
