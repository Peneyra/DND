import streamlit as st
from streamlit_autorefresh import st_autorefresh
import yaml
import os

def form_main(characters,world,npcs,initiative,char_names,DATA_DIR):
    st.title("🧙 Player Dashboard")
    st_autorefresh(interval=1000,key="refresh")

    if initiative["initiative"]["visible"]:
        st.subheader("⚔️ Initiative Tracker")
        st.write(" || ".join(f"{v}" for v in initiative["initiative"]["order"]))

    col1, col2, col3 = st.columns([3,1,1])

    # Select a character
    with col1:
        selected_name = st.selectbox(
            "Choose your character",
            char_names,
            index=char_names.index(st.session_state.character["name"]) if st.session_state.character["name"] in char_names else 0,
            key="character_select"
        )

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
    
    character = next(c for c in characters["characters"] if c["name"] == selected_name)
    if st.session_state.character != character:
        st.session_state.character = character
    st.subheader(f"🎭 {character['name']} the {character['race'].title()} {character['classtype'].title()}")
    # Level
    st.write("Level: ", character["level"])
    # Background
    st.write("Background: ", character["background"])
    # Alignment
    st.write("Alignment: ", character["alignment"])
    # Stats
    with st.expander("Stats: "):
        st.text("\n".join(f"- {k.upper()}: {v}" for k, v in sorted(character["stats"].items())))
    # Spells
    with st.expander("Spells: "):
        st.text("\n".join(f"- {v.title()}" for v in sorted(character["spells"])))
    # Equipment
    with st.expander("Equipment: "):
        st.text("\n".join(f"- {k.title()}: {v.title()}" for k, v in sorted(character["equipment"].items())))
    # Inventory
    with st.expander("Inventory: "):
        st.text("\n".join(f"- {v.title()}" for v in sorted(character["inventory"])))

    st.subheader("📍 Current Location")
    location = world.get("current_location", "Unknown")
    desc = world.get("locations", {}).get(location, {}).get("description", "No details")
    st.markdown(f"**{location}**\n\n{desc}")

    for npc in npcs.get("npcs", []):
        with st.expander(npc["name"]):
            st.write(npc["description"])

    st.subheader("📝 Personal Notes")
    notes = st.text_area("Write your notes here", height=150)