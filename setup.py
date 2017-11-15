#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup_requirements = [
    'pytest-runner'
]

test_requirements = [
    'pytest'
]

setup(
    name='pydov',
    version='0.1.0',
    description="A Python package to download data from Databank Ondergrond Vlaanderen (DOV).",
    long_description=readme + '\n\n' + history,
    author="DOV-Vlaanderen",
    author_email='dov@vlaanderen.be',
    url='https://github.com/DOV-Vlaanderen/pydov',
    packages=find_packages(include=['pydov']),
    # entry_points={
    #     'console_scripts': [
    #         'pydov=pydov.cli:main'
    #     ]
    # },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='pydov',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
