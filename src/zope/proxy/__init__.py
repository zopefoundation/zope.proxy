##############################################################################
#
# Copyright (c) 2003 Zope Foundation and Contributors.
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
"""More convenience functions for dealing with proxies.
"""
import operator
import pickle
import sys
import types

from zope.interface import moduleProvides
from zope.proxy.interfaces import IProxyIntrospection


moduleProvides(IProxyIntrospection)
__all__ = tuple(IProxyIntrospection)

def ProxyIterator(p):
    yield p
    while isProxy(p):
        p = getProxiedObject(p)
        yield p

def non_overridable(func):
    return property(lambda self: func.__get__(self))


class PyProxyBase(object):
    """Reference implementation.
    """
    __slots__ = ('_wrapped', )

    def __new__(cls, value):
        inst = super(PyProxyBase, cls).__new__(cls)
        inst._wrapped = value
        return inst

    def __init__(self, obj):
        self._wrapped = obj

    def __call__(self, *args, **kw):
        return self._wrapped(*args, **kw)

    def __repr__(self):
        return repr(self._wrapped)

    def __str__(self):
        return str(self._wrapped)

    def __unicode__(self):
        return unicode(self._wrapped)

    def __reduce__(self):
        raise pickle.PicklingError

    # Rich comparison protocol
    def __lt__(self, other):
        return self._wrapped < other

    def __le__(self, other):
        return self._wrapped <= other

    def __eq__(self, other):
        return self._wrapped == other

    def __ne__(self, other):
        return self._wrapped != other

    def __gt__(self, other):
        return self._wrapped > other

    def __ge__(self, other):
        return self._wrapped >= other

    def __nonzero__(self):
        return bool(self._wrapped)

    def __hash__(self):
        return hash(self._wrapped)

    # Attribute protocol
    def __getattr__(self, name):
        return getattr(self._wrapped, name)

    def __setattr__(self, name, value):
        if name == '_wrapped':
            return super(PyProxyBase, self).__setattr__(name, value)
        setattr(self._wrapped, name, value)

    def __delattr__(self, name):
        if name == '_wrapped':
            raise AttributeError()
        delattr(self._wrapped, name)

    # Container protocols

    def __len__(self):
        return len(self._wrapped)

    def __getitem__(self, key):
        if isinstance(key, types.SliceType):
            if isinstance(self._wrapped, (list, tuple)):
                return self._wrapped[key]
            start, stop = key.start, key.stop
            if start is None:
                start = 0
            if start < 0:
                start += len(self._wrapped)
            if stop is None:
                stop = sys.maxint
            if stop < 0:
                stop += len(self._wrapped)
            return operator.getslice(self._wrapped, start, stop)
        return self._wrapped[key]

    def __setitem__(self, key, value):
        self._wrapped[key] = value

    def __delitem__(self, key):
        del self._wrapped[key]

    def __iter__(self):
        for item in self._wrapped:
            yield item

    def next(self):
        # Called when we wrap an iterator itself.
        return self._wrapped.next()

    # Python 2.7 won't let the C wrapper support __reversed__ :(
    #def __reversed__(self):
    #    return reversed(self._wrapped)

    def __contains__(self, item):
        return item in self._wrapped

    # Numeric protocol:  unary operators
    def __neg__(self):
        return -self._wrapped

    def __pos__(self):
        return +self._wrapped

    def __abs__(self):
        return abs(self._wrapped)

    def __invert__(self):
        return ~self._wrapped

    # Numeric protocol:  unary conversions
    def __complex__(self):
        return complex(self._wrapped)

    def __int__(self):
        return int(self._wrapped)

    def __long__(self):
        return long(self._wrapped)

    def __float__(self):
        return float(self._wrapped)

    def __oct__(self):
        return oct(self._wrapped)

    def __hex__(self):
        return hex(self._wrapped)

    def __index__(self):
        return operator.index(self._wrapped)

    # Numeric protocol:  binary coercion
    def __coerce__(self, other):
        left, right = coerce(self._wrapped, other)
        if left == self._wrapped and type(left) is type(self._wrapped):
            left = self
        return left, right

    # Numeric protocol:  binary arithmetic operators
    def __add__(self, other):
        return self._wrapped + other

    def __sub__(self, other):
        return self._wrapped - other

    def __mul__(self, other):
        return self._wrapped * other

    def __floordiv__(self, other):
        return self._wrapped // other

    def __truediv__(self, other): #pragma NO COVER
        # Only one of __truediv__ and __div__ is meaningful at any one time.
        return self._wrapped / other

    def __div__(self, other): #pragma NO COVER
        # Only one of __truediv__ and __div__ is meaningful at any one time.
        return self._wrapped / other

    def __mod__(self, other):
        return self._wrapped % other

    def __divmod__(self, other):
        return divmod(self._wrapped, other)

    def __pow__(self, other, modulus=None):
        if modulus is None:
            return pow(self._wrapped, other)
        return pow(self._wrapped, other, modulus)

    def __radd__(self, other):
        return other + self._wrapped

    def __rsub__(self, other):
        return other - self._wrapped

    def __rmul__(self, other):
        return other * self._wrapped

    def __rfloordiv__(self, other):
        return other // self._wrapped

    def __rtruediv__(self, other): #pragma NO COVER
        # Only one of __rtruediv__ and __rdiv__ is meaningful at any one time.
        return other / self._wrapped

    def __rdiv__(self, other): #pragma NO COVER
        # Only one of __rtruediv__ and __rdiv__ is meaningful at any one time.
        return other / self._wrapped

    def __rmod__(self, other):
        return other % self._wrapped

    def __rdivmod__(self, other):
        return divmod(other, self._wrapped)

    def __rpow__(self, other, modulus=None):
        if modulus is None:
            return pow(other, self._wrapped)
        # We can't actually get here, because we can't lie about our type()
        return pow(other, self._wrapped, modulus) #pragma NO COVER

    # Numeric protocol:  binary bitwise operators
    def __lshift__(self, other):
        return self._wrapped << other

    def __rshift__(self, other):
        return self._wrapped >> other

    def __and__(self, other):
        return self._wrapped & other

    def __xor__(self, other):
        return self._wrapped ^ other

    def __or__(self, other):
        return self._wrapped | other

    def __rlshift__(self, other):
        return other << self._wrapped

    def __rrshift__(self, other):
        return other >> self._wrapped

    def __rand__(self, other):
        return other & self._wrapped

    def __rxor__(self, other):
        return other ^ self._wrapped

    def __ror__(self, other):
        return other | self._wrapped

    # Numeric protocol:  binary in-place operators
    def __iadd__(self, other):
        self._wrapped += other
        return self

    def __isub__(self, other):
        self._wrapped -= other
        return self

    def __imul__(self, other):
        self._wrapped *= other
        return self

    def __idiv__(self, other): #pragma NO COVER
        # Only one of __itruediv__ and __idiv__ is meaningful at any one time.
        self._wrapped /= other
        return self

    def __itruediv__(self, other): #pragma NO COVER
        # Only one of __itruediv__ and __idiv__ is meaningful at any one time.
        self._wrapped /= other
        return self

    def __ifloordiv__(self, other):
        self._wrapped //= other
        return self

    def __imod__(self, other):
        self._wrapped %= other
        return self

    def __ilshift__(self, other):
        self._wrapped <<= other
        return self

    def __irshift__(self, other):
        self._wrapped >>= other
        return self

    def __iand__(self, other):
        self._wrapped &= other
        return self

    def __ixor__(self, other):
        self._wrapped ^= other
        return self

    def __ior__(self, other):
        self._wrapped |= other
        return self

    def __ipow__(self, other, modulus=None):
        if modulus is None:
            self._wrapped **= other
        else: #pragma NO COVER
            # There is no syntax which triggers in-place pow w/ modulus
            self._wrapped = pow(self._wrapped, other, modulus)
        return self

