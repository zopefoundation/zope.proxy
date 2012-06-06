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
from zope.interface import moduleProvides
from zope.proxy.interfaces import IProxyIntrospection
from zope.proxy._zope_proxy_proxy import ProxyBase
from zope.proxy._zope_proxy_proxy import getProxiedObject
from zope.proxy._zope_proxy_proxy import setProxiedObject
from zope.proxy._zope_proxy_proxy import isProxy
from zope.proxy._zope_proxy_proxy import sameProxiedObjects
from zope.proxy._zope_proxy_proxy import queryProxy
from zope.proxy._zope_proxy_proxy import queryInnerProxy
from zope.proxy._zope_proxy_proxy import removeAllProxies
from zope.proxy._zope_proxy_proxy import _CAPI

moduleProvides(IProxyIntrospection)
__all__ = tuple(IProxyIntrospection)

def ProxyIterator(p):
    yield p
    while isProxy(p):
        p = getProxiedObject(p)
        yield p

def non_overridable(func):
    return property(lambda self: func.__get__(self))
