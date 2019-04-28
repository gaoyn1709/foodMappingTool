import json
import os


def load_json_file(file_path, default='obj'):
    if not os.path.exists(file_path):
        if default == 'list':
            return []
        else:
            return {}
    with open(file_path, 'r', encoding='utf8') as f:
        data = json.load(f)
    return data


def save_json_file(file_path, json_data):
    try:
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(json_data, f, ensure_ascii=False)
    except Exception as e:
        print(e)
        print('warning! I will try to save data with ensure_ascii=True: %s' % file_path)
        with open(file_path, 'w', encoding='utf8') as f:
            json.dump(json_data, f, ensure_ascii=True)
