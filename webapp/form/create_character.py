import streamlit as st
import yaml


def form_create_character(DATA_DIR):
    #initialize some variables into the session state
    st.title("➕ Create or Edit a Character")
    abilities = ["cha", "con", "dex", "int", "str", "wis"]

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
        st.session_state.back_index = None

        st.selectbox(
            "Class", 
            #sorted(st.session_state.backgrounds.keys()),
            [],
            key = "back_name",
            label_visibility="collapsed",
            index = st.session_state.back_index)

    #################################################################
    # A b i l i t i e s
    st.session_state.val_race = st.session_state.races.get(st.session_state.race_name,{}).get("abilities",{})
    st.session_state.val_clas = st.session_state.classes.get(st.session_state.clas_name,{}).get("abilities",{})

    if st.session_state.race_name == "half-elf":
        st.session_state.val_play_max = 74
    else:
        st.session_state.val_play_max = 72

    primary_abilities = st.session_state.classes[st.session_state.clas_name]['primary ability']
    saving_abilities = st.session_state.classes[st.session_state.clas_name]['saving throw proficiencies']

    st.subheader(f"Abilities ({' '.join(primary_abilities).upper()} | {' '.join(saving_abilities).upper()})",
                 help="(primary | saving)")

    abi_col = st.columns([1,1,1,1,1])
    abi_col[0].markdown("")
    abi_col[1].markdown("**Player** (max " + str(st.session_state.val_play_max) + ")")
    abi_col[2].markdown("**Race**")
    abi_col[3].markdown("**Class**")
    abi_col[4].markdown("**Total**")

    for abi in abilities:
        abi_col = st.columns([1,1,1,1,1])
        abi_col[0].markdown(f"**{abi.upper()}**")
        with abi_col[1]:
            st.number_input(
                abi + " player value", 
                min_value=8, 
                max_value=18,
                value=8,
                key=abi,
                label_visibility="collapsed")
        abi_col[2].markdown(f"**{st.session_state.val_race.get(abi,0)}**")
        abi_col[3].markdown(f"**{st.session_state.val_clas.get(abi,0)}**")
        abi_col[4].markdown(f"**{st.session_state.val_race.get(abi,0) + st.session_state.val_clas.get(abi,0) + st.session_state[abi]}**")
    total = 0
    for abi in abilities:
        if abi in st.session_state: total += st.session_state[abi]
    abi_col[1].markdown(f"**{total} of {st.session_state.val_play_max}**")

    if total > st.session_state.val_play_max:
        st.markdown(f"**W A R N I N G!!!**")
        st.markdown(f"Turn back! You've exceded your max allowable points!")
        st.markdown(f"**W A R N I N G!!!**")

    #################################################################
    # B a s i c   S k i l l s
    ski_col = st.columns([1,1,1])
    st.subheader("Skills")
    

    #################################################################
    # S p e l l s   a n d   a b i l i t i e s


    #################################################################
    # I n v e n t o r y / E q u i p m e n t

    #################################################################
    # D e s c r i p t i o n
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
            "abilities": abilities,
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