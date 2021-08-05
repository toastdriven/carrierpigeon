#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name="carrierpigeon",
    version="0.3.0-alpha",
    description="Contract-based messages.",
    author="Daniel Lindsley",
    author_email="daniel@toastdriven.com",
    url="http://github.com/toastdriven/carrierpigeon/",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    package_dir={"": "src"},
    py_modules=["carrierpigeon"],
    requires=[
        "jsonschema",
    ],
    install_requires=[],
    tests_require=[
        "pytest",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
