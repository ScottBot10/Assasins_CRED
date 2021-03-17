import os

import yaml
from dotenv import load_dotenv, find_dotenv

from assassins_cred.constants import config_file, PROJECT_ROOT

os.chdir(PROJECT_ROOT)

_node_types = {
    str: (yaml.ScalarNode, 'tag:yaml.org,2002:str'),
    bool: (yaml.ScalarNode, 'tag:yaml.org,2002:bool'),
    int: (yaml.ScalarNode, 'tag:yaml.org,2002:int'),
    float: (yaml.ScalarNode, 'tag:yaml.org,2002:float'),
    list: (yaml.SequenceNode, 'tag:yaml.org,2002:seq'),
    dict: (yaml.MappingNode, 'tag:yaml.org,2002:map'),
    type(None): (yaml.ScalarNode, 'tag:yaml.org,2002:null')
}


def _env_var_constructor(loader, node):
    default = None

    if node.id == 'scalar':
        value = loader.construct_scalar(node)
        key = str(value)
    else:
        value = loader.construct_sequence(node)

        if len(value) >= 2:
            default = value[1]
            key = value[0]
        else:
            key = value[0]

    return os.getenv(key, default)


def _path(*path):
    if path:
        path = os.path.join(*path) if len(path) - 1 else path[0]
        return os.path.normpath(os.path.abspath(path))
    return ''


def _path_constructor(loader, node):
    if node.id == 'scalar':
        return _path(loader.construct_scalar(node))
    else:
        return _path(*loader.construct_sequence(node))


def _project_root_constructor(loader, node):
    if node.id == 'scalar':
        value = loader.construct_scalar(node)
        keys = [str(value)]
    else:
        keys = loader.construct_sequence(node)

    return _path(os.path.join(PROJECT_ROOT, *keys))


def make_loader(anchors: dict = None):
    anchors = {
        name: _node_types[type(val)][0](_node_types[type(val)][1], val)
        for name, val in anchors.items()
    }

    class MyLoader(yaml.SafeLoader):
        def __init__(self, stream):
            super().__init__(stream)
            if anchors is not None:
                self.anchors = anchors

    return MyLoader


anchors = {
    'PROJECT_ROOT': PROJECT_ROOT
}

load_dotenv(find_dotenv())
yaml.SafeLoader.add_constructor("!ENV", _env_var_constructor)
yaml.SafeLoader.add_constructor("!PATH", _path_constructor)

with open(config_file, encoding="UTF-8") as f:
    _CONFIG_YAML = yaml.load(f, Loader=make_loader(anchors))


class YAMLObj(type):
    def __setattr__(self, key, value):
        super().__setattr__(key, value)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getattr__(cls, name):
        super().__getattr__(name)

    def __getitem__(cls, name):
        return cls.__getattr__(name)

    def __iter__(cls):
        """Return generator of key: value pairs of current constants class' config values."""
        for name, typ in cls.__annotations__.items():
            attr = getattr(cls, name)
            yield name, (attr if typ != dict else dict(attr))

    def get(cls, item):
        return cls.__getattr__(item)


def _get_class(name, qualname):
    class ConfigNode(metaclass=YAMLObj):
        __name__ = name
        __qualname__ = qualname
        __annotations__ = {}

    return ConfigNode


def _add_config(config, clazz=None, section_=''):
    for name, node in config.items():
        if isinstance(node, dict):
            section_name = f"{section_}.{name}" if section_ else name

            config_node = _get_class(name, section_name)

            clazz.__annotations__[name] = dict
            clazz[name] = config_node
            _add_config(node, clazz=config_node, section_=section_name)
        else:
            clazz.__annotations__[name] = type(node)
            clazz[name] = node


for _name, _node in _CONFIG_YAML.items():
    _config_node = _node
    if isinstance(_node, dict):
        _config_node = _get_class(_name, _name)
        _add_config(_node, clazz=_config_node, section_=_name)
    exec(f'{_name} = _config_node\n')
