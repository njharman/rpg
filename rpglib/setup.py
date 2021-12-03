#!/usr/bin/env python

try:
    from distutils.core import setup
except ImportError:
    from setuptools import setup


setup(
    name='rpg',
    version='0.0.1',
    author='Norman J. Harman Jr.',
    author_email='njharman@gmail.com',
    license='MIT',
    packages=['rpg', ],
    )
