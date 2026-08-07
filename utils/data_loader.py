import json
import os

def load_json_file(filepath: str) -> dict:
    """Safely loads a JSON file."""
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. Returning empty dictionary.")
        return {}

def get_all_game_data() -> dict:
    """Loads all configuration data into a single dictionary."""
    base_dir = os.path.dirname(os.path.dirname(__file__))
    data_dir = os.path.join(base_dir, 'data')
    
    return {
        "scenarios": load_json_file(os.path.join(data_dir, 'scenarios.json')),
        "areas": load_json_file(os.path.join(data_dir, 'areas.json')),
        "crafting": load_json_file(os.path.join(data_dir, 'crafting.json')),
        "survivors": load_json_file(os.path.join(data_dir, 'survivors.json')),
        "valid_resources": load_json_file(os.path.join(data_dir, 'valid_resources.json'))
    }