"""Query intent parsing service using Claude API."""
from anthropic import Anthropic
import json
from typing import Dict, List
from backend.config import settings


# Skill expansion mapping - when searching for a skill, also search for related variations
SKILL_EXPANSIONS = {
    'React': ['React', 'React Native'],
    'Node': ['Node.js'],
    'Python': ['Python', 'scikit-learn'],  # Python ML libraries
    'JavaScript': ['JavaScript', 'TypeScript'],
    'AWS': ['AWS', 'Terraform'],
}


def expand_skills(skills: List[str]) -> List[str]:
    """
    Expand skill list to include related variations.

    Args:
        skills: List of skill names from query

    Returns:
        Expanded list including variations
    """
    expanded = set()
    for skill in skills:
        # Add the original skill
        expanded.add(skill)
        # Add any expansions if they exist
        if skill in SKILL_EXPANSIONS:
            expanded.update(SKILL_EXPANSIONS[skill])

    return list(expanded)


async def parse_query_intent(query: str) -> Dict:
    """
    Parse user query and generate executable Neo4j Cypher query.

    Uses Claude API to:
    - Detect query intent
    - Normalize skill names
    - Generate appropriate Cypher query
    - Determine ranking strategy

    Args:
        query: User search query string

    Returns:
        Dictionary containing:
        - intent: Query type classification
        - cypher_query: Executable Cypher query
        - parameters: Query parameters (for parameterized queries)
        - ranking_strategy: How to rank results
        - explanation: Human-readable description

    Raises:
        Exception: If API call fails or JSON parsing fails
    """
    client = Anthropic(api_key=settings.anthropic_api_key)

    prompt = f"""You are an expert at converting natural language queries into Neo4j Cypher queries. Analyze the user's query and generate an executable Cypher query based on the graph schema.

GRAPH SCHEMA:

Nodes:
- Person {{name: string}}
- Skill {{name: string}}  // both hard & soft skills
- Project {{name: string, description: string}}

Relationships:
- (Person)-[:HAS_SKILL]->(Skill)
- (Person)-[:WORKS_ON {{role: string}}]->(Project)
- (Project)-[:USES_TECH]->(Skill)

SKILL NORMALIZATION (use these exact canonical terms):
Hard Skills: React, Node.js, Python, JavaScript, TypeScript, AWS, Docker, Kubernetes, PostgreSQL, SQL, GraphQL, REST API, Git, CI/CD
Soft Skills: leadership, communication, problem-solving, project management, collaboration, mentoring, analytical skills, strategic thinking

SKILL EXPANSION RULES (important for matching variations):
When searching for a skill, also search for related variations:
- "React" → search for both "React" AND "React Native"
- "Node" or "Node.js" → search for "Node.js"
- "Python" → search for "Python" and related libraries like "scikit-learn"
- "JavaScript" → search for both "JavaScript" AND "TypeScript"
- "AWS" → search for "AWS" and related tools like "Terraform"

INTENT TYPES:
1. skill_search - Find people with specific skills
2. project_search - Find projects using specific technologies
3. collaborator_search - Find people who worked with someone
4. person_details - Get details about a specific person
5. role_search - Find people by their role

MULTI-SKILL LOGIC:
- Query contains "and"/"both"/"all" → AND logic (all skills required)
- Query contains "or"/"either"/"any" → OR logic (any skill matches)
- Default for multiple skills → OR logic

RANKING STRATEGIES:
- skill_search → "match_count" (sort by number of matching skills)
- project_search → "match_count" (sort by number of matching technologies)
- collaborator_search → "shared_projects" (sort by number of shared projects)
- person_details → "none"
- role_search → "none"

EXAMPLE QUERIES:

1. "Find people with React"
   Intent: skill_search
   Cypher: MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) WHERE s.name IN ['React', 'React Native'] WITH DISTINCT p MATCH (p)-[:HAS_SKILL]->(all_s:Skill) RETURN p.name as name, collect(all_s.name) as all_skills ORDER BY name

2. "Who worked with Sarah Chen?"
   Intent: collaborator_search
   Cypher: MATCH (p1:Person {{name: 'Sarah Chen'}})-[:WORKS_ON]->(pr:Project)<-[:WORKS_ON]-(p2:Person) WHERE p1 <> p2 RETURN DISTINCT p2.name as name, collect(DISTINCT pr.name) as shared_projects, count(DISTINCT pr) as project_count ORDER BY project_count DESC

3. "Projects using Python and Docker"
   Intent: project_search (AND logic)
   Cypher: MATCH (pr:Project)-[:USES_TECH]->(s:Skill) WHERE s.name IN ['Python', 'Docker'] WITH pr, collect(s.name) as techs, count(DISTINCT s) as match_count WHERE match_count = 2 RETURN pr.name as name, pr.description as description, techs ORDER BY match_count DESC

4. "People with React or Python"
   Intent: skill_search (OR logic)
   Cypher: MATCH (p:Person)-[:HAS_SKILL]->(s:Skill) WHERE s.name IN ['React', 'Python'] WITH p, count(DISTINCT s) as match_count MATCH (p)-[:HAS_SKILL]->(all_s:Skill) RETURN p.name as name, collect(all_s.name) as all_skills, match_count ORDER BY match_count DESC, name

5. "Backend engineers"
   Intent: role_search
   Cypher: MATCH (p:Person)-[w:WORKS_ON]->(pr:Project) WHERE toLower(w.role) CONTAINS 'backend' RETURN DISTINCT p.name as name, collect(DISTINCT w.role) as roles, collect(DISTINCT pr.name) as projects ORDER BY name

6. "What did Alice work on?"
   Intent: person_details
   Cypher: MATCH (p:Person {{name: 'Alice'}})-[w:WORKS_ON]->(pr:Project) RETURN p.name as name, collect({{project: pr.name, role: w.role, description: pr.description}}) as projects

IMPORTANT RULES:
1. Always use DISTINCT to avoid duplicates
2. Normalize skill names to canonical terms
3. Apply SKILL EXPANSION when searching - if user asks for "React", search for both "React" AND "React Native" using IN clause
4. Use case-insensitive matching for roles (toLower)
5. For AND logic, use WHERE match_count = <number_of_skills>
6. For OR logic, use IN clause with skill list
7. Always include ORDER BY for consistent results
8. Return structured data with clear field names (name, skills, projects, etc.)
9. Use collect() to aggregate relationships
10. For skill_search: Return ALL skills for matched people (use WITH clause to separate filtering from collection), not just matching skills

User Query: {query}

Return ONLY a JSON object with this structure:
{{
  "intent": "skill_search|project_search|collaborator_search|person_details|role_search",
  "cypher_query": "MATCH ... RETURN ...",
  "parameters": {{}},  // Can be empty if query has no parameters
  "ranking_strategy": "match_count|shared_projects|none",
  "explanation": "Brief description of what this query does"
}}

Return ONLY the JSON object, no additional text or explanation."""

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1000,
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
        query_intent = json.loads(response_text)
        return query_intent
    except json.JSONDecodeError as e:
        raise Exception(f"Failed to parse Claude response as JSON: {str(e)}\n\nResponse: {response_text}")
