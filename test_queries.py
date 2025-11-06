#!/usr/bin/env python3
"""
Test Neo4j queries for Knowledge Graph MVP.

Tests the 5 queries from Day 2 plan:
1. Who knows GraphQL?
2. Who worked with Sarah Chen?
3. Projects using Python?
4. Who knows React?
5. Projects using Kubernetes?
"""

from neo4j import GraphDatabase
from dotenv import load_dotenv
import os


def test_query_1(session):
    """Query: Who knows GraphQL?"""
    print("\n" + "=" * 70)
    print("QUERY 1: Who knows GraphQL?")
    print("=" * 70)

    result = session.run("""
        MATCH (p:Person)-[:HAS_SKILL]->(s:Skill {name: 'GraphQL'})
        RETURN p.name as person
        ORDER BY p.name
    """)

    people = [record["person"] for record in result]
    print(f"\nFound {len(people)} people:")
    for person in people:
        print(f"  • {person}")


def test_query_2(session):
    """Query: Who worked with Sarah Chen?"""
    print("\n" + "=" * 70)
    print("QUERY 2: Who worked with Sarah Chen?")
    print("=" * 70)

    result = session.run("""
        MATCH (sarah:Person {name: 'Sarah Chen'})-[:WORKS_ON]->(pr:Project)<-[:WORKS_ON]-(colleague:Person)
        WHERE colleague.name <> 'Sarah Chen'
        RETURN DISTINCT colleague.name as person,
               collect(DISTINCT pr.name) as shared_projects
        ORDER BY colleague.name
    """)

    print(f"\nCollaborators:")
    for record in result:
        projects = record["shared_projects"]
        print(f"\n  • {record['person']}")
        print(f"    Shared projects: {', '.join(projects[:3])}")
        if len(projects) > 3:
            print(f"    ... and {len(projects) - 3} more")


def test_query_3(session):
    """Query: Projects using Python?"""
    print("\n" + "=" * 70)
    print("QUERY 3: Projects using Python?")
    print("=" * 70)

    result = session.run("""
        MATCH (pr:Project)-[:USES_TECH]->(s:Skill {name: 'Python'})
        RETURN pr.name as project, pr.description as description
        ORDER BY pr.name
    """)

    projects = list(result)
    print(f"\nFound {len(projects)} projects:")
    for record in projects:
        print(f"\n  • {record['project']}")
        desc = record['description']
        print(f"    {desc[:100]}..." if len(desc) > 100 else f"    {desc}")


def test_query_4(session):
    """Query: Who knows React?"""
    print("\n" + "=" * 70)
    print("QUERY 4: Who knows React?")
    print("=" * 70)

    result = session.run("""
        MATCH (p:Person)-[:HAS_SKILL]->(s:Skill {name: 'React'})
        RETURN p.name as person
        ORDER BY p.name
    """)

    people = [record["person"] for record in result]
    print(f"\nFound {len(people)} people:")
    for person in people:
        print(f"  • {person}")


def test_query_5(session):
    """Query: Projects using Kubernetes?"""
    print("\n" + "=" * 70)
    print("QUERY 5: Projects using Kubernetes?")
    print("=" * 70)

    result = session.run("""
        MATCH (pr:Project)-[:USES_TECH]->(s:Skill {name: 'Kubernetes'})
        RETURN pr.name as project,
               [(pr)-[:USES_TECH]->(tech:Skill) | tech.name] as all_techs
        ORDER BY pr.name
    """)

    projects = list(result)
    print(f"\nFound {len(projects)} projects:")
    for record in projects:
        print(f"\n  • {record['project']}")
        techs = record['all_techs']
        print(f"    Technologies: {', '.join(techs[:5])}")
        if len(techs) > 5:
            print(f"    ... and {len(techs) - 5} more")


def main():
    """Run all test queries."""
    load_dotenv()

    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USER")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    print("=" * 70)
    print("KNOWLEDGE GRAPH MVP - QUERY TESTING")
    print("=" * 70)

    driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    try:
        with driver.session() as session:
            test_query_1(session)
            test_query_2(session)
            test_query_3(session)
            test_query_4(session)
            test_query_5(session)

        print("\n" + "=" * 70)
        print("✅ All queries completed successfully!")
        print("=" * 70 + "\n")

    finally:
        driver.close()


if __name__ == "__main__":
    main()
