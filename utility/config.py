import yaml
from os import path

from utility.exceptions import NoConfigFile


file = './config.yaml'


def write_data(data: dict) -> None:
    with open(file, 'w', encoding='utf-8') as stream:
        yaml.dump(data, stream, encoding='utf-8', allow_unicode=True, sort_keys=False)


def read_data() -> dict:
    if not path.isfile(file):
        raise NoConfigFile
    with open(file, 'r', encoding='utf-8') as stream:
        return yaml.load(stream, Loader=yaml.FullLoader)
