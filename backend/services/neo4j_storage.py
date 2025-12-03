"""Neo4j entity storage service."""
from typing import Dict, Tuple
from backend.services.neo4j_client import get_driver


async def store_entities_in_neo4j(entities: Dict) -> Dict:
    """
    Store validated entities in Neo4j graph database.

    Uses MERGE to prevent duplicates.

    Args:
        entities: Dictionary containing people, projects, and relationships

    Returns:
        Dictionary with insertion statistics
    """
    driver = get_driver()

    with driver.session() as session:
        # Insert People
        for person in entities["people"]:
            session.run("""
                MERGE (p:Person {name: $name})
            """, name=person["name"])

        # Insert Skills and HAS_SKILL relationships
        skill_count = 0
        for person in entities["people"]:
            for skill in person["hard_skills"]:
                session.run("""
                    MERGE (s:Skill {name: $skill})
                    WITH s
                    MATCH (p:Person {name: $person})
                    MERGE (p)-[:HAS_SKILL]->(s)
                """, skill=skill, person=person["name"])
                skill_count += 1

            for skill in person.get("soft_skills", []):
                session.run("""
                    MERGE (s:Skill {name: $skill})
                    WITH s
                    MATCH (p:Person {name: $person})
                    MERGE (p)-[:HAS_SKILL]->(s)
                """, skill=skill, person=person["name"])
                skill_count += 1

        # Insert Projects
        for project in entities["projects"]:
            session.run("""
                MERGE (pr:Project {name: $name})
                SET pr.description = $description
            """, name=project["name"], description=project["description"])

        # Insert USES_TECH relationships
        tech_count = 0
        for project in entities["projects"]:
            for tech in project["technologies"]:
                session.run("""
                    MERGE (s:Skill {name: $tech})
                    WITH s
                    MATCH (pr:Project {name: $project})
                    MERGE (pr)-[:USES_TECH]->(s)
                """, tech=tech, project=project["name"])
                tech_count += 1

        # Insert WORKS_ON relationships
        for rel in entities["relationships"]:
            session.run("""
                MATCH (p:Person {name: $person})
                MATCH (pr:Project {name: $project})
                MERGE (p)-[r:WORKS_ON]->(pr)
                SET r.role = $role
            """, person=rel["person"], project=rel["project"], role=rel["role"])

    return {
        "people_inserted": len(entities["people"]),
        "projects_inserted": len(entities["projects"]),
        "skills_linked": skill_count,
        "technologies_linked": tech_count,
        "relationships_created": len(entities["relationships"])
    }


async def get_graph_data(limit: int = 500) -> Dict:
    """
    Get graph data for visualization.

    Args:
        limit: Maximum number of relationships to return

    Returns:
        Dictionary with nodes and links for graph visualization
    """
    driver = get_driver()

    with driver.session() as session:
        # Query all nodes and relationships
        result = session.run("""
            MATCH (n)-[r]->(m)
            RETURN n, r, m
            LIMIT $limit
        """, limit=limit)

        nodes_dict = {}
        links = []

        for record in result:
            source_node = record["n"]
            target_node = record["m"]
            relationship = record["r"]

            # Extract source node
            source_labels = list(source_node.labels)
            source_type = source_labels[0] if source_labels else "Unknown"
            source_id = f"{source_type}:{source_node['name']}"

            if source_id not in nodes_dict:
                nodes_dict[source_id] = {
                    "id": source_id,
                    "label": source_node["name"],
                    "type": source_type,
                    "properties": dict(source_node)
                }

            # Extract target node
            target_labels = list(target_node.labels)
            target_type = target_labels[0] if target_labels else "Unknown"
            target_id = f"{target_type}:{target_node['name']}"

            if target_id not in nodes_dict:
                nodes_dict[target_id] = {
                    "id": target_id,
                    "label": target_node["name"],
                    "type": target_type,
                    "properties": dict(target_node)
                }

            # Extract relationship
            rel_type = relationship.type
            links.append({
                "source": source_id,
                "target": target_id,
                "type": rel_type,
                "label": rel_type.lower().replace("_", " ")
            })

        nodes = list(nodes_dict.values())

        return {
            "nodes": nodes,
            "links": links,
            "stats": {
                "node_count": len(nodes),
                "link_count": len(links),
                "truncated": len(links) >= limit
            }
        }


async def get_graph_stats() -> Dict:
    """
    Get statistics about the knowledge graph.

    Returns:
        Dictionary with node and relationship counts
    """
    driver = get_driver()

    with driver.session() as session:
        people_count = session.run("MATCH (p:Person) RETURN count(p) as count").single()["count"]
        skills_count = session.run("MATCH (s:Skill) RETURN count(s) as count").single()["count"]
        projects_count = session.run("MATCH (pr:Project) RETURN count(pr) as count").single()["count"]
        has_skill_count = session.run("MATCH ()-[r:HAS_SKILL]->() RETURN count(r) as count").single()["count"]
        uses_tech_count = session.run("MATCH ()-[r:USES_TECH]->() RETURN count(r) as count").single()["count"]
        works_on_count = session.run("MATCH ()-[r:WORKS_ON]->() RETURN count(r) as count").single()["count"]

        return {
            "nodes": {
                "people": people_count,
                "skills": skills_count,
                "projects": projects_count,
                "total": people_count + skills_count + projects_count
            },
            "relationships": {
                "has_skill": has_skill_count,
                "uses_tech": uses_tech_count,
                "works_on": works_on_count,
                "total": has_skill_count + uses_tech_count + works_on_count
            }
        }
