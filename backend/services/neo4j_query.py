"""Neo4j query execution service."""
from typing import Dict, List, Any
from backend.services.neo4j_client import get_driver
from backend.services.query_intent_parser import parse_query_intent


async def execute_cypher_query(cypher_query: str, parameters: Dict = None) -> List[Dict]:
    """
    Execute a Cypher query and return formatted results.

    Args:
        cypher_query: The Cypher query to execute
        parameters: Optional query parameters

    Returns:
        List of result dictionaries

    Raises:
        Exception: If query execution fails
    """
    driver = get_driver()

    try:
        with driver.session() as session:
            result = session.run(cypher_query, parameters or {})

            # Convert Neo4j records to dictionaries
            records = []
            for record in result:
                records.append(dict(record))

            return records

    except Exception as e:
        raise Exception(f"Cypher query execution failed: {str(e)}\n\nQuery: {cypher_query}")


async def search_knowledge_graph(query: str) -> Dict:
    """
    Execute natural language search against the knowledge graph.

    Combines query intent parsing with Cypher execution to provide
    a complete search solution.

    Args:
        query: Natural language search query

    Returns:
        Dictionary containing:
        - intent: Detected query intent
        - results: List of matching results
        - result_count: Number of results
        - explanation: Human-readable description
        - cypher_query: The executed Cypher query (for debugging)

    Raises:
        Exception: If parsing or execution fails
    """
    # Parse the query intent and generate Cypher
    intent_data = await parse_query_intent(query)

    # Execute the generated Cypher query
    results = await execute_cypher_query(
        intent_data['cypher_query'],
        intent_data.get('parameters', {})
    )

    # Return formatted response
    return {
        'intent': intent_data['intent'],
        'results': results,
        'result_count': len(results),
        'explanation': intent_data['explanation'],
        'ranking_strategy': intent_data['ranking_strategy'],
        'cypher_query': intent_data['cypher_query']  # For debugging/transparency
    }


async def search_people_by_skill(skills: List[str], match_all: bool = False) -> List[Dict]:
    """
    Search for people with specific skills.

    Args:
        skills: List of skill names to search for
        match_all: If True, require all skills (AND). If False, require any skill (OR)

    Returns:
        List of people with their skills and match counts
    """
    driver = get_driver()

    with driver.session() as session:
        if match_all:
            # AND logic: person must have all skills
            cypher = """
                MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
                WHERE s.name IN $skills
                WITH p, count(DISTINCT s) as match_count
                WHERE match_count = $skill_count
                MATCH (p)-[:HAS_SKILL]->(all_s:Skill)
                RETURN p.name as name, collect(all_s.name) as all_skills, match_count
                ORDER BY name
            """
            result = session.run(cypher, skills=skills, skill_count=len(skills))
        else:
            # OR logic: person has any of the skills
            cypher = """
                MATCH (p:Person)-[:HAS_SKILL]->(s:Skill)
                WHERE s.name IN $skills
                WITH p, count(DISTINCT s) as match_count
                MATCH (p)-[:HAS_SKILL]->(all_s:Skill)
                RETURN p.name as name, collect(all_s.name) as all_skills, match_count
                ORDER BY match_count DESC, name
            """
            result = session.run(cypher, skills=skills)

        return [dict(record) for record in result]


async def search_projects_by_tech(technologies: List[str], match_all: bool = False) -> List[Dict]:
    """
    Search for projects using specific technologies.

    Args:
        technologies: List of technology/skill names
        match_all: If True, require all techs (AND). If False, require any tech (OR)

    Returns:
        List of projects with their technologies and match counts
    """
    driver = get_driver()

    with driver.session() as session:
        if match_all:
            # AND logic: project must use all technologies
            cypher = """
                MATCH (pr:Project)-[:USES_TECH]->(s:Skill)
                WHERE s.name IN $technologies
                WITH pr, collect(s.name) as techs, count(DISTINCT s) as match_count
                WHERE match_count = $tech_count
                RETURN pr.name as name, pr.description as description, techs, match_count
                ORDER BY name
            """
            result = session.run(cypher, technologies=technologies, tech_count=len(technologies))
        else:
            # OR logic: project uses any of the technologies
            cypher = """
                MATCH (pr:Project)-[:USES_TECH]->(s:Skill)
                WHERE s.name IN $technologies
                WITH pr, collect(s.name) as techs, count(DISTINCT s) as match_count
                RETURN pr.name as name, pr.description as description, techs, match_count
                ORDER BY match_count DESC, name
            """
            result = session.run(cypher, technologies=technologies)

        return [dict(record) for record in result]


async def find_collaborators(person_name: str) -> List[Dict]:
    """
    Find people who have worked with a specific person.

    Args:
        person_name: Name of the person to find collaborators for

    Returns:
        List of collaborators with shared projects and project count
    """
    driver = get_driver()

    with driver.session() as session:
        cypher = """
            MATCH (p1:Person {name: $person_name})-[:WORKS_ON]->(pr:Project)<-[:WORKS_ON]-(p2:Person)
            WHERE p1 <> p2
            RETURN DISTINCT p2.name as name,
                   collect(DISTINCT pr.name) as shared_projects,
                   count(DISTINCT pr) as project_count
            ORDER BY project_count DESC, name
        """
        result = session.run(cypher, person_name=person_name)

        return [dict(record) for record in result]


async def get_person_details(person_name: str) -> Dict:
    """
    Get detailed information about a specific person.

    Args:
        person_name: Name of the person

    Returns:
        Dictionary with person's skills, projects, and roles
    """
    driver = get_driver()

    with driver.session() as session:
        # Get skills
        skills_result = session.run("""
            MATCH (p:Person {name: $name})-[:HAS_SKILL]->(s:Skill)
            RETURN collect(s.name) as skills
        """, name=person_name)
        skills_record = skills_result.single()
        skills = skills_record['skills'] if skills_record else []

        # Get projects and roles
        projects_result = session.run("""
            MATCH (p:Person {name: $name})-[w:WORKS_ON]->(pr:Project)
            RETURN collect({
                project: pr.name,
                role: w.role,
                description: pr.description
            }) as projects
        """, name=person_name)
        projects_record = projects_result.single()
        projects = projects_record['projects'] if projects_record else []

        return {
            'name': person_name,
            'skills': skills,
            'projects': projects,
            'project_count': len(projects)
        }
