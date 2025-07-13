import streamlit as st
import yaml
from collections import Counter

def form_create_character(DATA_DIR):
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    form_error = False

    sess = st.session_state

    #initialize some variables into the session state
    st.title("➕ Create Character")
    abilities = ["cha", "con", "dex", "int", "str", "wis"]

    st.header("Basics", divider=True)
    #################################################################
    # N a m e
    st.subheader("Character Name")
    sess.name = st.text_input("Character Name",label_visibility="collapsed")
    rcb_col = st.columns([1,1,1])

    #################################################################
    # R a c e
    with rcb_col[0]:
        st.subheader("Race")
        race_default = "human"
        sess.race_index = sorted(sess.races.keys()).\
                index(sess.character.get("race",race_default))

        st.selectbox(
            "Race", 
            sorted(sess.races.keys()),
            key = "race_name",
            label_visibility="collapsed",
            index = sess.race_index)

    #################################################################
    # C l a s s
    with rcb_col[1]:
        st.subheader("Class")
        clas_default = "fighter"
        sess.clas_index = sorted(sess.classes.keys()).\
                index(sess.character.get("class",clas_default))

        st.selectbox(
            "Class", 
            sorted(sess.classes.keys()),
            key = "clas_name",
            label_visibility="collapsed",
            index = sess.clas_index)

    #################################################################
    # B a c k g r o u n d
    with rcb_col[2]:
        st.subheader("Background")
        back_default = ""
        sess.back_index = None

        st.selectbox(
            "Class", 
            #sorted(sess.backgrounds.keys()),
            [],
            key = "back_name",
            label_visibility="collapsed",
            index = sess.back_index)

    st.header("Stats", divider=True)
    #################################################################
    # A b i l i t i e s
    sess.val_race = sess.races.get(sess.race_name,{}).get("abilities",{})
    sess.val_clas = sess.classes.get(sess.clas_name,{}).get("abilities",{})

    # 
    if sess.race_name == "half-elf": sess.val_play_max = 74
    else: sess.val_play_max = 72

    primary_abilities = sess.classes[sess.clas_name]['primary ability']
    saving_abilities = sess.classes[sess.clas_name]['saving throw proficiencies']

    st.subheader(f"Abilities ({' '.join(primary_abilities).upper()} | {' '.join(saving_abilities).upper()})",
                 help="(primary | saving)")

    abi_col = st.columns([1,1,1,1,1])
    abi_col[0].markdown("")
    abi_col[1].markdown("**Player**")
    abi_col[2].markdown("**Race**")
    abi_col[3].markdown("**Class**")
    abi_col[4].markdown("**Total (Modifier)**")

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
        abi_col[2].markdown(f"**{sess.val_race.get(abi,0)}**")
        abi_col[3].markdown(f"**{sess.val_clas.get(abi,0)}**")
        sess[abi + "_total"] = sess.val_race.get(abi,0) + sess.val_clas.get(abi,0) + sess[abi]
        sess[abi + "_modifier"] = (sess[abi + "_total"] - 10) // 2
        abi_col[4].markdown(f"**{sess[abi + '_total']} ({sess[abi + '_modifier']})**")
    total = 0
    for abi in abilities: 
        if abi in sess: total += sess[abi]
    abi_col[1].markdown(f"**{total} of {sess.val_play_max}**")

    if total > sess.val_play_max:
        form_error = True
        st.markdown(f"**W A R N I N G!!!**")
        st.markdown(f"Turn back! You've exceded your max allowable points!")
        st.markdown(f"**W A R N I N G!!!**")
    else:
        form_error = False

    #################################################################
    # H i t   P o i n t s   /   D a m a g e
    hpd_col = st.columns([1,1])
    hit_points = 0
    hp_list = sess.classes[sess.clas_name]['levels'][1]['hit points']
    for abi, val in hp_list.items():
        if abi == 'any': hit_points += val
        else: hit_points += val * (sess[abi + "_modifier"]) 
    hpd_col[0].subheader(f"**Hit Points: {hit_points}**")

    damage_die = []
    damage_list = sess.classes[sess.clas_name]['levels'][1]['hit dice']
    for die, val in damage_list.items():
        damage_die.append(str(val) + die)
    hpd_col[1].subheader(f"**Attack Damage: {','.join(damage_die)}**")

    st.header("Skills and Spells", divider=True)
    #################################################################
    # B a s i c   S k i l l s
    st.subheader("Skills")
    if 'skills' in sess.races[sess.race_name]['proficiencies']:
        race_skills = sess.races[sess.race_name]['proficiencies']['skills']
        st.markdown(f"**{sess.races[sess.race_name]['name']} skills:**".title())
        skr_col = st.columns([1,1,1])
        k = 0
        for rs in race_skills:
            with skr_col[k]:
                st.selectbox(
                    "Race Skills",
                    sorted(rs),
                    key = "race_skills_" + str(k),
                    label_visibility = "collapsed",
                    index = k)
            k += 1
    if 'skills' in sess.classes[sess.clas_name]['proficiencies']:
        clas_skills = sess.classes[sess.clas_name]['proficiencies']['skills']
        st.markdown(f"**{sess.clas_name} skills:**".title())
        skc_col = st.columns([1,1,1,1])
        k = 0
        for cs in clas_skills:
            with skc_col[k]:
                st.selectbox(
                    "Class Skills",
                    sorted(cs),
                    key = "clas_skills_" + str(k),
                    label_visibility = "collapsed",
                    index = k)
            k += 1

    selected_skills = []
    if "race_skills_0" in sess: selected_skills.append(sess.race_skills_0)
    if "race_skills_1" in sess: selected_skills.append(sess.race_skills_1)
    if "race_skills_2" in sess: selected_skills.append(sess.race_skills_2)
    if "clas_skills_0" in sess: selected_skills.append(sess.clas_skills_0)
    if "clas_skills_1" in sess: selected_skills.append(sess.clas_skills_1)
    if "clas_skills_2" in sess: selected_skills.append(sess.clas_skills_2)
    if "clas_skills_3" in sess: selected_skills.append(sess.clas_skills_3)
    counts = Counter(selected_skills)
    skills_duplicate = [sd for sd, count in counts.items() if count > 1]

    if len(skills_duplicate) > 0:
        form_error = True
        st.markdown(f"**W A R N I N G!!!**")
        st.markdown(f"Turn back! You have duplicate skills chosen! {skills_duplicate}")
        st.markdown(f"**W A R N I N G!!!**")
    else:
        form_error = False

    #################################################################
    # C a n t r i p s   a n d   S p e l l s
    if "cantrip list" in sess.classes[sess.clas_name]['levels'][1]:
        num_cantrip = sess.classes[sess.clas_name]['levels'][1]['cantrip list']
        cantrip_book = sess.classes[sess.clas_name]['proficiencies']['spells'][0]
        st.subheader("Cantrips")
        st.markdown(f"**{sess.clas_name} cantrips:**".title())
        cal_col = st.columns([1,1,1,1])
        for k in range(num_cantrip):
            with cal_col[k]:
                st.selectbox(
                    "Cantrip",
                    sorted(cantrip_book),
                    key = "cantrip_" + str(k),
                    label_visibility = "collapsed",
                    index = k)
                
    selected_cantrips = []
    if "cantrip_0" in sess: selected_cantrips.append(sess.cantrip_0)
    if "cantrip_1" in sess: selected_cantrips.append(sess.cantrip_1)
    if "cantrip_2" in sess: selected_cantrips.append(sess.cantrip_2)
    if "cantrip_3" in sess: selected_cantrips.append(sess.cantrip_3)
    counts = Counter(selected_cantrips)
    cantrips_duplicate = [sd for sd, count in counts.items() if count > 1]

    if len(cantrips_duplicate) > 0:
        form_error = True
        st.markdown(f"**W A R N I N G!!!**")
        st.markdown(f"Turn back! You have duplicate cantrips chosen! {cantrips_duplicate}")
        st.markdown(f"**W A R N I N G!!!**")
    else:
        form_error = False

    if "spell list" in sess.classes[sess.clas_name]['levels'][1]:
        spell_list = sess.classes[sess.clas_name]['levels'][1]['spell list']
        num_spell = 0
        for abi, val in spell_list.items():
            if abi == 'any': num_spell += val
            else: num_spell += val * (sess[abi + "_modifier"]) 
        spell_book = sess.classes[sess.clas_name]['proficiencies']['spells'][1]
        st.subheader("Spells")
        st.markdown(f"**{sess.clas_name} level 1 spells:**".title())
        sp1_col = st.columns([1,1,1])
        for k in range(min(3,num_spell)):
            with sp1_col[k]:
                st.selectbox(
                    "Spells",
                    sorted(spell_book),
                    key = "spell_" + str(k),
                    label_visibility = "collapsed",
                    index = k)
        if num_spell > 3:
            sp2_col = st.columns([1,1,1])
            for k in range(3,num_spell):
                with sp2_col[k-3]:
                    st.selectbox(
                        "Spells",
                        sorted(spell_book),
                        key = "spell_" + str(k),
                        label_visibility = "collapsed",
                        index = k)
      
    selected_spells = []
    if "spell_0" in sess: selected_spells.append(sess.spell_0)
    if "spell_1" in sess: selected_spells.append(sess.spell_1)
    if "spell_2" in sess: selected_spells.append(sess.spell_2)
    if "spell_3" in sess: selected_spells.append(sess.spell_3)
    if "spell_2" in sess: selected_spells.append(sess.spell_4)
    if "spell_3" in sess: selected_spells.append(sess.spell_5)
    counts = Counter(selected_spells)
    spells_duplicate = [sd for sd, count in counts.items() if count > 1]

    if len(spells_duplicate) > 0:
        form_error = True
        st.markdown(f"**W A R N I N G!!!**")
        st.markdown(f"Turn back! You have duplicate cantrips chosen! {spells_duplicate}")
        st.markdown(f"**W A R N I N G!!!**")
    else:
        form_error = False


    st.header("Traits", divider=True)
    #################################################################
    # T r a i t s
    if 'traits' in sess.races[sess.race_name]:
        st.subheader(f"**{sess.races[sess.race_name]['name'].title()} Traits**")
        for trait, description in sess.races[sess.race_name]['traits'].items():
            st.markdown(f"**{trait.title()}**")
            st.markdown(f"{description}")
    if 'traits' in sess.classes[sess.clas_name]['levels'][1]:
        st.subheader(f"**{sess.clas_name.title()} Traits**")
        for trait, description in sess.classes[sess.clas_name]['levels'][1]['traits'].items():
            st.markdown(f"**{trait.title()}**")
            st.markdown(f"{description}")

    #################################################################
    # I n v e n t o r y / E q u i p m e n t

    #################################################################
    # D e s c r i p t i o n

    if st.button("💾 Save Character"):
        sess.character = {
            "name": sess.name,
            "classtype": sess.clas_name,
            "race": sess.race_name,
            "background": sess.back_name,
            "alignment": alignment,
            "level": 1,
            "abilities": abilities,
            "equipment": equipment,
            "inventory": inventory,
            "spells": spells
        }

        existing = next((c for c in sess.characters["characters"] if c["name"].lower() == sess.name.lower()), None)

        if existing:
            # Replace the existing character
            sess.characters["characters"] = [sess.character if c["name"].lower() == sess.name.lower() else c for c in sess.characters["characters"]]
            st.success(f"✅ Character '{sess.name}' updated.")
        else:
            sess.characters["characters"].append(sess.character)
            st.success(f"✅ New character '{sess.name}' created.")

        with open(DATA_DIR + "characters.yaml", "w", encoding="utf-8") as f:
            yaml.dump(sess.characters, f, allow_unicode=True)
        
        sess.display_form = "main"
        st.experimental_rerun()