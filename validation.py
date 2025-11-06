"""
Validation module for Knowledge Graph entities.

Enforces constraints that Neo4j Community Edition cannot enforce at DB level:
- NOT NULL constraints on properties
- Required relationship properties
- Duplicate relationship prevention (via MERGE in insertion code)
"""

from typing import Dict, List, Tuple


def validate_entities(entities: Dict) -> Tuple[bool, List[str]]:
    """
    Validate extracted entities meet all required constraints.

    Args:
        entities: Dictionary containing people, projects, and relationships

    Returns:
        Tuple of (is_valid: bool, errors: List[str])
    """
    errors = []

    # Extract entity lists
    people = entities.get("people", [])
    projects = entities.get("projects", [])
    relationships = entities.get("relationships", [])

    # Validate People
    for idx, person in enumerate(people):
        person_id = f"people[{idx}]"

        # Person.name NOT NULL
        if not person.get("name", "").strip():
            errors.append(f"{person_id}: Person missing required 'name'")

        # Person must have at least one hard skill
        hard_skills = person.get("hard_skills", [])
        if not hard_skills or not any(s.strip() for s in hard_skills):
            errors.append(f"{person_id} '{person.get('name')}': Missing required 'hard_skills'")

    # Validate Projects
    for idx, project in enumerate(projects):
        project_id = f"projects[{idx}]"

        # Project.name NOT NULL
        if not project.get("name", "").strip():
            errors.append(f"{project_id}: Project missing required 'name'")

        # Project.description NOT NULL
        if not project.get("description", "").strip():
            errors.append(f"{project_id} '{project.get('name')}': Missing required 'description'")

        # Project must have at least one technology
        technologies = project.get("technologies", [])
        if not technologies or not any(t.strip() for t in technologies):
            errors.append(f"{project_id} '{project.get('name')}': Missing required 'technologies'")

    # Validate Relationships
    person_names = {p.get("name", "").strip() for p in people if p.get("name", "").strip()}
    project_names = {p.get("name", "").strip() for p in projects if p.get("name", "").strip()}

    for idx, rel in enumerate(relationships):
        rel_id = f"relationships[{idx}]"

        person = rel.get("person", "").strip()
        project = rel.get("project", "").strip()
        role = rel.get("role", "").strip()

        # WORKS_ON.role NOT NULL
        if not role:
            errors.append(f"{rel_id}: Relationship missing required 'role'")

        # Validate person exists
        if not person:
            errors.append(f"{rel_id}: Relationship missing 'person'")
        elif person not in person_names:
            errors.append(f"{rel_id}: Person '{person}' not found in people list")

        # Validate project exists
        if not project:
            errors.append(f"{rel_id}: Relationship missing 'project'")
        elif project not in project_names:
            errors.append(f"{rel_id}: Project '{project}' not found in projects list")

    return (len(errors) == 0, errors)


def validate_person(name: str, hard_skills: List[str]) -> Tuple[bool, List[str]]:
    """Validate a single person."""
    errors = []

    if not name or not name.strip():
        errors.append("Person name cannot be empty")

    if not hard_skills or not any(s.strip() for s in hard_skills):
        errors.append(f"Person '{name}' must have at least one hard skill")

    return (len(errors) == 0, errors)


def validate_project(name: str, description: str, technologies: List[str]) -> Tuple[bool, List[str]]:
    """Validate a single project."""
    errors = []

    if not name or not name.strip():
        errors.append("Project name cannot be empty")

    if not description or not description.strip():
        errors.append(f"Project '{name}' description cannot be empty")

    if not technologies or not any(t.strip() for t in technologies):
        errors.append(f"Project '{name}' must have at least one technology")

    return (len(errors) == 0, errors)


def validate_relationship(person: str, project: str, role: str) -> Tuple[bool, List[str]]:
    """Validate a single relationship."""
    errors = []

    if not person or not person.strip():
        errors.append("Relationship person cannot be empty")

    if not project or not project.strip():
        errors.append("Relationship project cannot be empty")

    if not role or not role.strip():
        errors.append("Relationship role cannot be empty")

    return (len(errors) == 0, errors)
