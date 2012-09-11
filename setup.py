#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

from distutils.core import setup
import setuptools

setup(
  name='pyedsl',
  version='0.1.1',
  description='Simple Python Embedded DSL framework.',
  author='Grigory Petrov',
  author_email='grigory.v.p@gmail.com',
  url='http://bitbucket.org/eyeofhell/pyedsl/',
  packages=[ 'pyedsl' ],
  classifiers=[
    'Development Status :: 1 - Prototype',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: GPLv3',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Framework' ])

