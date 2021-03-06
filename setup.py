from os.path import dirname, join

from setuptools import setup

import micropm4py


def read_file(filename):
    with open(join(dirname(__file__), filename)) as f:
        return f.read()


setup(
    name=micropm4py.__name__,
    version="0.2.1",
    description="MicroPM4Py - Process Mining for Micro-Controllers".strip(),
    long_description=read_file('README.md'),
    author="Alessandro Berti",
    author_email="alessandro.berti89@gmail.com",
    py_modules=[micropm4py.__name__],
    include_package_data=True,
    packages=['micropm4py', 'micropm4py.log', 'micropm4py.util', 'micropm4py.petrinet', 'micropm4py.random', 'micropm4py.discovery',
              'micropm4py.conversion', 'micropm4py.conversion.dfg', 'micropm4py.conversion.pm4py', 'micropm4py.visualization'],
    url='http://www.pm4py.org',
    license='GPL 3.0',
    install_requires=[
    ],
    project_urls={
        'Documentation': 'https://www.micropm4py.org/documentation.html',
        'Source': 'https://github.com/Javert899/micropm4py/tree/master/micropm4py',
        'Tracker': 'https://github.com/Javert899/micropm4py/issues',
    }
)
