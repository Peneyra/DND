
import streamlit as st
import yaml
import os
import time
from form.create_character import form_create_character
from form.main import form_main
from form.dm import form_dm
6
def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/data/"

# ingest the yaml files to the local browser if they have been updated
if "utime" not in st.session_state: st.session_state.utime = time.time()
# initialize/update characters
if not "characters" in st.session_state or os.path.getmtime(DATA_DIR + 'characters.yaml') > st.session_state.utime:
    st.session_state.characters = load_yaml(DATA_DIR + 'characters.yaml')["characters"]
# initialize/update character
if not "character" in st.session_state:
    st.session_state.character = {}
elif os.path.getmtime(DATA_DIR + 'characters.yaml') > st.session_state.utime:
    st.session_state.character = st.session_state.characters[st.session_state.character["name"]]
# initialize/update world
if not "world" in st.session_state or os.path.getmtime(DATA_DIR + 'worldmap.yaml') > st.session_state.utime:
    st.session_state.world = load_yaml(DATA_DIR + 'worldmap.yaml')
# initialize/update npcs
if not "npcs" in st.session_state or os.path.getmtime(DATA_DIR + 'npcs.yaml') > st.session_state.utime:
    st.session_state.npcs = load_yaml(DATA_DIR + 'npcs.yaml')
# initialize/update initiative
if not "initiative" in st.session_state or os.path.getmtime(DATA_DIR + 'initiative.yaml') > st.session_state.utime:
    st.session_state.initiative = load_yaml(DATA_DIR + 'initiative.yaml')["initiative"]
# initialize/update races
if not "races" in st.session_state or os.path.getmtime(DATA_DIR + 'character_creation.yaml') > st.session_state.utime:
    st.session_state.races = load_yaml(DATA_DIR + 'character_creation.yaml')["races"]
# initialize/update classses
if not "classes" in st.session_state or os.path.getmtime(DATA_DIR + 'character_creation.yaml') > st.session_state.utime:
    st.session_state.classes = load_yaml(DATA_DIR + 'character_creation.yaml')["classes"]
st.session_state.utime = time.time()

if "display_form" not in st.session_state:
    st.session_state.display_form = "create_character"

# open the correct form
if st.session_state.display_form == "create_character":
    form_create_character(DATA_DIR)
elif st.session_state.display_form == "DM":
    form_dm(DATA_DIR)
elif st.session_state.display_form == "main":
    form_main(DATA_DIR)

None