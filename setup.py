#!/usr/bin/env python

from setuptools import setup

setup(name='python-contact-importer',
    version='0.1',
    description='Allows to export user contacts from Google, Yahoo! and Hotmail.',
    author='Millioner',
    author_email='millioner.bbb@gmail.com',
    url='https://github.com/millioner/Python-contact-importer',
    packages=['contact_importer', ],
    include_package_data = True,    # include everything in source control
    zip_safe=False,
    install_requires=['PyCrypto', 'oauth2', ],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Development Status :: 4 - Beta",
        'Environment :: Web Environment',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Social Integration",
        "Framework :: Django",
        ],
    long_description = """\
Allows to export user contacts from Google, Yahoo! and Hotmail. Uses OAuth protocol for working with Google and Yahoo!. And Microsoft's "Delegated authentification" for Hotmail.
"""
)
