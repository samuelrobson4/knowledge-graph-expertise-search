# Knowledge Graph Expertise Search Engine

## Project Overview
Build a graph-based expert recommendation system that helps employees discover relevant expertise, projects, and resources within their organization. Users upload status documents, and the system extracts entities to populate a searchable knowledge graph.

## Problem Statement
In growing organizations, knowledge about who knows what and where to find relevant information is scattered. This leads to duplicated effort, slower progress, and missed collaboration opportunities. This system centralizes expertise discovery through automated entity extraction and natural language search.

## Core User Flow

### Phase 1: Seeding the Graph
1. Team leads upload status documents (PDFs, DOCX, TXT files)
2. System extracts people, skills, projects, and relationships
3. Data is stored in a knowledge graph
4. Summary shows: "X people, Y skills, Z projects indexed"

### Phase 2: Querying the Graph
1. Users enter natural language queries ("Who knows React?", "Projects using GraphQL?")
2. System parses intent and searches the graph
3. Results show relevant people with their skills and project history
4. Users can contact recommended experts

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: Neo4j (graph database)
- **NLP**: Claude API (Anthropic) for entity extraction and query parsing
- **Document Processing**: PyMuPDF, python-docx for text extraction

### Frontend
- **Framework**: React with TypeScript
- **Build Tool**: Vite
- **Styling**: Inline styles (keep it simple for MVP)

### Infrastructure
- **Neo4j**: Docker container (local development)
- **API Keys**: Anthropic Claude API

## Graph Data Model

### Nodes
- **Person**: {name: string}
- **Skill**: {name: string}
- **Project**: {name: string, description: string}

### Relationships
- **(Person)-[:HAS_SKILL]->(Skill)**
- **(Person)-[:WORKS_ON {role: string}]->(Project)**
- **(Project)-[:USES_TECH]->(Skill)**

## Key Features

1. **Document Upload Interface**: Upload multiple files (PDF, DOCX, TXT)
2. **Entity Extraction Pipeline**: Automated extraction using Claude API
3. **Knowledge Graph Storage**: Neo4j backend with proper constraints
4. **Natural Language Search**: Query interface with intent parsing
5. **Results Display**: Show people with relevant skills and projects

## Environment Requirements

- Python 3.11+
- Node.js 18+
- Docker (for Neo4j)
- Anthropic API key
- 3-5 real status documents for testing
```