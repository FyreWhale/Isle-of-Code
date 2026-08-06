import pytest
from utils.game_logic import get_initial_game_state

def test_get_initial_game_state() -> None:
    """Tests that initial game state contains the required base keys and starting values."""
    state = get_initial_game_state()
    assert state["day"] == 1
    assert state["resources"]["food"] == 10
    assert len(state["survivors"]) == 1