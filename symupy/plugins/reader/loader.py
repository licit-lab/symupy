import os
import re
import sys
import importlib

_reader_plugin_default_path = os.path.dirname(os.path.realpath(__file__))

READER_PLUGIN_DIRS = [_reader_plugin_default_path]

def get_all_readers():
    readers = dict()
    for dirs in READER_PLUGIN_DIRS:
        for entry in os.scandir(dirs):
            if entry.path.endswith(".py") and (entry.name!='__init__.py' and entry.name!='loader.py'):
                readers[entry.path] = get_class(entry.path)

    return readers


def get_class(file):
    all_reader = []
    with open(file, 'r') as f:
        contents = f.read()
    match = re.findall('class (\w+)\(AbstractNetworkReader\)', contents, re.MULTILINE)
    if match is not None:
        for reader in match:
            all_reader.append(reader)

    return all_reader


def add_dir_to_plugin(folder):
    assert os.path.isdir(folder)
    READER_PLUGIN_DIRS.append(os.path.abspath(folder))

def load_plugins():
    readers =  get_all_readers()
    modules = dict()
    for file, cls in readers.items():
        module_name = 'PLG'+file.split('/')[-1].split('.')[0]
        spec = importlib.util.spec_from_file_location(module_name, file)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        imp = importlib.import_module(module_name)
        for c in cls:
            modules[c] = getattr(imp, c)


    return modules


#
# if __name__ == '__main__':
#     plugins = get_all_plugins()
