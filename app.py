import streamlit as st
import utils.game_logic as game_logic
import utils.llm_engine as llm_engine
from utils.prompts import NARRATIVE_SYSTEM_PROMPT

# 1. Set Page Configuration to Wide Layout
st.set_page_config(
    page_title="Isle of Code",
    page_icon="🏝️",
    layout="wide"
)

# Initialize Streamlit Session State
if "game_state" not in st.session_state:
    st.session_state.game_state = game_logic.get_initial_game_state()

if "narrative_log" not in st.session_state:
    st.session_state.narrative_log = ["You wash ashore on a mysterious, uncharted coast. Your survival begins now."]

# Sidebar: Display Current Resources and Survivor Stats
st.sidebar.header("📊 Camp Status")
state = st.session_state.game_state

st.sidebar.subheader(f"Day: {state['day']}")
st.sidebar.markdown("### Resources")
for res, amount in state["resources"].items():
    st.sidebar.text(f"{res.capitalize()}: {amount}")

# Header
st.title("🏝️ Isle of Code")
st.caption("A text-based survival management RPG.")

# 2. Split Page into Two Columns (Left Controls : Right Log)
left_col, right_col = st.columns([1.2, 1], gap="medium")

# ==========================================
# LEFT COLUMN: Controls & Actions (No Scroll)
# ==========================================
with left_col:
    # Use Tabs to consolidate controls on one screen
    tab_tasks, tab_custom, tab_craft = st.tabs([
        "🏕️ Task Assignment", 
        "✍️ Custom Action", 
        "🔨 Crafting & Inventory"
    ])

    # --- TAB 1: SURVIVOR TASKS ---
    with tab_tasks:
        available_areas = ["Idle", "Deep Jungle", "Ruined Shore", "Mountain Cave", "Camp (Rest)"]
        updated_survivors = []

        # Display survivors side-by-side or cleanly stacked
        for i, survivor in enumerate(state["survivors"]):
            col_a, col_b = st.columns([1, 1.5])
            with col_a:
                st.markdown(f"**{survivor['name']}**")
                st.caption(f"Energy: {survivor['energy']}/100 | HP: {survivor['hp']}/100")
            with col_b:
                current_area_index = available_areas.index(survivor["assigned_area"]) if survivor["assigned_area"] in available_areas else 0
                selected_area = st.selectbox(
                    f"Assign to area:",
                    options=available_areas,
                    index=current_area_index,
                    key=f"area_{i}",
                    label_visibility="collapsed"
                )
            
            updated_survivor = survivor.copy()
            updated_survivor["assigned_area"] = selected_area
            updated_survivors.append(updated_survivor)
            st.divider()

        state["survivors"] = updated_survivors

        # Execute Day Button
        if st.button("🚀 Proceed Day (Execute Assignments)", use_container_width=True):
            new_resources = state["resources"].copy()
            narrative_summaries = []
            
            for survivor in state["survivors"]:
                area = survivor["assigned_area"]
                if area == "Camp (Rest)":
                    survivor.update(game_logic.full_rest_survivor(survivor))
                    narrative_summaries.append(f"{survivor['name']} rested at camp, fully recovering energy.")
                elif area == "Deep Jungle":
                    if survivor["energy"] >= 15:
                        survivor = game_logic.consume_survivor_energy(survivor, 15)
                        new_resources["wood"] = new_resources.get("wood", 0) + 4
                        narrative_summaries.append(f"{survivor['name']} scoured the Deep Jungle and gathered 4 wood.")
                    else:
                        narrative_summaries.append(f"{survivor['name']} was too exhausted to work in the Deep Jungle.")
                elif area == "Ruined Shore":
                    if survivor["energy"] >= 15:
                        survivor = game_logic.consume_survivor_energy(survivor, 15)
                        new_resources["food"] = new_resources.get("food", 0) + 4
                        narrative_summaries.append(f"{survivor['name']} searched the Ruined Shore and scavenged 4 food.")
                    else:
                        narrative_summaries.append(f"{survivor['name']} was too exhausted to scavenge the Ruined Shore.")
                elif area == "Mountain Cave":
                    if survivor["energy"] >= 20:
                        survivor = game_logic.consume_survivor_energy(survivor, 20)
                        new_resources["wood"] = new_resources.get("wood", 0) + 2
                        new_resources["food"] = new_resources.get("food", 0) + 2
                        narrative_summaries.append(f"{survivor['name']} mined the Mountain Cave, finding mixed supplies.")
                    else:
                        narrative_summaries.append(f"{survivor['name']} was too exhausted to explore the Mountain Cave.")
                else:
                    narrative_summaries.append(f"{survivor['name']} remained idle at camp.")

            state["resources"] = new_resources
            state = game_logic.advance_day(state)
            st.session_state.game_state = state
            
            combined_outcome = " ".join(narrative_summaries)
            flavor = llm_engine.generate_narrative_flavor(combined_outcome, NARRATIVE_SYSTEM_PROMPT)
            st.session_state.narrative_log.append(f"Day {state['day'] - 1}: {flavor}")
            st.rerun()

    # --- TAB 2: CUSTOM ACTION ---
    with tab_custom:
        st.caption("Type a free-form action for the survivors.")
        custom_action_input = st.text_input("What do you want the survivors to do?", placeholder="e.g., Search the beach for wreckage")

        if st.button("Execute Custom Action", use_container_width=True):
            if custom_action_input:
                intent = llm_engine.parse_custom_action_intent(custom_action_input)
                active_survivor = next((s for s in state["survivors"] if s["hp"] > 0), None)
                
                if active_survivor and active_survivor["energy"] >= 10:
                    updated_survivor = game_logic.consume_survivor_energy(active_survivor, 10)
                    for i, s in enumerate(state["survivors"]):
                        if s["name"] == updated_survivor["name"]:
                            state["survivors"][i] = updated_survivor
                            break
                    
                    state = game_logic.advance_day(state)
                    st.session_state.game_state = state
                    
                    flavor = llm_engine.generate_narrative_flavor(
                        f"Player executed custom action: '{custom_action_input}'. Parsed intent: {intent.get('action_type', 'unknown')} targeting {intent.get('target_resource', 'none')} with {intent.get('estimated_risk', 'low')} risk.",
                        NARRATIVE_SYSTEM_PROMPT
                    )
                    st.session_state.narrative_log.append(f"Day {state['day'] - 1}: {flavor}")
                    st.rerun()
                else:
                    st.warning("The camp is too exhausted for this custom action!")
            else:
                st.warning("Please type an action first.")

    # --- TAB 3: CRAFTING & INVENTORY ---
    with tab_craft:
        CRAFTING_RECIPES = {
            "Campfire": {"wood": 3},
            "Spear": {"wood": 2},
            "Food Pack": {"food": 3, "wood": 1}
        }

        current_inventory = state.get("inventory", [])
        st.markdown(f"**Current Inventory:** {', '.join(current_inventory) if current_inventory else 'Empty'}")
        st.divider()

        item_to_craft = st.selectbox("Select item to craft:", options=list(CRAFTING_RECIPES.keys()))
        cost = CRAFTING_RECIPES[item_to_craft]
        cost_str = ", ".join([f"{amount} {res.capitalize()}" for res, amount in cost.items()])
        st.caption(f"**Cost:** {cost_str}")

        if st.button(f"Craft {item_to_craft}", use_container_width=True):
            if game_logic.has_sufficient_resources(state["resources"], cost):
                state = game_logic.craft_item(state, cost, item_to_craft)
                st.session_state.game_state = state
                
                flavor = llm_engine.generate_narrative_flavor(
                    f"The survivors successfully crafted a {item_to_craft}.",
                    NARRATIVE_SYSTEM_PROMPT
                )
                st.session_state.narrative_log.append(f"Day {state['day']}: {flavor}")
                st.rerun()
            else:
                st.warning(f"Not enough resources to craft {item_to_craft}!")

# ==========================================
# RIGHT COLUMN: Scrollable Survival Log
# ==========================================
with right_col:
    st.subheader("📜 Survival Log")
    
    # Scrollable container dedicated to log entries
    with st.container(height=500, border=True):
        for entry in reversed(st.session_state.narrative_log):
            st.markdown(f"• {entry}")