import streamlit as st
import utils.game_logic as game_logic
import utils.llm_engine as llm_engine
from utils.prompts import NARRATIVE_SYSTEM_PROMPT

# Page configuration
st.set_page_config(
    page_title="Isle of Code",
    page_icon="🏝️",
    layout="centered"
)

# Initialize Streamlit Session State for Game State persistence
if "game_state" not in st.session_state:
    st.session_state.game_state = game_logic.get_initial_game_state()

if "narrative_log" not in st.session_state:
    st.session_state.narrative_log = ["You wash ashore on a mysterious, uncharted coast. Your survival begins now."]

# App Header
st.title("🏝️ Isle of Code")
st.markdown("A text-based survival management RPG.")

# Sidebar: Display Current Resources and Survivor Stats
st.sidebar.header("📊 Camp Status")
state = st.session_state.game_state

st.sidebar.subheader(f"Day: {state['day']}")

st.sidebar.markdown("### Resources")
for res, amount in state["resources"].items():
    st.sidebar.text(f"{res.capitalize()}: {amount}")

st.sidebar.markdown("### Survivors")
for survivor in state["survivors"]:
    st.sidebar.text(f"{survivor['name']} (HP: {survivor['hp']} | Energy: {survivor['energy']})")

# Main Dashboard: Actions & Narrative Output
st.subheader("🏕️ Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🪵 Forage Wood"):
        # Check resources/energy, consume cost, add reward, advance day
        survivor = state["survivors"][0]
        if survivor["energy"] >= 10:
            updated_survivor = game_logic.consume_survivor_energy(survivor, 10)
            state["survivors"][0] = updated_survivor
            
            earned = {"wood": 3}
            state["resources"] = game_logic.add_resources(state["resources"], earned)
            state = game_logic.advance_day(state)
            st.session_state.game_state = state
            
            # Generate narrative flavor
            flavor = llm_engine.generate_narrative_flavor(
                "Player successfully foraged 3 units of wood at the cost of 10 energy.",
                NARRATIVE_SYSTEM_PROMPT
            )
            st.session_state.narrative_log.append(f"Day {state['day'] - 1}: {flavor}")
            st.rerun()
        else:
            st.warning("Survivor is too exhausted to forage!")

with col2:
    if st.button("🍖 Hunt Food"):
        survivor = state["survivors"][0]
        if survivor["energy"] >= 15:
            updated_survivor = game_logic.consume_survivor_energy(survivor, 15)
            state["survivors"][0] = updated_survivor
            
            earned = {"food": 4}
            state["resources"] = game_logic.add_resources(state["resources"], earned)
            state = game_logic.advance_day(state)
            st.session_state.game_state = state
            
            flavor = llm_engine.generate_narrative_flavor(
                "Player hunted successfully, securing 4 units of food at the cost of 15 energy.",
                NARRATIVE_SYSTEM_PROMPT
            )
            st.session_state.narrative_log.append(f"Day {state['day'] - 1}: {flavor}")
            st.rerun()
        else:
            st.warning("Survivor is too exhausted to hunt!")

with col3:
    if st.button("💤 Rest Camp"):
        survivor = state["survivors"][0]
        updated_survivor = game_logic.add_survivor_energy(survivor, 25)
        state["survivors"][0] = updated_survivor
        state = game_logic.advance_day(state)
        st.session_state.game_state = state
        
        flavor = llm_engine.generate_narrative_flavor(
            "Survivors rested at camp, recovering 25 energy.",
            NARRATIVE_SYSTEM_PROMPT
        )
        st.session_state.narrative_log.append(f"Day {state['day'] - 1}: {flavor}")
        st.rerun()

# Narrative History Log
st.markdown("---")
st.subheader("📜 Survival Log")
for entry in reversed(st.session_state.narrative_log):
    st.write(f"- {entry}")