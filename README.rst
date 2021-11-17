================
 ``zope.proxy``
================

.. image:: https://img.shields.io/pypi/v/zope.proxy.svg
    :target: https://pypi.python.org/pypi/zope.proxy/
    :alt: Latest Version

.. image:: https://github.com/zopefoundation/zope.proxy/actions/workflows/tests.yml/badge.svg
        :target: https://github.com/zopefoundation/zope.proxy/actions/workflows/tests.yml

.. image:: https://readthedocs.org/projects/zopeproxy/badge/?version=latest
        :target: http://zopeproxy.readthedocs.org/en/latest/
        :alt: Documentation Status

Proxies are special objects which serve as mostly-transparent
wrappers around another object, intervening in the apparent behavior of
the wrapped object only when necessary to apply the policy (e.g., access
checking, location brokering, etc.) for which the proxy is responsible.

zope.proxy is implemented via a C extension module, which lets it do things
like lie about its own ``__class__`` that are difficult in pure Python (and
were completely impossible before metaclasses).  It also proxies all the
internal slots (such as ``__int__``/``__str__``/``__add__``).

Complete documentation is at https://zopeproxy.readthedocs.io
