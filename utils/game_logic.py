import os
import random

def get_initial_game_state(survivor_pool: list) -> dict:
    """Generates the initial game state with default resources, survivors, and inventory.

    Args:
        survivor_pool (list): A list of dictionaries containing potential survivor data.

    Returns:
        dict: The initial game state dictionary.
    """
    if not survivor_pool:
        survivor_pool = [{"name": "Default", "skills": {}, "trait": "A standard survivor."}]

    chosen_survivors = random.sample(survivor_pool, min(2, len(survivor_pool)))

    starting_roster = []
    for s in chosen_survivors:
        active_survivor = s.copy()
        active_survivor["hp"] = 100
        active_survivor["assigned_area"] = "Idle"
        starting_roster.append(active_survivor)

    return {
        "day": 1,
        "resources": {
            "food": 10,
            "wood": 5
        },
        "survivors": starting_roster,
        "inventory": []
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

def consume_item_from_inventory(state: dict, item_name: str) -> dict:
    """Removes an item from the inventory and applies its baseline survival effect.

    Args:
        state (dict): The current overall game state dictionary.
        item_name (str): The name of the item to consume from inventory.

    Returns:
        dict: The updated game state dictionary.
    """
    updated_state = state.copy()
    inventory = updated_state.get("inventory", [])
    
    if item_name in inventory:
        inventory.remove(item_name)
        updated_state["inventory"] = inventory
        
        # Apply item effects based on name
        if item_name.lower() in ["ration", "food pack"]:
            updated_state["resources"]["food"] = updated_state["resources"].get("food", 0) + 2
        elif item_name.lower() in ["medkit", "bandage"]:
            if updated_state.get("survivors"):
                updated_state["survivors"][0] = add_survivor_hp(updated_state["survivors"][0], 30)
                
    return updated_state

def check_any_survivor_alive(state: dict) -> bool:
    """Checks whether at least one survivor in the game state still has greater than 0 HP.

    Args:
        state (dict): The current overall game state dictionary.

    Returns:
        bool: True if at least one survivor is alive, False if all survivors are dead.
    """
    survivors = state.get("survivors", [])
    for survivor in survivors:
        if survivor.get("hp", 0) > 0:
            return True
    return False

def resolve_defense_check(state: dict, raid_difficulty: int) -> dict:
    """Evaluates whether the camp's defense capability withstands a hostile raid, applying damage on failure.

    Args:
        state (dict): The current overall game state dictionary.
        raid_difficulty (int): The target threshold required to successfully defend the camp.

    Returns:
        dict: The updated game state dictionary after resolving the defense check.
    """
    updated_state = state.copy()
    
    # Calculate total combat skill or defense power available from survivors
    total_combat_power = sum(
        survivor.get("skills", {}).get("combat", 0) 
        for survivor in updated_state.get("survivors", [])
        if survivor.get("hp", 0) > 0
    )
    
    # Resolve success or failure
    if total_combat_power < raid_difficulty:
        # Defense failed: apply damage to the first active survivor
        if updated_state.get("survivors"):
            updated_state["survivors"][0] = consume_survivor_hp(
                updated_state["survivors"][0], 
                damage=20
            )
            
    return updated_state

def assign_survivor_to_area(state: dict, survivor_name: str, area_name: str) -> dict:
    """Assigns a specific survivor to a designated exploration or work area.

    Args:
        state (dict): The current overall game state dictionary.
        survivor_name (str): The name of the survivor being assigned.
        area_name (str): The name of the area to assign them to.

    Returns:
        dict: The updated game state dictionary.
    """
    updated_state = state.copy()
    for survivor in updated_state.get("survivors", []):
        if survivor["name"] == survivor_name:
            survivor["assigned_area"] = area_name
    return updated_state

def full_rest_survivor(survivor: dict) -> dict:
    """Restores a survivor's HP when they rest at camp.
    
    Args:
        survivor (dict): The survivor dictionary containing HP stats.

    Returns:
        dict: The updated survivor dictionary with restored HP.
    """
    updated_survivor = survivor.copy()
    # Cap HP at 100
    updated_survivor["hp"] = min(100, updated_survivor["hp"] + 20)
    return updated_survivor