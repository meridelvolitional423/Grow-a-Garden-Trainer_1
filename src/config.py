import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'offsets.json')

def load_offsets():
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)
