**| [Installation](#installation) | [Usage](#usage) |  [External tools](#external-tools) | [License](#license) | [Contact](#contact) |**

 # symupy

[![Join the chat at https://gitter.im/symupy/Lobby](https://badges.gitter.im/symupy/Lobby.svg)](https://gitter.im/symupy/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A Python API to control and manipulate SymuVia

## Installation

Clone this repository or download the files [here](https://github.com/symuvia/symupy/archive/master.zip)

```sh 
git clone https://github.com/research-licit/Hierarchical-Platooning.git
```

Be sure to place one copy of the simulator within the folder `symuvia`. Be sure to respect the following structure

```sh
└── symupy
    ├── control
    ├── func
    ├── io
    ├── symuvia
    │   └── Contents
    │       └── Frameworks
    ├── tests
    └── util
```


## Usage 

In python 

```python 
from symupy.func import Simulation 

XML_path = 'users/Documents/file.xml'
Sim_path = 'users/Simulator/Contents/Frameworks/libSymuVia.dylib

x = Simulation(fildir,symdir)
b = x.run_Simulation()
```
## External tools

- SymuVia library.

## License

These API is licensed under [MIT License](https://github.com/symuvia/symupy/blob/master/LICENSE)

## Contact 

If you run into problems or bugs, please let us know by [creating an issue](https://github.com/research-licit/Hierarchical-Platooning/issues/new) an issue in this repository.