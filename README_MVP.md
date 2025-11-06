# Knowledge Graph MVP - Entity Extraction

Quick proof-of-concept script to validate entity extraction from team status documents.

## What It Does

Takes a PDF document and extracts:
- **People** with their names
- **Hard Skills** (technical: React, Python, AWS, etc.)
- **Soft Skills** (leadership, communication, etc.)
- **Projects** they worked on (with roles)
- **Collaborators** (who worked with whom)

Outputs structured JSON that can later be loaded into a Neo4j graph database.

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your Anthropic API key:**
   ```bash
   export ANTHROPIC_API_KEY='your-api-key-here'
   ```

   Get an API key at: https://console.anthropic.com/

## Usage

Place a PDF file in this directory (or anywhere) and run:

```bash
python extract_entities_mvp.py your_status_document.pdf
```

### Example

```bash
python extract_entities_mvp.py team_status_q4.pdf
```

## Output

The script will:
1. Extract text from the PDF
2. Send it to Claude API for entity extraction
3. Save results to `{filename}_entities.json`
4. Print a formatted summary to the console

### Example Output

```
======================================================================
EXTRACTION SUMMARY
======================================================================

📊 Found: 3 people, 2 projects

👥 PEOPLE:
----------------------------------------------------------------------

  Sarah Chen
    💻 Hard Skills: React, TypeScript, Node.js
    🗣️  Soft Skills: Team leadership, Mentoring
    📁 Projects:
       - Customer Dashboard (Lead Developer)
    🤝 Worked with: John Smith, Maria Garcia

  John Smith
    💻 Hard Skills: Python, FastAPI, PostgreSQL
    🗣️  Soft Skills: Problem solving
    📁 Projects:
       - API Migration (Backend Engineer)
    🤝 Worked with: Sarah Chen
```

## Next Steps

Once you've validated extraction quality:
1. Set up Neo4j database
2. Create FastAPI backend to load entities into Neo4j
3. Build React frontend for querying
4. Test with real users

## Troubleshooting

**"ANTHROPIC_API_KEY not set"**
- Make sure you've exported the environment variable in your current shell session

**"File not found"**
- Check the PDF path is correct
- Use absolute path if relative path doesn't work: `/full/path/to/file.pdf`

**Poor extraction quality**
- Try PDFs with clearer formatting
- Ensure text is not just scanned images (needs actual text content)
- Check that document has sufficient context about people and projects
