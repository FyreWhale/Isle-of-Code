import streamlit as st
import utils.game_logic as game_logic
import utils.llm_engine as llm_engine
import utils.data_loader as data_loader

# ==========================================
# 1. PAGE CONFIG & STATE INIT
# ==========================================
st.set_page_config(
    page_title="Isle of Code",
    page_icon="🏝️",
    layout="wide"
)

# 1. Load all game data FIRST
game_data = data_loader.get_all_game_data()
scenario_data = game_data.get("scenarios", {}).get("lost_island", {})
areas_data = game_data.get("areas", {})
survivor_pool = game_data.get("survivors", [])
valid_resources = game_data.get("valid_resources", [])

# 2. Game Setup & Character Creation Phase
if "game_started" not in st.session_state:
    st.session_state.game_started = False

if not st.session_state.game_started:
    st.title("🏝️ Isle of Code - Camp Setup")
    st.write("Create the two founding survivors of your camp!")
    
    # Helper function to dynamically stitch together the personality string
    def generate_dynamic_trait(ei, sn, tf, jp):
        traits = []
        
        if ei <= -3: traits.append("deeply introverted and avoids speaking")
        elif ei < 0: traits.append("quiet and keeps to themselves")
        elif ei == 0: traits.append("socially balanced")
        elif ei >= 3: traits.append("extremely loud, outgoing, and never stops talking")
        else: traits.append("sociable and enjoys chatting")
        
        if sn <= -3: traits.append("obsessed with literal facts and tangible resources")
        elif sn < 0: traits.append("grounded and highly practical")
        elif sn == 0: traits.append("pragmatic yet open-minded")
        elif sn >= 3: traits.append("wildly imaginative and easily distracted by abstract ideas")
        else: traits.append("creative and constantly thinking of new concepts")
        
        if tf <= -3: traits.append("cold, calculating, and entirely emotionally detached")
        elif tf < 0: traits.append("highly logical and relies on reason over feelings")
        elif tf == 0: traits.append("reasonable but considers others' feelings")
        elif tf >= 3: traits.append("a bleeding-heart who is intensely emotional and sensitive")
        else: traits.append("empathetic and driven heavily by their emotions")
        
        if jp <= -3: traits.append("utterly chaotic, impulsive, and hates following plans")
        elif jp < 0: traits.append("flexible and prefers taking things as they come")
        elif jp == 0: traits.append("adaptable but appreciates basic order")
        elif jp >= 3: traits.append("rigidly structured, bossy, and panics if routines break")
        else: traits.append("organized and prefers having a clear plan")
        
        return ", ".join(traits[:-1]) + ", and " + traits[-1] + "."

    # Helper function to generate a dynamic archetype title based on extreme scores
    def generate_dynamic_title(ei, sn, tf, jp):
        # Determine the Adjective (from EI or SN, whichever is more extreme)
        if abs(ei) >= abs(sn):
            if ei <= -3: adj = "Silent"
            elif ei < 0: adj = "Reserved"
            elif ei == 0: adj = "Steady"
            elif ei >= 3: adj = "Radiant"
            else: adj = "Bold"
        else:
            if sn <= -3: adj = "Ironclad"
            elif sn < 0: adj = "Grounded"
            elif sn >= 3: adj = "Visionary"
            else: adj = "Curious"
            
        # Determine the Noun (from TF or JP, whichever is more extreme)
        if abs(tf) >= abs(jp):
            if tf <= -3: noun = "Machine"
            elif tf < 0: noun = "Tactician"
            elif tf == 0: noun = "Survivor"
            elif tf >= 3: noun = "Martyr"
            else: noun = "Guardian"
        else:
            if jp <= -3: noun = "Wildcard"
            elif jp < 0: noun = "Drifter"
            elif jp >= 3: noun = "Dictator"
            else: noun = "Architect"
            
        # Catch-all for a perfectly balanced character
        if ei == 0 and sn == 0 and tf == 0 and jp == 0:
            return "The True Neutral"
            
        return f"The {adj} {noun}"

    tab1, tab2 = st.tabs(["👤 Survivor 1", "👤 Survivor 2"])
    
    with tab1:
        col_name, col_pronoun = st.columns([3, 1])
        with col_name:
            name1 = st.text_input("Survivor 1 Name", "Mark", key="name1")
        with col_pronoun:
            pronoun1 = st.selectbox("Pronouns", ["He", "She", "They"], key="pro1")
            
        st.caption("Adjust the sliders to define their profile.")
        
        col_a, col_b = st.columns(2)
        with col_a:
            ei1 = st.slider("Reserved ⟷ Outgoing", -5, 5, 0, key="ei1")
            sn1 = st.slider("Practical ⟷ Imaginative", -5, 5, 0, key="sn1")
        with col_b:
            tf1 = st.slider("Logical ⟷ Empathetic", -5, 5, 0, key="tf1")
            jp1 = st.slider("Adaptable ⟷ Structured", -5, 5, 0, key="jp1")
            
        title1 = generate_dynamic_title(ei1, sn1, tf1, jp1)
        core_traits1 = generate_dynamic_trait(ei1, sn1, tf1, jp1)

        st.markdown(f"**Calculated Archetype:** `{title1}`")
        st.caption(f"*They are {core_traits1}*")
        
        verb1 = "are" if pronoun1 == "They" else "is"
        game_trait1 = f"{pronoun1} {verb1} {core_traits1}"
        
    with tab2:
        col_name, col_pronoun = st.columns([3, 1])
        with col_name:
            name2 = st.text_input("Survivor 2 Name", "Jonas", key="name2")
        with col_pronoun:
            pronoun2 = st.selectbox("Pronouns", ["He", "She", "They"], key="pro2")
            
        st.caption("Adjust the sliders to define their profile.")
        
        col_c, col_d = st.columns(2)
        with col_c:
            ei2 = st.slider("Reserved ⟷ Outgoing", -5, 5, 0, key="ei2")
            sn2 = st.slider("Practical ⟷ Imaginative", -5, 5, 0, key="sn2")
        with col_d:
            tf2 = st.slider("Logical ⟷ Empathetic", -5, 5, 0, key="tf2")
            jp2 = st.slider("Adaptable ⟷ Structured", -5, 5, 0, key="jp2")
            
        title2 = generate_dynamic_title(ei2, sn2, tf2, jp2)
        core_traits2 = generate_dynamic_trait(ei2, sn2, tf2, jp2)
        
        st.markdown(f"**Calculated Archetype:** `{title2}`")
        st.caption(f"*They are {core_traits2}*")
        
        verb2 = "are" if pronoun2 == "They" else "is"
        game_trait2 = f"{pronoun2} {verb2} {core_traits2}"
        
    # Start Game Execution
    if st.button("🚀 Start Survival Run", use_container_width=True):
        
        survivor_1 = {"name": name1, "skills": {"scavenge": 4, "combat": 4}, "trait": game_trait1}
        survivor_2 = {"name": name2, "skills": {"scavenge": 4, "combat": 4}, "trait": game_trait2}
        
        st.session_state.game_state = {
            "day": 1,
            "resources": {"food": 10, "wood": 5},
            "inventory": [],
            "survivors": [
                {**survivor_1, "hp": 100, "assigned_area": "Idle"},
                {**survivor_2, "hp": 100, "assigned_area": "Idle"}
            ]
        }
        
        with st.spinner("Generating world and landing survivors..."):
            intro_text = llm_engine.generate_intro_narrative(
                st.session_state.game_state["survivors"], 
                scenario_data
            )
            st.session_state.narrative_log = [intro_text]
        
        st.session_state.game_started = True
        st.rerun()

    st.stop()

