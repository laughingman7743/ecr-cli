#!/usr/bin/env python
#  -*- coding: utf-8 -*-
from __future__ import print_function
import codecs

from setuptools import setup

import ecr_cli


with codecs.open('README.rst', 'rb', 'utf-8') as readme:
    long_description = readme.read()


setup(
    name='ecr-cli',
    version=ecr_cli.__version__,
    description='Goodbye docker login & a long repository URL for Amazon ECR :)',
    long_description=long_description,
    url='https://github.com/laughingman7743/ecr-cli/',
    author='laughingman7743',
    author_email='laughingman7743@gmail.com',
    license='MIT License',
    packages=['ecr_cli'],
    package_data={
        '': ['*.rst'],
    },
    install_requires=[
        'future',
        'click>=6.0',
        'PyYAML>=3.12',
        'boto3>=1.5.0',
        'docker>=3.1.0',
        'tqdm>=4.19.0'
    ],
    tests_require=[
        'pytest>=3.5',
        'pytest-cov',
        'pytest-flake8',
    ],
    entry_points={
        'console_scripts': [
            'ecr = ecr_cli.cli:cli',
        ],
    },
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
