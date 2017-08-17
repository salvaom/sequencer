#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    version='0.1.0',
    description='File sequence helper',
    author='Salvador Olmos Miralles',
    name='sequencer',
    author_email='salvaom11@gmail.com',
    packages=find_packages(exclude=['source/test']),
    install_requires=[
        'sphinx',
        'sphinx_rtd_theme'
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
