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