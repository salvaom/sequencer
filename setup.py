#!/usr/bin/env python
import sys
from setuptools import setup, find_packages

sys.path.append('source')

setup(
    version='0.1.0',
    description='File sequence helper',
    author='Salvador Olmos Miralles',
    name='sequencer',
    author_email='salvaom11@gmail.com',
    packages=find_packages('source'),
    package_dir={
        '': 'source'
    },
    install_requires=[
        'sphinx',
        'sphinx_rtd_theme'
    ],
    setup_requires=['pytest-runner', 'sphinx', 'sphinx_rtd_theme'],
    tests_require=['pytest', 'pytest-cov'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
    ]
)
