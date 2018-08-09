Changes
=======

4.3.1 (2018-08-09)
------------------

- Simplify the internal C handling of attribute names in
  ``__getattribute__`` and ``__setattr__``.

- Make building the C extension optional. We still attempt to build it
  on supported platforms, but we allow it to fail in case of a missing
  compiler or headers. See `issue 26
  <https://github.com/zopefoundation/zope.proxy/issues/26>`_.

- Test the PURE_PYTHON environment and PyPy3 on Travis CI.

- Add support for Python 3.7.

4.3.0 (2017-09-13)
------------------

- Fix a potential rare crash when deallocating proxies. See `issue 20
  <https://github.com/zopefoundation/zope.proxy/issues/20>`_.

- Drop support for Python 3.3.

- Drop support for "python setup.py test".

- 100% test coverage.

- Fix indexing pure-Python proxies with slices under Python 3, and
  restore the use of ``__getslice__`` (if implemented by the target's
  type) under Python 2. Previously, pure-Python proxies would fail
  with an AttributeError when given a slice on Python 3, and on Python
  2, a custom ``__getslice__`` was ignored. See `issue 21
  <https://github.com/zopefoundation/zope.proxy/issues/21>`_.

4.2.1 (2017-04-23)
------------------

- Make the pure-Python implementation of ``sameProxiedObjects`` handle
  ``zope.security`` proxies. See `issue 15 <https://github.com/zopefoundation/zope.proxy/issues/15>`_.

- Add support for Python 3.6.

4.2.0 (2016-05-05)
------------------

- Correctly strip ``zope.security`` proxies in ``removeAllProxies``.
  See `issue 13 <https://github.com/zopefoundation/zope.proxy/pull/13>`_.

- Avoid poisoning the user's global wheel cache when testing ``PURE_PYTHON``
  environments under ``tox``,

- Drop support for Python 2.6 and 3.2.

- Add support for Python 3.5.

4.1.6 (2015-06-02)
------------------

- Make subclasses of ProxyBase properly delegate ``__module__`` to the
  wrapped object. This fixes some ``zope.interface`` lookups under
  PyPy.

- Make the pure-Python implementation of ProxyBase properly report the
  ``zope.interface`` interfaces implemented by builtin types like
  ``list``. This fixes some ``zope.interface`` lookups under PyPy.

4.1.5 (2015-05-19)
------------------

- Make the C implementation proxy ``__unicode__`` correctly.

- Make the C implementation use the standard methods to proxy ``int`` and
  ``float``.

- Make the pure Python implementation handle descriptors defined in
  subclasses like the C version. See
  https://github.com/zopefoundation/zope.proxy/issues/5.

4.1.4 (2014-03-19)
------------------

- Add support for Python 3.4.

- Update ``bootstrap.py`` to version 2.2.

4.1.3 (2013-03-12)
------------------

- Fix interface object introspection in PyPy. For some reason PyPy makes
  attributes available despite the restrictive ``__slots__`` declaration.

- Add a bunch of tests surrounding interface lookup and adaptation.

4.1.2 (2013-03-11)
------------------

- Make ``PyProxyBase.__iter__()`` return the result of
  ``PyProxyBase._wrapped.__iter__`` if available, otherwise falling back to
  Python internals. The previous implementation always created a generator.

- In ``PyProxyBase.__setattr__()``, allow setting of properties on the
  proxy itself. This is needed to properly allow proxy extensions as was
  evidenced int he ``zope.security.decorator`` module.

4.1.1 (2012-12-31)
------------------

- Fleshed out PyPI Trove classifiers.

4.1.0 (2012-12-19)
------------------

- Enable compilation of dependent modules under Py3k.

- Replace use of ``PyCObject`` APIs with equivalent ``PyCapsule`` APIs,
  except under Python 2.6.

  N.B.  This change is an ABI incompatibility under Python 2.7:
        extensions built under Python 2.7 against 4.0.x versions of
        ``zope.proxy`` must be rebuilt.

4.0.1 (2012-11-21)
------------------

- Add support for Python 3.3.

4.0.0 (2012-06-06)
------------------

- Add support for PyPy.

  N.B.:  the C extension is *not* built under PyPy.

- Add a pure-Python reference / fallback implementations of
  ``zope.proxy.ProxyBase`` and the proxy module API functions.

  N.B.:  the pure-Python proxy implements all regular features of
  ``ProxyBase``;  however, it does not exclude access to the wrapped object
  in the same way that the C version does.  If you need that information
  hiding (e.g., to implement security sandboxing), you still need to use
  the C version.

- Add support for continuous integration using ``tox`` and ``jenkins``.

- 100% unit test coverage.

- Add Sphinx documentation:  moved doctest examples to API reference.

- Add 'setup.py docs' alias (installs ``Sphinx`` and dependencies).

- Add 'setup.py dev' alias (runs ``setup.py develop`` plus installs
  ``nose`` and ``coverage``).

- Replace deprecated ``zope.interface.implements`` usage with equivalent
  ``zope.interface.implementer`` decorator.

- Drop support for Python 2.4 and 2.5.

- Add Python 3.2 support.

3.6.1 (2010-07-06)
------------------

- Make tests compatible with Python 2.7.

3.6.0 (2010-04-30)
------------------

- Remove test extra and the remaining dependency on zope.testing.

- Remove use of 'zope.testing.doctestunit' in favor of stdlib's 'doctest.

3.5.0 (2009/01/31)
------------------

- Add support to bootstrap on Jython.

- Use ``zope.container`` instead of ``zope.app.container``.

3.4.2 (2008/07/27)
------------------

- Make C code compatible with Python 2.5 on 64bit architectures.

3.4.1 (2008/06/24)
------------------

- Bug: Update ``setup.py`` script to conform to common layout. Also updated
  some of the fields.

- Bug: Honor pre-cooked indices for tuples and lists in the ``__getslice__()``
  and ``__setslice__()`` methods. See
  http://docs.python.org/ref/sequence-methods.html.

3.4.0 (2007/07/12)
------------------

- Feature: Add a ``decorator`` module that supports declaring interfaces on
  proxies that get blended with the interfaces of the things they proxy.

3.3.0 (2006/12/20)
------------------

- Corresponds to the verison of the ``zope.proxy`` package shipped as part of
  the Zope 3.3.0 release.


3.2.0 (2006/01/05)
------------------

- Corresponds to the verison of the ``zope.proxy`` package shipped as part of
  the Zope 3.2.0 release.


3.0.0 (2004/11/07)
------------------

- Corresponds to the verison of the ``zope.proxy`` package shipped as part of
  the Zope X3.0.0 release.
