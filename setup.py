from setuptools import setup, find_packages
from version import find_version

CLASSIFIERS = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Topic :: Scientific/Engineering",
    "Topic :: Scientific/Engineering :: Mathematics",
    "Natural Language :: English",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS :: MacOS X",
    "Programming Language :: Python :: 3.7",
]

with open("README.md", "r") as f:
    LONG_DESCRIPTION = f.read()

setup(
    name="symupy",
    version=find_version("symupy", "__init__.py"),
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "numpy>=1.14",
        "lxml>=4.3.3",
        "xmltodict>=0.12",
        "networkx>=2.2",
        "matplotlib>=3.0",
        "sqlalchemy>=1.3",
    ],
    author="Andres Ladino",
    author_email="aladinoster@gmail.com",
    description="Using Symuvia inside Python",
    url="https://github.com/symuvia/symupy",
    download_url="https://github.com/symuvia/symupy",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    keywords="traffic microsimulation",
    license="MIT",
    classifiers=CLASSIFIERS,
)
