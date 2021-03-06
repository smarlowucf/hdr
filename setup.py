#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# hdr: A Python API and CLI to create hdr images.
#
# Copyright (C) 2017 Sean Marlow
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

with open('README.adoc') as readme_file:
    readme = readme_file.read()

with open('CHANGES.adoc') as changes_file:
    changes = changes_file.read()

requirements = [
    'Click',
    'opencv-contrib-python',
    'Pillow'
]

test_requirements = [
]

setup(
    name='hdr',
    version='0.0.1',
    description='A CLI utility for craeting hdr images.',
    long_description=readme + '\n\n' + changes,
    author="Sean Marlow",
    url='https://github.com/smarlowucf/hdr',
    packages=[
        'hdr',
    ],
    package_dir={'hdr':
                 'hdr'},
    entry_points={
        'console_scripts': [
            'hdr=hdr.cli:main'
        ]
    },
    install_requires=requirements,
    extras_require={
        'test': test_requirements,
    },
    license='GPLv3+',
    zip_safe=False,
    keywords='hdr',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
