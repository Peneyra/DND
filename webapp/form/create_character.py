import streamlit as st
import yaml
from collections import Counter
None
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
        "Stats",
        "Skills & Spells",
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

        abi_col = st.columns([2,1,1,1,1,1,2])
        abi_col[1].markdown("")
        abi_col[2].markdown("Player")
        abi_col[3].markdown("Race")
        abi_col[4].markdown("Total")
        abi_col[5].markdown("**Modifier**")

        for abi in abilities:
            abi_col[1].markdown(f"**{abi.upper()}**")
            with abi_col[2]:
                st.number_input(
                    abi + " player value", 
                    min_value=8, 
                    max_value=18,
                    value=8,
                    key=abi,
                    label_visibility="collapsed")
            abi_col[3].markdown(f"{sess.val_race.get(abi,0)}")
            sess[abi + "_total"] = sess.val_race.get(abi,0) + sess[abi]
            sess[abi + "_modifier"] = (sess[abi + "_total"] - 10) // 2
            abi_col[4].markdown(f"{sess[abi + '_total']}  ({sess[abi + '_modifier']})")
            abi_col[5].markdown(f"**{sess[abi + '_modifier']}**")
        total = 0
        for abi in abilities: 
            if abi in sess: total += sess[abi]
        abi_col[2].markdown(f"**{total} of {sess.val_play_max}**")

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
        hp_list = sess.clas['hit points']
        for abi, val in hp_list.items():
            if abi == 'any': hit_points += val
            else: hit_points += val * (sess[abi + "_modifier"]) 
        hpd_col[0].subheader(f"**Hit Points: {hit_points}**")

        damage_die = []
        damage_list = sess.clas['hit dice']
        for die, val in damage_list.items():
            damage_die.append(str(val) + die)
        hpd_col[1].subheader(f"**Attack Damage: {','.join(damage_die)}**")

    with ccr_tab[1]:
        scs_tab = st.tabs([
            "Skills",
            "Cantrips",
            "Spells"
        ])

        with scs_tab[0]:
            #################################################################
            # B a s i c   S k i l l s
            st.header("Skills",divider = 'rainbow')
            sess.selected_skills = []
            for cat in ['race','clas','back']:
                skills = []
                skl_col = {}
                if 'skills' in sess[cat]['proficiencies']:
                    skills = sess[cat]['proficiencies']['skills']
                    st.subheader(f"**{sess[cat]['name']} skills:**".title())
                    skl_col[cat] = st.columns([1,1,1,1])
                    k = 0
                    for s in skills:
                        with skl_col[cat][k]:
                            if len(s) == 1:
                                if s[0] in sess.selected_skills:
                                    st.markdown(f"*{s[0]}*")
                                else:
                                    st.markdown(f"**{s[0]}**")
                                    sess.selected_skills.append(s[0])
                            else:
                                st.selectbox(
                                    cat.title() + " Skills",
                                    sorted(s),
                                    key = cat + "_skills_" + str(k),
                                    label_visibility = "collapsed",
                                    index = k)
                        k += 1
            for cat in ['race','clas','back']:
                for k in range(4):
                    key_name = cat + "_skills_" + str(k)
                    if key_name in sess:
                        sess.selected_skills.append(sess[cat + "_skills_" + str(k)])
            skills_duplicate = [sd for sd, count in Counter(sess.selected_skills).items() if count > 1]

            if len(skills_duplicate) > 0:
                form_error = True
                st.markdown(f"**W A R N I N G!!!**")
                st.markdown(f"Turn back! You have duplicate skills chosen! {skills_duplicate}")
                st.markdown(f"**W A R N I N G!!!**")
            else:
                form_error = False

        with scs_tab[1]:
            #################################################################
            # C a n t r i p s
            if "cantrip list" in sess.clas:
                num_cantrip = sess.clas['cantrip list']
                cantrip_book = sess.clas['proficiencies']['spells'][0]
                st.header("Cantrips",divider = 'rainbow')
                st.subheader(f"**{sess.clas['name']} cantrips:**".title())
                cal_col = st.columns([1,1,1,1])
                for k in range(num_cantrip):
                    with cal_col[k]:
                        st.selectbox(
                            "Cantrip",
                            sorted(cantrip_book),
                            key = "cantrip_" + str(k),
                            label_visibility = "collapsed",
                            index = k)
                            
                sess.selected_cantrips = []
                for k in range(num_cantrip):
                    if "cantrip_" + str(k) in sess:
                        sess.selected_cantrips.append(sess['cantrip_' + str(k)])
                cantrips_duplicate = [
                    sd for sd, 
                    count in Counter(sess.selected_cantrips).items() if count > 1
                    ]

                if len(cantrips_duplicate) > 0:
                    form_error = True
                    st.markdown(f"**W A R N I N G!!!**")
                    st.markdown(f"Turn back! You have duplicate cantrips chosen! {cantrips_duplicate}")
                    st.markdown(f"**W A R N I N G!!!**")
                else:
                    form_error = False

        with scs_tab[2]:
            #################################################################
            # S p e l l s
            if "spell list" in sess.clas:
                spell_list = sess.clas['spell list']
                num_spell = 0
                for abi, val in spell_list.items():
                    if abi == 'any': num_spell += val
                    else: num_spell += val * (sess[abi + "_modifier"])
                num_spell = max(num_spell, 1)
                spell_book = sess.clas['proficiencies']['spells'][1]
                st.header("Spells",divider = 'rainbow')
                st.subheader(f"**{sess.clas_name} level 1 spells:**".title())
                sp1_col = st.columns([1,1,1,1])
                for k in range(min(4,num_spell)):
                    with sp1_col[k]:
                        st.selectbox(
                            "Spells",
                            sorted(spell_book),
                            key = "spell_" + str(k),
                            label_visibility = "collapsed",
                            index = k)
                if num_spell > 4:
                    sp2_col = st.columns([1,1,1,1])
                    for k in range(4,num_spell):
                        with sp2_col[k-4]:
                            st.selectbox(
                                "Spells",
                                sorted(spell_book),
                                key = "spell_" + str(k),
                                label_visibility = "collapsed",
                                index = k)
            
                sess.selected_spells = []
                for k in range(num_spell):
                    if "spell_" + str(k) in sess:
                        sess.selected_spells.append(sess['spell_' + str(k)])
                spells_duplicate = [
                    sd for sd, 
                    count in Counter(sess.selected_spells).items() if count > 1
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
        for cat in ['race','clas','back']:
            if 'traits' in sess[cat]:
                st.header(f"**{sess[cat]['name'].title()} Traits**",divider = 'rainbow')
                for trait, description in sess[cat]['traits'].items():
                    st.subheader(f"{trait.title()}")
                    st.markdown(f"{description}")

    with ccr_tab[3]:
        #################################################################
        # P r o f i c i e n c i e s
        for p in ['weapons','armor','tools','languages']:
            pro_list = []
            for cat in ['clas','race','back']:
                if p in sess[cat]['proficiencies']: pro_list += sess[cat]['proficiencies'][p]
            if p == 'languages':
                language_choice_num = pro_list.count('any')
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
                    "deep speech",
                    "infernal",
                    "primordial",
                    "sylvan",
                    "undercommon"
                    ]
            pro_list = sorted(list(set(pro_list)))
            sess[p + "_proficiencies"] = pro_list
            if len(pro_list) == 0: pro_list = ['None']
            st.header(p.title(),divider='rainbow')
            for pl in pro_list:
                st.markdown(f"- {pl.title()}")
        if language_choice_num > 0:
            lan_col = {}
            for k in range(language_choice_num):
                lan_col[k] = st.columns([1,2,1],vertical_alignment = 'center')
                with lan_col[k][0]: st.markdown(f"**Choose a Language**")
                with lan_col[k][1]:
                    st.selectbox(
                        "Language",
                        language_list,
                        key='language_' + str(k),
                        label_visibility="collapsed",
                        index = k + 1
                        )
                sess["languages_proficiencies"] += [sess['language_' + str(k)]]
        languages_duplicate = [sd for sd, count in Counter(sess["languages_proficiencies"]).items() if count > 1]
        print(sess["languages_proficiencies"])
        if len(languages_duplicate) > 0:
            form_error = True
            st.markdown(f"**W A R N I N G!!!**")
            st.markdown(f"Turn back! You have duplicate languages chosen! {languages_duplicate}")
            st.markdown(f"**W A R N I N G!!!**")
        else:
            form_error = False
            
    with ccr_tab[4]:
        #################################################################
        # I n v e n t o r y / E q u i p m e n t
        k = 0
        for cat in ['race','clas','back']:
            if 'equipment' in sess[cat]:
                st.header(f"**{sess[cat]['name'].title()} Equipment**",divider = 'rainbow')
                for e in sess[cat]['equipment']:
                    if isinstance(e,dict):
                        for k,v in e.items():
                            st.markdown(f"- {k} *({v})*")
                    elif isinstance(e,list):
                        st.selectbox(
                            "Equipment",
                            e,
                            key='equipment_' + str(k),
                            label_visibility='collapsed'
                        )
                        k += 1
                    else:
                        st.markdown(f"- {e.title()}")

    with ccr_tab[5]:
        des_tab = st.tabs([
            "Player",
            "Race",
            "Class",
            "Background"
        ])

        with des_tab[0]:
            #################################################################
            # D e s c r i p t i o n
            st.header("Basics",divider = 'rainbow')
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
            #################################################################
            # A l i g n m e n t
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
        
        with des_tab[1]:
            #################################################################
            # R a c e   D e s c r i p t i o n
            sup_race = ['dwarf','elf','gnome','halfling']
            st.header(f"{sess.race['name'].title()}",divider = 'rainbow')
            for sr in sup_race:
                if sr in sess.race['name'] and sess.race['name'] not in sr:
                    if sr in sess.race['description']: st.markdown(f"{sess.race['description'][sr]}")
            st.markdown(f"{sess.race['description'][sess.race['name']]}")
            for title, description in sess.race['description'].items():
                if title != sess.race['name'] and title not in sup_race:
                    st.subheader(f"{title.title()}")
                    st.markdown(f"{sess.race['description'][title]}")
        
        with des_tab[2]:
            #################################################################
            # C l a s s   D e s c r i p t i o n
            st.header(f"{sess.clas['name'].title()}",divider = 'rainbow')
            st.markdown(f"{sess.clas['description'][sess.clas['name']]}")
            for title, description in sess.clas['description'].items():
                if title != sess.clas['name']:
                    st.subheader(f"{title.title()}")
                    st.markdown(f"{sess.clas['description'][title]}")
        
        with des_tab[3]:
            #################################################################
            # B a c k g r o u n d   D e s c r i p t i o n
            st.header(f"{sess.back['name'].title()}",divider = 'rainbow')
            if 'variation' in sess.back.keys():
                bde_col = st.columns([1,2])
                with bde_col[0]:
                    var_name = list(sess.back['variation'].keys())[0]
                    st.subheader(var_name.title())
                with bde_col[1]:
                    st.selectbox(
                        "Background Variation",
                        sess.back['variation'][var_name],
                        key = "back_variation",
                        label_visibility = "collapsed"
                    )
            st.markdown(f"{sess.back['description'][sess.back['name']]}")
            for title, description in sess.back['description'].items():
                if title != sess.back['name']:
                    st.subheader(f"{title.title()}")
                    st.markdown(f"{sess.back['description'][title]}")

    st.header("",divider = "rainbow")
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