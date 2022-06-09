# -*- coding: utf-8 -*-
"""
Created on Mon May 17 09:46:26 2021

@author: Akileshvar A Mosi
"""

from distutils.core import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sniperl",
    version="1.0.1",
    author="Akileshvar A",
    author_email="akileshvar008@gmail.com",
    description="A python Reinforcement Market Trader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Apex-Capitals/SnipeRL",
    packages=['sniperl'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)