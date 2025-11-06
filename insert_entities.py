#!/usr/bin/env python3
"""
Insert extracted entities from JSON into Neo4j graph database.

Usage:
    python insert_entities.py <entities_json_file>

Example:
    python insert_entities.py testreport_entities.json
"""

import sys
import json
from pathlib import Path
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os
from validation import validate_entities


def insert_entities_to_neo4j(entities: dict, driver):
    """
    Insert validated entities into Neo4j using MERGE to prevent duplicates.

    Args:
        entities: Dictionary containing people, projects, and relationships
        driver: Neo4j driver instance
    """

    with driver.session() as session:
        # Insert People
        print("\n📝 Inserting people...")
        for person in entities["people"]:
            session.run("""
                MERGE (p:Person {name: $name})
            """, name=person["name"])
            print(f"  ✓ {person['name']}")

        # Insert Skills and HAS_SKILL relationships
        print("\n💻 Inserting skills...")
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

        print(f"  ✓ {skill_count} skills linked")

        # Insert Projects
        print("\n🚀 Inserting projects...")
        for project in entities["projects"]:
            session.run("""
                MERGE (pr:Project {name: $name})
                SET pr.description = $description
            """, name=project["name"], description=project["description"])
            print(f"  ✓ {project['name']}")

        # Insert USES_TECH relationships
        print("\n🔧 Linking projects to technologies...")
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

        print(f"  ✓ {tech_count} technologies linked")

        # Insert WORKS_ON relationships
        print("\n🤝 Inserting work relationships...")
        for rel in entities["relationships"]:
            session.run("""
                MATCH (p:Person {name: $person})
                MATCH (pr:Project {name: $project})
                MERGE (p)-[r:WORKS_ON]->(pr)
                SET r.role = $role
            """, person=rel["person"], project=rel["project"], role=rel["role"])

        print(f"  ✓ {len(entities['relationships'])} relationships created")


def get_graph_stats(driver):
    """Get counts of nodes and relationships in the graph."""
    with driver.session() as session:
        people_count = session.run("MATCH (p:Person) RETURN count(p) as count").single()["count"]
        skills_count = session.run("MATCH (s:Skill) RETURN count(s) as count").single()["count"]
        projects_count = session.run("MATCH (pr:Project) RETURN count(pr) as count").single()["count"]
        has_skill_count = session.run("MATCH ()-[r:HAS_SKILL]->() RETURN count(r) as count").single()["count"]
        uses_tech_count = session.run("MATCH ()-[r:USES_TECH]->() RETURN count(r) as count").single()["count"]
        works_on_count = session.run("MATCH ()-[r:WORKS_ON]->() RETURN count(r) as count").single()["count"]

        return {
            "people": people_count,
            "skills": skills_count,
            "projects": projects_count,
            "has_skill": has_skill_count,
            "uses_tech": uses_tech_count,
            "works_on": works_on_count
        }


def main():
    """Main execution function."""
    load_dotenv()

    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python insert_entities.py <entities_json_file>")
        print("\nExample: python insert_entities.py testreport_entities.json")
        sys.exit(1)

    json_path = sys.argv[1]

    # Validate file exists
    if not Path(json_path).exists():
        print(f"❌ Error: File not found: {json_path}")
        sys.exit(1)

    print("=" * 70)
    print("KNOWLEDGE GRAPH MVP - NEO4J DATA INSERTION")
    print("=" * 70)

    # Load entities from JSON
    print(f"\n📂 Loading entities from: {json_path}")
    with open(json_path, 'r') as f:
        entities = json.load(f)

    # Validate entities
    print("🔍 Validating entities...")
    valid, errors = validate_entities(entities)
    if not valid:
        print("❌ Validation failed:\n")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    print("✓ Validation passed")

    # Connect to Neo4j
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USER")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    if not all([neo4j_uri, neo4j_user, neo4j_password]):
        print("❌ Error: Neo4j credentials not found in .env")
        sys.exit(1)

    print(f"\n🔌 Connecting to Neo4j at {neo4j_uri}...")
    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    try:
        # Test connection
        with driver.session() as session:
            session.run("RETURN 1")
        print("✓ Connected to Neo4j")

        # Insert entities
        insert_entities_to_neo4j(entities, driver)

        # Get and display stats
        print("\n" + "=" * 70)
        print("GRAPH STATISTICS")
        print("=" * 70)
        stats = get_graph_stats(driver)
        print(f"\n📊 Nodes:")
        print(f"  • People: {stats['people']}")
        print(f"  • Skills: {stats['skills']}")
        print(f"  • Projects: {stats['projects']}")
        print(f"\n🔗 Relationships:")
        print(f"  • HAS_SKILL: {stats['has_skill']}")
        print(f"  • USES_TECH: {stats['uses_tech']}")
        print(f"  • WORKS_ON: {stats['works_on']}")

        print("\n✅ Data insertion complete!")
        print(f"\n💡 Next: Test queries in Neo4j Browser at http://localhost:7474")
        print("=" * 70 + "\n")

    finally:
        driver.close()


if __name__ == "__main__":
    main()
