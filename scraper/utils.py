import json
import os

def save_json(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding='utf-8') as f:   ##writes the data inside it as formatted JSON- proper spacing and Unicode support
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)
