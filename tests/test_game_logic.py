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