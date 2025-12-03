"""FastAPI application for Knowledge Graph API."""
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from backend.config import settings
from backend.services.neo4j_client import test_connection
from backend.services.document_processor import extract_text
from backend.services.entity_extractor import extract_entities_with_claude
from backend.services.neo4j_storage import store_entities_in_neo4j, get_graph_stats, get_graph_data
from backend.services.neo4j_query import search_knowledge_graph
from backend.validation import validate_entities

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="API for knowledge graph extraction and search",
    version="0.1.0"
)

# Add CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

    # Step 4: Store entities in Neo4j
    try:
        storage_stats = await store_entities_in_neo4j(entities)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to store entities in Neo4j: {str(e)}"
        )

    # Return success with storage stats
    return {
        "filename": file.filename,
        "text_length": len(text),
        "extraction_summary": {
            "people_count": len(entities.get("people", [])),
            "projects_count": len(entities.get("projects", [])),
            "relationships_count": len(entities.get("relationships", []))
        },
        "storage_stats": storage_stats,
        "message": "Document processed and entities stored successfully"
    }


@app.get("/stats")
async def get_stats():
    """
    Get knowledge graph statistics.

    Returns:
        JSON with node counts and relationship counts
    """
    try:
        stats = await get_graph_stats()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve graph stats: {str(e)}"
        )


@app.get("/graph")
async def get_graph(limit: int = Query(500, description="Maximum number of relationships to return")):
    """
    Get graph data for visualization.

    Returns nodes and links for all entities in the knowledge graph.

    Args:
        limit: Maximum number of relationships to return (default 100)

    Returns:
        JSON with:
        - nodes: List of nodes (id, label, type, properties)
        - links: List of relationships (source, target, type, label)
        - stats: Graph statistics (node_count, link_count, truncated)
    """
    try:
        graph_data = await get_graph_data(limit)
        return graph_data
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve graph data: {str(e)}"
        )


@app.get("/search")
async def search(query: str = Query(..., description="Natural language search query")):
    """
    Search the knowledge graph using natural language.

    Parses the query intent and executes appropriate Neo4j queries to find:
    - People with specific skills
    - Projects using specific technologies
    - Collaborators who worked together
    - Detailed information about specific people

    Args:
        query: Natural language search query (e.g., "Find people with React", "Who worked with Sarah?")

    Returns:
        JSON with:
        - intent: Detected query type
        - results: List of matching results
        - result_count: Number of results
        - explanation: Human-readable description
        - ranking_strategy: How results are ranked
    """
    if not query or not query.strip():
        raise HTTPException(status_code=400, detail="Query parameter is required")

    try:
        result = await search_knowledge_graph(query)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    from backend.services.neo4j_client import Neo4jClient
    Neo4jClient.close_driver()
