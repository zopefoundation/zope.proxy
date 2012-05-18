##############################################################################
#
# Copyright (c) 2006-2008 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
# This package is developed by the Zope Toolkit project, documented here:
# http://docs.zope.org/zopetoolkit
# When developing and releasing this package, please follow the documented
# Zope Toolkit policies as described by this documentation.
##############################################################################
"""Setup for zope.proxy package
"""
import os, sys
from setuptools import setup, Extension

if sys.version_info >= (3,):
    extra = dict(use_2to3 = True,
                 convert_2to3_doctests = [
                     'src/zope/i18nmessageid/messages.txt',
                     ],
                 )
else:
    extra = {}

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='zope.proxy',
      version = '4.0.0dev',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      description='Generic Transparent Proxies',
      long_description=(
          read('README.txt')
          + '\n\n' +
          read('CHANGES.txt')
          ),
      url='http://pypi.python.org/pypi/zope.proxy',
      license='ZPL 2.1',
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.2',
          'Natural Language :: English',
          'Operating System :: OS Independent'],
      keywords='proxy generic transparent',
      packages=['zope', 'zope.proxy'],
      package_dir = {'': 'src'},
      namespace_packages=['zope',],

      headers=[os.path.join('src', 'zope', 'proxy', 'proxy.h')],
      ext_modules=[Extension("zope.proxy._zope_proxy_proxy",
                             [os.path.join('src', 'zope', 'proxy',
                                           "_zope_proxy_proxy.c")
                              ]),
                   ],

      test_suite = 'zope.proxy',
      install_requires=[
          'zope.interface',
          'setuptools'],
      include_package_data = True,
      zip_safe = False,
      **extra
      )
