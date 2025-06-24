import streamlit as st
import yaml

def form_create_character(characters, DATA_DIR):

    with open(DATA_DIR + "character_creation.yaml") as f:
        create_char = yaml.safe_load(f)
    races = sorted(list(create_char["races"].keys()))
    race = ""
    clas = ""


    st.title("➕ Create or Edit a Character")

    #################################################################
    # N a m e
    st.subheader("Character Name")
    name = st.text_input("Character Name",label_visibility="collapsed")
    # Auto-fill if character already exists
    character = next(
        (c for c in characters["characters"] if c["name"] == name), 
        None
        )


    #################################################################
    # R a c e
    try:
        race_index = races.index(character.get("race"))
    except:
        try:
            race_index = races.index("human")
        except:
            race_index = 0
    st.subheader("Race")
    race = st.selectbox(
        "Race", 
        races,
        index=race_index,
        label_visibility="collapsed")

    #################################################################
    # S t a t s
    if race == "half-elf":
        play_max = 74
    else:
        play_max = 72

    st.subheader("Stats")
    stats = ["cha", "con", "dex", "int", "str", "wis"]
    stat_col = st.columns([1,1,1,1,1])
    stat_col[0].markdown("")
    stat_col[1].markdown("**Race**")
    stat_col[2].markdown("**Class**")
    stat_col[3].markdown("**Player** (max " + str(play_max) + ")")
    stat_col[4].markdown("**Total**")
    race_val = create_char.get("races",{}).get(race, {}).get("stats",{})
    clas_val = create_char.get("classes",{}).get(clas, {}).get("stats",{})
    play_val = {}

    for stat in stats:
        stat_col = st.columns([1,1,1,1,1])
        stat_col[0].markdown(f"**{stat.upper()}**")

        race_val[stat] = race_val.get(stat,0)
        stat_col[1].markdown(f"**{race_val[stat]}**")

        clas_val[stat] = clas_val.get(stat,0)
        stat_col[2].markdown(f"**{clas_val[stat]}**")

        play_val[stat] = play_val.get(stat,8)
        with stat_col[3]:
            play_val[stat] = st.number_input(
                stat + " player value", 
                min_value=8, 
                max_value=18,
                value=8,
                key=stat + "_play",
                label_visibility="collapsed")
            
        total = race_val[stat] + clas_val[stat] + play_val[stat]
        stat_col[4].markdown(f"**{total}**")

    # Pre-fill with existing values or defaults
    classtype = st.text_input("Class", value=character.get("classtype") if character else "")
    background = st.text_input("Background", value=character.get("background") if character else "")
    alignment = st.text_input("Alignment", value=character.get("alignment") if character else "")
    level = st.number_input("Level", min_value=1, value=character.get("level", 1) if character else 1)

    # Equipment
    st.subheader("🧤 Equipment Slots")
    equipment = {}
    slots = ["head", "armor", "feet", "back", "hand-left", "hand-hand", "neck", "ring"]
    for slot in slots:
        equipment[slot] = st.text_input(slot.capitalize(), value=character.get("equipment", {}).get(slot, "none") if character else "none")

    # Inventory
    st.subheader("🎒 Inventory Items")
    inventory_input = st.text_area("List items separated by commas",
                                value=", ".join(character.get("inventory", [])) if character else "")
    inventory = [item.strip() for item in inventory_input.split(",") if item.strip()]

    # Spells
    st.subheader("🪄 Spells")
    spells_input = st.text_area("List spells separated by commas",
                                value=", ".join(character.get("spells", [])) if character else "")
    spells = [spell.strip() for spell in spells_input.split(",") if spell.strip()]
    if st.button("💾 Save Character"):
        character = {
            "name": name,
            "classtype": classtype,
            "race": race,
            "background": background,
            "alignment": alignment,
            "level": level,
            "stats": stats,
            "equipment": equipment,
            "inventory": inventory,
            "spells": spells
        }

        existing = next((c for c in characters["characters"] if c["name"].lower() == name.lower()), None)

        if existing:
            # Replace the existing character
            characters["characters"] = [character if c["name"].lower() == name.lower() else c for c in characters["characters"]]
            st.success(f"✅ Character '{name}' updated.")
        else:
            characters["characters"].append(character)
            st.success(f"✅ New character '{name}' created.")

        with open(DATA_DIR + "characters.yaml", "w", encoding="utf-8") as f:
            yaml.dump(characters, f, allow_unicode=True)
        
        st.session_state.display_form = "main"
        st.experimental_rerun()