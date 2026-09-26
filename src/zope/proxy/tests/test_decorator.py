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
        from zope.interface import implementer
        from zope.interface import provider

        class IContextFactory(Interface):
            pass

        class IContext(Interface):
            pass

        @provider(IContextFactory)
        @implementer(IContext)
        class Context:
            pass
        dsd = self._makeOne()
        self.assertEqual(list(dsd.__get__(None, Context)), [IContextFactory])

    def test___get___w_inst_no_proxy(self):
        from zope.interface import Interface
        from zope.interface import implementer
        from zope.interface import provider

        class IContextFactory(Interface):
            pass

        class IContext(Interface):
            pass

        @provider(IContextFactory)
        @implementer(IContext)
        class Context:
            pass
        dsd = self._makeOne()
        self.assertEqual(list(dsd.__get__(Context(), None)), [IContext])

    def test___get___w_inst_w_proxy(self):
        from zope.interface import Interface
        from zope.interface import implementer
        from zope.interface import provider

        from zope.proxy import ProxyBase

        class IContextFactory(Interface):
            pass

        class IContext(Interface):
            pass

        @provider(IContextFactory)
        @implementer(IContext)
        class Context:
            pass
        context = Context()
        proxy = ProxyBase(context)
        dsd = self._makeOne()
        self.assertEqual(list(dsd.__get__(proxy, None)), [IContext])

    def test___get___w_inst_w_derived_proxy(self):
        from zope.interface import Interface
        from zope.interface import implementer
        from zope.interface import provider

        from zope.proxy import ProxyBase

        class IContextFactory(Interface):
            pass

        class IContext(Interface):
            pass

        @provider(IContextFactory)
        @implementer(IContext)
        class Context:
            pass

        class IProxyFactory(Interface):
            pass

        class IProxy(Interface):
            pass

        @provider(IProxyFactory)
        @implementer(IProxy)
        class Proxy(ProxyBase):
            pass
        context = Context()
        proxy = Proxy(context)
        dsd = self._makeOne()
        self.assertEqual(list(dsd.__get__(proxy, None)),
                         [IContext, IProxy])

    def test___set___not_allowed(self):
        from zope.interface import Interface
        from zope.interface import implementer

        class IFoo(Interface):
            pass

        @implementer(IFoo)
        class Foo:
            pass
        foo = Foo()
        dsd = self._makeOne()
        self.assertRaises(TypeError, dsd.__set__, foo, object())

    def test___get___w_nested_decorators_sharing_a_base(self):
        # Wrapping a decorated object with a second decorator whose
        # class shares a common base with the first decorator's class
        # (and hence shares an implemented interface) must not raise
        # an InconsistentResolutionOrderError, even when zope.interface
        # is running with strict interface resolution order checking.
        # See https://github.com/zopefoundation/zope.proxy/issues/41
        from zope.interface import Interface
        from zope.interface import implementer
        from zope.interface import providedBy

        from zope.proxy.decorator import SpecificationDecoratorBase

        class IBase(Interface):
            pass

        class I1(Interface):
            pass

        class I2(Interface):
            pass

        class IContext(Interface):
            pass

        @implementer(IBase)
        class BaseDecorator(SpecificationDecoratorBase):
            pass

        @implementer(I1)
        class D1(BaseDecorator):
            pass

        @implementer(I2)
        class D2(BaseDecorator):
            pass

        @implementer(IContext)
        class Context:
            pass

        context = Context()
        # This should not raise, and I2 should come before the
        # interfaces contributed by the shared base class.
        result = list(providedBy(D2(D1(context))))
        self.assertEqual(
            result, [IContext, I1, I2, IBase])


class SpecificationDecoratorBaseTests(unittest.TestCase):

    def _getTargetClass(self):
        from zope.proxy.decorator import SpecificationDecoratorBase
        return SpecificationDecoratorBase

    def _makeOne(self, wrapped):
        return self._getTargetClass()(wrapped)

    def test_wrapped_instance(self):
        from zope.interface import Interface
        from zope.interface import implementer
        from zope.interface import providedBy

        class IFoo(Interface):
            pass

        @implementer(IFoo)
        class Foo:
            pass
        foo = Foo()
        proxy = self._makeOne(foo)
        self.assertEqual(list(providedBy(proxy)), list(providedBy(foo)))

    def test_proxy_that_provides_interface_as_well_as_wrapped(self):
        # If both the wrapper and the wrapped object provide
        # interfaces, the wrapper provides the sum
        from zope.interface import Interface
        from zope.interface import implementer
        from zope.interface import providedBy

        class IFoo(Interface):
            pass

        @implementer(IFoo)
        class Foo:
            from_foo = 1

        class IWrapper(Interface):
            pass

        @implementer(IWrapper)
        class Proxy(self._getTargetClass()):
            pass

        foo = Foo()
        proxy = Proxy(foo)

        self.assertEqual(proxy.from_foo, 1)
        self.assertEqual(list(providedBy(proxy)), [IFoo, IWrapper])


def test_suite():
    return unittest.TestSuite((
        unittest.defaultTestLoader.loadTestsFromTestCase(
            DecoratorSpecificationDescriptorTests),
        unittest.defaultTestLoader.loadTestsFromTestCase(
            SpecificationDecoratorBaseTests),
    ))
