import os
import json
import random
from litellm import completion
from dotenv import load_dotenv
import utils.prompts as prompts

# Load environment variables securely from .env
load_dotenv()

def generate_narrative_flavor(outcome_summary: str, system_prompt: str) -> str:
    """Generates 2-3 sentences of atmospheric narrative flavor text based on calculated game outcomes.

    Args:
        outcome_summary (str): The deterministic math outcome calculated by Python.
        system_prompt (str): The role-defining system prompt for the AI narrative engine.

    Returns:
        str: Atmospheric narrative text or a fallback error message if the API call fails.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Warning: GROQ_API_KEY is missing from your environment variables."

    try:
        response = completion(
            model="groq/llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompts.NARRATIVE_SYSTEM_PROMPT},
                {"role": "user", "content": f"The outcome of the action is: {outcome_summary}. Describe this briefly."}
            ],
            api_key=api_key,
            temperature=0.7,
            max_tokens=150
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        # Fallback error handling to prevent application crashes
        return f"Narrative engine temporarily offline. (Error: {e})"

def generate_procedural_encounter(environment_name: str) -> dict:
    """Generates a procedural survival encounter based on the player's active environment.

    Args:
        environment_name (str): The active survival environment theme.

    Returns:
        dict: A structured dictionary containing encounter title, description, stat_type, and difficulty_threshold.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {
            "title": "Quiet Exploration",
            "description": "You scout the immediate vicinity for resources without incident.",
            "stat_type": "scavenge",
            "difficulty_threshold": 3
        }

    try:
        response = completion(
            model="groq/llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompts.ENCOUNTER_GENERATOR_PROMPT},
                {"role": "user", "content": f"The current environment is: {environment_name}."}
            ],
            api_key=api_key,
            temperature=0.7,
            max_tokens=200
        )
        content = response["choices"][0]["message"]["content"].strip()
        return json.loads(content)
    except Exception:
        # Fallback default encounter to prevent crashes on API errors
        return {
            "title": "Quiet Exploration",
            "description": "You scout the immediate vicinity for resources without incident.",
            "stat_type": "scavenge",
            "difficulty_threshold": 3
        }

def parse_custom_action_intent(user_input: str) -> dict:
    """Parses free-form player input into a structured JSON action intent.

    Args:
        user_input (str): The player's free-form custom action text.

    Returns:
        dict: A structured dictionary containing action_type, target_resource, and estimated_risk.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"action_type": "unknown", "target_resource": "none", "estimated_risk": "low"}

    try:
        response = completion(
            model="groq/llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompts.INTENT_PARSER_PROMPT},
                {"role": "user", "content": user_input}
            ],
            api_key=api_key,
            temperature=0.3,
            max_tokens=100
        )
        content = response["choices"][0]["message"]["content"].strip()
        return json.loads(content)
    except Exception:
        # Fallback dictionary to prevent application crashes on parse errors
        return {"action_type": "unknown", "target_resource": "none", "estimated_risk": "low"}

def resolve_dynamic_exploration(survivor_name: str, survivor_trait: str, area_data: dict) -> dict:
    """Generates a dynamic exploration outcome based on JSON area data and survivor personality."""
    api_key = os.getenv("GROQ_API_KEY")
    fallback = {"narrative": f"I found nothing.", "resources_gained": {}, "hp_change": 0}
    
    if not api_key: return fallback

    context = f"Survivor: {survivor_name}\nPersonality Trait: {survivor_trait}\nArea Data: {json.dumps(area_data)}"

    try:
        response = completion(
            model="groq/llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompts.DYNAMIC_EXPLORATION_PROMPT},
                {"role": "user", "content": context}
            ],
            api_key=api_key,
            temperature=0.7,
            max_tokens=150
        )
        content = response["choices"][0]["message"]["content"].strip()
        return json.loads(content)
    except Exception as e:
        print(f"Exploration Error: {e}")
        return fallback

def generate_daily_event(day: int, scenario_data: dict) -> dict:
    """Generates a random morning event based on the scenario JSON and a weighted tone."""
    api_key = os.getenv("GROQ_API_KEY")
    fallback = {"event_title": "A Quiet Morning", "narrative": "Nothing unusual happens today.", "camp_resource_change": {}}
    
    if not api_key: return fallback

    # 1. Safely extract the events dictionary from the scenario data
    scenario_events = scenario_data.get("events", {
        "Positive": ["A good day"],
        "Negative": ["A bad day"],
        "Neutral": ["A normal day"]
    })

    # 2. Pick the overarching tone
    selected_tone = random.choices(
        population=["Positive", "Negative", "Neutral"],
        weights=[35, 30, 35],
        k=1
    )[0]

    # 3. Pick the EXACT theme from the JSON arrays
    specific_theme = random.choice(scenario_events[selected_tone])

    # 4. Inject the scenario name, description, and specific theme into the context
    context = f"Day: {day}. Scenario Theme: {scenario_data.get('name', 'Island')} ({scenario_data.get('description', '')}). Today's Forced Tone: {selected_tone}. Specific Topic: {specific_theme}."

    try:
        response = completion(
            model="groq/llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompts.RANDOM_EVENT_PROMPT},
                {"role": "user", "content": context}
            ],
            api_key=api_key,
            temperature=0.8,
            max_tokens=200
        )
        content = response["choices"][0]["message"]["content"].strip()
        return json.loads(content)
    except Exception as e:
        print(f"Event Error: {e}")
        return fallback