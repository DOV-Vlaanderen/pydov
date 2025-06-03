#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()
with open('requirements_dev.txt') as f:
    # ignore the general requirements
    requirements_dev = f.read().splitlines()[1:]
with open('requirements_doc.txt') as f:
    requirements_doc = f.read().splitlines()
with open('requirements_geom.txt') as f:
    requirements_geom = f.read().splitlines()
with open('requirements_proxy.txt') as f:
    requirements_proxy = f.read().splitlines()

setup(
    name='pydov',
    version='3.3.0',
    description=("A Python package to download data from Databank Ondergrond "
                 "Vlaanderen (DOV)."),
    long_description=readme,
    long_description_content_type='text/markdown',
    author="DOV-Vlaanderen",
    author_email='dov@vlaanderen.be',
    url='https://github.com/DOV-Vlaanderen/pydov',
    packages=find_packages(
        include=['pydov']),
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
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Programming Language :: Python :: 3.13',
            'Topic :: Scientific/Engineering',
    ],
    test_suite='tests',
    tests_require=requirements_dev,
    extras_require={
        'docs': requirements_doc,
        'devs': requirements_dev,
        'vectorfile': requirements_geom,  # deprecated
        'geom': requirements_geom,
        'proxy': requirements_proxy
    }
)
