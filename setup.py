#!/usr/bin/env python3

import os
import sys
from setuptools import setup

exec(open("bacassembly/__about__.py").read())

if sys.argv[-1] == "publish":
    os.system("python setup.py sdist upload")
    sys.exit()

with open("README.md") as f:
    long_description = f.read()

packages = ["bacassembly"]
package_data = {
    "bacassembly": [
        "bacassembly/config/*.yaml",
        "bacassembly/Snakefile",
        "bacassembly/rules/*.smk",
        "bacassembly/*.py",
    ]
}
data_files = [(".", ["LICENSE", "README.md"])]

entry_points = {"console_scripts": ["bacassembly=bacassembly.corer:main"]}

requires = [
    req.strip()
    for req in open("requirements.txt", "rU").readlines()
    if not req.startswith("#")
]

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]

setup(
    name="bacassembly",
    version=__version__,
    author=__author__,
    author_email="zhaohailong@genomics.cn",
    url="https://github.com/zhaoxvwahaha/BacAssembly",
    description="hybrid assembly and polish using short and long reads",
    long_description_content_type="text/markdown",
    long_description=long_description,
    entry_points=entry_points,
    packages=packages,
    package_data=package_data,
    data_files=data_files,
    include_package_data=True,
    install_requires=requires,
    license="GPLv3+",
    classifiers=classifiers,
)
