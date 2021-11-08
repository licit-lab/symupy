import os
import re
import sys
import importlib

_reader_plugin_default_path = os.path.dirname(os.path.realpath(__file__))

READER_PLUGIN_DIRS = [_reader_plugin_default_path]


def get_all_readers():
    """Parse all python file in READER_PLUGIN_DIRS to get plugin classes.

    Returns
    -------
    dict
        Return dict with input and output reader classes.

    """
    readers = dict(input=dict(), output=dict())
    for dirs in READER_PLUGIN_DIRS:
        for entry in os.scandir(dirs):
            if entry.path.endswith(".py") and (
                entry.name != "__init__.py" and entry.name != "loader.py"
            ):
                in_readers, out_readers = get_class(entry.path)
                readers["input"][entry.path] = in_readers
                readers["output"][entry.path] = out_readers

    return readers


def get_class(file):
    """From a file return a dict or input and output readers.

    Parameters
    ----------
    file : str
        Plugin file to parse.

    Returns
    -------
    (list, list)
        List of input reader and list of output reader.

    """
    all_reader_input = []
    all_reader_output = []
    with open(file, "r") as f:
        contents = f.read()
    match = re.findall("class (\w+)\(AbstractNetworkReader\)", contents, re.MULTILINE)
    if match is not None:
        for reader in match:
            all_reader_input.append(reader)

    match = re.findall(
        "class (\w+)\(AbstractTrafficDataReader\)", contents, re.MULTILINE
    )
    if match is not None:
        for reader in match:
            all_reader_output.append(reader)

    return all_reader_input, all_reader_output


def add_dir_to_plugin(folder):
    """Add dir folder to READER_PLUGIN_DIRS.

    Parameters
    ----------
    folder : str
        Path to dir to add.

    """
    assert os.path.isdir(folder)
    READER_PLUGIN_DIRS.append(os.path.abspath(folder))


def load_plugins(type):
    """Load all plugins contained in READER_PLUGIN_DIRS.

    Parameters
    ----------
    type : str
        Type of reader to load ('input' or 'output').

    Returns
    -------
    dict
        Dict with plugin classes.

    """
    readers = get_all_readers()[type]
    modules = dict()
    for file, cls in readers.items():
        if cls:
            module_name = "PLG" + file.split("/")[-1].split(".")[0]
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
