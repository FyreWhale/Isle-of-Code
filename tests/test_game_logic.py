import pytest
import utils.game_logic as game_logic

def test_get_initial_game_state() -> None:
    """Tests that initial game state contains the required base keys and starting values."""
    survivor_pool = [{"name": "Alex", "skills": {}, "trait": "Brave"}]
    state = game_logic.get_initial_game_state(survivor_pool)
    
    assert state["day"] == 1
    assert state["resources"]["food"] == 10
    assert state["resources"]["wood"] == 5
    assert len(state["survivors"]) == 1
    assert state["survivors"][0]["hp"] == 100
    assert state["survivors"][0]["assigned_area"] == "Idle"

def test_has_sufficient_resources_success() -> None:
    """Tests resource validation logic when player has sufficient stock."""
    # Updated to test advanced resources
    resources = {"food": 10, "wood": 5, "scrap_electronics": 2}
    cost = {"food": 5, "wood": 2, "scrap_electronics": 1}
    assert game_logic.has_sufficient_resources(resources, cost) is True

def test_has_sufficient_resources_failure() -> None:
    """Tests resource validation logic when player lacks sufficient stock."""
    resources = {"food": 2, "wood": 1, "silicon": 0}
    cost = {"food": 5, "wood": 2, "silicon": 1}
    assert game_logic.has_sufficient_resources(resources, cost) is False

def test_consume_resources() -> None:
    """Tests that resource costs are correctly subtracted from player inventory."""
    resources = {"food": 10, "wood": 5, "copper_wire": 4}
    cost = {"food": 3, "wood": 2, "copper_wire": 4}
    
    updated = game_logic.consume_resources(resources, cost)
    
    assert updated["food"] == 7
    assert updated["wood"] == 3
    assert updated["copper_wire"] == 0

def test_add_resources() -> None:
    """Tests that gathered resources are correctly added to player inventory."""
    resources = {"food": 5, "wood": 2}
    # Testing with advanced resources gathered from Custom Actions
    earned = {"food": 4, "wood": 3, "memory_sticks": 2}
    
    updated = game_logic.add_resources(resources, earned)
    
    assert updated["food"] == 9
    assert updated["wood"] == 5
    assert updated["memory_sticks"] == 2

def test_consume_survivor_hp() -> None:
    """Tests that survivor HP is correctly deducted without dropping below zero."""
    survivor = {"name": "Alex", "hp": 100, "skills": {"scavenge": 5}}
    
    updated = game_logic.consume_survivor_hp(survivor, 30)
    assert updated["hp"] == 70
    
    # Test boundary condition (HP shouldn't go negative)
    fatal = game_logic.consume_survivor_hp(updated, 100)
    assert fatal["hp"] == 0

def test_add_survivor_hp() -> None:
    """Tests that survivor HP is correctly restored without exceeding maximum limit."""
    survivor = {"name": "Alex", "hp": 60, "skills": {"scavenge": 5}}
    
    updated = game_logic.add_survivor_hp(survivor, 25)
    assert updated["hp"] == 85
    
    # Test boundary condition (HP shouldn't exceed 100)
    maxed = game_logic.add_survivor_hp(updated, 50)
    assert maxed["hp"] == 100

def test_evaluate_skill_check() -> None:
    """Tests that survivor skill check correctly evaluates success and failure conditions."""
    survivor = {"name": "Alex", "hp": 100, "skills": {"scavenge": 5, "combat": 2}}
    
    # Success condition (skill >= threshold)
    assert game_logic.evaluate_skill_check(survivor, "scavenge", 4) is True
    assert game_logic.evaluate_skill_check(survivor, "combat", 2) is True
    
    # Failure condition (skill < threshold)
    assert game_logic.evaluate_skill_check(survivor, "scavenge", 8) is False

