:mod:`zope.proxy` Narrative Documentation
=========================================

Subclassing :class:`ProxyBase`
------------------------------

If you subclass a proxy, instances of the subclass have access to
data defined in the class, including descriptors.

Your subclass instances don't get instance dictionaries, but they
can have slots.

.. doctest::

   >>> from zope.proxy import ProxyBase
   >>> class MyProxy(ProxyBase):
   ...    __slots__ = 'x', 'y'
   ...
   ...    def f(self):
   ...        return self.x

   >>> l = [1, 2, 3]
   >>> p = MyProxy(l)

You can use attributes defined by the class, including slots:

.. doctest::

   >>> p.x = 'x'
   >>> p.x
   'x'
   >>> p.f()
   'x'

You can also use attributes of the proxied object:

.. doctest::

   >>> p
   [1, 2, 3]
   >>> p.pop()
   3
   >>> p
   [1, 2]


Using get descriptors in proxy classes
--------------------------------------

A non-data descriptor in a proxy class doesn't hide an attribute on
a proxied object or prevent writing the attribute.

.. doctest::

    >>> class ReadDescr(object):
    ...     def __get__(self, i, c):
    ...         return 'read'

    >>> from zope.proxy import ProxyBase
    >>> class MyProxy(ProxyBase):
    ...    __slots__ = ()
    ...
    ...    z = ReadDescr()
    ...    q = ReadDescr()

    >>> class MyOb:
    ...    q = 1

    >>> o = MyOb()
    >>> p = MyProxy(o)
    >>> p.q
    1

    >>> p.z
    'read'

    >>> p.z = 1
    >>> o.z, p.z
    (1, 1)


Marking proxy attributes as non-overridable
-------------------------------------------

Normally, methods defined in proxies are overridden by
methods of proxied objects.  This applies to all non-data
descriptors.  The non_overridable function can be used to
convert a non-data descriptor to a data descriptor that disallows
writes.  This function can be used as a decorator to make functions
defined in proxy classes take precedence over functions defined
in proxied objects.

.. doctest::

   >>> from zope.proxy import ProxyBase
   >>> from zope.proxy import non_overridable
   >>> class MyProxy(ProxyBase):
   ...    __slots__ = ()
   ...
   ...    @non_overridable
   ...    def foo(self):
   ...        return 'MyProxy foo'

   >>> class MyOb:
   ...    def foo(self):
   ...        return 'MyOb foo'

   >>> o = MyOb()
   >>> p = MyProxy(o)
   >>> p.foo()
   'MyProxy foo'


Changing the proxied object
---------------------------

.. doctest::

   >>> from zope.proxy import ProxyBase
   >>> from zope.proxy import setProxiedObject, getProxiedObject

   >>> class C(object):
   ...     pass

   >>> c1 = C()
   >>> c2 = C()

   >>> p = ProxyBase(c1)

`setProxiedObject()` allows us to change the object a proxy refers to,
returning the previous referent:

.. doctest::

   >>> old = setProxiedObject(p, c2)
   >>> old is c1
   True

   >>> getProxiedObject(p) is c2
   True

The first argument  to `setProxiedObject()` must be a proxy; other objects
cause it to raise an exception:

.. doctest::

   >>> try:
   ...     setProxiedObject(c1, None)
   ... except TypeError:
   ...     print "TypeError raised"
   ... else:
   ...     print "Expected TypeError not raised"
   TypeError raised
