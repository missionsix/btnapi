import os
from distutils.core import setup

version = '0.1'
README = os.path.join(os.path.dirname(__file__), 'README')
long_description = open(README).read() + '\n'

setup(
    name='btnapi',
    version=version,
    description=("A python API interface to BTN"),
    long_description=long_description,
    packages=['btnapi',],
    license='GPL',
    author='missionsix',
    author_email='btn-api@missionsix.net'
)
