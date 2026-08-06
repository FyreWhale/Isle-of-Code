import pytest
import os
import utils.llm_engine as llm_engine

def test_generate_narrative_flavor_missing_key(monkeypatch) -> None:
    """Tests that the LLM engine fails gracefully with a warning message when the API key is missing."""
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    
    result = llm_engine.generate_narrative_flavor("Success", "You are a game master.")
    assert "GROQ_API_KEY is missing" in result

def test_generate_procedural_encounter_missing_key(monkeypatch) -> None:
    """Tests that procedural encounter generation falls back safely when the API key is missing."""
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    
    result = llm_engine.generate_procedural_encounter("Glacial Wasteland")
    assert "title" in result
    assert "description" in result
    assert "stat_type" in result
    assert "difficulty_threshold" in result

def test_parse_custom_action_intent_missing_key(monkeypatch) -> None:
    """Tests that custom action intent parsing falls back safely when the API key is missing."""
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    
    result = llm_engine.parse_custom_action_intent("hunt for food in the forest")
    assert result["action_type"] == "unknown"
    assert result["target_resource"] == "none"
    assert result["estimated_risk"] == "low"