import os
import json
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