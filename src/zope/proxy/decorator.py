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
"""Decorator support

Decorators are proxies that are mostly transparent but that may provide
additional features.
"""
__docformat__ = "reStructuredText"

from zope.interface import implementedBy
from zope.interface import providedBy
from zope.interface.declarations import ObjectSpecificationDescriptor
from zope.interface.declarations import Provides
from zope.interface.declarations import getObjectSpecification

from zope.proxy import ProxyBase
from zope.proxy import getProxiedObject


class DecoratorSpecificationDescriptor(ObjectSpecificationDescriptor):
    """Support for interface declarations on decorators
    """

    def __get__(self, inst, cls=None):
        if inst is None:
            return getObjectSpecification(cls)
        else:
            provided = providedBy(getProxiedObject(inst))

            # Use type rather than __class__ because inst is a proxy and
            # will return the proxied object's class.
            cls = type(inst)

            # Don't repeat interfaces already implemented by the
            # decorator class itself (usually through inheritance from
            # a common base). Otherwise, nesting two decorators that
            # share such a base can produce an inconsistent interface
            # resolution order. See
            # https://github.com/zopefoundation/zope.proxy/issues/41
            implemented_by_cls = implementedBy(cls)
            for iface in list(provided):
                if implemented_by_cls.isOrExtends(iface):
                    provided = provided - iface
            return Provides(cls, provided)

    def __set__(self, inst, value):
        raise TypeError("Can't set __providedBy__ on a decorated object")


class SpecificationDecoratorBase(ProxyBase):
    """Base class for a proxy that provides additional interfaces."""

    __providedBy__ = DecoratorSpecificationDescriptor()
