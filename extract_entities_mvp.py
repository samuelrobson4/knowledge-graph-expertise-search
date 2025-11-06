#!/usr/bin/env python3
"""
Knowledge Graph MVP - Entity Extraction Proof of Concept

This script extracts people, skills, projects, and relationships from a PDF document
using Claude API. This validates the core extraction approach before building the full system.

Usage:
    python extract_entities_mvp.py <pdf_file_path>

Example:
    python extract_entities_mvp.py status_report.pdf
"""

import sys
import json
import os
from pathlib import Path
import pymupdf  # PyMuPDF for PDF text extraction
from anthropic import Anthropic
from dotenv import load_dotenv
from validation import validate_entities


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text as a single string
    """

    print(f"📄 Extracting text from: {pdf_path}")

    doc = pymupdf.open(pdf_path)
    text_content = []

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text()
        text_content.append(text)
        print(f"   Page {page_num}: {len(text)} characters")

    doc.close()

    full_text = "\n\n".join(text_content)
    print(f"✓ Total extracted: {len(full_text)} characters\n")

    return full_text


def extract_entities_with_claude(text: str, api_key: str) -> dict:
    """
    Use Claude API to extract structured entities from text.

    Extracts:
    - People (with their soft skills, hard skills, projects)
    - Project details
    - Relationships between people

    Args:
        text: Document text to analyze
        api_key: Anthropic API key

    Returns:
        Dictionary containing extracted entities
    """
    print("🤖 Sending to Claude API for entity extraction...")

    client = Anthropic(api_key=api_key)

    prompt = f"""You are an expert at extracting structured information from team status documents and reports. Analyze the following document and extract:

1. **People**: Full names (REQUIRED)
2. **Hard Skills**: Technical skills (React, Python, AWS, SQL, Docker, etc.) (REQUIRED - at least one per person)
3. **Soft Skills**: Leadership, communication, mentoring, project management (DO NOT INCLUDE ANY TECHNICAL SKILLS i.e. REACT NATIVE, NODE.JS etc.!) (REQUIRED - at least one per person)
4. **Projects**: Names and descriptions (BOTH REQUIRED)
5. **Relationships**: Who worked on which projects with their role (ALL REQUIRED)

SKILL NORMALIZATION - Use these canonical terms for similar skills:

Hard Skills:
- React/React Native/React.js/ReactJS → "React"
- Node/Node.js/NodeJS → "Node.js"
- Python/Python3/py → "Python"
- JavaScript/JS/Javascript → "JavaScript"
- TypeScript/TS → "TypeScript"
- AWS/Amazon Web Services → "AWS"
- Docker/Docker Engine → "Docker"
- Kubernetes/K8s/k8s → "Kubernetes"
- PostgreSQL/Postgres/psql → "PostgreSQL"
- SQL/Structured Query Language → "SQL"
- GraphQL/GQL → "GraphQL"
- REST API/REST/RESTful API → "REST API"
- Git/Github/Gitlab → "Git"
- CI/CD/Continuous Integration → "CI/CD"

Soft Skills:
- Leadership/Leading/Lead → "leadership"
- Communication/Communicating → "communication"
- Problem solving/Problem-solving/Troubleshooting → "problem-solving"
- Project management/PM/Managing projects → "project management"
- Team collaboration/Collaboration/Teamwork → "collaboration"
- Mentoring/Mentorship/Coaching → "mentoring"
- Analytical/Analysis/Analytical thinking → "analytical skills"
- Strategic thinking/Strategy → "strategic thinking"

IMPORTANT: Use exact canonical terms from lists above. If encounter similar skill not listed, normalize to closest match.

Return JSON:
{{
  "people": [
    {{
      "name": "Full Name",  // REQUIRED: must not be empty
      "hard_skills": ["technical skill1", "tool1"],  // REQUIRED: at least one skill
      "soft_skills": ["leadership skill1", "soft skill1"]  // OPTIONAL
    }}
  ],
  "projects": [
    {{
      "name": "Project Name",  // REQUIRED: must not be empty
      "description": "Brief description",  // REQUIRED: must not be empty (1-2 sentences)
      "technologies": ["tech1", "tech2"]  // REQUIRED: at least one technology
    }}
  ],
  "relationships": [
    {{
      "person": "Full Name",  // REQUIRED: must match a person name above
      "project": "Project Name",  // REQUIRED: must match a project name above
      "role": "lead developer"  // REQUIRED: their role (1-3 words, e.g., "lead developer", "backend engineer")
    }}
  ]
}}

