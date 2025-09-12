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

import os
import platform
from distutils.errors import CCompilerError
from distutils.errors import DistutilsExecError
from distutils.errors import DistutilsPlatformError

from setuptools import Extension
from setuptools import setup
from setuptools.command.build_ext import build_ext


version = '7.0'


class optional_build_ext(build_ext):
    """This class subclasses build_ext and allows
       the building of C extensions to fail.
    """

    def run(self):
        try:
            build_ext.run(self)
        except DistutilsPlatformError as e:
            self._unavailable(e)

    def build_extension(self, ext):
        try:
            build_ext.build_extension(self, ext)
        except (CCompilerError, DistutilsExecError, OSError) as e:
            self._unavailable(e)

    def _unavailable(self, e):
        print('*' * 80)
        print("""WARNING:
        An optional code optimization (C extension) could not be compiled.
        Optimizations for this package will not be available!""")
        print()
        print(e)
        print('*' * 80)


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames)) as f:
        return f.read()


codeoptimization = [
    Extension(
        "zope.proxy._zope_proxy_proxy",
        [os.path.join('src', 'zope', 'proxy', "_zope_proxy_proxy.c")],
    ),
]

# PyPy won't build the extension.
is_pypy = platform.python_implementation() == 'PyPy'
if is_pypy:
    ext_modules = []
    headers = []
else:
    ext_modules = codeoptimization
    headers = [os.path.join('src', 'zope', 'proxy', 'proxy.h')]

setup(name='zope.proxy',
      version=version,
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.dev',
      description='Generic Transparent Proxies',
      long_description=(
          read('README.rst')
          + '\n\n' +
          read('CHANGES.rst')
      ),
      url='http://github.com/zopefoundation/zope.proxy',
      project_urls={
          'Documentation': 'https://zopeproxy.readthedocs.io',
          'Issue Tracker': 'https://github.com/zopefoundation/'
                           'zope.proxy/issues',
          'Sources': 'https://github.com/zopefoundation/zope.proxy',
      },
      license='ZPL-2.1',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Programming Language :: Python :: 3.13',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          'Framework :: Zope :: 3',
          'Natural Language :: English',
          'Operating System :: OS Independent',
      ],
      keywords='proxy generic transparent',
      # we need the following two parameters because we compile C code,
      # otherwise only the shared library is installed:
      package_dir={'': 'src'},
      packages=['zope.proxy'],
      cmdclass={
          'build_ext': optional_build_ext,
      },
      headers=headers,
      ext_modules=ext_modules,
      python_requires='>=3.9',
      install_requires=[
          'zope.interface',
          'setuptools',
      ],
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'test': [
              # We have a circular dependency with zope.security for testing
              'zope.security >= 7.3',
              'zope.testrunner >= 6.4',
          ],
          'docs': [
              'Sphinx',
              'repoze.sphinx.autointerface',
              'sphinx_rtd_theme',
          ],
      },
      )
