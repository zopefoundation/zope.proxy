##############################################################################
#
# Copyright (c) 2006-2008 Zope Corporation and Contributors.
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
"""Setup for zope.proxy package

$Id$
"""
import os
from setuptools import setup, Extension

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(name='zope.proxy',
      version = '3.5.0dev',
      author='Zope Corporation and Contributors',
      author_email='zope-dev@zope.org',
      description='Generic Transparent Proxies',
      long_description=(
          read('README.txt')
          + '\n\n' +
# Waaa   'Detailed Documentation\n'
#        '----------------------\n'
#       + '\n\n' +
          read('CHANGES.txt')
          ),
      url='http://pypi.python.org/pypi/zope.proxy',
      license='ZPL 2.1',
      classifiers = [
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
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

      extras_require=dict(
          test=['zope.testing']),
      tests_require = [
          'zope.testing'],
      test_suite = 'zope.proxy',
      install_requires=[
          'zope.interface',
          'setuptools'],
      include_package_data = True,
      zip_safe = False,
      )
