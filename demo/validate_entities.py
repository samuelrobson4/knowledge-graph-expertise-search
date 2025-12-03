#!/usr/bin/env python3
"""
Entity Extraction Validation Test Program

Validates extracted entities from testreport.pdf against validation rules
and outputs results as a human-readable text file.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


class EntityValidator:
    """Validates extracted entities against defined rules."""

    def __init__(self, entities: Dict):
        self.entities = entities
        self.errors = []
        self.warnings = []
        self.stats = {
            'people_count': 0,
            'projects_count': 0,
            'relationships_count': 0,
            'total_hard_skills': 0,
            'total_soft_skills': 0,
        }

    def validate_all(self) -> Tuple[bool, List[str], List[str]]:
        """Run all validations and return results."""
        self.validate_people()
        self.validate_projects()
        self.validate_relationships()
        self.collect_statistics()

        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings

    def validate_people(self):
        """Validate people entities."""
        people = self.entities.get('people', [])

        if not people:
            self.errors.append("CRITICAL: No people found in extracted entities")
            return

        person_names = set()

        for idx, person in enumerate(people, 1):
            # Check name exists and is not empty
            name = person.get('name', '').strip()
            if not name:
                self.errors.append(f"Person #{idx}: Missing or empty name")
            else:
                if name in person_names:
                    self.errors.append(f"Person #{idx}: Duplicate name '{name}'")
                person_names.add(name)

            # Check hard skills (REQUIRED - at least one)
            hard_skills = person.get('hard_skills', [])
            if not hard_skills:
                self.errors.append(f"Person '{name}': Missing hard skills (at least one required)")
            elif not isinstance(hard_skills, list):
                self.errors.append(f"Person '{name}': hard_skills must be a list")
            else:
                # Check for empty strings
                empty_skills = [s for s in hard_skills if not s.strip()]
                if empty_skills:
                    self.errors.append(f"Person '{name}': Contains empty hard skills")

            # Check soft skills (OPTIONAL but should be list if present)
            soft_skills = person.get('soft_skills', [])
            if soft_skills and not isinstance(soft_skills, list):
                self.errors.append(f"Person '{name}': soft_skills must be a list")

            # Warn if no soft skills
            if not soft_skills:
                self.warnings.append(f"Person '{name}': No soft skills listed")

            # Check for technical skills in soft_skills (common error)
            technical_indicators = ['js', 'react', 'node', 'python', 'sql', 'aws', 'docker',
                                   'api', 'database', 'server', 'cloud', 'framework']
            for skill in soft_skills:
                skill_lower = skill.lower()
                if any(tech in skill_lower for tech in technical_indicators):
                    self.errors.append(f"Person '{name}': Technical skill '{skill}' found in soft_skills")

    def validate_projects(self):
        """Validate project entities."""
        projects = self.entities.get('projects', [])

        if not projects:
            self.errors.append("CRITICAL: No projects found in extracted entities")
            return

        project_names = set()

        for idx, project in enumerate(projects, 1):
            # Check name exists and is not empty
            name = project.get('name', '').strip()
            if not name:
                self.errors.append(f"Project #{idx}: Missing or empty name")
            else:
                if name in project_names:
                    self.errors.append(f"Project #{idx}: Duplicate name '{name}'")
                project_names.add(name)

            # Check description (REQUIRED)
            description = project.get('description', '').strip()
            if not description:
                self.errors.append(f"Project '{name}': Missing or empty description (required)")
            elif len(description) < 10:
                self.warnings.append(f"Project '{name}': Description is very short ({len(description)} chars)")

            # Check technologies (REQUIRED - at least one)
            technologies = project.get('technologies', [])
            if not technologies:
                self.errors.append(f"Project '{name}': Missing technologies (at least one required)")
            elif not isinstance(technologies, list):
                self.errors.append(f"Project '{name}': technologies must be a list")
            else:
                # Check for empty strings
                empty_techs = [t for t in technologies if not t.strip()]
                if empty_techs:
                    self.errors.append(f"Project '{name}': Contains empty technology entries")

    def validate_relationships(self):
        """Validate relationships between people and projects."""
        relationships = self.entities.get('relationships', [])

        if not relationships:
            self.errors.append("CRITICAL: No relationships found")
            return

        # Get valid person and project names
        person_names = {p.get('name', '') for p in self.entities.get('people', [])}
        project_names = {p.get('name', '') for p in self.entities.get('projects', [])}

        for idx, rel in enumerate(relationships, 1):
            # Check person field
            person = rel.get('person', '').strip()
            if not person:
                self.errors.append(f"Relationship #{idx}: Missing person name")
            elif person not in person_names:
                self.errors.append(f"Relationship #{idx}: Person '{person}' not found in people list")

            # Check project field
            project = rel.get('project', '').strip()
            if not project:
                self.errors.append(f"Relationship #{idx}: Missing project name")
            elif project not in project_names:
                self.errors.append(f"Relationship #{idx}: Project '{project}' not found in projects list")

            # Check role field
            role = rel.get('role', '').strip()
            if not role:
                self.errors.append(f"Relationship #{idx}: Missing role (person: {person}, project: {project})")
            elif len(role.split()) > 5:
                self.warnings.append(f"Relationship #{idx}: Role '{role}' is very long (should be 1-3 words)")

    def collect_statistics(self):
        """Collect statistics about the entities."""
        self.stats['people_count'] = len(self.entities.get('people', []))
        self.stats['projects_count'] = len(self.entities.get('projects', []))
        self.stats['relationships_count'] = len(self.entities.get('relationships', []))

        # Count skills
        for person in self.entities.get('people', []):
            self.stats['total_hard_skills'] += len(person.get('hard_skills', []))
            self.stats['total_soft_skills'] += len(person.get('soft_skills', []))


def format_validation_report(entities: Dict, is_valid: bool, errors: List[str],
                            warnings: List[str], stats: Dict) -> str:
    """Format validation results as a readable text report."""

    lines = []
    lines.append("=" * 80)
    lines.append("ENTITY EXTRACTION VALIDATION REPORT")
    lines.append("=" * 80)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Source: tests/02_knowledge_graph_data/testreport_entities.json")
    lines.append("")

    # Overall Status
    lines.append("-" * 80)
    lines.append("VALIDATION STATUS")
    lines.append("-" * 80)
    status = "✓ PASSED" if is_valid else "✗ FAILED"
    lines.append(f"Overall: {status}")
    lines.append(f"Errors: {len(errors)}")
    lines.append(f"Warnings: {len(warnings)}")
    lines.append("")

    # Statistics
    lines.append("-" * 80)
    lines.append("EXTRACTION STATISTICS")
    lines.append("-" * 80)
    lines.append(f"People: {stats['people_count']}")
    lines.append(f"Projects: {stats['projects_count']}")
    lines.append(f"Relationships: {stats['relationships_count']}")
    lines.append(f"Total Hard Skills: {stats['total_hard_skills']}")
    lines.append(f"Total Soft Skills: {stats['total_soft_skills']}")
    if stats['people_count'] > 0:
        avg_hard = stats['total_hard_skills'] / stats['people_count']
        avg_soft = stats['total_soft_skills'] / stats['people_count']
        lines.append(f"Avg Hard Skills per Person: {avg_hard:.1f}")
        lines.append(f"Avg Soft Skills per Person: {avg_soft:.1f}")
    lines.append("")

    # Errors
    if errors:
        lines.append("-" * 80)
        lines.append("VALIDATION ERRORS")
        lines.append("-" * 80)
        for error in errors:
            lines.append(f"✗ {error}")
        lines.append("")

    # Warnings
    if warnings:
        lines.append("-" * 80)
        lines.append("WARNINGS")
        lines.append("-" * 80)
        for warning in warnings:
            lines.append(f"⚠ {warning}")
        lines.append("")

    # Detailed Entity Breakdown
    lines.append("-" * 80)
    lines.append("EXTRACTED ENTITIES DETAIL")
    lines.append("-" * 80)
    lines.append("")

    # People
    lines.append("PEOPLE:")
    lines.append("")
    for person in entities.get('people', []):
        name = person.get('name', 'UNNAMED')
        lines.append(f"  • {name}")
        lines.append(f"    Hard Skills: {', '.join(person.get('hard_skills', []))}")
        lines.append(f"    Soft Skills: {', '.join(person.get('soft_skills', []))}")
        lines.append("")

    # Projects
    lines.append("PROJECTS:")
    lines.append("")
    for project in entities.get('projects', []):
        name = project.get('name', 'UNNAMED')
        desc = project.get('description', 'NO DESCRIPTION')
        techs = ', '.join(project.get('technologies', []))
        lines.append(f"  • {name}")
        lines.append(f"    Description: {desc}")
        lines.append(f"    Technologies: {techs}")
        lines.append("")

    # Relationships
    lines.append("RELATIONSHIPS:")
    lines.append("")
    # Group by person
    from collections import defaultdict
    by_person = defaultdict(list)
    for rel in entities.get('relationships', []):
        person = rel.get('person', 'UNKNOWN')
        by_person[person].append(rel)

    for person, rels in sorted(by_person.items()):
        lines.append(f"  • {person}")
        for rel in rels:
            project = rel.get('project', 'UNKNOWN')
            role = rel.get('role', 'UNKNOWN')
            lines.append(f"    - {project} ({role})")
        lines.append("")

    lines.append("=" * 80)
    lines.append("END OF REPORT")
    lines.append("=" * 80)

    return "\n".join(lines)


def main():
    """Main execution function."""
    # Paths
    project_root = Path(__file__).parent.parent
    entities_file = project_root / "tests" / "02_knowledge_graph_data" / "testreport_entities.json"
    output_file = project_root / "tests" / "03_test_queries" / "validation_report.txt"

    print("=" * 80)
    print("Entity Extraction Validation Test")
    print("=" * 80)
    print()

    # Load entities
    print(f"Loading entities from: {entities_file}")
    try:
        with open(entities_file, 'r', encoding='utf-8') as f:
            entities = json.load(f)
        print(f"✓ Loaded entities successfully")
    except FileNotFoundError:
        print(f"✗ Error: File not found: {entities_file}")
        return
    except json.JSONDecodeError as e:
        print(f"✗ Error: Invalid JSON: {e}")
        return

    print()

    # Validate
    print("Running validation checks...")
    validator = EntityValidator(entities)
    is_valid, errors, warnings = validator.validate_all()

    print(f"✓ Validation complete")
    print(f"  - Errors: {len(errors)}")
    print(f"  - Warnings: {len(warnings)}")
    print()

    # Generate report
    print("Generating validation report...")
    report = format_validation_report(entities, is_valid, errors, warnings, validator.stats)

    # Write to file
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(f"✓ Report saved to: {output_file}")
    print()

    # Print summary
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    status = "PASSED ✓" if is_valid else "FAILED ✗"
    print(f"Validation Status: {status}")
    print(f"People: {validator.stats['people_count']}")
    print(f"Projects: {validator.stats['projects_count']}")
    print(f"Relationships: {validator.stats['relationships_count']}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")
    print("=" * 80)

    # Print first few errors if any
    if errors:
        print()
        print("First 5 errors:")
        for error in errors[:5]:
            print(f"  ✗ {error}")
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more (see full report)")


if __name__ == "__main__":
    main()
