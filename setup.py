import os
from setuptools import find_packages, setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="svpg",
    author="SVPG team-SU",
    license="MIT",
    url="https://github.com/Anidwyd/pandroide-svpg.git",
    python_requires=">=3.9",
    packages=[
        "svpg",
        "svpg.algos",
        "svpg.algos.a2c.mono",
        "svpg.algos.a2c.multi",
        "svpg.algos.reinforce.mono",
        "svpg.algos.reinforce.multi",
        "svpg.helpers",
    ],
    # packages=find_packages(),
    long_description=read("README.md"),
)