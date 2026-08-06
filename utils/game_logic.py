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