from .json_parser import JsonParser
from .toml_parser import TomlParser
from .yaml_parser import YamlParser
from .pickle_parser import PickleParser


def create_parser(name):
    name.lower()
    if name == 'json':
        return JsonParser()
    if name == 'toml':
        return TomlParser()
    if name == 'yaml':
        return YamlParser()
    if name == 'pickle':
        return PickleParser()
    raise Exception("There is no such parser")
