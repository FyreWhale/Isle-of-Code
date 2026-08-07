# Project Title and Description
**Isle of Code** 
Isle of Code is a turn-based survival management text RPG where the player controls a group of stranded survivors. Developed by Jerell Tan as a Capstone Project for the AI Application Development Bootcamp 2026 at the DigiPen Institute of Technology Singapore, the game utilizes a highly structured hybrid architecture. Python strictly handles all mathematical state management (resources, day tracking, health, starvation, crafting), while an LLM serves as a procedural encounter generator, collaborative crafting narrator, and atmospheric story teller. This application is designed for players who enjoy survival simulators and want a highly replayable interactive narrative experience.

# Problem Statement
Traditional text-based survival games suffer from a core design limitation: they become repetitive and predictable very quickly, which results in low replayability. Their scenarios and outcomes are strictly hardcoded. Isle of Code addresses this by leveraging Large Language Models to act as a dynamic "Game Master," seamlessly translating unstructured, highly creative player inputs into a strict, immutable backend resource management system. It demonstrates robust API integration, multi-provider fallback error handling, and precise LLM prompting while enforcing a strict boundary between AI creative text generation and game-state integrity.

# Technology Stack
*   **Language:** Python 3.10 or later
*   **Frontend / UI:** Streamlit
*   **AI Gateway & Auto-Swapper:** The `litellm` library routing through a multi-provider fallback chain to ensure continuous uptime during rate limits
*   **AI APIs:** Groq Llama 3.3 (Primary), Groq Llama 3.1 8B (Fallback 1), Google Gemini 1.5 (Fallback 2)
*   **State Management:** Streamlit's `st.session_state`
*   **Security:** The `python-dotenv` library is used to manage API keys securely via `os.getenv()`
*   **Data Storage:** Local JSON files for static scenarios, areas, and crafting recipes

# Setup Instructions

1. Clone the repository to your local machine:
    
    ```bash
    git clone <your-repository-url>
    ```

2. Navigate into the project directory:

    ```bash
    cd isle-of-code
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Copy the `.env.example` file to create a new `.env` file, then open it and fill in your actual API keys:

    ```bash
    cp .env.example .env
    ```
   *(Ensure your `.env` contains `GROQ_API_KEY=your_key_here` and `GEMINI_API_KEY=your_key_here`)*

5. Run the application:

    ```bash
    streamlit run app.py
    ```

# Usage Examples

1. **Task Assignment (Area Exploration / Rest)**
    *   **User Input:** The player assigns a survivor to a specific location (e.g., Jungle, Beach) or Camp Rest (`+20 HP`).
    *   **Application Output:** The LLM calculates first-person exploration outcomes with personality-driven dialogue and resource/HP changes (e.g., `[+2 Wood, -10 HP]`).

2. **Custom Action (Free-form Input)**
    *   **User Input:** The player types free-form commands (e.g., *"Search the beach for wreckage"*).
    *   **Application Output:** The LLM acts as the Game Master, evaluating feasibility, applying HP penalties or resource gains, and generating character-driven text for each active survivor.

3. **Group Crafting & Engineering**
    *   **User Input:** The player initiates crafting for items like a Spear or Distress Beacon.
    *   **Application Output:** The crafting action consumes camp resources and triggers a group narrative detailing how survivors worked together based on their personality traits.

# Known Limitations

*   **Frontend State Management:** The dynamic player state is maintained entirely in Python via `st.session_state` to prevent AI hallucinations from altering game mechanics[cite: 4]. However, because Streamlit is fundamentally a data-dashboard framework, rapidly clicking through tabs can sometimes cause the visual interface to lag behind the backend data calculations.
*   **API Rate Limiting:** The multi-provider fallback chain in `config.json` ensures continuous uptime during individual rate limits[cite: 4]. However, simultaneous timeouts across all configured LLM providers will still cause temporary generation delays.
*   **AI Statelessness ("Amnesia"):** To drastically reduce token consumption and improve generation speed, the application does not feed previous daily logs back into the LLM. The AI evaluates each action purely based on the current turn's state payload (current resources, survivor HP, and static traits)[cite: 4]. Consequently, the AI cannot reference specific narrative events that occurred on previous days.

# Future Improvements

*   **Decoupled UI Architecture:** Migrating the frontend away from the `app.py` Streamlit dashboard to a native React interface for more granular control over the front-end[cite: 1].
*   **Expanded Roster & Persistence:** Adding custom characters to the roster and implementing persistent database saving using SQLite so players can safely save and resume their runs[cite: 1].
*   **Expanded Data Models:** Adding more modular JSON files via `data_loader.py` to increase the pool of static scenarios, exploration areas, and crafting recipes.