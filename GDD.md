# Game Design Document: Isle of Code

**Author:** Jerell Tan
**Project:** AI Application Development Bootcamp 2026 Capstone

---

## 1. Overview & Concept
**Title:** Isle of Code
**Genre:** Turn-based Survival Management / Text RPG
**Core Inspiration:** *Tinker Island*

**Summary:** 
A text-based survival management game where the player controls a group of stranded survivors. The game utilizes a highly structured hybrid architecture: Python strictly handles all mathematical state management (resources, day tracking, health, starvation, crafting), while an LLM serves as a procedural encounter generator, dynamic custom action engine, collaborative crafting narrator, and atmospheric story teller.

**Application Purpose:** 
To provide an engaging, replayable interactive narrative experience while demonstrating robust API integration, multi-provider fallback error handling, precise LLM prompting, and reliable application state management.

---

## 2. Technology Stack & Modularity
*   **Language:** Python 3.10 or later.
*   **Frontend / UI:** Streamlit.
*   **AI Gateway & Auto-Swapper:** The `litellm` library routing through a multi-provider fallback chain to ensure continuous uptime during rate limits.
*   **Configuration:** `config.json` stores the primary and fallback model hierarchies centrally.
*   **Data Storage:** Local JSON files for static scenarios, areas, and crafting recipes.
*   **State Management:** Streamlit's `st.session_state`.
*   **Security:** The `python-dotenv` library is used to manage API keys securely via `os.getenv()`. API keys never appear in source code or commits.

### 2.1 Modular File Architecture
To maintain professional coding standards and project modularity, the codebase is split into specific modules:
*   `app.py`: The main Streamlit dashboard, tab layout interfaces, side-by-side layout, and day advancement loop.
*   `config.json`: The model registry file managing primary models and fallback provider chains.
*   `requirements.txt`: The dependency declarations listing required libraries (`streamlit`, `litellm`, `python-dotenv`).
*   `.env` / `.env.example`: Secure environment files managing API keys for Groq and Gemini.
*   `utils/game_logic.py`: Pure Python backend state management (resource math, HP consumption, starvation penalties, day advancements, win/loss state checks).
*   `utils/llm_engine.py`: Handles multi-provider `litellm` calls, fallback executions, JSON parsing, and graceful error handling.
*   `utils/data_loader.py`: Reads external JSON template data for scenarios, exploration areas, and crafting recipes.
*   `utils/prompts.py`: Centralized system prompts enforcing persona rules, trait integration, first-person narrative constraints, and JSON output schemas.

---

## 3. Core Gameplay Loop & Architecture
The game operates in distinct daily turns. The engine enforces a strict boundary between AI creative text generation and Python game-state integrity.

### Phase 1: Game Setup & Data Loading
The application loads external scenario files, areas, and recipes via `data_loader.py`. `game_logic.py` initializes the starting state in `st.session_state` with camp resources and survivor profiles (names, HP, personality traits).

### Phase 2: Daily Morning Events (LLM -> JSON)
Each turn, `llm_engine.generate_daily_event` constructs a dynamic morning event featuring active survivors by name and trait. The tone is dynamically weighted (Positive, Negative, or Neutral) and affects camp resources (e.g., `+2 food` or `-3 wood`).

### Phase 3: Player Action & Task Assignments
Players assign actions across three interface tabs:
1.  **Task Assignment (Area Exploration / Rest):** Assign survivors to specific locations (e.g., Jungle, Beach) or Camp Rest (`+20 HP`). The LLM calculates first-person exploration outcomes with personality-driven dialogue and resource/HP changes (`[+2 Wood, -10 HP]`).
2.  **Custom Action (Free-form Input):** The player types free-form commands (e.g., *"Search the beach for wreckage"*). The LLM acts as the Game Master, evaluating feasibility, applying HP penalties or resource gains, and generating character-driven text for each active survivor.
3.  **Group Crafting & Engineering:** Crafting items (e.g., Spear, Distress Beacon) requires camp resources. Crafting is treated as a collaborative project that consumes a full day, triggering a group narrative detailing how survivors worked together based on their personality traits.

### Phase 4: Resolution, Math & Daily Logistics (Python)
Python executes state modifications (`game_logic.py`):
*   Applies resource changes and updates survivor HP dictionaries using `.update()`.
*   **Daily Rations & Starvation System:** Deducts 1 Food per conscious survivor at the end of each day. If food is insufficient, food resets to 0 and all active survivors suffer -15 HP starvation damage.
*   Advances the game day counter by +1.

### Phase 5: Win / Loss State Evaluation
*   **Victory Condition:** Crafting and activating the "Distress Beacon" triggers celebratory balloons, displays a Victory banner, and offers a game restart.
*   **Defeat Condition:** If all survivors reach 0 HP, controls are hidden, replacing the main dashboard with a "Game Over" screen and a restart option.

---

## 4. Game State & Data Models

### 4.1 Dynamic Player State
Maintained entirely in Python via `st.session_state` to prevent AI hallucinations from altering game mechanics.

```json
{
  "day": 1,
  "resources": {
    "food": 10,
    "wood": 5
  },
  "inventory": [],
  "survivors": [
    {
      "name": "Alex",
      "hp": 100,
      "trait": "Cynical and pragmatic, complains often but gets the job done.",
      "assigned_area": "Camp (Rest)"
    },
    {
      "name": "Bailey",
      "hp": 100,
      "trait": "Overly optimistic and easily distracted by nature.",
      "assigned_area": "Idle"
    }
  ]
}