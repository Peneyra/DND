import yaml
import os
import ast

def load_yaml(path):
    with open(path, 'r') as f: return yaml.safe_load(f)

def save_yaml(path,data,data_old):
    with open(path + ".old", 'w') as f: yaml.dump(data_old,f)
    with open(path, 'w') as f: return yaml.dump(data,f)
    print("Saved new data to " + path)
    print("Moved old data to " + path + ".old")

def update_1(data,val):
    output = data
    output["description"] = val[0]
    output["hit die"] = val[1]
    output["primary ability"] = val[2].split(', ')
    output["saving throw proficiencies"] = val[3].split(', ')
    output["armor and weapon proficiencies"] = val[4].split(', ')
    return output

#mode = "edit yaml"
#mode = "format spells"
#mode = "check spells"
mode = "rebuild yaml"
#FILE = "scratch.yaml"
FILE = "phb_races.yaml"


DATA_DIR = os.path.dirname(os.path.abspath(__file__)) + "/data/"

# print("Here are your files:")
# try:
#     for item in os.listdir(DATA_DIR): print(item)
# except:
#     None

if mode in {"edit yaml", "check spells","rebuild yaml"}:
    try:
        data = load_yaml(DATA_DIR + FILE)
        data_old = data.copy()
    except Exception as e:
        print(f"{e}.")

elif mode == "format spells":
    try:
        with open(DATA_DIR + FILE, 'r') as f: data = f.read()
    except:
        print(f"{FILE} not found.")



if mode == "edit yaml":
    while True:
        print("Choose an action and section: ")
        print("  0 - Move")
        print("  1 - Add")
        print("  2 - Update")
        print("  3 - Back")
        print("  4 - Save")
        try:
            print(list(data['classes'].keys()))
        except:
            print(f"{FILE} is not the correct format.")
        action = input("# data:")
        if action[0] == "1":
            val = action[2:]
            data['classes'][val] = {"name":val}
        if action[0] == "2":
            val = action[2:].split("/")
            data['classes'][val[0]] = update_1(data['classes'][val[0]],val[1:])
        if action[0] == "4":
            save_yaml(DATA_DIR + FILE,data,data_old)
            print("Saved data to " + DATA_DIR + FILE)
        print(data['classes'])

elif mode == "format spells":
    data_out = ""
    for d in  data.splitlines():
        if d == "Cantrips":
            data_out += "0:\n"
        elif d == "1st-level":
            data_out += "1:\n"
        elif d == "2nd-level":
            data_out += "2:\n"
        elif d == "3rd-level":
            data_out += "3:\n"
        elif d == "4th-level":
            data_out += "4:\n"
        elif d == "5th-level":
            data_out += "5:\n"
        elif d == "6th-level":
            data_out += "6:\n"
        elif d == "7th-level":
            data_out += "7:\n"
        elif d == "8th-level":
            data_out += "8:\n"
        elif d == "9th-level":
            data_out += "9:\n"
        else:
            data_out += "- " + d + "\n"
        with open(DATA_DIR + FILE, 'w') as f: f.write(data_out)

elif mode == "check spells":
    for c in data['classes']:
        print(f"**{c}**")
        if 'weapons' in data['classes'][c]['proficiencies']:
            print("weapons")
            for w in data['classes'][c]['proficiencies']['weapons']:
                print("  - " + w)
        if 'armor' in data['classes'][c]['proficiencies']:
            print("armor")
            for w in data['classes'][c]['proficiencies']['armor']:
                print("  - " + w)
        if 'spells' in data['classes'][c]['proficiencies']:
            print("spells")
            for w in data['classes'][c]['proficiencies']['spells']:
                print("level " + str(w))
                for s in sorted(list(data['classes'][c]['proficiencies']['spells'][w])):
                    print("  - " + s)

elif mode == "rebuild yaml":
    save_yaml(DATA_DIR + FILE,data,data_old)