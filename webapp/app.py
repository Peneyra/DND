
import streamlit as st
import yaml
import os
from form.create_character import form_create_character
from form.main import form_main
from form.dm import form_dm

def load_yaml(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/data/"
characters = load_yaml(DATA_DIR + 'characters.yaml')
char_names = sorted([c["name"] for c in characters["characters"]])
world = load_yaml(DATA_DIR + 'worldmap.yaml')
npcs = load_yaml(DATA_DIR + 'npcs.yaml')
initiative = load_yaml(DATA_DIR + 'initiative.yaml')


if "display_form" not in st.session_state:
    st.session_state.display_form = "main"
if "character" not in st.session_state:
    st.session_state.character = characters["characters"][0]
if "character" not in st.session_state:
    st.session_state.character_temp = characters["characters"][0]

if st.session_state.display_form == "create_character":
    form_create_character(characters, DATA_DIR)
elif st.session_state.display_form == "DM":
    form_dm(DATA_DIR)
elif st.session_state.display_form == "main":
    form_main(characters,world,npcs,initiative,char_names,DATA_DIR)