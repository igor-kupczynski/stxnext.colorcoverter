#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages
setup(
    name = "stxnext.colorconverter",
    version = "0.1",
    packages = find_packages('src'),

	author = 'STX Next Sp. z o.o, Igor Kupczyński',
    author_email = 'info@stxnext.pl, igor.kupczynski@stxnext.pl',
	description = 'Converts one color to another one in an image',
    long_description = open('README').read(),
    keywords = 'python hsv color conversion',
    platforms = ['any'],
    url = 'http://stxnext.pl/',
    license = 'Zope Public License, Version 2.1 (ZPL)',
    include_package_data = True,
    package_dir = {'':'src'},
    namespace_packages = ['stxnext'],
    zip_safe = False,
    install_requires = ['setuptools']
)

