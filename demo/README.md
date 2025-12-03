# Tests Folder - Video Demo Guide

## Purpose
Demo materials for video walkthrough showing the knowledge graph expertise search system end-to-end.

## Structure
```
tests/
   01_input_document.txt — Sample document uploaded to the system
   02_extracted_entities.json — Entities extracted by Claude NER
   03_validation_report.txt — Validation results against constraints outlined in 1 and 2 below.
   04_knowledge_graph.png — Neo4j graph visualization after upload
   05_test_queries.csv — 20 natural language queries with generated Cypher and results
   06_demo_video.mp4 — Video walkthrough of the full system

```

## Prerequisites
Before starting demo:
1. Neo4j running (Docker: `docker run -p 7474:7474 -p 7687:7687 neo4j`)
2. Backend running (`cd backend && uvicorn main:app --reload`)
3. Frontend running (`cd frontend && npm run dev`)
4. Empty Neo4j database (fresh start)

## Video Demo Script

### Part 1: Upload Document (2-3 min)
1. Open web interface (http://localhost:5173)
2. Navigate to upload page
3. Upload `01_input/testreport.pdf`
4. Show upload progress
5. Display entity extraction results:
   - 10 people extracted
   - 15 projects identified
   - Skills and relationships mapped
6. Confirm data stored in Neo4j

### Part 2: View Extracted Entities (1-2 min)
1. Show `02_extracted_entities/testreport_entities.json`
2. Highlight key entities:
   - **Sarah Chen**: GraphQL, TypeScript, Node.js, React Native
   - **Marcus Rodriguez**: PostgreSQL, Python, FastAPI, Apache Kafka
   - **Priya Sharma**: AWS, Terraform, Docker, Kubernetes
3. Point out relationships:
   - Sarah works on API Migration Project (tech lead)
   - Marcus works on Infrastructure Modernization
   - Multiple people share skills and projects

### Part 3: Execute Queries (3-4 min)

#### Query 1: "Who knows React?"
- Enter query in search interface
- Expected: Sarah Chen (has React Native)
- Show person card with skills and projects

#### Query 2: "Projects using Kubernetes?"
- Enter query in search interface
- Expected: Infrastructure Modernization, Platform Security Enhancement
- Show project cards with technologies and team members

#### Query 3: "Who worked with Sarah Chen?"
- Enter query in search interface
- Expected: Marcus Rodriguez, David Park, and others on shared projects
- Demonstrate collaboration discovery

### Part 4: Wrap Up (1 min)
- Summarize system capabilities:
  - Automated entity extraction from documents
  - Natural language query understanding
  - Graph-based expertise discovery
- Potential use cases:
  - Find experts for new projects
  - Discover collaboration opportunities
  - Map organizational knowledge

## Total Demo Time: ~8-10 minutes

## Tips for Recording
- Clear browser cache before starting
- Have all terminals open and ready
- Test upload/queries once before recording
- Show both UI interactions and underlying data
- Explain what's happening at each step
- Keep it conversational, not scripted

## Troubleshooting
- **Upload fails**: Check backend logs, verify Claude API key in .env
- **No results**: Ensure Neo4j constraints created, check query intent parsing
- **Slow extraction**: Normal for large documents (30-60 seconds)