def py_getProxiedObject(obj):
    if isinstance(obj, PyProxyBase):
        return obj._wrapped
    return obj

def py_setProxiedObject(obj, new_value):
    if not isinstance(obj, PyProxyBase):
        raise TypeError('Not a proxy')
    old, obj._wrapped = obj._wrapped, new_value
    return old

def py_isProxy(obj, klass=None):
    if klass is None:
        klass = PyProxyBase
    return isinstance(obj, klass)

def py_sameProxiedObjects(lhs, rhs):
    while isinstance(lhs, PyProxyBase):
        lhs = lhs._wrapped
    while isinstance(rhs, PyProxyBase):
        rhs = rhs._wrapped
    return lhs is rhs

def py_queryProxy(obj, klass=None, default=None):
    if klass is None:
        klass = PyProxyBase
    while obj is not None and not isinstance(obj, klass):
        obj = getattr(obj, '_wrapped', None)
    if obj is not None:
        return obj
    return default

def py_queryInnerProxy(obj, klass=None, default=None):
    if klass is None:
        klass = PyProxyBase
    found = []
    while obj is not None:
        if isinstance(obj, klass):
            found.append(obj) # stack
        obj = getattr(obj, '_wrapped', None)
    if found:
        return found[-1]
    return default

def py_removeAllProxies(obj):
    while isinstance(obj, PyProxyBase):
        obj = obj._wrapped
    return obj

try:
    # Python API:  not used in this module
    from zope.proxy._zope_proxy_proxy import ProxyBase
    from zope.proxy._zope_proxy_proxy import getProxiedObject
    from zope.proxy._zope_proxy_proxy import setProxiedObject
    from zope.proxy._zope_proxy_proxy import isProxy
    from zope.proxy._zope_proxy_proxy import sameProxiedObjects
    from zope.proxy._zope_proxy_proxy import queryProxy
    from zope.proxy._zope_proxy_proxy import queryInnerProxy
    from zope.proxy._zope_proxy_proxy import removeAllProxies

    # API for proxy-using C extensions.
    from zope.proxy._zope_proxy_proxy import _CAPI
except ImportError: #pragma NO COVER
    # no C extension available, fall back
    ProxyBase = PyProxyBase
    getProxiedObject = py_getProxiedObject
    setProxiedObject = py_setProxiedObject
    isProxy = py_isProxy
    sameProxiedObjects = py_sameProxiedObjects
    queryProxy = py_queryProxy
    queryInnerProxy = py_queryInnerProxy
    removeAllProxies = py_removeAllProxies
