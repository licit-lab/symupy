from setuptools import setup, find_packages

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

with open("HISTORY.md", "r") as history_file:
    HISTORY = history_file.read()

setup(
    name="symupy",
    version="0.2.3",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        "numpy>=1.16",
        "lxml>=4.3.3",
        "xmltodict>=0.12",
        "networkx>=2.2",
        "matplotlib>=3.0.0",
        "sqlalchemy>=1.3.5",
        "pandas>=0.24",
        "scipy>=1.4.1",
    ],
    author="Andres Ladino",
    author_email="aladinoster@gmail.com",
    description="A module for Symuvia inside Python",
    url="https://github.com/symuvia/symupy",
    download_url="https://github.com/symuvia/symupy",
    include_package_data=True,
    long_description=LONG_DESCRIPTION + "\n\n" + HISTORY,
    long_description_content_type="text/markdown",
    keywords="traffic microsimulation",
    license="MIT",
    classifiers=CLASSIFIERS,
    zip_safe=False,
)
