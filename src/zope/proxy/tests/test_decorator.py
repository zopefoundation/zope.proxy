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
"""Test Harness
"""
import unittest


class DecoratorSpecificationDescriptorTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.proxy.decorator import DecoratorSpecificationDescriptor
        return DecoratorSpecificationDescriptor

    def _makeOne(self):
        return self._getTargetClass()()

    def test___get___w_class(self):
        from zope.interface import Interface
        from zope.interface import provider
        class IFoo(Interface):
            pass
        @provider(IFoo)
        class Foo(object):
            pass
        dsd = self._makeOne()
        self.assertEqual(list(dsd.__get__(None, Foo)), [IFoo])

    def test___get___w_inst_no_proxy(self):
        from zope.interface import Interface
        from zope.interface import implementer
        class IFoo(Interface):
            pass
        @implementer(IFoo)
        class Foo(object):
            pass
        dsd = self._makeOne()
        self.assertEqual(list(dsd.__get__(Foo(), None)), [IFoo])

    def test___get___w_inst_w_proxy(self):
        from zope.interface import Interface
        from zope.interface import implementer
        from zope.proxy import ProxyBase
        class IFoo(Interface):
            pass
        @implementer(IFoo)
        class Foo(object):
            pass
        foo = Foo()
        p_foo = ProxyBase(foo)
        dsd = self._makeOne()
        self.assertEqual(list(dsd.__get__(p_foo, None)), [IFoo])

    def test___set___not_allowed(self):
        from zope.interface import Interface
        from zope.interface import implementer
        class IFoo(Interface):
            pass
        @implementer(IFoo)
        class Foo(object):
            pass
        foo = Foo()
        dsd = self._makeOne()
        self.assertRaises(TypeError, dsd.__set__, foo, object())


def test_suite():
    return unittest.TestSuite((
    ))
