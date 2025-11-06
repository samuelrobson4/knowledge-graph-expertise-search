from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI"),
    auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
)

constraints = [
    # Uniqueness constraints (Community Edition compatible)
    "CREATE CONSTRAINT person_name_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.name IS UNIQUE",
    "CREATE CONSTRAINT skill_name_unique IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE",
    "CREATE CONSTRAINT project_name_unique IF NOT EXISTS FOR (pr:Project) REQUIRE pr.name IS UNIQUE"
]

# Note: Property existence (NOT NULL) and relationship constraints require Enterprise Edition
# For MVP, we'll handle validation at application level:
#   - Person.name, Skill.name, Project.name, Project.description must not be null
#   - WORKS_ON.role must not be null
#   - No duplicate HAS_SKILL or USES_TECH relationships

with driver.session() as session:
    for constraint in constraints:
        session.run(constraint)
        print(f"Created: {constraint.split()[2]}")

# Verify constraints
with driver.session() as session:
    result = session.run("SHOW CONSTRAINTS")
    print("\nActive constraints:")
    for record in result:
        print(f"  - {record['name']}")

driver.close()
