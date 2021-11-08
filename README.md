**| [Overview](#overview) | [Download](#download) | [Instalation](#installation) | [License](#license) | [Contact](#contact) |**

# Symupy

[![Documentation Status](https://readthedocs.org/projects/symupy/badge/?version=stable)](https://symupy.readthedocs.io/en/stable/?badge=stable) ![PyPI](https://img.shields.io/pypi/v/symupy) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/symupy)

A Python API to control and interact with SymuFlow. Please find more information in the [documentation](https://symupy.readthedocs.io/en/stable/)

## Overview

`SymuPy` is a python package to perform and deploy traffic simulations within the [*SymuVia*](http://github.com/licit-lab/symuvia) ecosystem via python without much effort.

## Download

You can download the latest version in this [link](https://github.com/licit-lab/symupy/archive/master.zip) or clone this repository at

```
git clone https://github.com/licit-lab/symupy.git
```

## Installation

There are two possibilities to install this package.

1. To get the last stable release. You can install this package via `anaconda`:

  ```
  conda install -c licit-lab symupy
  ```

  **Note**: We recommend to use conda as a default environment for installation. An alternative version is also available via [PyPI](https://pypi.org/project/symupy/). But in this version the simulation platform [symuflow](https://github.com/licit-lab/symuflow) is not distributed and it is required to be installed externally.

2. To retrieve the `edge` version with latest changes. You can install from the source code:

   ```
   pip install https://github.com/licit-lab/symupy/archive/master.zip
   ```

## Usage

For more details check the [documentation](https://symupy.readthedocs.io/en/stable/) or this [repository](https://github.com/licit-lab/symupy-examples) with examples:

## License

This code is licensed via an [MIT license](LICENSE.md)

## Contact

If you run into problems or bugs, please let us know by [creating an issue](https://github.com/licit-lab/symupy/issues/new/choose) in this repository.