import streamlit as st
import utils.game_logic as game_logic
import utils.llm_engine as llm_engine
import utils.data_loader as data_loader
from utils.prompts import NARRATIVE_SYSTEM_PROMPT

# ==========================================
# 1. PAGE CONFIG & STATE INIT
# ==========================================
st.set_page_config(
    page_title="Isle of Code",
    page_icon="🏝️",
    layout="wide"
)

if "game_state" not in st.session_state:
    st.session_state.game_state = game_logic.get_initial_game_state()

if "narrative_log" not in st.session_state:
    st.session_state.narrative_log = ["Day 0: You wash ashore on a mysterious, uncharted coast. Your survival begins now."]

state = st.session_state.game_state

# Load all game data
game_data = data_loader.get_all_game_data()
scenario_data = game_data.get("scenarios", {}).get("lost_island", {})
areas_data = game_data.get("areas", {})

# ==========================================
# 2. SIDEBAR: SCROLLING HISTORY LOG
# ==========================================
st.sidebar.header("📜 Full Survival Log")
with st.sidebar.container(height=750, border=False):
    for entry in reversed(st.session_state.narrative_log):
        st.markdown(f"• {entry}")
        st.markdown("---")

# ==========================================
# 3. TOP DASHBOARD: DAY & RESOURCES
# ==========================================
col_title, col_day = st.columns([4, 1])
with col_title:
    st.title("🏝️ Isle of Code")
    st.caption("A text-based survival management RPG.")
with col_day:
    st.metric("☀️ Current Day", state['day'])

st.subheader("📦 Camp Resources")
# Dynamically create columns based on how many resource types exist
res_keys = list(state["resources"].keys())
res_cols = st.columns(max(len(res_keys), 4)) # Ensure at least 4 columns for spacing
for i, (res, amount) in enumerate(state["resources"].items()):
    res_cols[i].metric(label=res.capitalize(), value=amount)

st.divider()

# ==========================================
# 4. MAIN LAYOUT (SIDE-BY-SIDE)
# ==========================================
left_col, right_col = st.columns([1.5, 1], gap="large")

# --- LEFT COLUMN: CONTROLS ---
with left_col:
    tab_tasks, tab_custom, tab_craft = st.tabs([
        "🏕️ Task Assignment", 
        "✍️ Custom Action", 
        "🔨 Crafting & Inventory"
    ])

    # --- TAB 1: SURVIVOR TASKS ---
    with tab_tasks:
        available_areas = ["Camp (Rest)", "Idle"] + list(areas_data.keys())
        updated_survivors = []

        for i, survivor in enumerate(state["survivors"]):
            col_a, col_b = st.columns([1, 2])
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
                    label_visibility="collapsed",
                    format_func=lambda x: areas_data[x].get("name", x) if x in areas_data else x
                )
            
            updated_survivor = survivor.copy()
            updated_survivor["assigned_area"] = selected_area
            updated_survivors.append(updated_survivor)
            st.markdown("---")

        state["survivors"] = updated_survivors

        if st.button("🚀 Proceed Day (Execute Assignments)", use_container_width=True):
            new_resources = state["resources"].copy()
            narrative_summaries = []
            
            # --- 1. Random Event (With Stat Formatting) ---
            event_outcome = llm_engine.generate_daily_event(state["day"], scenario_data)
            event_res = event_outcome.get("camp_resource_change", {})
            new_resources = game_logic.add_resources(new_resources, event_res)
            
            # Build stat tags for the event (e.g., [+5 food])
            e_stats = [f"+{amt} {res}" if amt > 0 else f"{amt} {res}" for res, amt in event_res.items() if amt != 0]
            e_stat_str = f" `[{', '.join(e_stats)}]`" if e_stats else ""
            
            # Use blockquotes (>) to make the event stand out from the survivor logs
            narrative_summaries.append(f"**🌟 Event: {event_outcome.get('event_title', 'Update')}**\n> {event_outcome.get('narrative', '')}{e_stat_str}")
            
            # --- 2. Resolve Survivor Actions ---
            for survivor in state["survivors"]:
                area_name = survivor["assigned_area"]
                
                if area_name == "Camp (Rest)":
                    survivor.update(game_logic.full_rest_survivor(survivor))
                    narrative_summaries.append(f"**{survivor['name']}**: \"I rested at camp and fully recovered my energy.\" `[+Energy]`")
                
                elif area_name in areas_data:
                    if survivor["energy"] >= 15:
                        survivor = game_logic.consume_survivor_energy(survivor, 15)
                        outcome = llm_engine.resolve_dynamic_exploration(survivor["name"], areas_data[area_name])
                        
                        # Apply resources
                        res_gained = outcome.get("resources_gained", {})
                        hp_change = outcome.get("hp_change", 0)
                        
                        new_resources = game_logic.add_resources(new_resources, res_gained)
                        if hp_change < 0:
                            survivor = game_logic.consume_survivor_hp(survivor, abs(hp_change))
                            
                        # Build stat tags for the survivor (e.g., [+2 wood, -5 HP])
                        s_stats = [f"+{amt} {res}" for res, amt in res_gained.items() if amt > 0]
                        if hp_change < 0:
                            s_stats.append(f"{hp_change} HP")
                            
                        s_stat_str = f" `[{', '.join(s_stats)}]`" if s_stats else ""
                        
                        # Format as First-Person quote with tags
                        narrative_summaries.append(f"**{survivor['name']}**: \"{outcome.get('narrative', f'I explored {area_name}.')}\"{s_stat_str}")
                    else:
                        narrative_summaries.append(f"**{survivor['name']}**: \"I was too exhausted to explore {area_name}.\"")
                else:
                    narrative_summaries.append(f"**{survivor['name']}**: \"I remained idle at camp today.\"")

            # --- 3. Update State & Log ---
            state["resources"] = new_resources
            state = game_logic.advance_day(state)
            st.session_state.game_state = state
            
            daily_log = "\n\n".join(narrative_summaries)
            st.session_state.narrative_log.append(f"Day {state['day'] - 1}: \n\n{daily_log}")
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
                    st.session_state.narrative_log.append(f"Day {state['day'] - 1}: \n\n{flavor}")
                    st.rerun()
                else:
                    st.warning("The camp is too exhausted for this custom action!")
            else:
                st.warning("Please type an action first.")

    # --- TAB 3: CRAFTING & INVENTORY ---
    with tab_craft:
        CRAFTING_RECIPES = game_data.get("crafting", {})

        current_inventory = state.get("inventory", [])
        st.markdown(f"**Current Inventory:** {', '.join(current_inventory) if current_inventory else 'Empty'}")
        st.divider()

        item_to_craft = st.selectbox("Select item to craft:", options=list(CRAFTING_RECIPES.keys()))
        if item_to_craft:
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
                    st.session_state.narrative_log.append(f"Day {state['day']}: \n\n{flavor}")
                    st.rerun()
                else:
                    st.warning(f"Not enough resources to craft {item_to_craft}!")

# --- RIGHT COLUMN: LATEST REPORT ---
with right_col:
    st.subheader("🔔 Latest Report")
    with st.container(border=True):
        if st.session_state.narrative_log:
            latest_entry = st.session_state.narrative_log[-1]
            
            # Safely check if a colon exists before splitting
            if ':' in latest_entry:
                day_text, body_text = latest_entry.split(':', 1)
                st.markdown(f"#### {day_text}")
                st.markdown(body_text.strip())
            else:
                # Fallback if no colon is found
                st.markdown(latest_entry.strip())