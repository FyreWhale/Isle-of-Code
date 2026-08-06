import pytest
import utils.game_logic as game_logic

def test_get_initial_game_state() -> None:
    """Tests that initial game state contains the required base keys and starting values."""
    state = game_logic.get_initial_game_state()
    assert state["day"] == 1
    assert state["resources"]["food"] == 10
    assert len(state["survivors"]) == 1

def test_has_sufficient_resources_success() -> None:
    """Tests resource validation logic when player has sufficient stock."""
    resources = {"food": 10, "wood": 5}
    cost = {"food": 5, "wood": 2}
    assert game_logic.has_sufficient_resources(resources, cost) is True

def test_has_sufficient_resources_failure() -> None:
    """Tests resource validation logic when player lacks sufficient stock."""
    resources = {"food": 2, "wood": 1}
    cost = {"food": 5, "wood": 2}
    assert game_logic.has_sufficient_resources(resources, cost) is False

def test_consume_resources() -> None:
    """Tests that resource costs are correctly subtracted from player inventory."""
    resources = {"food": 10, "wood": 5}
    cost = {"food": 3, "wood": 2}
    updated = game_logic.consume_resources(resources, cost)
    assert updated["food"] == 7
    assert updated["wood"] == 3

def test_add_resources() -> None:
    """Tests that gathered resources are correctly added to player inventory."""
    resources = {"food": 5, "wood": 2}
    earned = {"food": 4, "wood": 3}
    updated = game_logic.add_resources(resources, earned)
    assert updated["food"] == 9
    assert updated["wood"] == 5

def test_consume_survivor_energy() -> None:
    """Tests that survivor energy is correctly deducted without dropping below zero."""
    survivor = {"name": "Alex", "hp": 100, "energy": 50, "skills": {"scavenge": 5}}
    updated = game_logic.consume_survivor_energy(survivor, 20)
    assert updated["energy"] == 30
    
    # Test boundary condition (energy shouldn't go negative)
    exhausted = game_logic.consume_survivor_energy(updated, 50)
    assert exhausted["energy"] == 0

def test_add_survivor_energy() -> None:
    """Tests that survivor energy is correctly increased without exceeding maximum limit."""
    survivor = {"name": "Alex", "hp": 100, "energy": 40, "skills": {"scavenge": 5}}
    updated = game_logic.add_survivor_energy(survivor, 30)
    assert updated["energy"] == 70
    
    # Test boundary condition (Energy shouldn't exceed 100)
    maxed = game_logic.add_survivor_energy(updated, 50)
    assert maxed["energy"] == 100

def test_consume_survivor_hp() -> None:
    """Tests that survivor HP is correctly deducted without dropping below zero."""
    survivor = {"name": "Alex", "hp": 100, "energy": 50, "skills": {"scavenge": 5}}
    updated = game_logic.consume_survivor_hp(survivor, 30)
    assert updated["hp"] == 70
    
    # Test boundary condition (HP shouldn't go negative)
    fatal = game_logic.consume_survivor_hp(updated, 100)
    assert fatal["hp"] == 0

def test_add_survivor_hp() -> None:
    """Tests that survivor HP is correctly restored without exceeding maximum limit."""
    survivor = {"name": "Alex", "hp": 60, "energy": 50, "skills": {"scavenge": 5}}
    updated = game_logic.add_survivor_hp(survivor, 25)
    assert updated["hp"] == 85
    
    # Test boundary condition (HP shouldn't exceed 100)
    maxed = game_logic.add_survivor_hp(updated, 50)
    assert maxed["hp"] == 100

def test_evaluate_skill_check() -> None:
    """Tests that survivor skill check correctly evaluates success and failure conditions."""
    survivor = {"name": "Alex", "hp": 100, "energy": 50, "skills": {"scavenge": 5, "combat": 2}}
    
    # Success condition (skill >= threshold)
    assert game_logic.evaluate_skill_check(survivor, "scavenge", 4) is True
    assert game_logic.evaluate_skill_check(survivor, "combat", 2) is True
    
    # Failure condition (skill < threshold)
    assert game_logic.evaluate_skill_check(survivor, "scavenge", 8) is False

def test_advance_day() -> None:
    """Tests that the game day counter increments correctly."""
    state = game_logic.get_initial_game_state()
    assert state["day"] == 1
    
    advanced_state = game_logic.advance_day(state)
    assert advanced_state["day"] == 2