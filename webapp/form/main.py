import streamlit as st
from streamlit_autorefresh import st_autorefresh

def form_main(DATA_DIR):
    st.title("🧙 Player Dashboard")
    st_autorefresh(interval=3000,key="refresh")

    if st.session_state.character == {}:
        st.session_state.character = next(iter(st.session_state.characters.values()))
    print(st.session_state.initiative)
    if st.session_state.initiative["visible"]:
        st.subheader("⚔️ Initiative Tracker")
        st.write(" || ".join(f"{v}" for \
                v in st.session_state.initiative["order"]))

    col1, col2, col3 = st.columns([3,1,1])

    # Select a character
    with col1:
        char_name = st.selectbox(
            "Choose your character",
            sorted(list(st.session_state.characters.keys())),
            index=sorted(list(st.session_state.characters.keys())).index(st.session_state.character["name"]),
            key="character_select"
        )
        st.session_state.character = st.session_state.characters[char_name]

    # Create a character
    with col2:
        st.markdown("###")
        if st.button("➕ Create New"):
            st.session_state.display_form = "create_character"
            st.experimental_rerun()

    # Shift to DM editing form
    with col3:
        st.markdown("###")
        if st.button("🧠 I am the DM"):
            st.session_state.display_form = "DM"
            st.experimental_rerun()

    st.subheader(f"""
                🎭 {st.session_state.character['name'].title()} the
                {st.session_state.character["race"].title()}
                {st.session_state.character["class"].title()}
                """)
    
    # Level
    st.write("Level: ", st.session_state.character["level"])
    # Background
    st.write("Background: ", st.session_state.character["background"])
    # Alignment
    st.write("Alignment: ", st.session_state.character["alignment"])
    # Stats
    with st.expander("Abilities: "):
        st.text("\n".join(f"- {k.upper()}: {v}" for \
                k, v in \
                sorted(st.session_state.character["abilities"].items())))
    # Spells
    with st.expander("Spells: "):
        st.text("\n".join(f"- {v.title()}" for v in \
                sorted(st.session_state.character["spells"])))
    # Equipment
    with st.expander("Equipment: "):
        st.text("\n".join(f"- {k.title()}: {v.title()}" for \
                k, v in \
                sorted(st.session_state.character["equipment"].items())))
    # Inventory
    with st.expander("Inventory: "):
        st.text("\n".join(f"- {v.title()}" for v in \
                sorted(st.session_state.character["inventory"])))

    st.subheader("📍 Current Location")
    location = st.session_state.world.get("current_location", "Unknown")
    desc = st.session_state.world.get(
        "locations", 
        {}).get(location, {}).get("description", "No details")
    st.markdown(f"**{location}**\n\n{desc}")

    for npc in st.session_state.npcs.get("npcs", []):
        with st.expander(npc["name"]):
            st.write(npc["description"])

    st.subheader("📝 Personal Notes")
    notes = st.text_area("Write your notes here", height=150)