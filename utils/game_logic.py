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

def consume_resources(current_resources: dict, cost: dict) -> dict:
    """Deducts specified resource costs from the current resource stock.

    Args:
        current_resources (dict): The player's available resources.
        cost (dict): The resources to deduct.

    Returns:
        dict: The updated resource dictionary.
    """
    updated_resources = current_resources.copy()
    for resource, amount in cost.items():
        if resource in updated_resources:
            updated_resources[resource] = max(0, updated_resources[resource] - amount)
    return updated_resources

def add_resources(current_resources:dict, earned: dict) -> dict:
    """Adds earned resources to the current resource stock.

    Args:
        current_resources (dict): The player's current available resources.
        earned (dict): The resources gained from an action.

    Returns:
        dict: The updated resource dictionary.
    """
    updated_resources = current_resources.copy()
    for resource, amount in earned.items():
        updated_resources[resource] = updated_resources.get(resource, 0) + amount
    return updated_resources

def consume_survivor_energy(survivor: dict, energy_cost: int) -> dict:
    """Deducts energy cost from a survivor's current pool, ensuring it does not drop below zero.

    Args:
        survivor (dict): The survivor dictionary containing energy stats.
        energy_cost (int): The amount of energy to subtract.

    Returns:
        dict: The updated survivor dictionary.
    """
    updated_survivor = survivor.copy()
    updated_survivor["energy"] = max(0, updated_survivor["energy"] - energy_cost)
    return updated_survivor