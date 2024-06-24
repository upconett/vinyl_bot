import json
from os import path


file = './template_images.json'


def write_data(data: dict) -> None:
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_data() -> dict:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        write_data({
            'templates_vinyl': None,
            'templates_album': None
        })
        return read_data()


def change_image(key: str, image_id: str) -> None:
    data = read_data() 
    data[key] = image_id
    write_data(data)


def get_image(key: str) -> str | None:
    try: return read_data()[key]
    except KeyError: return None
    
import json
from os import path


file = './template_images.json'


def write_data(data: dict) -> None:
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def read_data() -> dict:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        write_data({
            'templates_vinyl': None,
            'templates_album': None
        })
        return read_data()


def change_image(key: str, image_id: str) -> None:
    data = read_data() 
    data[key] = image_id
    write_data(data)


def get_image(key: str) -> str | None:
    try: return read_data()[key]
    except KeyError: return None
    