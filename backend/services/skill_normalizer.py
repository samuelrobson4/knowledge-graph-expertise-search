"""Skill normalization service using hybrid matching."""
import json
import os
from difflib import SequenceMatcher
from typing import Dict, List, Tuple
from anthropic import Anthropic
from backend.config import settings


REGISTRY_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'skill_registry.json')


def load_registry() -> Dict:
    """Load skill registry from JSON file."""
    if not os.path.exists(REGISTRY_PATH):
        return {}

    with open(REGISTRY_PATH, 'r') as f:
        return json.load(f)


def save_registry(registry: Dict) -> None:
    """Save skill registry to JSON file."""
    with open(REGISTRY_PATH, 'w') as f:
        json.dump(registry, f, indent=2)


def exact_match(raw_skill: str, registry: Dict) -> str | None:
    """Check for exact match (case-insensitive) in canonical skills or synonyms."""
    raw_lower = raw_skill.lower().strip()

    # Check canonical skills
    for canonical in registry.keys():
        if raw_lower == canonical.lower():
            return canonical

    # Check synonyms
    for canonical, data in registry.items():
        for synonym in data.get("synonyms", []):
            if raw_lower == synonym.lower():
                return canonical

    return None


def fuzzy_match(raw_skill: str, registry: Dict) -> Tuple[str | None, float]:
    """Find best fuzzy match using string similarity."""
    raw_lower = raw_skill.lower().strip()
    best_match = None
    best_score = 0.0

    # Check canonical skills
    for canonical in registry.keys():
        score = SequenceMatcher(None, raw_lower, canonical.lower()).ratio()
        if score > best_score:
            best_score = score
            best_match = canonical

    # Check synonyms
    for canonical, data in registry.items():
        for synonym in data.get("synonyms", []):
            score = SequenceMatcher(None, raw_lower, synonym.lower()).ratio()
            if score > best_score:
                best_score = score
                best_match = canonical

    return best_match, best_score


async def llm_batch_match(uncertain_skills: List[str], registry: Dict) -> Dict[str, str]:
    """Use Claude to match uncertain skills to canonical skills."""
    if not uncertain_skills:
        return {}

    canonical_list = list(registry.keys())

    prompt = f"""Given these raw skills from a document:
{json.dumps(uncertain_skills, indent=2)}

Match each to the closest canonical skill from this registry:
{json.dumps(canonical_list, indent=2)}

Rules:
- If exact match exists, return it
- If close semantic match (synonym/variant), return canonical name
- If no good match, return "NEW_SKILL"

Return ONLY a JSON object mapping raw skill → canonical skill or "NEW_SKILL":
{{
  "raw_skill_1": "Canonical Skill",
  "raw_skill_2": "NEW_SKILL",
  ...
}}

No explanation, just JSON."""

    client = Anthropic(api_key=settings.anthropic_api_key)

    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text.strip()

    # Strip markdown if present
    if response_text.startswith("```"):
        response_text = response_text.split("\n", 1)[1]
        if response_text.endswith("```"):
            response_text = response_text.rsplit("\n```", 1)[0]

    try:
        matches = json.loads(response_text)
        return matches
    except json.JSONDecodeError:
        # If LLM fails, treat all as new skills
        return {skill: "NEW_SKILL" for skill in uncertain_skills}


async def normalize_skills(raw_skills: List[str], category: str) -> List[str]:
    """
    Normalize a list of skills using hybrid matching.

    Args:
        raw_skills: List of raw skill names from extraction
        category: "hard" or "soft" skill category

    Returns:
        List of canonical skill names
    """
    registry = load_registry()
    normalized = []
    uncertain_skills = []
    uncertain_indices = []

    for i, raw_skill in enumerate(raw_skills):
        # Step 1: Exact match
        match = exact_match(raw_skill, registry)
        if match:
            normalized.append(match)
            continue

        # Step 2: Fuzzy match
        fuzzy, score = fuzzy_match(raw_skill, registry)

        if score > 0.85:  # High confidence
            normalized.append(fuzzy)
        elif score > 0.6:  # Uncertain, needs LLM
            normalized.append(None)  # Placeholder
            uncertain_skills.append(raw_skill)
            uncertain_indices.append(i)
        else:  # New skill
            # Add to registry
            registry[raw_skill] = {
                "category": category,
                "synonyms": []
            }
            save_registry(registry)
            normalized.append(raw_skill)

    # Step 3: LLM batch matching for uncertain skills
    if uncertain_skills:
        llm_matches = await llm_batch_match(uncertain_skills, registry)

        for idx, raw_skill in zip(uncertain_indices, uncertain_skills):
            match = llm_matches.get(raw_skill, "NEW_SKILL")

            if match == "NEW_SKILL":
                # Add to registry
                registry[raw_skill] = {
                    "category": category,
                    "synonyms": []
                }
                save_registry(registry)
                normalized[idx] = raw_skill
            else:
                normalized[idx] = match

    return normalized


async def normalize_entities(entities: Dict) -> Dict:
    """
    Normalize all skills in extracted entities.

    Args:
        entities: Dictionary with people, projects, relationships

    Returns:
        Dictionary with normalized skill names
    """
    # Normalize hard skills for all people
    for person in entities.get("people", []):
        if "hard_skills" in person:
            person["hard_skills"] = await normalize_skills(person["hard_skills"], "hard")

        if "soft_skills" in person:
            person["soft_skills"] = await normalize_skills(person["soft_skills"], "soft")

    # Normalize technologies for all projects
    for project in entities.get("projects", []):
        if "technologies" in project:
            project["technologies"] = await normalize_skills(project["technologies"], "hard")

    return entities
