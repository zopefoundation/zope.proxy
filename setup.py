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
from __future__ import print_function
import os
import platform


from distutils.errors import CCompilerError
from distutils.errors import DistutilsExecError
from distutils.errors import DistutilsPlatformError

from setuptools import Extension
from setuptools.command.build_ext import build_ext
from setuptools import setup
from setuptools import Feature


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


Cwrapper = Feature(
    "C wrapper",
    standard=True,
    headers=[os.path.join('src', 'zope', 'proxy', 'proxy.h')],
    ext_modules=[
        Extension(
            "zope.proxy._zope_proxy_proxy",
            [os.path.join('src', 'zope', 'proxy', "_zope_proxy_proxy.c")],
        ),
    ],
)

# PyPy won't build the extension.
is_pypy = platform.python_implementation() == 'PyPy'
if is_pypy:
    features = {}
else:
    features = {'Cwrapper': Cwrapper}

setup(name='zope.proxy',
      version='4.3.1',
      author='Zope Foundation and Contributors',
      author_email='zope-dev@zope.org',
      description='Generic Transparent Proxies',
      long_description=(
          read('README.rst')
          + '\n\n' +
          read('CHANGES.rst')
      ),
      url='http://github.com/zopefoundation/zope.proxy',
      license='ZPL 2.1',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Zope Public License',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: Implementation :: CPython',
          'Programming Language :: Python :: Implementation :: PyPy',
          "Framework :: Zope3",
          'Natural Language :: English',
          'Operating System :: OS Independent'
      ],
      keywords='proxy generic transparent',
      packages=['zope', 'zope.proxy'],
      package_dir={'': 'src'},
      namespace_packages=['zope'],
      cmdclass={
          'build_ext': optional_build_ext,
      },
      features=features,
      install_requires=[
          'zope.interface',
          'setuptools',
      ],
      include_package_data=True,
      zip_safe=False,
      extras_require={
          'test': [
              'zope.security',  # We have a circular dependency for testing
              'zope.testrunner',
          ],
          'docs': [
              'Sphinx',
              'repoze.sphinx.autointerface',
          ],
      },
)
