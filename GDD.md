# Game Design Document: Text Survival RPG

**Author:** Jerell Tan  
**Project:** AI Application Development Bootcamp 2026 Capstone  

---

## 1. Overview & Concept
**Title:** (TBD - e.g., *Stranded Whispers* or *Isle of Code*)
**Genre:** Turn-based Survival Management / Text RPG
**Core Inspiration:** *Tinker Island*

**Summary:** 
A text-based survival management game where the player controls a group of stranded survivors. The player assigns survivors to tasks (Foraging, Exploring, Building) across different island zones. The game utilizes a hybrid architecture: strict mathematical state management for resources and stats, paired with an LLM for dynamic, atmospheric narrative resolution.

**Application Purpose:** 
To provide an engaging, replayable interactive narrative experience while demonstrating robust API integration, precise LLM prompting, and reliable application state management.

---

## 2. Technology Stack
*   **Language:** Python 3.10+
*   **Frontend / UI:** Streamlit (Phase 1 Prototype) -> React (Phase 2 Potential Migration)
*   **AI Integration:** `litellm` library connecting to Google Gemini or Groq
*   **Data Storage:** Local JSON files for static game data (`events.json`, `enemies.json`)
*   **Security:** `python-dotenv` to manage API keys securely in a `.env` file, ensuring no keys are committed to source control.

---

## 3. Core Gameplay Loop
The game operates in distinct turns (Days). Each Day follows this sequence:

1.  **Setup Phase:** The UI displays the current Day, accumulated resources (Wood, Food), and survivor status (Health, Energy).
2.  **Assignment Phase:** The player selects a survivor and assigns them a task in a specific location (e.g., "Assign Alex to Forage in the Jungle").
3.  **Resolution Phase:**
    *   Python logic calculates the outcome (Success/Failure/Combat) based on the survivor's stats.
    *   Python selects an appropriate encounter template from local JSON data.
    *   The outcome and template are passed to the LLM via `litellm`.
    *   The LLM generates a 2-3 sentence narrative describing the event.
4.  **Update Phase:** The UI displays the narrative text, and resources/health are mathematically adjusted in the backend.

---

## 4. Game State & Data Models

### 4.1 Dynamic Player State
Maintained in Python (via `st.session_state` in Streamlit).
```json
{
  "day": 1,
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