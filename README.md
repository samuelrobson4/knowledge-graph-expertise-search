# Knowledge Graph MVP - Project Brief

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

### Must-Have (P0)
1. **Document Upload Interface**: Upload multiple files (PDF, DOCX, TXT)
2. **Entity Extraction Pipeline**: Automated extraction using Claude API
3. **Knowledge Graph Storage**: Neo4j backend with proper constraints
4. **Natural Language Search**: Query interface with intent parsing
5. **Results Display**: Show people with relevant skills and projects

### Nice-to-Have (P1 - Post-MVP)
1. Graph visualization (D3.js or React Flow)
2. Query autocomplete and filters
3. Feedback loop ("Was this helpful?")
4. Enhanced ranking algorithms

### Future (P2)
1. Slack bot integration
2. Google Drive connector
3. Email digests
4. Real-time collaborative features

## MVP Scope Decisions

### What We're Building
- Direct Neo4j integration (no RDF/SHACL layer)
- Claude API for NLP (no SpaCy custom training)
- Simple FastAPI backend (no Node.js adapter)
- Basic constraint validation using Neo4j features
- Manual document upload (no automated integrations yet)

### What We're NOT Building (MVP)
- User authentication (trust model for now)
- Graph visualization (P1 feature)
- Vector embeddings or semantic search
- Document versioning
- Mobile applications
- Third-party integrations (Slack, Google Drive, etc.)
- Advanced recommendation algorithms

## Success Metrics

### Week 1: Validation
- Entity extraction accuracy >70% on real documents
- Confirmed approach works with actual team status docs

### Week 4: MVP Complete
- 3 teams actively using the system
- 30+ documents uploaded and processed
- 10+ queries per day
- Qualitative feedback: "This saved me time finding expertise"

### Long-term (Post-MVP)
- 50%+ of users return within a week
- 85%+ of users find relevant experts within 3 searches
- Sub-100ms query latency for most searches

## Technical Considerations

### Entity Extraction
- Uses Claude API with structured prompts
- Extracts: people (with skills), projects (with technologies), relationships
- Returns JSON format for easy parsing
- No training data required

### Query Processing
- Natural language queries parsed by Claude API
- Determines query type (find_person, find_project)
- Extracts skills and keywords
- Maps to Cypher queries for Neo4j

### Data Validation
- Neo4j constraints ensure data integrity (uniqueness, existence)
- Application-level validation for complex rules
- No external SHACL/RDF validation needed

### Recommendation Logic
- Graph traversal to find relevant people/projects
- Ranking by skill matches and project involvement
- Multi-hop queries for implicit expertise discovery
- Similar patterns to LinkedIn, Netflix recommendation systems

## Development Approach

### Phase 1: Validate Extraction (Week 1)
Test entity extraction quality on real documents before building anything else. This is the critical validation that determines if the approach works.

### Phase 2: Build Backend (Week 2)
Implement FastAPI endpoints, Neo4j integration, and Claude API calls. Focus on getting the data flow working end-to-end.

### Phase 3: Build Frontend (Week 3)
Create simple React interface with upload and search functionality. Prioritize functionality over aesthetics.

### Phase 4: Test & Refine (Week 4)
Get real users, collect feedback, measure usage, and decide whether to continue or pivot.

## Critical Success Factors

1. **Extraction quality is everything** - Test this first with real documents
2. **Real users, real data** - No synthetic testing
3. **Start ugly, iterate fast** - Function over form for MVP
4. **Measure what matters** - Track usage, not vanity metrics
5. **Be ready to pivot** - If extraction fails or users don't engage, adjust approach

## Environment Requirements

- Python 3.11+
- Node.js 18+
- Docker (for Neo4j)
- Anthropic API key
- 3-5 real status documents for testing
```