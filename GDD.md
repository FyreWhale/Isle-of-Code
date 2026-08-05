# Game Design Document: Isle of Code

**Author:** Jerell Tan  
**Project:** AI Application Development Bootcamp 2026 Capstone  

---

## 1. Overview & Concept
**Title:** Isle of Code  
**Genre:** Turn-based Survival Management / Text RPG
**Core Inspiration:** *Tinker Island*

**Summary:** 
A text-based survival management game where the player controls a group of stranded survivors. The game utilizes a highly structured hybrid architecture: Python strictly handles all mathematical state management (resources, day tracking, health), while an LLM serves as a procedural encounter generator, player intent parser, and atmospheric narrative engine.

**Application Purpose:** 
To provide an engaging, replayable interactive narrative experience while demonstrating robust API integration, precise LLM prompting, and reliable application state management.

---

## 2. Technology Stack & Modularity
*   **Language:** Python 3.10 or later.
*   **Frontend / UI:** Streamlit.
*   **AI Gateway:** The `litellm` library routing to Groq, which runs open-source models, offers very fast response times, and is entirely free.
*   **Data Storage:** Local JSON files for static templates.
*   **State Management:** Streamlit's `st.session_state`.
*   **Security:** The `python-dotenv` library is used to manage API keys securely via `os.getenv()`. API keys will never appear in the source code or be committed to GitHub.

### 2.1 Modular File Architecture
To maintain professional coding standards and project modularity, the codebase will be split into specific files:
*   `app.py`: The main Streamlit UI and Python game state math calculator.
*   `llm_engine.py`: Handles all Groq API connections, JSON parsing, and mandatory error handling.
*   `prompts.py`: Stores all system prompts as named constant variables at the top of the file.
*   `.env`: The local environment file for the API key.
*   `.env.example`: A template file showing which environment variables are needed, utilizing placeholder values instead of real keys.
*   `requirements.txt`: The dependency file listing the libraries the project needs to run.

---

## 3. Core Gameplay Loop & Architecture
The game operates in distinct turns (Days). The engine enforces a strict boundary between AI creativity and Game State integrity.

### Phase 1: Game Setup (World Selection)
The player selects their survival environment. This injects specific thematic rules into the LLM system prompts for the duration of the session.

### Phase 2: Encounter Generation (LLM -> JSON)
When the player explores, the LLM procedurally generates an encounter tailored to the active world. The LLM is forced to output this encounter strictly as a structured JSON template (e.g., `{"title": str, "description": str, "stat_check": str}`). This dynamic template is then injected into the UI.

### Phase 3: Player Action (Hybrid UI)
The player can respond to the encounter in one of two ways:
1.  **Standard Action (Button):** A safe, predictable action leveraging predefined survivor stats.
2.  **Custom Action (Text Box):** The player types a free-form action. The LLM parses this intent into structured JSON rules, allowing the application to successfully handle unexpected or out-of-scope player inputs without breaking the experience.

### Phase 4: Resolution & Math (Python)
Python evaluates the action (from the button or the parsed text intent), checks `st.session_state` to see if the survivor has the required stats/energy, and calculates the mathematical outcome (Success/Failure). 

### Phase 5: Narrative Generation (LLM -> Text)
Python passes the calculated mathematical outcome back to the LLM. The LLM acts strictly as a narrative engine, generating 2-3 sentences of atmospheric flavor text based on the outcome without altering the game state itself.

---

## 4. Game State & Data Models

### 4.1 Dynamic Player State
Maintained entirely in Python via `st.session_state` to prevent AI hallucinations from breaking game balance.

```json
{
  "day": 1,
  "world": {
      "name": "Glacial Wasteland",
      "hazard": "Freezing Frost"
  },
  "resources": {
    "food": 10,
    "wood": 0
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