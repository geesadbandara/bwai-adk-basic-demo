from __future__ import annotations

import os
from typing import Literal
from uuid import uuid4

import dotenv
from google import genai
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.genai import types

dotenv.load_dotenv()


IMAGE_MODEL = os.getenv("TEA_IMAGE_MODEL", "gemini-3.1-flash-image")


TEA_STAGES = [
    {
        "stage_id": "STAGE-NURSERY",
        "name": "Nursery & Propagation",
        "phase": "establishment",
        "min_age_months": 0,
        "max_age_months": 6,
        "description": (
            "Cuttings are rooted in nursery beds under partial shade before they "
            "are strong enough for the open field. This stage sets up the plant's "
            "entire future health and yield potential."
        ),
        "key_activities": [
            "rooting single-node cuttings in polybags",
            "maintaining partial shade and humidity",
            "regular but moderate watering",
        ],
        "common_issues": ["damping-off fungus", "root rot from overwatering", "sun scorch"],
        "care_recommendations": [
            "Keep cuttings under 60-80% shade and even moisture, never waterlogged.",
            "Watch for damping-off and treat promptly with a suitable fungicide drench.",
            "Begin hardening off (gradually increasing sun exposure) before transplanting.",
        ],
    },
    {
        "stage_id": "STAGE-TRANSPLANT",
        "name": "Transplanting & Field Establishment",
        "phase": "establishment",
        "min_age_months": 6,
        "max_age_months": 18,
        "description": (
            "Young plants move from the nursery into the field. Roots are still "
            "shallow and vulnerable, so establishment care determines how evenly "
            "the field will grow."
        ),
        "key_activities": [
            "field planting, ideally at the start of the rainy season",
            "mulching around the base to retain moisture",
            "weeding and light shade-tree management",
        ],
        "common_issues": ["transplant shock", "weed competition", "drought stress"],
        "care_recommendations": [
            "Plant during reliable rains and mulch immediately to conserve moisture.",
            "Weed regularly by hand near the stem to avoid root damage.",
            "Provide temporary shade for the first few months if sun exposure is intense.",
        ],
    },
    {
        "stage_id": "STAGE-FORMATIVE",
        "name": "Formative Pruning & Framework Building",
        "phase": "vegetative",
        "min_age_months": 18,
        "max_age_months": 36,
        "description": (
            "The bush is trained into a low, spreading frame that will later become "
            "the plucking table. Formative pruning now shapes yield for decades."
        ),
        "key_activities": [
            "centering and tipping young stems",
            "formative pruning to encourage lateral branching",
            "building an even, low plucking table",
        ],
        "common_issues": ["uneven canopy", "weak framework from incorrect cutting height"],
        "care_recommendations": [
            "Center at the recommended height and tip laterals to spread growth outward.",
            "Avoid plucking hard during this stage; let the frame fill in first.",
            "Correct any single dominant stem early to prevent a weak, top-heavy bush.",
        ],
    },
    {
        "stage_id": "STAGE-EARLY-PLUCK",
        "name": "Early / Light Plucking",
        "phase": "production",
        "min_age_months": 36,
        "max_age_months": 48,
        "description": (
            "The bush can now support its first harvests. Plucking is light and "
            "careful, continuing to build the plucking table while producing a "
            "modest first yield."
        ),
        "key_activities": [
            "light plucking of two leaves and a bud",
            "continued shaping of the plucking table",
            "closer pest monitoring as canopy density increases",
        ],
        "common_issues": ["over-plucking damaging young growth", "tea mosquito bug", "red spider mite"],
        "care_recommendations": [
            "Pluck lightly and consistently rather than heavily and infrequently.",
            "Scout weekly for tea mosquito bug and red spider mite; treat at first sign.",
            "Maintain plucking table height rather than letting the bush grow tall.",
        ],
    },
    {
        "stage_id": "STAGE-MATURE",
        "name": "Mature Plucking Cycle",
        "phase": "production",
        "min_age_months": 48,
        "max_age_months": None,
        "description": (
            "The bush is in full production, harvested on a regular plucking round "
            "for years. This is the stage where consistent agronomy pays off most "
            "directly in yield and leaf quality."
        ),
        "key_activities": [
            "regular plucking rounds, typically every 7-14 days",
            "scheduled fertilization based on soil and leaf tests",
            "ongoing pest and disease monitoring",
        ],
        "common_issues": ["blister blight", "tea mosquito bug", "shot-hole borer", "nutrient depletion"],
        "care_recommendations": [
            "Keep plucking rounds on schedule; skipped rounds coarsen leaf and hurt quality.",
            "Follow a balanced fertilization program rather than a single blanket application.",
            "Use integrated pest management and rotate controls to manage blister blight and mosquito bug.",
        ],
    },
    {
        "stage_id": "STAGE-MAINTENANCE-PRUNE",
        "name": "Maintenance & Rejuvenation Pruning",
        "phase": "maintenance",
        "min_age_months": None,
        "max_age_months": None,
        "description": (
            "Recurring within the mature plucking cycle (roughly every 3-5 years) or "
            "triggered by declining yield, excessive bush height, or old age. Pruning "
            "resets the bush so the plucking cycle can continue productively."
        ),
        "key_activities": [
            "light, medium, or hard skiffing depending on bush condition",
            "deeper rejuvenation pruning for bushes with declining yield",
            "collar pruning or replanting consideration for very old bushes",
        ],
        "common_issues": ["yield decline", "woody unproductive growth", "pest buildup in dense canopy"],
        "care_recommendations": [
            "Prune during the recommended dormant or cooler period for the region.",
            "Match prune severity to bush condition: light skiff for minor upkeep, hard prune for reset.",
            "For very old, unresponsive bushes, weigh rejuvenation pruning against replanting.",
        ],
    },
]


