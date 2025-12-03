"""Entity extraction service using Claude API."""
from anthropic import Anthropic
import json
from typing import Dict
from backend.config import settings
from backend.services.skill_normalizer import normalize_entities


async def extract_entities_with_claude(text: str) -> Dict:
    """
    Use Claude API to extract structured entities from text.

    Extracts:
    - People (with their soft skills, hard skills)
    - Project details
    - Relationships between people and projects

    Args:
        text: Document text to analyze

    Returns:
        Dictionary containing extracted entities

    Raises:
        Exception: If API call fails or JSON parsing fails
    """
    client = Anthropic(api_key=settings.anthropic_api_key)

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
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse Claude response as JSON: {str(e)}\n\nResponse: {response_text}")

    # Normalize skills
    entities = await normalize_entities(entities)

    return entities
