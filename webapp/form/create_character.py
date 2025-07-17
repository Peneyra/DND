import streamlit as st
import yaml
from collections import Counter

def form_create_character(DATA_DIR):
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")


    #initialize some variables into the session state
    abilities = ["cha", "con", "dex", "int", "str", "wis"]
    form_error = False
    sess = st.session_state

    st.title("➕ Create Character")
    #################################################################
    # N a m e
    nam_col = st.columns([1,2])
    with nam_col[0]: st.subheader("Character Name")
    with nam_col[1]:
        st.text_input(
            "Character Name",
            key = 'name',
            label_visibility="collapsed"
            )

    rcb_col = st.columns([1,1,1])

    #################################################################
    # R a c e
    with rcb_col[0]:
        st.subheader("Race")
        race_default = "human"
        sess.race_index = sorted(sess.races.keys()).index(race_default)

        st.selectbox(
            "Race", 
            sorted(sess.races.keys()),
            key = "race_name",
            label_visibility="collapsed",
            index = sess.race_index
            )
    sess.race = sess.races[sess.race_name]

    #################################################################
    # C l a s s
    with rcb_col[1]:
        st.subheader("Class")
        clas_default = "fighter"
        sess.clas_index = sorted(sess.classes.keys()).index(clas_default)

        st.selectbox(
            "Class", 
            sorted(sess.classes.keys()),
            key = "clas_name",
            label_visibility="collapsed",
            index = sess.clas_index
            )
    sess.clas = sess.classes[sess.clas_name]

    #################################################################
    # B a c k g r o u n d
    with rcb_col[2]:
        st.subheader("Background")
        back_default = "hermit"
        sess.back_index = sorted(sess.backgrounds.keys()).index(back_default)

        st.selectbox(
            "Background", 
            sorted(sess.backgrounds.keys()),
            key = "back_name",
            label_visibility="collapsed",
            index = sess.back_index
            )
    sess.back = sess.backgrounds[sess.back_name]

    ccr_tab = st.tabs([
        "Player Stats",
        "Skills and Spells",
        "Traits",
        "Proficiencies",
        "Equipment",
        "Description"])

    with ccr_tab[0]:
        #################################################################
        # A b i l i t i e s
        sess.val_race = sess.race['abilities']
        if sess.race_name == "half-elf": sess.val_play_max = 74
        else: sess.val_play_max = 72

        st.subheader(f"Abilities ({' '.join(sess.clas['primary ability']).upper()} | {' '.join(sess.clas['saving throw proficiencies']).upper()})",
                    help="(primary | saving)")

        abi_col = st.columns([1,1,1,1])
        abi_col[0].markdown("")
        abi_col[1].markdown("**Player**")
        abi_col[2].markdown("**Race**")
        abi_col[3].markdown("**Total (Modifier)**")

        for abi in abilities:
            abi_col = st.columns([1,1,1,1])
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
            sess[abi + "_total"] = sess.val_race.get(abi,0) + sess[abi]
            sess[abi + "_modifier"] = (sess[abi + "_total"] - 10) // 2
            abi_col[3].markdown(f"**{sess[abi + '_total']}  ({sess[abi + '_modifier']})**")
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
        hp_list = sess.clas['levels'][1]['hit points']
        for abi, val in hp_list.items():
            if abi == 'any': hit_points += val
            else: hit_points += val * (sess[abi + "_modifier"]) 
        hpd_col[0].subheader(f"**Hit Points: {hit_points}**")

        damage_die = []
        damage_list = sess.clas['levels'][1]['hit dice']
        for die, val in damage_list.items():
            damage_die.append(str(val) + die)
        hpd_col[1].subheader(f"**Attack Damage: {','.join(damage_die)}**")

    with ccr_tab[1]:
        #################################################################
        # B a s i c   S k i l l s
        st.subheader("Skills")
        if 'skills' in sess.race['proficiencies']:
            race_skills = sess.race['proficiencies']['skills']
            st.markdown(f"**{sess.race['name']} skills:**".title())
            skr_col = st.columns([1,1,1,1])
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
        if 'skills' in sess.clas['proficiencies']:
            clas_skills = sess.clas['proficiencies']['skills']
            st.markdown(f"**{sess.clas['name']} skills:**".title())
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
        for k in range(4):
            if "race_skills_" + str(k) in sess:
                selected_skills.append(sess['race_skills_' + str(k)])
        for k in range(4):
            if "clas_skills_" + str(k) in sess:
                selected_skills.append(sess['clas_skills_' + str(k)])
        skills_duplicate = [
            sd for sd, 
            count in Counter(selected_skills).items() if count > 1
            ]

        if len(skills_duplicate) > 0:
            form_error = True
            st.markdown(f"**W A R N I N G!!!**")
            st.markdown(f"Turn back! You have duplicate skills chosen! {skills_duplicate}")
            st.markdown(f"**W A R N I N G!!!**")
        else:
            form_error = False

        #################################################################
        # C a n t r i p s   a n d   S p e l l s
        if "cantrip list" in sess.clas['levels'][1]:
            num_cantrip = sess.clas['levels'][1]['cantrip list']
            cantrip_book = sess.clas['proficiencies']['spells'][0]
            st.subheader("Cantrips")
            st.markdown(f"**{sess.clas['name']} cantrips:**".title())
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
            for k in range(num_cantrip):
                if "cantrip_" + str(k) in sess:
                    selected_cantrips.append(sess['cantrip_' + str(k)])
            cantrips_duplicate = [
                sd for sd, 
                count in Counter(selected_cantrips).items() if count > 1
                ]

            if len(cantrips_duplicate) > 0:
                form_error = True
                st.markdown(f"**W A R N I N G!!!**")
                st.markdown(f"Turn back! You have duplicate cantrips chosen! {cantrips_duplicate}")
                st.markdown(f"**W A R N I N G!!!**")
            else:
                form_error = False

        if "spell list" in sess.clas['levels'][1]:
            spell_list = sess.clas['levels'][1]['spell list']
            num_spell = 0
            for abi, val in spell_list.items():
                if abi == 'any': num_spell += val
                else: num_spell += val * (sess[abi + "_modifier"])
            num_spell = max(num_spell, 1)
            spell_book = sess.clas['proficiencies']['spells'][1]
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
            for k in range(num_spell):
                if "spell_" + str(k) in sess:
                    selected_spells.append(sess['spell_' + str(k)])
            spells_duplicate = [
                sd for sd, 
                count in Counter(selected_spells).items() if count > 1
                ]

            if len(spells_duplicate) > 0:
                form_error = True
                st.markdown(f"**W A R N I N G!!!**")
                st.markdown(f"Turn back! You have duplicate cantrips chosen! {spells_duplicate}")
                st.markdown(f"**W A R N I N G!!!**")
            else:
                form_error = False

    with ccr_tab[2]:
        #################################################################
        # T r a i t s
        if 'traits' in sess.race:
            st.subheader(f"**{sess.race['name'].title()} Traits**")
            for trait, description in sess.race['traits'].items():
                st.markdown(f"**{trait.title()}**")
                st.markdown(f"{description}")
        if 'traits' in sess.clas['levels'][1]:
            st.subheader(f"**{sess.clas['name'].title()} Traits**")
            for trait, description in sess.clas['levels'][1]['traits'].items():
                st.markdown(f"**{trait.title()}**")
                st.markdown(f"{description}")

    with ccr_tab[3]:
        #################################################################
        # P r o f i c i e n c i e s
        pro_col = st.columns([1,5])
        pro_types = ['weapons','armor','tools','languages']
        for p in pro_types:
            pro_list = []
            if p in sess.clas['proficiencies']: pro_list += sess.clas['proficiencies'][p]
            if p in sess.race['proficiencies']: pro_list += sess.race['proficiencies'][p]
            if p in sess.back['proficiencies']: pro_list += sess.back['proficiencies'][p]
            pro_list = sorted(list(set(pro_list)))
            if p == 'languages': language_known = pro_list
            if len(pro_list) == 0: pro_list = ['None']
            with pro_col[0]: st.markdown(p.title())
            with pro_col[1]: st.markdown(", ".join(pro_list).title())
        if 'any' in language_known:
            language_list = [
                "common",
                "dwarvish",
                "elvish",
                "giant",
                "gnomish",
                "goblin",
                "halfling",
                "orc",
                "abyssal",
                "celestial",
                "draconic",
                "deep Speech",
                "infernal",
                "primordial",
                "sylvan",
                "undercommon"
                ]
            for l in language_known:
                if l in language_list: language_list.remove(l)
            lan_col = st.columns([1,2,1])
            with lan_col[0]: st.markdown(f"**Choose a Language**")
            with lan_col[1]:
                st.selectbox(
                    "Language",
                    language_list,
                    key='Language',
                    label_visibility="collapsed"
                    )

    with ccr_tab[4]:
        None
        #################################################################
        # I n v e n t o r y / E q u i p m e n t

    with ccr_tab[5]:
        #################################################################
        # D e s c r i p t i o n
        gen_col = st.columns([1,2,1])
        with gen_col[0]: st.subheader("Gender")
        with gen_col[1]:
            st.text_input(
                "Gender",
                key='gender',
                label_visibility="collapsed"
                )
        st.markdown(sess.race['size'])
        siz_col = st.columns([1,2,1])
        with siz_col[0]: st.subheader("Height")
        with siz_col[1]:
            hei_col = st.columns([1,1,1,1])
            with hei_col[0]:
                st.text_input(
                    "Height Feet",
                    key='height_feet',
                    label_visibility="collapsed"
                    )
            with hei_col[1]: st.markdown(f"**ft**")
            with hei_col[2]:
                st.text_input(
                    "Height Inches",
                    key='height_inches',
                    label_visibility="collapsed"
                    )
            with hei_col[3]:
                st.markdown(f"**in**")
        with siz_col[0]: st.subheader("Weight")
        with siz_col[1]:
            wei_col = st.columns([1,1,1,1])
            with wei_col[0]:
                st.text_input(
                    "Weight",
                    key='weight',
                    label_visibility="collapsed"
                    )
            with wei_col[1]: st.markdown(f"**lbs**")
        st.markdown(sess.race['age'])
        age_col = st.columns([2,1,1,4])
        with age_col[0]: st.subheader("Age")
        with age_col[1]:
            st.text_input(
                "Age",
                key='age',
                label_visibility="collapsed"
                )
        with age_col[2]: st.markdown(f"**years**")
        st.markdown(sess.race['alignment'])
        ali_col = st.columns([1,3])
        with ali_col[0]: st.subheader("Alignment")
        with ali_col[1]:
            onm_col = st.columns([1,1,1,1])
            with onm_col[0]:
                st.selectbox(
                    "Order",
                    ['Lawful','Neutral','Chaotic'],
                    key = 'alignment_order',
                    label_visibility = 'collapsed',
                    index = None
                )
            with onm_col[1]: st.markdown(f"**Order**")
            with onm_col[2]:
                st.selectbox(
                    "Morality",
                    ['Good','Neutral','Evil'],
                    key = 'alignment_morality',
                    label_visibility = 'collapsed',
                    index = None
                )
            with onm_col[3]: st.markdown(f"**Morality**")
        if sess.alignment_order == 'Lawful' and sess.alignment_morality == 'Good':
            sess.alignment = "**Lawful good** (LG) creatures can be counted on to do the right thing as expected by society. Gold dragons, paladins, and most dwarves are lawful good."
        elif sess.alignment_order == 'Neutral' and sess.alignment_morality == 'Good':
            sess.alignment = "**Neutral good** (NG) creatures do the best they can to help others according to their needs. Many celestials, healers, and kind-hearted folk are neutral good."
        elif sess.alignment_order == 'Chaotic' and sess.alignment_morality == 'Good':
            sess.alignment = "**Chaotic good** (CG) creatures act as their conscience directs, with little regard for rules. Many elves, rebels, and freedom fighters are chaotic good."
        elif sess.alignment_order == 'Lawful' and sess.alignment_morality == 'Neutral':
            sess.alignment = "**Lawful neutral** (LN) creatures act in accordance with law, tradition, or personal codes. Judges, bureaucrats, and disciplined monks often follow this alignment."
        elif sess.alignment_order == 'Neutral' and sess.alignment_morality == 'Neutral':
            sess.alignment = "**Neutral** (N) creatures prefer to maintain balance and avoid taking sides. Druids, some animals, and those indifferent to conflict are often neutral."
        elif sess.alignment_order == 'Chaotic' and sess.alignment_morality == 'Neutral':
            sess.alignment = "**Chaotic neutral** (CN) creatures follow their whims and desires, unbound by laws or expectations. Rogues, eccentrics, and free spirits may be chaotic neutral."
        elif sess.alignment_order == 'Lawful' and sess.alignment_morality == 'Evil':
            sess.alignment = "**Lawful evil** (LE) creatures methodically take what they want within the limits of a code or tradition. Devils and tyrants often fall into this alignment."
        elif sess.alignment_order == 'Neutral' and sess.alignment_morality == 'Evil':
            sess.alignment = "**Neutral evil** (NE) creatures do whatever they can get away with, without compassion or qualms. Assassins, schemers, and self-serving villains fit here."
        elif sess.alignment_order == 'Chaotic' and sess.alignment_morality == 'Evil':
            sess.alignment = "**Chaotic evil** (CE) creatures act with arbitrary violence and cruelty, driven by selfishness or madness. Demons, savage warlords, and monstrous villains are chaotic evil."
        else:
            form_error = True
        if 'alignment' in sess: st.markdown(f"{sess.alignment}")

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