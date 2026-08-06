import os
import json
import random
from litellm import completion
from dotenv import load_dotenv
import utils.prompts as prompts

# Load environment variables securely from .env
load_dotenv()

def parse_custom_action_intent(user_input: str) -> dict:
    """Parses free-form player input into a structured JSON action intent.

    Args:
        user_input (str): The player's free-form custom action text.

    Returns:
        dict: A structured dictionary containing action_type, target_resource, and estimated_risk.
    """
    if not os.getenv("GROQ_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        return {"action_type": "unknown", "target_resource": "none", "estimated_risk": "low"}

    try:
        response = completion(
            model="groq/llama-3.3-70b-versatile",
            fallbacks=[
                "groq/llama-3.1-8b-instant", 
                "gemini/gemini-1.5-flash"
            ],
            messages=[
                {"role": "system", "content": prompts.INTENT_PARSER_PROMPT},
                {"role": "user", "content": user_input}
            ],
            temperature=0.3,
            max_tokens=100
        )
        content = response["choices"][0]["message"]["content"].strip()
        return json.loads(content)
    except Exception:
        # Fallback dictionary to prevent application crashes on parse errors
        return {"action_type": "unknown", "target_resource": "none", "estimated_risk": "low"}

def resolve_dynamic_exploration(survivor_name: str, survivor_trait: str, area_data: dict) -> dict:
    """Generates a dynamic exploration outcome based on JSON area data and survivor personality.

    Args:
        survivor_name (str): The name of the survivor exploring the area.
        survivor_trait (str): The personality trait of the survivor affecting exploration outcomes.
        area_data (dict): The JSON data representing the area being explored.

    Returns:
        dict: A structured dictionary containing narrative, resources_gained, and hp_change.
    """
    fallback = {"narrative": f"I found nothing.", "resources_gained": {}, "hp_change": 0}
    
    if not os.getenv("GROQ_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        return fallback

    context = f"Survivor: {survivor_name}\nPersonality Trait: {survivor_trait}\nArea Data: {json.dumps(area_data)}"

    try:
        response = completion(
            model="groq/llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompts.DYNAMIC_EXPLORATION_PROMPT},
                {"role": "user", "content": context}
            ],
            fallbacks=[
                "groq/llama-3.1-8b-instant", 
                "gemini/gemini-1.5-flash"
            ],
            temperature=0.7,
            max_tokens=150
        )
        content = response["choices"][0]["message"]["content"].strip()
        return json.loads(content)
    except Exception as e:
        print(f"Exploration Error: {e}")
        return fallback

def generate_daily_event(day: int, scenario_data: dict) -> dict:
    """Generates a random morning event based on the scenario JSON and a weighted tone.
    
    Args:
        day (int): The current day in the game.
        scenario_data (dict): The JSON data representing the current scenario.

    Returns:
        dict: A structured dictionary containing event_title, narrative, and camp_resource_change.
    """
    fallback = {"event_title": "A Quiet Morning", "narrative": "Nothing unusual happens today.", "camp_resource_change": {}}
    
    if not os.getenv("GROQ_API_KEY") and not os.getenv("GEMINI_API_KEY"):
        return fallback

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
            fallbacks=[
                "groq/llama-3.1-8b-instant", 
                "gemini/gemini-1.5-flash"
            ],  
            messages=[
                {"role": "system", "content": prompts.RANDOM_EVENT_PROMPT},
                {"role": "user", "content": context}
            ],
            temperature=0.8,
            max_tokens=200
        )
        content = response["choices"][0]["message"]["content"].strip()
        return json.loads(content)
    except Exception as e:
        print(f"Event Error: {e}")
        return fallback

def resolve_custom_action(survivor_name: str, survivor_trait: str, action_text: str) -> dict:
    """Generates a dynamic outcome based on a player's free-form custom action.
    
    Args:
        survivor_name (str): The name of the survivor performing the action.
        survivor_trait (str): The personality trait of the survivor affecting action outcomes.
        action_text (str): The free-form text describing the player's custom action.

    Returns:
        dict: A structured dictionary containing narrative, resources_gained, and hp_change.
    """
    fallback = {"narrative": "I tried to do that, but nothing happened.", "resources_gained": {}, "hp_change": 0}

    if not os.getenv("GROQ_API_KEY") and not os.getenv("GEMINI_API_KEY"): 
        return fallback

    # Pass the survivor details AND the player's custom text
    context = f"Survivor: {survivor_name}\nPersonality Trait: {survivor_trait}\nCustom Action Attempted: {action_text}"

    try:
        response = completion(
            model="groq/llama-3.3-70b-versatile",
            fallbacks=[
                "groq/llama-3.1-8b-instant", 
                "gemini/gemini-1.5-flash"
            ],
            messages=[
                {"role": "system", "content": prompts.CUSTOM_ACTION_PROMPT},
                {"role": "user", "content": context}
            ],
            temperature=0.7,
            max_tokens=200
        )
        content = response["choices"][0]["message"]["content"].strip()

        if content.startswith("```json"):
            content = content.replace("```json\n", "").replace("\n```", "")

        return json.loads(content)
    except Exception as e:
        print(f"Custom Action Error: {e}")
        return fallback