#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


setup(
    name='pyloniex',
    version='0.0.9',

    packages=find_packages(),

    install_requires=[
        'cryptography',
        'requests>=2.20.0',
        'tenacity',
    ],

    author='Adam Rothman',
    author_email='rothman.adam@gmail.com',
    description='Python bindings for the Poloniex API',
    url='https://github.com/adamrothman/pyloniex',
)
