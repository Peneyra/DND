
import streamlit as st
import yaml
import os
import time
from form.create_character import form_create_character
from form.main import form_main
from form.dm import form_dm

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/data/"

# ingest the yaml files to the local browser if they have been updated
if "update" not in st.session_state: st.session_state.update = time.time()
if os.path.getmtime(DATA_DIR + 'characters.yaml') > st.session_state.update:
    st.session_state.characters = load_yaml(DATA_DIR + 'characters.yaml')["characters"]
if "character" not in st.session_state:
    st.session_state.character = sorted(list(st.session_state.characters.keys()))[0]
elif os.path.getmtime(DATA_DIR + 'characters.yaml') > st.session_state.update:
    st.session_state.character = st.session_state.characters[st.session_state.character["name"]]
if os.path.getmtime(DATA_DIR + 'characters.yaml') > st.session_state.update:
    st.session_state.characters = load_yaml(DATA_DIR + 'characters.yaml')["characters"]
if os.path.getmtime(DATA_DIR + 'worldmap.yaml') > st.session_state.update:
    st.session_state.world = load_yaml(DATA_DIR + 'worldmap.yaml')
if os.path.getmtime(DATA_DIR + 'npcs.yaml') > st.session_state.update:
    st.session_state.npcs = load_yaml(DATA_DIR + 'npcs.yaml')
if os.path.getmtime(DATA_DIR + 'initiative.yaml') > st.session_state.update:
    st.session_state.initiative = load_yaml(DATA_DIR + 'initiative.yaml')["initiative"]
st.session_state.update = time.time()

if "display_form" not in st.session_state:
    st.session_state.display_form = "main"

# open the correct form
if st.session_state.display_form == "create_character":
    form_create_character(DATA_DIR)
elif st.session_state.display_form == "DM":
    form_dm(DATA_DIR)
elif st.session_state.display_form == "main":
    form_main(DATA_DIR)