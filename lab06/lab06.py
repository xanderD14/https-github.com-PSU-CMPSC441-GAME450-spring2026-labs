"""
Lab 06: Structured Output with Pydantic and Ollama

This lab demonstrates how to use Pydantic models with Ollama's `format`
parameter to get structured, validated JSON output from an LLM.
"""

from typing import List

import ollama
from pydantic import BaseModel, Field


MODEL = "llama3.2:latest"


# ============================================================================
# Pydantic Models (provided -- do not modify)
# ============================================================================

class AbilityScores(BaseModel):
    strength: int = Field(..., ge=1, le=20, description="Strength score")
    dexterity: int = Field(..., ge=1, le=20, description="Dexterity score")
    constitution: int = Field(..., ge=1, le=20, description="Constitution score")
    intelligence: int = Field(..., ge=1, le=20, description="Intelligence score")
    wisdom: int = Field(..., ge=1, le=20, description="Wisdom score")
    charisma: int = Field(..., ge=1, le=20, description="Charisma score")


class CharacterSheet(BaseModel):
    name: str = Field(..., min_length=1, description="Character name")
    race: str = Field(..., min_length=1, description="Character race, e.g. Elf, Dwarf, Human")
    char_class: str = Field(..., min_length=1, description="Character class, e.g. Wizard, Fighter, Rogue")
    level: int = Field(..., ge=1, le=20, description="Character level")
    ability_scores: AbilityScores
    hit_points: int = Field(..., ge=1, description="Maximum hit points")
    backstory: str = Field(..., min_length=1, description="Brief character backstory")


class MonsterStats(BaseModel):
    name: str = Field(..., min_length=1, description="Monster name")
    monster_type: str = Field(..., min_length=1, description="Monster type, e.g. Undead, Beast, Dragon")
    challenge_rating: float = Field(..., ge=0, le=30, description="Challenge rating")
    hit_points: int = Field(..., ge=1, description="Hit points")
    armor_class: int = Field(..., ge=1, le=30, description="Armor class")
    abilities: List[str] = Field(..., min_length=1, description="List of special abilities")
    description: str = Field(..., min_length=1, description="Physical description of the monster")


class Encounter(BaseModel):
    title: str = Field(..., min_length=1, description="Encounter title")
    setting: str = Field(..., min_length=1, description="Description of where the encounter takes place")
    monsters: List[MonsterStats] = Field(..., min_length=1, description="Monsters in this encounter")
    difficulty: str = Field(..., description="Encounter difficulty: Easy, Medium, Hard, or Deadly")
    treasure: List[str] = Field(default_factory=list, description="Possible treasure rewards")
    narrative_hook: str = Field(..., min_length=1, description="Story hook that leads into this encounter")


# ============================================================================
# Functions to implement
# ============================================================================

def generate_character(description: str) -> CharacterSheet:
    """
    Generate a D&D character sheet from a natural language description.
    """
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a D&D 5e character creator. Given a character description, "
                    "generate a complete and creative character sheet with appropriate stats, "
                    "a fitting name, race, class, level, ability scores (all between 1-20), "
                    "hit points, and a brief backstory. Ensure all numeric values are within "
                    "their valid ranges."
                ),
            },
            {
                "role": "user",
                "content": f"Create a D&D character sheet for: {description}",
            },
        ],
        format=CharacterSheet.model_json_schema(),
    )
    return CharacterSheet.model_validate_json(response.message.content)


def generate_monster(concept: str) -> MonsterStats:
    """
    Generate D&D monster stats from a concept description.
    """
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a D&D 5e monster designer. Given a monster concept, generate "
                    "complete and balanced monster stats including a creative name, monster type, "
                    "an appropriate challenge rating (0-30), hit points, armor class (1-30), "
                    "a list of at least 2 special abilities, and a vivid physical description."
                ),
            },
            {
                "role": "user",
                "content": f"Create D&D monster stats for: {concept}",
            },
        ],
        format=MonsterStats.model_json_schema(),
    )
    return MonsterStats.model_validate_json(response.message.content)


def generate_encounter(party_level: int, num_monsters: int, theme: str) -> Encounter:
    """
    Generate a complete D&D encounter with nested structured output.
    """
    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a D&D 5e encounter designer. Generate complete, balanced encounters "
                    "with vivid settings, compelling narrative hooks, and fully detailed monster "
                    "stat blocks. Difficulty must be exactly one of: Easy, Medium, Hard, or Deadly. "
                    "Each monster must have a name, type, challenge rating, hit points, armor class, "
                    "at least one special ability, and a physical description."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Create a D&D encounter with the following parameters:\n"
                    f"- Party level: {party_level}\n"
                    f"- Number of monsters: {num_monsters}\n"
                    f"- Theme: {theme}\n"
                    f"Generate exactly {num_monsters} monster(s) appropriate for a level {party_level} party."
                ),
            },
        ],
        format=Encounter.model_json_schema(),
    )
    return Encounter.model_validate_json(response.message.content)


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    print("=== Generating Character ===")
    character = generate_character("A brave halfling rogue who grew up on the streets")
    print(character.model_dump_json(indent=2))

    print("\n=== Generating Monster ===")
    monster = generate_monster("A shadow wolf that phases through walls")
    print(monster.model_dump_json(indent=2))

    print("\n=== Generating Encounter ===")
    encounter = generate_encounter(party_level=3, num_monsters=2, theme="haunted forest")
    print(encounter.model_dump_json(indent=2))