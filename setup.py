# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in custom_scripts/__init__.py
from custom_scripts import __version__ as version

setup(
	name='custom_scripts',
	version=version,
	description='For custom scripts',
	author='C.R.I.O',
	author_email='criogroups@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