VALIDATION RULES:
- Every person MUST have a name and at least one hard skill
- Every project MUST have a name AND description (description cannot be empty)
- Every relationship MUST have person, project, AND role filled in
- Be specific with skills. Include all people who worked on each project.

Document to analyze:

{text}

Return ONLY the JSON object, no additional text or explanation."""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=4000,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the response text
    response_text = message.content[0].text

    print("✓ Received response from Claude\n")

    # Strip markdown code fences if present
    if response_text.startswith("```"):
        # Remove opening fence
        response_text = response_text.split("\n", 1)[1]
        # Remove closing fence
        if response_text.endswith("```"):
            response_text = response_text.rsplit("\n```", 1)[0]

    # Parse JSON response
    try:
        entities = json.loads(response_text)
        return entities
    except json.JSONDecodeError as e:
        print(f"⚠️  Warning: Response wasn't valid JSON. Raw response:")
        print(response_text)
        raise e


def print_extraction_summary(entities: dict):
    """
    Print a human-readable summary of extracted entities.

    Args:
        entities: Dictionary of extracted entities
    """
    print("=" * 70)
    print("EXTRACTION SUMMARY")
    print("=" * 70)

    people = entities.get("people", [])
    projects = entities.get("projects", [])

    print(f"\n📊 Found: {len(people)} people, {len(projects)} projects\n")

    print("👥 PEOPLE:")
    print("-" * 70)
    for person in people:
        print(f"\n  {person['name']}")

        if person.get('hard_skills'):
            print(f"    💻 Hard Skills: {', '.join(person['hard_skills'])}")

        if person.get('soft_skills'):
            print(f"    🗣️  Soft Skills: {', '.join(person['soft_skills'])}")

        if person.get('projects'):
            print(f"    📁 Projects:")
            for proj in person['projects']:
                role = f" ({proj['role']})" if proj.get('role') else ""
                print(f"       - {proj['project_name']}{role}")

        if person.get('collaborators'):
            print(f"    🤝 Worked with: {', '.join(person['collaborators'])}")

    if projects:
        print("\n\n🚀 PROJECTS:")
        print("-" * 70)
        for project in projects:
            print(f"\n  {project['name']}")
            if project.get('description'):
                print(f"    {project['description']}")
            if project.get('technologies'):
                print(f"    🔧 Technologies: {', '.join(project['technologies'])}")

    print("\n" + "=" * 70)


def main():
    """
    Main execution function.
    """
    # Load environment variables from .env file (override any existing ones)
    load_dotenv(override=True)

    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python extract_entities_mvp.py <pdf_file_path>")
        print("\nExample: python extract_entities_mvp.py status_report.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]

    # Validate PDF exists
    if not Path(pdf_path).exists():
        print(f"❌ Error: File not found: {pdf_path}")
        sys.exit(1)

    # Get API key from environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("❌ Error: ANTHROPIC_API_KEY not found")
        print("\nAdd your API key to .env file:")
        print("  ANTHROPIC_API_KEY=your-api-key-here")
        sys.exit(1)

    # Strip any whitespace that might have been added
    api_key = api_key.strip()

    print(f"🔑 API Key loaded: {api_key[:15]}... (length: {len(api_key)})")

    print("\n" + "=" * 70)
    print("KNOWLEDGE GRAPH MVP - ENTITY EXTRACTION")
    print("=" * 70 + "\n")

    # Step 1: Extract text from PDF
    text = extract_text_from_pdf(pdf_path)

    # Step 2: Extract entities using Claude
    entities = extract_entities_with_claude(text, api_key)

    # Step 2.5: Validate entities
    print("🔍 Validating extracted entities...")
    valid, errors = validate_entities(entities)
    if not valid:
        print("❌ Validation failed:\n")
        for error in errors:
            print(f"  - {error}")
        print("\n⚠️  Extraction did not meet required constraints. Check the document or refine the prompt.\n")
        sys.exit(1)
    print("✓ Validation passed\n")

    # Step 3: Save results to JSON file
    output_file = Path(pdf_path).stem + "_entities.json"
    with open(output_file, 'w') as f:
        json.dump(entities, f, indent=2)
    print(f"💾 Saved full results to: {output_file}\n")

    # Step 4: Print summary
    print_extraction_summary(entities)

    print(f"\n✅ Extraction complete! Check {output_file} for full JSON output.\n")


if __name__ == "__main__":
    main()
