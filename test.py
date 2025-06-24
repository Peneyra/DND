import yaml

path = "./data/character_creation.yaml"

with open(path, 'r') as f:
    x = yaml.safe_load(f)

None