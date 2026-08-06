import os

def get_initial_game_state() -> dict:
    """Initializes default resources, day tracker, and survivor state for a new game session.

    Returns:
        dict: A dictionary containing the starting day, resources, and survivor attributes.
    """
    return {
        "day": 1,
        "resources": {
            "food": 10,
            "wood": 5
        },
        "survivors": [
            {
                "name": "Alex",
                "hp": 100,
                "energy": 50,
                "skills": {"scavenge": 5, "combat": 2}
            }
        ]
    }

def has_sufficient_resources(current_resources: dict, cost: dict) -> bool:
    """Validates whether current resource stock meets a required cost dictionary.

    Args:
        current_resources (dict): The player's available resources.
        cost (dict): The required resources for the action.

    Returns:
        bool: True if sufficient resources are available, False otherwise.
    """
    for resource, required_amount in cost.items():
        if current_resources.get(resource, 0) < required_amount:
            return False
    return True