state = st.session_state.game_state

# ==========================================
# 2. SIDEBAR: SCROLLING HISTORY LOG
# ==========================================
st.sidebar.header("📜 Full Survival Log")
with st.sidebar.container(height=650, border=False):
    for entry in reversed(st.session_state.narrative_log):
        st.markdown(f"• {entry}")
        st.markdown("---")

st.sidebar.divider()
if st.sidebar.button("🔄 Abandon Run / Restart", use_container_width=True):
    st.session_state.clear()
    st.rerun()

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
res_items = list(state["resources"].items())

# Create wrapping rows of 4 columns to support infinite resource types
cols_per_row = 4
for i in range(0, len(res_items), cols_per_row):
    row_cols = st.columns(cols_per_row)
    for j, (res, amount) in enumerate(res_items[i:i+cols_per_row]):
        row_cols[j].metric(label=res.capitalize(), value=amount)

st.write("")

living_survivors = [s for s in state["survivors"] if s.get("hp", 0) > 0]
food_needed = len(living_survivors)
current_food = state["resources"].get("food", 0)

if food_needed > 0:
    if current_food < food_needed:
        st.warning(f"⚠️ **STARVATION RISK:** The camp requires **{food_needed} Food** to survive the night, but only has **{current_food}**. Active survivors will lose 15 HP if you proceed!")
    else:
        st.info(f"🍲 **Daily Upkeep:** Your camp will consume **{food_needed} Food** at the end of this day.")

