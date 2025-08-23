import streamlit as st
from streamlit_autorefresh import st_autorefresh

def form_main(DATA_DIR):
    st_autorefresh(interval=3000,key="refresh")
    sess = st.session_state
    char = sess.character

    hdr_col = st.columns([1,1], vertical_alignment = 'bottom')
    with hdr_col[0]:
        st.title("🧙Character")
    with hdr_col[1]:
        char_name = st.selectbox(
            "Choose your character",
            sorted(list(char.keys())),
            index=sorted(list(sess.characters.keys())).index(char["name"]),
            key="character_select",
            label_visibility="collapsed"
        )
        char = sess.characters[char_name]

    if char == {}:
        char = next(iter(sess.characters.values()))
    if sess.initiative["visible"]:
        st.subheader("⚔️ Initiative Tracker")
        st.write(" || ".join(f"{v}" for \
                v in sess.initiative["order"]))

    but_col = st.columns([1,1,2])

    # Create a character
    with but_col[0]:
        if st.button("➕ Create New"):
            sess.display_form = "create_character"
            st.rerun()

    # Shift to DM editing form
    with but_col[1]:
        if st.button("🧠 I am the DM"):
            sess.display_form = "DM"
            st.rerun()
    print(char)
    st.subheader(f"🎭 {char['name'].title()} the {char['race'].title()} {char['class'].title()}")
    
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