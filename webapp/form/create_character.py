import streamlit as st
import yaml


def form_create_character(DATA_DIR):
    #initialize some variables into the session state
    st.title("➕ Create or Edit a Character")
    if not "race" in st.session_state: st.session_state.race = {}
    if not "clas" in st.session_state: st.session_state.clas = {}
    if not "bkrd" in st.session_state: st.session_state.bkrd = {}
    if not "race_index" in st.session_state: st.session_state.race_index = 0
    if not "clas_index" in st.session_state: st.session_state.clas_index = 0
    if not "back_index" in st.session_state: st.session_state.back_index = 0
    stats = ["cha", "con", "dex", "int", "str", "wis"]


    #################################################################
    # N a m e
    st.subheader("Character Name")
    st.session_state.name = st.text_input("Character Name",label_visibility="collapsed")

    rcb_col = st.columns([1,1,1])

    #################################################################
    # R a c e
    with rcb_col[0]:
        st.subheader("Race")
        race_default = "human"
        st.session_state.race_index = sorted(st.session_state.races.keys()).\
                index(st.session_state.character.get("race",race_default))

        st.selectbox(
            "Race", 
            sorted(st.session_state.races.keys()),
            key = "race_name",
            label_visibility="collapsed",
            index = st.session_state.race_index)

    #################################################################
    # C l a s s
    with rcb_col[1]:
        st.subheader("Class")
        clas_default = "barbarian"
        st.session_state.clas_index = sorted(st.session_state.classes.keys()).\
                index(st.session_state.character.get("class",clas_default))


        st.selectbox(
            "Class", 
            sorted(st.session_state.classes.keys()),
            key = "clas_name",
            label_visibility="collapsed",
            index = st.session_state.clas_index)

    #################################################################
    # B a c k g r o u n d
    with rcb_col[2]:
        st.subheader("Background")
        back_default = ""
        st.session_state.back_index
        #st.session_state.back_index = sorted(st.session_state.backgrounds.keys()).\
        #        index(st.session_state.character.get("background",back_default))


        st.selectbox(
            "Class", 
            #sorted(st.session_state.backgrounds.keys()),
            [],
            key = "back_name",
            label_visibility="collapsed",
            index = st.session_state.back_index)
        
    #################################################################
    # S t a t s
    st.session_state.val_race = st.session_state.races.get(st.session_state.race_name,{}).get("stats",{})
    st.session_state.val_clas = st.session_state.clas.get("stats",{})

    if st.session_state.race_name == "half-elf":
        st.session_state.val_play_max = 74
    else:
        st.session_state.val_play_max = 72
    print("Max allowable")
    print(st.session_state.val_play_max)

    st.subheader("Stats")
    stat_col = st.columns([1,1,1,1,1])
    stat_col[0].markdown("")
    stat_col[1].markdown("**Race**")
    stat_col[2].markdown("**Class**")
    stat_col[3].markdown("**Player** (max " + str(st.session_state.val_play_max) + ")")
    stat_col[4].markdown("**Total**")

    for stat in stats:
        stat_col = st.columns([1,1,1,1,1])
        stat_col[0].markdown(f"**{stat.upper()}**")
        stat_col[1].markdown(f"**{st.session_state.val_race.get(stat,0)}**")
        stat_col[2].markdown(f"**{st.session_state.val_clas.get(stat,0)}**")

        with stat_col[3]:
            st.number_input(
                stat + " player value", 
                min_value=8, 
                max_value=18,
                value=8,
                key=stat,
                label_visibility="collapsed")
        stat_col[4].markdown(f"**{st.session_state.val_race.get(stat,0) + st.session_state.val_clas.get(stat,0) + st.session_state[stat]}**")

    total = 0
    for stat in stats:
        if stat in st.session_state: total += st.session_state[stat]
    if total > st.session_state.val_play_max:
        st.markdown(f"**W A R N I N G!!!**")
        st.markdown(f"**You've used {total} of {st.session_state.val_play_max} points.**")
        st.markdown(f"Turn back! You've exceded your max allowable points!")
        st.markdown(f"**W A R N I N G!!!**")
    else:
        st.markdown(f"**You've used {total} of {st.session_state.val_play_max} points.**")

    # Pre-fill with existing values or defaults
    alignment = st.text_input(
        "Alignment", 
        value=st.session_state.character.get("alignment") if \
            st.session_state.character else "")

    # Equipment
    st.subheader("🧤 Equipment Slots")
    equipment = {}
    slots = ["head", "armor", "feet", "back", "hand-left", "hand-hand", "neck", "ring"]
    for slot in slots:
        equipment[slot] = st.text_input(slot.capitalize(), 
                                        value=st.session_state.character.get("equipment", {}).get(slot, "none") if st.session_state.character else "none")

    # Inventory
    st.subheader("🎒 Inventory Items")
    inventory_input = st.text_area("List items separated by commas",
                                value=", ".join(st.session_state.character.get("inventory", [])) if st.session_state.character else "")
    inventory = [item.strip() for item in inventory_input.split(",") if item.strip()]

    # Spells
    st.subheader("🪄 Spells")
    spells_input = st.text_area("List spells separated by commas",
                                value=", ".join(st.session_state.character.get("spells", [])) if st.session_state.character else "")
    spells = [spell.strip() for spell in spells_input.split(",") if spell.strip()]

    if st.button("💾 Save Character"):
        st.session_state.character = {
            "name": st.session_state.name,
            "classtype": st.session_state.clas_name,
            "race": st.session_state.race_name,
            "background": st.session_state.back_name,
            "alignment": alignment,
            "level": 1,
            "stats": stats,
            "equipment": equipment,
            "inventory": inventory,
            "spells": spells
        }

        existing = next((c for c in st.session_state.characters["characters"] if c["name"].lower() == st.session_state.name.lower()), None)

        if existing:
            # Replace the existing character
            st.session_state.characters["characters"] = [st.session_state.character if c["name"].lower() == st.session_state.name.lower() else c for c in st.session_state.characters["characters"]]
            st.success(f"✅ Character '{st.session_state.name}' updated.")
        else:
            st.session_state.characters["characters"].append(st.session_state.character)
            st.success(f"✅ New character '{st.session_state.name}' created.")

        with open(DATA_DIR + "characters.yaml", "w", encoding="utf-8") as f:
            yaml.dump(st.session_state.characters, f, allow_unicode=True)
        
        st.session_state.display_form = "main"
        st.experimental_rerun()