st.divider()

# ==========================================
# 4. MAIN LAYOUT & GAME OVER CHECK
# ==========================================
# Check if anyone is still alive using your existing backend logic
is_alive = game_logic.check_any_survivor_alive(state)
has_won = "Distress Beacon" in state.get("inventory", [])

if has_won:
    st.balloons()
    st.success("🎉 **VICTORY!** - You successfully crafted and activated the Distress Beacon. A rescue vessel has spotted your signal. You survived the Isle of Code!")
    
    if st.button("Play Again", use_container_width=True):
        st.session_state.clear()
        st.rerun()

elif not is_alive:
    st.markdown("---")
    st.error("💀 **GAME OVER** - The camp has fallen silent. All survivors have perished.")
    
    # Let the player easily restart without refreshing the browser
    if st.button("Restart Game", use_container_width=True):
        st.session_state.clear()
        st.rerun()

else:
    # --- The game continues! Show the normal controls ---
    left_col, mid_col, right_col = st.columns([1, 1.2, 1.2], gap="large")

    # ==========================================
    # LEFT COLUMN: SURVIVOR STATUS
    # ==========================================
    with left_col:
        st.subheader("🏕️ Survivor Roster")
        with st.container(border=True):
            total_survivors = len(state["survivors"])
            
            for i, survivor in enumerate(state["survivors"]):
                if survivor["hp"] <= 0:
                    st.markdown(f"💀 ~~**{survivor['name']}**~~ `[DEAD]`")
                else:
                    st.markdown(f"👤 **{survivor['name']}** — `{survivor['hp']}/100 HP`")
                    st.progress(survivor["hp"] / 100)
                    st.caption(f"*{survivor.get('trait', 'A standard survivor.')}*")

                if i < total_survivors - 1:
                    st.divider()

        if "Herbal Salve" in state.get("inventory", []):
            st.markdown("---")
            st.subheader("🎒 Use Items")
            with st.container(border=True):
                target_name = st.selectbox(
                    "Apply Herbal Salve to:", 
                    [s["name"] for s in state["survivors"] if s["hp"] > 0], 
                    key="salve_target"
                )
                if st.button("Heal 5 HP (Consume Salve)", use_container_width=True):
                    # Remove it from inventory
                    state["inventory"].remove("Herbal Salve")
                    # Find the survivor and apply the +5 HP heal
                    for i, s in enumerate(state["survivors"]):
                        if s["name"] == target_name:
                            state["survivors"][i] = game_logic.add_survivor_hp(s, 5)
                            break
                    st.session_state.game_state = state
                    st.rerun()

    # ==========================================
    # MIDDLE COLUMN: CONTROLS & TABS
    # ==========================================
    with mid_col:
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
                    if survivor["hp"] <= 0:
                        continue
                    else:
                        st.markdown(f"**{survivor['name']}**")
                
                with col_b:
                    if survivor["hp"] <= 0:
                        continue
                    else:
                        current_area_index = available_areas.index(survivor["assigned_area"]) if survivor["assigned_area"] in available_areas else 0

                        def format_area_label(area_key):
                            if area_key in areas_data:
                                res_list = areas_data[area_key].get("primary_resources", [])
                                res_str = ", ".join(res_list).title()
                                return f"{areas_data[area_key].get('name', area_key)} (Loot: {res_str})"
                            return area_key
                        
                        selected_area = st.selectbox(
                            "Assign task:",
                            options=available_areas,
                            index=current_area_index,
                            key=f"area_{i}",
                            label_visibility="collapsed",
                            format_func=format_area_label
                        )
                
                updated_survivor = survivor.copy()
                updated_survivor["assigned_area"] = selected_area
                updated_survivors.append(updated_survivor)
                st.markdown("---")

            state["survivors"] = updated_survivors

            if st.button("🚀 Proceed Day (Execute Assignments)", use_container_width=True):
                new_resources = state["resources"].copy()
                narrative_summaries = []
                
                # --- 1. Random Event ---
                living_survivors = [s for s in state["survivors"] if s["hp"] > 0]
                outcome = llm_engine.generate_daily_event(
                    state["day"], 
                    scenario_data, 
                    living_survivors,
                    valid_resources
                )
                
                # Apply the generated math
                raw_res_gained = outcome.get("resources_gained", {})
                res_gained = {}
                
                for res, amt in raw_res_gained.items():
                    try:
                        safe_amt = int(amt)
                        res_gained[res] = min(max(safe_amt, -5), 4)
                    except (ValueError, TypeError):
                        continue
                
                raw_hp_change = outcome.get("hp_change", 0)
                hp_change = min(max(raw_hp_change, -10), 0)

                if hp_change < 0 and "Spear" in state.get("inventory", []):
                    hp_change = min(0, hp_change + 1)
                    state["inventory"].remove("Spear")
                    narrative_summaries.append("**⚠️ Weapon Destroyed**: A Spear snapped in half fending off the danger! \n\n`[-1 Spear, Damage Mitigated]`")

                if hp_change < 0:
                    for active_survivor in living_survivors:
                        for i, s in enumerate(state["survivors"]):
                            if s["name"] == active_survivor["name"]:
                                state["survivors"][i].update(game_logic.consume_survivor_hp(s, abs(hp_change)))
                                break
                
                # Build stat tags for the event (e.g., [+5 food])
                e_stats = [f"+{amt} {res}" if amt > 0 else f"{amt} {res}" for res, amt in res_gained.items() if amt != 0]
                if hp_change < 0:
                    e_stats.append(f"{hp_change} HP")

                e_stat_str = f"\n\n`[{', '.join(e_stats)}]`" if e_stats else ""
                
                # Use blockquotes (>) to make the event stand out from the survivor logs
                narrative_summaries.append(f"**🌟 Event: {outcome.get('event_title', 'Update')}**\n> {outcome.get('narrative', '')}{e_stat_str}")
                
                # --- 2. Resolve Survivor Actions ---
                for survivor in living_survivors:
                    area_name = survivor["assigned_area"]
                    
                    if area_name == "Camp (Rest)":
                        survivor.update(game_logic.full_rest_survivor(survivor))
                        
                        bonus = 0
                        if "Sturdy Shelter" in state.get("inventory", []):
                            survivor.update(game_logic.add_survivor_hp(survivor, 5))
                            bonus = 5
                            
                        narrative_summaries.append(f"**{survivor['name']}**: \"I rested at camp and recovered some health.\" `[+{20 + bonus} HP]`")
                    
                    elif area_name in areas_data:
                        # Energy checks are gone. They just explore!
                        outcome = llm_engine.resolve_dynamic_exploration(
                            survivor["name"], 
                            survivor.get("trait", "A standard survivor."), 
                            areas_data[area_name]
                        )
                        
                        res_gained = outcome.get("resources_gained", {})
                        new_resources = game_logic.add_resources(new_resources, res_gained)

                        raw_hp_change = outcome.get("hp_change", 0)
                        hp_change = min(max(raw_hp_change, -10), 0)

                        if hp_change < 0 and "Spear" in state.get("inventory", []):
                            hp_change = min(0, hp_change + 1)
                            state["inventory"].remove("Spear")
                            narrative_summaries.append("**⚠️ Weapon Destroyed**: A Spear snapped in half fending off the danger! \n\n`[-1 Spear, Damage Mitigated]`")
                        
                        if hp_change < 0:
                            survivor.update(game_logic.consume_survivor_hp(survivor, abs(hp_change)))
                            
                        s_stats = [f"+{amt} {res}" for res, amt in res_gained.items() if amt > 0]
                        if hp_change < 0:
                            s_stats.append(f"{hp_change} HP")
                            
                        s_stat_str = f"\n\n`[{', '.join(s_stats)}]`" if s_stats else ""
                        narrative_summaries.append(f"**{survivor['name']}**: \"{outcome.get('narrative', f'I explored {area_name}.')}\"{s_stat_str}")
                    else:
                        narrative_summaries.append(f"**{survivor['name']}**: \"I remained idle at camp today.\"")

                # --- 3. Daily Food Consumption (Starvation Mechanic) ---
                living_survivors = [s for s in state["survivors"] if s["hp"] > 0]
                food_needed = len(living_survivors)
                
                if new_resources.get("food", 0) >= food_needed:
                    new_resources["food"] -= food_needed
                    narrative_summaries.append(f"**Camp Logistics**: The group ate their daily rations. \n\n`[-{food_needed} food]`")
                else:
                    new_resources["food"] = 0
                    for survivor in living_survivors:
                        survivor.update(game_logic.consume_survivor_hp(survivor, 15)) # Starvation penalty
                    narrative_summaries.append(f"**⚠️ STARVATION**: There was not enough food! Everyone goes hungry and grows weaker. \n\n`[-15 HP to all]`")

                camp_inventory = state.get("inventory", [])
                
                if "Water Purifier" in camp_inventory:
                    new_resources["water"] = new_resources.get("water", 0) + 1
                    narrative_summaries.append("**💧 Purifier**: The Water Purifier filtered some fresh water. \n\n`[+1 water]`")
                
                if "Campfire" in camp_inventory:
                    for survivor in living_survivors:
                        for i, s in enumerate(state["survivors"]):
                            if s["name"] == survivor["name"]:
                                state["survivors"][i] = game_logic.add_survivor_hp(s, 1)
                                break
                    narrative_summaries.append("**🔥 Campfire**: The warmth of the fire healed everyone slightly overnight. \n\n`[+1 HP to all]`")
                
                # --- 4. Update State & Log ---
                state["resources"] = new_resources
                state = game_logic.advance_day(state)
                st.session_state.game_state = state
                
                daily_log = "\n\n---\n\n".join(narrative_summaries)
                st.session_state.narrative_log.append(f"Day {state['day'] - 1}: \n\n{daily_log}")
                st.rerun()

        # --- TAB 2: CUSTOM ACTION ---
        with tab_custom:
            st.caption("Type a free-form action for the survivors.")
            custom_action_input = st.text_input("What do you want the survivors to do?", placeholder="e.g., Build a signal flare")

            if st.button("Execute Custom Action", use_container_width=True):
                if custom_action_input:
                    living_survivors = [s for s in state["survivors"] if s["hp"] > 0]

                    if living_survivors:
                        new_resources = state["resources"].copy()
                        narrative_summaries = []
                        
                        # 1. Loop through ALL conscious survivors
                        for survivor in living_survivors:
                            
                            # Ask the LLM to resolve the custom action dynamically for this specific survivor
                            outcome = llm_engine.resolve_custom_action(
                                survivor["name"],
                                survivor.get("trait", "A standard survivor."),
                                custom_action_input,
                                scenario_data,
                                living_survivors,
                                valid_resources
                            )
                            
                            # Apply the generated math
                            raw_res_gained = outcome.get("resources_gained", {})
                            res_gained = {}
                            
                            for res, amt in raw_res_gained.items():
                                try:
                                    safe_amt = int(amt)
                                    res_gained[res] = min(max(safe_amt, -10), 10)
                                except (ValueError, TypeError):
                                    continue

                            new_resources = game_logic.add_resources(new_resources, res_gained)

                            hp_change = outcome.get("hp_change", 0)
                            if hp_change < 0:
                                for i, s in enumerate(state["survivors"]):
                                    if s["name"] == survivor["name"]:
                                        state["survivors"][i].update(game_logic.consume_survivor_hp(s, abs(hp_change)))
                                        break
                            
                            # Build the stat tags (e.g., [+2 wood, -5 HP])
                            s_stats = [f"+{amt} {res}" for res, amt in res_gained.items() if amt > 0]
                            if hp_change < 0:
                                s_stats.append(f"{hp_change} HP")
                            s_stat_str = f"\n\n`[{', '.join(s_stats)}]`" if s_stats else ""
                            
                            # Format the custom narrative and append to the list
                            narrative_summaries.append(f"**{survivor['name']}**: \"{outcome.get('narrative', 'I tried, but failed.')}\"{s_stat_str}")
                        
                        # --- 2. Daily Food Consumption (Starvation Mechanic) ---
                        food_needed = len(living_survivors)
                        
                        if new_resources.get("food", 0) >= food_needed:
                            new_resources["food"] -= food_needed
                            narrative_summaries.append(f"**Camp Logistics**: The group ate their daily rations. \n\n`[-{food_needed} food]`")
                        else:
                            new_resources["food"] = 0
                            for survivor in living_survivors:
                                for i, s in enumerate(state["survivors"]):
                                    if s["name"] == survivor["name"]:
                                        state["survivors"][i].update(game_logic.consume_survivor_hp(s, 15))
                                        break
                            narrative_summaries.append(f"**⚠️ STARVATION**: There was not enough food! Everyone goes hungry and grows weaker. \n\n`[-15 HP to all]`")

                        camp_inventory = state.get("inventory", [])
                
                        if "Water Purifier" in camp_inventory:
                            new_resources["water"] = new_resources.get("water", 0) + 1
                            narrative_summaries.append("**💧 Purifier**: The Water Purifier filtered some fresh water. \n\n`[+1 water]`")
                        
                        if "Campfire" in camp_inventory:
                            for survivor in living_survivors:
                                for i, s in enumerate(state["survivors"]):
                                    if s["name"] == survivor["name"]:
                                        state["survivors"][i] = game_logic.add_survivor_hp(s, 1)
                                        break
                            narrative_summaries.append("**🔥 Campfire**: The warmth of the fire healed everyone slightly overnight. \n\n`[+1 HP to all]`")
                        
                        # --- 3. Update State & Log ---
                        state["resources"] = new_resources
                        state = game_logic.advance_day(state)
                        st.session_state.game_state = state
                        
                        # Combine all individual narratives with a separator
                        daily_log = "\n\n---\n\n".join(narrative_summaries)

                        clean_action = outcome.get("interpreted_action", custom_action_input.capitalize())
                        action_header = f"🎯 **Objective:** *\"{clean_action}\"*"
                        
                        st.session_state.narrative_log.append(f"Day {state['day'] - 1}: \n\n{action_header}\n\n---\n\n{daily_log}")
                        st.rerun()
                    else:
                        st.warning("There are no conscious survivors left to perform this action!")
                else:
                    st.warning("Please type an action first.")

        # --- TAB 3: CRAFTING & INVENTORY ---
        with tab_craft:
            CRAFTING_RECIPES = game_data.get("crafting", {})

            current_inventory = state.get("inventory", [])
            st.markdown(f"**Current Inventory:** {', '.join(current_inventory) if current_inventory else 'Empty'}")
            st.divider()

            item_to_craft = st.selectbox(
                "Select item to craft:", 
                options=list(CRAFTING_RECIPES.keys()),
                key=f"crafting_dropdown_{state['day']}" 
            )

            if item_to_craft:
                recipe_data = CRAFTING_RECIPES[item_to_craft]
                cost = recipe_data.get("cost", {})
                effect_desc = recipe_data.get("effect", "No known effect.")

                cost_str = ", ".join([f"{amount} {res.capitalize()}" for res, amount in cost.items()])

                st.markdown(f"**Effect:** {effect_desc}")
                st.caption(f"**Cost:** {cost_str}")

                if st.button(f"Craft {item_to_craft}", use_container_width=True):
                    if game_logic.has_sufficient_resources(state["resources"], cost):
                        # 1. Deduct cost and add item to inventory
                        state = game_logic.craft_item(state, cost, item_to_craft)
                        
                        living_survivors = [s for s in state["survivors"] if s["hp"] > 0]
                        new_resources = state["resources"].copy()
                        narrative_summaries = []
                        
                        # 2. Generate the collaborative group crafting story
                        group_narrative = llm_engine.generate_crafting_narrative(living_survivors, item_to_craft)
                        narrative_summaries.append(f"**🔨 Group Project: {item_to_craft}**\n> {group_narrative}")
                        
                        # 3. Crafting takes a full day: Apply Daily Food Consumption / Starvation Mechanic
                        food_needed = len(living_survivors)
                        
                        if new_resources.get("food", 0) >= food_needed:
                            new_resources["food"] -= food_needed
                            narrative_summaries.append(f"**Camp Logistics**: While working hard on the project, the group ate their daily rations. \n\n`[-{food_needed} food]`")
                        else:
                            new_resources["food"] = 0
                            for survivor in living_survivors:
                                for i, s in enumerate(state["survivors"]):
                                    if s["name"] == survivor["name"]:
                                        state["survivors"][i].update(game_logic.consume_survivor_hp(s, 15))
                                        break
                            narrative_summaries.append(f"**⚠️ STARVATION**: Working on an empty stomach! Everyone grows weaker. \n\n`[-15 HP to all]`")

                        camp_inventory = state.get("inventory", [])
                
                        if "Water Purifier" in camp_inventory:
                            new_resources["water"] = new_resources.get("water", 0) + 1
                            narrative_summaries.append("**💧 Purifier**: The Water Purifier filtered some fresh water. \n\n`[+1 water]`")
                        
                        if "Campfire" in camp_inventory:
                            for survivor in living_survivors:
                                for i, s in enumerate(state["survivors"]):
                                    if s["name"] == survivor["name"]:
                                        state["survivors"][i] = game_logic.add_survivor_hp(s, 1)
                                        break
                            narrative_summaries.append("**🔥 Campfire**: The warmth of the fire healed everyone slightly overnight. \n\n`[+1 HP to all]`")
                        
                        # --- 4. Update State & Log ---
                        state["resources"] = new_resources
                        state = game_logic.advance_day(state)
                        st.session_state.game_state = state
                        
                        daily_log = "\n\n---\n\n".join(narrative_summaries)
                        st.session_state.narrative_log.append(f"Day {state['day'] - 1}: \n\n{daily_log}")
                        st.rerun()
                    else:
                        st.warning(f"Not enough resources to craft {item_to_craft}!")

    # ==========================================
    # RIGHT COLUMN: LATEST REPORT
    # ==========================================
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