def test_advance_day() -> None:
    """Tests that the game day counter increments correctly."""
    survivor_pool = [{"name": "Alex", "skills": {}, "trait": "Brave"}]
    state = game_logic.get_initial_game_state(survivor_pool)
    assert state["day"] == 1
    
    advanced_state = game_logic.advance_day(state)
    assert advanced_state["day"] == 2

def test_craft_item() -> None:
    """Tests that crafting an item correctly deducts resources and updates inventory."""
    survivor_pool = [{"name": "Alex", "skills": {}, "trait": "Brave"}]
    state = game_logic.get_initial_game_state(survivor_pool)
    
    # Inject advanced resources for testing mid-game crafting
    state["resources"]["scrap_electronics"] = 5
    state["resources"]["copper_wire"] = 2
    
    # Test crafting a high-tier item
    recipe = {"scrap_electronics": 3, "copper_wire": 1}
    updated_state = game_logic.craft_item(state, recipe, "Distress Beacon")
    
    assert updated_state["resources"]["scrap_electronics"] == 2
    assert "Distress Beacon" in updated_state["inventory"]
    
    # Test failed craft due to insufficient resources
    failed_state = game_logic.craft_item(updated_state, {"wood": 10}, "Spear")
    assert "Spear" not in failed_state.get("inventory", [])

def test_consume_item_from_inventory() -> None:
    """Tests that consuming an item removes it from inventory and applies appropriate effects."""
    survivor_pool = [{"name": "Alex", "skills": {}, "trait": "Brave"}]
    state = game_logic.get_initial_game_state(survivor_pool)
    state["inventory"] = ["Ration", "Medkit"]
    
    # Consume ration (adds 2 food)
    updated = game_logic.consume_item_from_inventory(state, "Ration")
    assert "Ration" not in updated["inventory"]
    assert updated["resources"]["food"] == 12
    
    # Consume medkit (heals survivor)
    updated["survivors"][0]["hp"] = 50
    healed = game_logic.consume_item_from_inventory(updated, "Medkit")
    assert "Medkit" not in healed["inventory"]
    assert healed["survivors"][0]["hp"] == 80

def test_check_any_survivor_alive() -> None:
    """Tests game-over condition tracking based on survivor HP across all survivors."""
    survivor_pool = [{"name": "Alex", "skills": {}, "trait": "Brave"}]
    state = game_logic.get_initial_game_state(survivor_pool)
    
    # Initially survivor has 100 HP, so should be alive
    assert game_logic.check_any_survivor_alive(state) is True
    
    # Set survivor's HP to 0 (dead)
    state["survivors"][0]["hp"] = 0
    assert game_logic.check_any_survivor_alive(state) is False

def test_resolve_defense_check() -> None:
    """Tests defense check resolution, applying damage when total combat power is insufficient."""
    survivor_pool = [{"name": "Alex", "skills": {"combat": 1}, "trait": "Brave"}]
    state = game_logic.get_initial_game_state(survivor_pool)
        
    # Total combat power is 1. Raid difficulty 5 exceeds power -> should take damage
    updated = game_logic.resolve_defense_check(state, raid_difficulty=5)
    assert updated["survivors"][0]["hp"] == 80

def test_assign_survivor_to_area() -> None:
    """Tests that a survivor is correctly assigned to a specific area."""
    survivor_pool = [{"name": "Alex", "skills": {}, "trait": "Brave"}]
    state = game_logic.get_initial_game_state(survivor_pool)
    
    updated = game_logic.assign_survivor_to_area(state, "Alex", "Deep Jungle")
    
    assert updated["survivors"][0]["assigned_area"] == "Deep Jungle"

def test_full_rest_survivor() -> None:
    """Tests that a survivor recovers 20 HP without exceeding maximum HP when resting."""
    survivor = {"name": "Alex", "hp": 70, "skills": {}}

    updated = game_logic.full_rest_survivor(survivor)
    assert updated["hp"] == 90  # Should recover 20 HP
    
    updated = game_logic.full_rest_survivor(updated)
    assert updated["hp"] == 100  # Should not exceed max HP