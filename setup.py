##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
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

long_description=(
        read('README.txt')
        + '\n' +
# Waaa  'Detailed Documentation\n'
#       '**********************\n'
#       + '\n' +
#       + '\n' +
        'Download\n'
        '**********************\n'
        )

open('doc.txt', 'w').write(long_description)

name = 'zope.proxy'
setup(name=name,
      version = '3.4.0',
      url='http://www.python.org/pypi/'+name,
      license='ZPL 2.1',
      description='Generic Transparent Proxies',
      author='Zope Corporation and Contributors',
      author_email='zope3-dev@zope.org',
      long_description=long_description,
      
      packages=['zope', 'zope.proxy'],
      package_dir = {'': 'src'},

      headers=[os.path.join('src', 'zope', 'proxy', 'proxy.h')],
      ext_modules=[Extension("zope.proxy._zope_proxy_proxy",
                             [os.path.join('src', 'zope', 'proxy',
                                           "_zope_proxy_proxy.c")
                              ]),
                   ],

      namespace_packages=['zope',],
      tests_require = ['zope.testing'],
      install_requires=['zope.interface', 'setuptools'],
      include_package_data = True,
      zip_safe = False,
      )
