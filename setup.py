# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from mdi import __version__

NAME = "mdi"
DESCRIPTION = "Flask application for ingesting data from mobile devices"
URL = "https://github.com/lalanza808/flask-mdi.git"
EMAIL = "lance@lzahq.tech"
AUTHOR = "Lance Allen"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = __version__
REQUIRED = [
    "boto3==1.9.74",
    "Flask==1.0.2"
]
EXTRAS = {}
TESTS = []
SETUP = []

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=EMAIL,
    include_package_data=True,
    extras_require=EXTRAS,
    install_requires=REQUIRED,
    setup_requires=SETUP,
    tests_require=TESTS,
    packages=find_packages(exclude=['ez_setup']),
    zip_safe=False
)