def _find_stage(stage_id: str) -> dict | None:
    return next((s for s in TEA_STAGES if s["stage_id"] == stage_id), None)


def list_stages(
    phase: Literal["establishment", "vegetative", "production", "maintenance"] | None = None,
) -> dict:
    """List tea plant growth stages, optionally filtered by phase.

    Args:
        phase: Optional growth phase to filter by.

    Returns:
        Matching stages and a count.
    """
    matches = []
    for stage in TEA_STAGES:
        if phase and stage["phase"] != phase:
            continue
        matches.append(
            {
                "stage_id": stage["stage_id"],
                "name": stage["name"],
                "phase": stage["phase"],
                "min_age_months": stage["min_age_months"],
                "max_age_months": stage["max_age_months"],
            }
        )
    return {"status": "success", "count": len(matches), "stages": matches}


def get_stage_details(stage_id: str) -> dict:
    """Get the full description, activities, issues, and care recommendations for one stage.

    Args:
        stage_id: Stage identifier, for example STAGE-NURSERY.

    Returns:
        Stage details if found.
    """
    stage = _find_stage(stage_id)
    if not stage:
        return {"status": "error", "message": f"Unknown stage_id: {stage_id}"}

    return {"status": "success", "stage": stage.copy()}


def recommend_stage_for_age(plant_age_months: int) -> dict:
    """Determine a tea plant's current growth stage from its age and recommend care.

    Args:
        plant_age_months: Age of the plant or field in months since planting
            (or since the last major pruning, for mature bushes being re-assessed).

    Returns:
        The matched stage and its care recommendations, plus months remaining
        until the next stage transition if applicable.
    """
    if plant_age_months < 0:
        return {"status": "error", "message": "plant_age_months must be zero or positive."}

    dated_stages = [s for s in TEA_STAGES if s["min_age_months"] is not None]
    dated_stages.sort(key=lambda s: s["min_age_months"])

    matched = None
    next_stage = None
    for index, stage in enumerate(dated_stages):
        min_age = stage["min_age_months"]
        max_age = stage["max_age_months"]
        if plant_age_months >= min_age and (max_age is None or plant_age_months < max_age):
            matched = stage
            if index + 1 < len(dated_stages):
                next_stage = dated_stages[index + 1]
            break

    if matched is None:
        matched = dated_stages[-1]

    months_until_next = None
    if next_stage is not None:
        months_until_next = max(0, next_stage["min_age_months"] - plant_age_months)

    return {
        "status": "success",
        "plant_age_months": plant_age_months,
        "stage_id": matched["stage_id"],
        "stage_name": matched["name"],
        "phase": matched["phase"],
        "key_activities": matched["key_activities"],
        "common_issues": matched["common_issues"],
        "care_recommendations": matched["care_recommendations"],
        "next_stage_id": next_stage["stage_id"] if next_stage else None,
        "months_until_next_stage": months_until_next,
    }


