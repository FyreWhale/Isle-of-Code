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

def add_survivor_energy(survivor: dict, energy_gain: int) -> dict:
    """Adds energy to a survivor's current pool, capping it at a maximum of 100.

    Args:
        survivor (dict): The survivor dictionary containing energy stats.
        energy_gain (int): The amount of energy to add.

    Returns:
        dict: The updated survivor dictionary.
    """
    updated_survivor = survivor.copy()
    updated_survivor["energy"] = min(100, updated_survivor["energy"] + energy_gain)
    return updated_survivor

def consume_survivor_hp(survivor: dict, damage: int) -> dict:
    """Deducts damage from a survivor's current HP pool, ensuring it does not drop below zero.

    Args:
        survivor (dict): The survivor dictionary containing HP stats.
        damage (int): The amount of health damage to subtract.

    Returns:
        dict: The updated survivor dictionary.
    """
    updated_survivor = survivor.copy()
    updated_survivor["hp"] = max(0, updated_survivor["hp"] - damage)
    return updated_survivor

def add_survivor_hp(survivor: dict, hp_gain: int) -> dict:
    """Adds health points to a survivor's current HP pool, capping it at a maximum of 100.

    Args:
        survivor (dict): The survivor dictionary containing HP stats.
        hp_gain (int): The amount of health points to add.

    Returns:
        dict: The updated survivor dictionary.
    """
    updated_survivor = survivor.copy()
    updated_survivor["hp"] = min(100, updated_survivor["hp"] + hp_gain)
    return updated_survivor

def evaluate_skill_check(survivor: dict, skill_name: str, difficulty_threshold: int) -> bool:
    """Evaluates whether a survivor's skill meets or exceeds a required difficulty threshold.

    Args:
        survivor (dict): The survivor dictionary containing skill mappings.
        skill_name (str): The specific skill to test (e.g., 'scavenge', 'combat').
        difficulty_threshold (int): The target number required for success.

    Returns:
        bool: True if the survivor's skill is greater than or equal to the threshold, False otherwise.
    """
    survivor_skill_value = survivor.get("skills", {}).get(skill_name, 0)
    return survivor_skill_value >= difficulty_threshold

def advance_day(state: dict) -> dict:
    """Advances the current game day counter by 1.

    Args:
        state (dict): The current overall game state dictionary.

    Returns:
        dict: The updated game state dictionary with incremented day.
    """
    updated_state = state.copy()
    updated_state["day"] += 1
    return updated_state

def craft_item(state: dict, recipe_cost: dict, item_name: str) -> dict:
    """Validates and executes the crafting of an item, consuming resources and updating inventory.

    Args:
        state (dict): The current overall game state dictionary.
        recipe_cost (dict): The resource cost required to craft the item.
        item_name (str): The name of the item being crafted.

    Returns:
        dict: The updated game state dictionary.
    """
    updated_state = state.copy()
    current_resources = updated_state.get("resources", {})
    
    # Check if sufficient resources exist using our existing helper
    if has_sufficient_resources(current_resources, recipe_cost):
        # Consume the resources
        updated_state["resources"] = consume_resources(current_resources, recipe_cost)
        
        # Add item to inventory (initialize inventory list if not present)
        if "inventory" not in updated_state:
            updated_state["inventory"] = []
        updated_state["inventory"].append(item_name)
        
    return updated_state