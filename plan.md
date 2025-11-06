
Phase 1: Backend Core (Days 3-7)

Day 3: Project Setup
Create backend/ directory
Set up requirements.txt (fastapi, uvicorn, anthropic, neo4j, pymupdf, python-docx, python-multipart, python-dotenv)
Create .env file (ANTHROPIC_API_KEY, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
Create .gitignore (venv, .env, pycache)
Initialize Git repo

Day 4: Document Processing
Create main.py with FastAPI app
Implement extract_text(file: UploadFile) -> str
Handle PDF (PyMuPDF)
Handle DOCX (python-docx)
Handle TXT (decode utf-8)
Test with sample files via pytest or manual upload

Day 5: Claude API Integration
Implement extract_entities(text: str) -> Dict
Use your refined prompt
Handle JSON parsing (strip markdown if present)
Add error handling for API failures
Test with multiple document types

Day 6: Neo4j Storage
Implement store_in_neo4j(entities: Dict)
Create Person nodes + HAS_HARD_SKILL relationships
Create Person nodes + HAS_SOFT_SKILL relationships
Create Project nodes + USES_TECH relationships
Create WORKS_ON relationships with role property
Handle duplicates (MERGE instead of CREATE)

Day 7: API Endpoints
POST /upload - process document, return entities
GET /stats - return counts (people, hard_skills, soft_skills, projects)
Test endpoints with curl or Postman
Verify data in Neo4j Browser
Milestone: Backend functional end-to-end


Phase 2: Query System (Days 8-10)

Day 8: Query Intent Parsing
Implement parse_query_intent(query: str) -> Dict
Call Claude API to extract: type, skills, keywords
Test with 10 sample queries
Refine prompt based on results

Day 9: Neo4j Query Logic
Implement search_people_by_skill(skills: List[str]) -> List[Dict]
Implement search_projects_by_tech(techs: List[str]) -> List[Dict]
Implement find_collaborators(person_name: str) -> List[Dict]
Add ranking by skill match count
Return people with their projects

Day 10: Search Endpoint
GET /search?query={query} endpoint
Parse intent → execute appropriate Neo4j query
Return ranked results
Add CORS middleware for frontend
Test 20+ realistic queries
Milestone: Search working via API
Phase 3: Frontend Basics (Days 11-14)

Day 11: Vite Setup
npm create vite@latest frontend -- --template react-ts
Install dependencies
Test dev server runs
Create basic App.tsx with two-view navigation

Day 12: Upload View
Create components/upload/UploadView.tsx
File input (multiple, accept .pdf/.docx/.txt)
Upload button with loading state
Display stats after upload
Test uploading 3 documents

Day 13: Search View
Create components/search/QueryView.tsx
Search input with Enter key support
Search button with loading state
Results list showing: name, skills, projects
Test 10 different queries

Day 14: Polish UI
Add basic styling (can use inline styles or simple CSS)
Loading spinners
Error messages
Empty states ("No results found")
Milestone: Functional UI end-to-end