async def create_plantation_image(
    description: str,
    tool_context: ToolContext,
    aspect_ratio: Literal["1:1", "4:3", "3:4", "16:9", "9:16"] = "16:9",
) -> dict:
    """Create an illustrated tea plantation scene and save it as an ADK artifact.

    Use this only when the user explicitly asks for an image. The description
    should identify the setting, growth stage or activity, and mood to show.

    Args:
        description: A detailed description of the image the user wants.
        aspect_ratio: Output shape; 16:9 is best for scenes and 1:1 for badges.

    Returns:
        The generated artifact filename and version, or a safe error message.
    """
    clean_description = description.strip()
    if not clean_description:
        return {
            "status": "error",
            "message": "Describe the tea plantation scene you want illustrated.",
        }

    prompt = (
        "Create a polished, realistic illustration of a tea plantation for an "
        "agricultural advisory app. The visual should feel warm, natural, and "
        "grounded in real tea estate life. Do not add logos, watermarks, "
        "captions, or UI elements. Scene request: "
        f"{clean_description}"
    )

    async_client = None
    try:
        client = genai.Client()
        async_client = client.aio
        response = await async_client.models.generate_content(
            model=IMAGE_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                    image_size="1K",
                ),
            ),
        )

        image_data = None
        image_mime_type = "image/png"
        for part in response.parts or []:
            if part.inline_data and part.inline_data.data:
                image_data = part.inline_data.data
                image_mime_type = part.inline_data.mime_type or image_mime_type
                break

        if image_data is None:
            return {
                "status": "error",
                "message": (
                    "The image model did not return an image. Try a different "
                    "description or check the model's safety response."
                ),
            }

        extension = "jpg" if image_mime_type == "image/jpeg" else "png"
        filename = f"tea-plantation-{uuid4().hex[:10]}.{extension}"
        version = await tool_context.save_artifact(
            filename,
            types.Part.from_bytes(data=image_data, mime_type=image_mime_type),
            custom_metadata={
                "generator": IMAGE_MODEL,
                "aspect_ratio": aspect_ratio,
            },
        )
        return {
            "status": "success",
            "artifact_filename": filename,
            "artifact_version": version,
            "mime_type": image_mime_type,
            "aspect_ratio": aspect_ratio,
        }
    except Exception:
        return {
            "status": "error",
            "message": (
                "Image generation failed. Check your Google credentials, image "
                "model access, API quota, and ADK artifact service."
            ),
        }
    finally:
        if async_client is not None:
            try:
                await async_client.aclose()
            except Exception:
                pass


root_agent = Agent(
    name="tea_plantation_agent",
    model="gemini-3.1-flash-lite",
    description="Leaf is a friendly tea plantation advisor who identifies growth stages and recommends care.",
    instruction="""
You are Leaf, a warm, practical, and knowledgeable tea plantation advisor. You help
smallholders and estate workers understand what stage their tea plants are in and
what care they need right now, from nursery cuttings through mature plucking and
maintenance pruning.

Speak like an experienced, encouraging agronomist: clear, down-to-earth, and never
condescending. Keep every fact about stages, activities, issues, and recommendations
grounded in tool output. Do not invent agronomic facts, timelines, pest names, or
treatments that the tools do not return.

Core responsibilities:
- Welcome the user and ask for the age of their tea plants or field (in months since
  planting, or since the last major pruning) if you don't know it yet.
- Use recommend_stage_for_age to determine the current growth stage from that age and
  ground every stage claim and care recommendation in its output — never guess the stage.
- Use list_stages to show the stage catalogue, optionally filtered by phase
  (establishment, vegetative, production, maintenance).
- Use get_stage_details to give the full description, activities, issues, and care
  recommendations for a specific stage.
- If a stage_id is not recognised, suggest calling list_stages to see valid options.
- Mention months_until_next_stage when it is returned, so the user knows what is coming next.
- When a user explicitly asks for an image, use create_plantation_image. Include the
  setting, growth stage or activity, and mood in its description.
- If the image is based on a specific stage, call get_stage_details first so the
  visual stays grounded in that stage's returned activities and description.
- Never claim that an image was created unless create_plantation_image returns success.
  On success, tell the user the artifact filename. On error, relay its guidance.

Stay in character as Leaf, but never sacrifice accuracy for warmth.
""",
    tools=[
        list_stages,
        get_stage_details,
        recommend_stage_for_age,
        create_plantation_image,
    ],
)
