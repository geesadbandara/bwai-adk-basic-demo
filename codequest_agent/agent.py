from __future__ import annotations

from typing import Literal

import dotenv
from google.adk.agents import Agent

dotenv.load_dotenv()


QUESTS = [
    {
        "quest_id": "QUEST-OFFBYONE",
        "name": "The Off-By-One Forest",
        "difficulty": "novice",
        "guild": "Algorithms Guild",
        "required_level": 1,
        "xp_reward": 50,
        "boss": "The Fencepost Wolf",
        "description": (
            "A twisting forest where every loop seems to end one step too early "
            "or one step too late. Adventurers must tame the Fencepost Wolf by "
            "mastering loop boundaries."
        ),
        "skills_taught": ["for loops", "array indexing", "boundary conditions"],
    },
    {
        "quest_id": "QUEST-NULLSWAMP",
        "name": "Null Pointer Swamp",
        "difficulty": "novice",
        "guild": "Systems Guild",
        "required_level": 2,
        "xp_reward": 75,
        "boss": "The Segfault Serpent",
        "description": (
            "A murky swamp where careless adventurers vanish without a trace. "
            "Defeat the Segfault Serpent by learning to check references before "
            "you use them."
        ),
        "skills_taught": ["null checks", "defensive programming", "error handling"],
    },
    {
        "quest_id": "QUEST-RECURSION",
        "name": "The Recursion Labyrinth",
        "difficulty": "apprentice",
        "guild": "Algorithms Guild",
        "required_level": 5,
        "xp_reward": 150,
        "boss": "The Infinite Loop Hydra",
        "description": (
            "A labyrinth that folds in on itself endlessly. Only those who "
            "master base cases can stop the Infinite Loop Hydra from regrowing "
            "its heads."
        ),
        "skills_taught": ["recursion", "base cases", "call stacks"],
    },
    {
        "quest_id": "QUEST-BIGO",
        "name": "Big-O Mountain",
        "difficulty": "apprentice",
        "guild": "Performance Guild",
        "required_level": 6,
        "xp_reward": 175,
        "boss": "The Quadratic Time Giant",
        "description": (
            "A mountain that grows taller the more you climb it. Bring down the "
            "Quadratic Time Giant by choosing better algorithms and data "
            "structures."
        ),
        "skills_taught": ["time complexity", "algorithm analysis", "data structures"],
    },
    {
        "quest_id": "QUEST-MERGECONFLICT",
        "name": "The Merge Conflict Dragon's Lair",
        "difficulty": "master",
        "guild": "Version Control Guild",
        "required_level": 10,
        "xp_reward": 300,
        "boss": "The Merge Conflict Dragon",
        "description": (
            "A treasure-filled lair guarded by a dragon that breathes conflicting "
            "diffs. Only adventurers fluent in branching and rebasing survive "
            "its fire."
        ),
        "skills_taught": ["git branching", "merge conflicts", "code review"],
    },
    {
        "quest_id": "QUEST-DEADLOCK",
        "name": "Deadlock Dungeon",
        "difficulty": "master",
        "guild": "Systems Guild",
        "required_level": 12,
        "xp_reward": 350,
        "boss": "The Deadlock Twins",
        "description": (
            "Two locked doors, each waiting for the other to open first. Escape "
            "the dungeon by learning to order your locks and avoid circular "
            "waits."
        ),
        "skills_taught": ["concurrency", "locks", "deadlock avoidance"],
    },
]


def _find_quest(quest_id: str) -> dict | None:
    return next((q for q in QUESTS if q["quest_id"] == quest_id), None)


def list_quests(
    difficulty: Literal["novice", "apprentice", "master"] | None = None,
) -> dict:
    """List available quests at CodeQuest Academy, optionally filtered by difficulty.

    Args:
        difficulty: Optional quest difficulty to filter by.

    Returns:
        Matching quests and a count.
    """
    matches = []
    for quest in QUESTS:
        if difficulty and quest["difficulty"] != difficulty:
            continue
        matches.append(
            {
                "quest_id": quest["quest_id"],
                "name": quest["name"],
                "difficulty": quest["difficulty"],
                "guild": quest["guild"],
                "required_level": quest["required_level"],
                "xp_reward": quest["xp_reward"],
            }
        )
    return {"status": "success", "count": len(matches), "quests": matches}


def get_quest_details(quest_id: str) -> dict:
    """Get the full story, boss, and rewards for one quest.

    Args:
        quest_id: Quest identifier, for example QUEST-OFFBYONE.

    Returns:
        Quest details if found.
    """
    quest = _find_quest(quest_id)
    if not quest:
        return {"status": "error", "message": f"Unknown quest_id: {quest_id}"}

    return {"status": "success", "quest": quest.copy()}


def check_quest_readiness(quest_id: str, hero_level: int) -> dict:
    """Check whether a hero's level is high enough to attempt a quest.

    Args:
        quest_id: Quest identifier.
        hero_level: The adventurer's current level.

    Returns:
        Whether the hero is ready, and the level still needed if not.
    """
    quest = _find_quest(quest_id)
    if not quest:
        return {"status": "error", "message": f"Unknown quest_id: {quest_id}"}

    required_level = quest["required_level"]
    is_ready = hero_level >= required_level
    return {
        "status": "success",
        "quest_id": quest_id,
        "quest_name": quest["name"],
        "hero_level": hero_level,
        "required_level": required_level,
        "is_ready": is_ready,
        "levels_needed": max(0, required_level - hero_level),
    }


root_agent = Agent(
    name="codequest_agent",
    model="gemini-3.1-flash-lite",
    description="ARIA, the AI Guildmaster of CodeQuest Academy, assigns coding quests to new adventurers.",
    instruction="""
You are ARIA, the AI Guildmaster of CodeQuest Academy — a training ground where new
adventurers (students) defeat legendary programming bugs to grow from Novice into
Archmage of Code.

Speak with warmth and a light fantasy-guildmaster flavor (quests, guilds, bosses, XP),
but keep every fact about quests grounded in tool output. Do not invent quest details,
rewards, or bosses that the tools do not return.

Core responsibilities:
- Welcome new adventurers and ask their hero name and current level if you don't know them yet.
- Use list_quests to show available quests, optionally filtered by difficulty (novice, apprentice, master).
- Use get_quest_details to tell the full story, boss, skills taught, and XP reward for a specific quest.
- Use check_quest_readiness before confirming an adventurer can start a quest — never guess whether they're ready.
- If a hero is not ready, encourage them and tell them how many levels they still need.
- If a quest_id is not recognised, suggest calling list_quests to see valid options.
- When an adventurer seems unsure what to do next, recommend a novice quest first.

Stay in character as a guildmaster, but never sacrifice accuracy for flavor.
""",
    tools=[
        list_quests,
        get_quest_details,
        check_quest_readiness,
    ],
)
