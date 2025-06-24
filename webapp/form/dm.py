import streamlit as st
import yaml
import os

def form_dm(DATA_DIR):
    st.title("🧠 Dungeon Master's Playground")

    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".yaml")]
    file_selected = st.selectbox("Choose something to edit", files)

    file_path = os.path.join(DATA_DIR, file_selected)

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    edited = st.text_area("📝 Edit YAML content", value=content, height=400)

    if st.button("💾 Update File"):
        try:
            yaml.safe_load(edited)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(edited)
            st.success(f"✅ {file_selected} updated successfully.")
        except yaml.YAMLError as e:
            st.error(f"❌ Invalid YAML: {e}")
        st.experimental_rerun()