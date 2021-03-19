#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
with open('requirements_dev.txt') as f:
    requirements_dev = f.read().splitlines()[1:] # ignore the general requirements
with open('requirements_doc.txt') as f:
    requirements_doc = f.read().splitlines()

setup(
    name='pydov',
    version='2.0.1',
    description="A Python package to download data from Databank Ondergrond Vlaanderen (DOV).",
    long_description=readme,
    long_description_content_type='text/markdown',
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
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Dutch',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Scientific/Engineering',
    ],
    test_suite='tests',
    tests_require=requirements_dev,
    extras_require={
        'docs': requirements_doc,
        'devs': requirements_dev
    }
)
