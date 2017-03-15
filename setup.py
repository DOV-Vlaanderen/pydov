#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

setup(
    name='pydov',
    version='0.1.0',
    description="A python package to retrieve data from Databank Ondergrond Vlaanderen (DOV)",
    long_description=readme,
    author="DOV-Vlaanderen",
    author_email='dov@vlaanderen.be',
    url='https://github.com/DOV-Vlaanderen/pydov',
    packages=[
        'pydov',
    ],
    package_dir={'pydov':
                 'pydov'},
    include_package_data=True,
    install_requires=[
        'pandas',
        'xmltodict'
    ],
    license="MIT license",
    zip_safe=False,
    keywords='pydov',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=['pandas']
)
