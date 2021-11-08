from setuptools import setup, find_packages

import os

if os.environ.get("READTHEDOCS"):
    file_path = os.path.realpath(__file__)
    checkout_name = os.path.basename(os.path.dirname(file_path))
    symuvia_rel_path = os.path.join("..", "..", "conda", checkout_name, "lib")
    symuvia_path = os.path.realpath(symuvia_rel_path)
    os.environ["SYMUVIA_PATH"] = symuvia_path

CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Natural Language :: English",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS :: MacOS X",
    "Programming Language :: Python :: 3.9",
]

with open("README.md", "r", encoding="UTF8") as f:
    LONG_DESCRIPTION = f.read()

with open("HISTORY.md", "r", encoding="UTF8") as history_file:
    HISTORY = history_file.read()

requirements = [
    "numpy>=1.16",
    "lxml>=4.3.3",
    "networkx>=2.5",
    "matplotlib>=3.0.0",
    "sqlalchemy>=1.3.5",
    "pandas>=1.0.0",
    "scipy>=1.4.1",
    "click>=7.0",
    "python-decouple>=3.3",
    "PyQt5>=5.15.4",
    "pyqtgraph>=0.12",
]

test_requirements = [
    "pytest>=3",
]

dev_requirements = [
    "sphinx==3.2.1",
    "recommonmark==0.6.0",
    "pytest==6.1.1",
    "bump2version==1.0.0",
    "twine==3.2.0",
    "black==19.10b0",
    "pylint==2.6.0",
    "sphinx-rtd-theme==0.5.0",
    "tox==3.20.0",
    "coverage==5.3",
    "flake8==3.8.4",
]

setup(
    name="symupy",
    version="1.0.0",
    description="A module for SymuFlow inside Python",
    long_description=LONG_DESCRIPTION + "\n\n" + HISTORY,
    long_description_content_type="text/markdown",
    author="Andres Ladino",
    author_email="aladinoster@gmail.com",
    maintainer="Andres Ladino",
    maintainer_email="aladinoster@gmail.com",
    url="https://github.com/symuflow/symupy",
    download_url="https://github.com/symuflow/symupy",
    packages=find_packages(
        include=["symupy", "symupy.*", "*.ini", "*.xml", "*.xsd"]
    ),
    classifiers=CLASSIFIERS,
    license="MIT",
    keywords="traffic microsimulation",
    include_package_data=True,
    package_data={
        "": ["*.ini", "*.xml", "*.xsd"],
    },
    install_requires=requirements,
    entry_points={"console_scripts": ["symupy=symupy.cli:main"]},
    extra_require={"dev": dev_requirements},
    python_requires=">=3.7",
    test_suite="tests",
    tests_require=test_requirements,
    zip_safe=False,
)
