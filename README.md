**| [Installation](#installation) | [Usage](#usage) |  [External tools](#external-tools) | [License](#license) | [Contact](#contact) |**

 # symupy

[![Join the chat at https://gitter.im/symupy/Lobby](https://badges.gitter.im/symupy/Lobby.svg)](https://gitter.im/symupy/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) ![Packagist](https://img.shields.io/packagist/l/doctrine/orm.svg)

A Python API to control and manipulate SymuVia

## Installation

Clone this repository or download the files [here](https://github.com/symuvia/symupy/archive/master.zip)

```sh 
git clone https://github.com/symuvia/symupy.git
```

## Work environment 

This package does not validate dependencies for the moment and relies on [Conda](https://www.anaconda.com/distribution/) for the updates. An environment is for the moment required. In a bash terminal launch:

```sh
conda create --file requirements.yaml
```

## Symuvia library 

A copy compiled version of symuvia is provided within the folder `symupy/lib`. Unfortunately while we fix this [issue](https://github.com/symuvia/symupy/issues/7), it is likely to fix dependencies manually. For this: 

```sh 
cd symupy/lib
python3 launch.py
```

## Usage 

In python 

```python 
from symupy.func import Simulation 

xml_path = 'path/file.xml'
sim_path = 'path/libSymuVia.dylib'

# Use the following in case you dont have access to a version of SymuVia 
import os
lib_path = ("symupy", "lib", "darwin", "libSymuVia.dylib")
sim_path = os.path.join(os.getcwd(), *lib_path)

# Charge library
sim_instance = Simulation(sim_path)
sim_instance.load_symuvia()

# Location of Simulation File
sim_file = Simulation(xml_path)

# Run simulation 
simulator.run_simulation(sim_case)

```
## External tools

- SymuVia library.

## License

These API is licensed under [MIT License](https://github.com/symuvia/symupy/blob/master/LICENSE)

## Contact 

If you run into problems or bugs, please let us know by [creating an issue](https://github.com/research-licit/Hierarchical-Platooning/issues/new) an issue in this repository.