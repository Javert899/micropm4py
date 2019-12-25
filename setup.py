from os.path import dirname, join

from setuptools import setup

import micropm4py


def read_file(filename):
    with open(join(dirname(__file__), filename)) as f:
        return f.read()


setup(
    name=micropm4py.__name__,
    version=micropm4py.__version__,
    description=micropm4py.__doc__.strip(),
    long_description=read_file('README.md'),
    author=micropm4py.__author__,
    author_email=micropm4py.__author_email__,
    py_modules=[micropm4py.__name__],
    include_package_data=True,
    packages=['micropm4py', 'micropm4py.log', 'micropm4py.util', 'micropm4py.petrinet',
              'micropm4py.conversion', 'micropm4py.conversion.dfg', 'micropm4py.conversion.pm4py'],
    url='http://www.pm4py.org',
    license='GPL 3.0',
    install_requires=[
    ],
    project_urls={
        'Documentation': 'http://pm4py.pads.rwth-aachen.de/documentation/',
        'Source': 'https://github.com/pm4py/pm4py-source',
        'Tracker': 'https://github.com/pm4py/pm4py-source/issues',
    }
)
