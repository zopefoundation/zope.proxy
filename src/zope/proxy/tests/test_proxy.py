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
"""Test base proxy class.
"""
import unittest


class ModuleConformanceCase(unittest.TestCase):

    def test_module_conforms_to_IProxyIntrospection(self):
        from zope.interface.verify import verifyObject
        import zope.proxy
        from zope.proxy.interfaces import IProxyIntrospection
        verifyObject(IProxyIntrospection, zope.proxy)


class ProxyBaseTestCase(unittest.TestCase):

    @property
    def proxy_class(self):
        from zope.proxy import ProxyBase
        return ProxyBase

    def setUp(self):
        self.x = Thing()
        self.p = self.new_proxy(self.x)

    def new_proxy(self, o):
        return self.proxy_class(o)

    def test_constructor(self):
        o = object()
        self.assertRaises(TypeError, self.proxy_class, o, o)
        self.assertRaises(TypeError, self.proxy_class, o, key='value')
        self.assertRaises(TypeError, self.proxy_class, key='value')

    def test_subclass_constructor(self):
        class MyProxy(self.proxy_class):
            def __new__(cls, *args, **kwds):
                return super(MyProxy, cls).__new__(cls, *args, **kwds)
            def __init__(self, *args, **kwds):
                super(MyProxy, self).__init__(*args, **kwds)
        o1 = object()
        o2 = object()
        o = MyProxy((o1, o2))

        self.assertEquals(o1, o[0])
        self.assertEquals(o2, o[1])

        self.assertRaises(TypeError, MyProxy, o1, o2)
        self.assertRaises(TypeError, MyProxy, o1, key='value')
        self.assertRaises(TypeError, MyProxy, key='value')

        # Check that are passed to __init__() overrides what's passed
        # to __new__().
        class MyProxy2(self.proxy_class):
            def __new__(cls, *args, **kwds):
                return super(MyProxy2, cls).__new__(cls, 'value')

        p = MyProxy2('splat!')
        self.assertEquals(list(p), list('splat!'))

        class MyProxy3(MyProxy2):
            def __init__(self, arg):
                if list(self) != list('value'):
                    raise AssertionError("list(self) != list('value')")
                super(MyProxy3, self).__init__('another')

        p = MyProxy3('notused')
        self.assertEquals(list(p), list('another'))

    def test_proxy_attributes(self):
        o = Thing()
        o.foo = 1
        w = self.new_proxy(o)
        self.assert_(w.foo == 1)

    def test___class__(self):
        o = object()
        w = self.new_proxy(o)
        self.assert_(w.__class__ is o.__class__)

    def test_pickle_prevention(self):
        import pickle
        from zope.proxy._compat import PY3
        # Proxies of old-style classes can't be pickled.
        if not PY3: # No old-style classes in Python 3.
            w = self.new_proxy(Thing())
            self.assertRaises(pickle.PicklingError,
                            pickle.dumps, w)

    def test_proxy_equality(self):
        w = self.new_proxy('foo')
        self.assertEquals(w, 'foo')

        o1 = Comparable(1)
        o2 = Comparable(1.0)
        o3 = Comparable("splat!")

        w1 = self.new_proxy(o1)
        w2 = self.new_proxy(o2)
        w3 = self.new_proxy(o3)

        self.assertEquals(o1, w1)
        self.assertEquals(o1, w2)
        self.assertEquals(o2, w1)
        self.assertEquals(w1, o2)
        self.assertEquals(w2, o1)

        self.assertNotEquals(o3, w1)
        self.assertNotEquals(w1, o3)
        self.assertNotEquals(w3, o1)
        self.assertNotEquals(o1, w3)

    def test_proxy_ordering_lt(self):
        o1 = Comparable(1)
        o2 = Comparable(2.0)

        w1 = self.new_proxy(o1)
        w2 = self.new_proxy(o2)

        self.assert_(w1 < w2)
        self.assert_(w1 <= w2)
        self.assert_(o1 < w2)
        self.assert_(o1 <= w2)
        self.assert_(w1 < o2)
        self.assert_(w2 <= o2)

    def test_proxy_callable(self):
        from zope.proxy._compat import PY3
        if not PY3: # Gone in Python 3:
            w = self.new_proxy({}.get)
            self.assert_(callable(w))

    def test_proxy_item_protocol(self):
        w = self.new_proxy({})
        self.assertRaises(KeyError, lambda: w[1])
        w[1] = 'a'
        self.assertEquals(w[1], 'a')
        del w[1]
        self.assertRaises(KeyError, lambda: w[1])
        def del_w_1():
            del w[1]
        self.assertRaises(KeyError, del_w_1)

    def test_wrapped_iterable(self):
        a = [1, 2, 3]
        b = []
        for x in self.new_proxy(a):
            b.append(x)
        self.assertEquals(a, b)

    def test_iteration_over_proxy(self):
        # Wrap an iterator before starting iteration.
        # PyObject_GetIter() will still be called on the proxy.
        a = [1, 2, 3]
        b = []
        for x in self.new_proxy(iter(a)):
            b.append(x)
        self.assertEquals(a, b)
        t = tuple(self.new_proxy(iter(a)))
        self.assertEquals(t, (1, 2, 3))

    def test_iteration_using_proxy(self):
        # Wrap an iterator within the iteration protocol, expecting it
        # still to work.  PyObject_GetIter() will not be called on the
        # proxy, so the tp_iter slot won't unwrap it.

        class Iterable(object):
            def __init__(self, test, data):
                self.test = test
                self.data = data
            def __iter__(self):
                return self.test.new_proxy(iter(self.data))

        a = [1, 2, 3]
        b = []
        for x in Iterable(self, a):
            b.append(x)
        self.assertEquals(a, b)

    def test_bool_wrapped_None(self):
        w = self.new_proxy(None)
        self.assertEquals(not w, 1)

    # Numeric ops.

    @property
    def unops(self):
        from zope.proxy._compat import PY3
        ops = [
            "-x",
            "+x",
            "abs(x)",
            "~x",
            "int(x)",
            "float(x)",
        ]
        if not PY3: # long is gone in Python 3
            ops.append("long(x)") 
        return ops

    def test_unops(self):
        P = self.new_proxy
        for expr in self.unops:
            x = 1
            y = eval(expr)
            x = P(1)
            z = eval(expr)
            self.assertEqual(z, y,
                             "x=%r; expr=%r" % (x, expr))

    def test_odd_unops(self):
        from zope.proxy._compat import PY3
        # unops that don't return a proxy
        P = self.new_proxy
        funcs = (lambda x: not x,)
        if not PY3:
            funcs += (oct, hex)
        for func in funcs:
            self.assertEqual(func(P(100)), func(100))

    binops = [
        "x+y", "x-y", "x*y", "x/y", "divmod(x, y)", "x**y", "x//y",
        "x<<y", "x>>y", "x&y", "x|y", "x^y",
        ]

    def test_binops(self):
        P = self.new_proxy
        for expr in self.binops:
            first = 1
            for x in [1, P(1)]:
                for y in [2, P(2)]:
                    if first:
                        z = eval(expr)
                        first = 0
                    else:
                        self.assertEqual(eval(expr), z,
                                         "x=%r; y=%r; expr=%r" % (x, y, expr))

    def test_inplace(self):
        # TODO: should test all inplace operators...
        P = self.new_proxy

        pa = P(1)
        pa += 2
        self.assertEqual(pa, 3)

        a = [1, 2, 3]
        pa = qa = P(a)
        pa += [4, 5, 6]
        self.failUnless(pa is qa)
        self.assertEqual(a, [1, 2, 3, 4, 5, 6])

        pa = P(2)
        pa **= 2
        self.assertEqual(pa, 4)

    def test_coerce(self):
        from zope.proxy._compat import PY3
        if PY3: # No coercion in Python 3
            return
        P = self.new_proxy

        # Before 2.3, coerce() of two proxies returns them unchanged

        x = P(1)
        y = P(2)
        a, b = coerce(x, y)
        self.failUnless(a is x and b is y)

        x = P(1)
        y = P(2.1)
        a, b = coerce(x, y)
        self.failUnless(a == 1.0)
        self.failUnless(b is y)
        self.failUnless(a.__class__ is float, a.__class__)

        x = P(1.1)
        y = P(2)
        a, b = coerce(x, y)
        self.failUnless(a is x)
        self.failUnless(b == 2.0)
        self.failUnless(b.__class__ is float, b.__class__)

        x = P(1)
        y = 2
        a, b = coerce(x, y)
        self.failUnless(a is x)
        self.failUnless(b is y)

        x = P(1)
        y = 2.1
        a, b = coerce(x, y)
        self.failUnless(a.__class__ is float, a.__class__)
        self.failUnless(b is y)

        x = P(1.1)
        y = 2
        a, b = coerce(x, y)
        self.failUnless(a is x)
        self.failUnless(b.__class__ is float, b.__class__)

        x = 1
        y = P(2)
        a, b = coerce(x, y)
        self.failUnless(a is x)
        self.failUnless(b is y)

        x = 1.1
        y = P(2)
        a, b = coerce(x, y)
        self.failUnless(a is x)
        self.failUnless(b.__class__ is float, b.__class__)

        x = 1
        y = P(2.1)
        a, b = coerce(x, y)
        self.failUnless(a.__class__ is float, a.__class__)
        self.failUnless(b is y)

    def test_getslice(self):
        # These tests are moot under Python 3 as __slice__ isn't supported.
        from zope.proxy._compat import PY3
        if PY3:
            return
        
        # Lists have special slicing behavior.
        pList = self.new_proxy([1, 2])
        self.assertEqual(pList[-1:], [2])
        self.assertEqual(pList[-2:], [1, 2])
        self.assertEqual(pList[-3:], [1, 2])

        # Tuples also have special slicing behavior.
        pTuple = self.new_proxy((1, 2))
        self.assertEqual(pTuple[-1:], (2,))
        self.assertEqual(pTuple[-2:], (1, 2))
        self.assertEqual(pTuple[-3:], (1, 2))

        # This behavior should be true for all list- and tuple-derived classes.
        class DerivedList(list):

            def __getslice__(self, start, end, step=None):
                return (start, end, step)

        pList = self.new_proxy(DerivedList([1, 2]))
        self.assertEqual(pList[-1:], [2])
        self.assertEqual(pList[-2:], [1, 2])
        self.assertEqual(pList[-3:], [1, 2])

        # Another sort of sequence has a different slicing interpretation.
        class Slicer(object):

            def __len__(self):
                return 2

            def __getslice__(self, start, end, step=None):
                return (start, end, step)

        pSlicer = self.new_proxy(Slicer())
        self.assertEqual(pSlicer[-1:][0], 1)
        self.assertEqual(pSlicer[-2:][0], 0)
        # Note that for non-lists and non-tuples the slice is computed
        # differently
        self.assertEqual(pSlicer[-3:][0], 1)

    def test_setslice(self):
        # Lists have special slicing bahvior for assignment as well.
        pList = self.new_proxy([1, 2])
        pList[-1:] = [3, 4]
        self.assertEqual(pList, [1, 3, 4])
        pList = self.new_proxy([1, 2])
        pList[-2:] = [3, 4]
        self.assertEqual(pList, [3, 4])
        pList = self.new_proxy([1, 2])
        pList[-3:] = [3, 4]
        self.assertEqual(pList, [3, 4])

        # This behavior should be true for all list-derived classes.
        class DerivedList(list):
            pass

        pList = self.new_proxy(DerivedList([1, 2]))
        pList[-1:] = [3, 4]
        self.assertEqual(pList, [1, 3, 4])
        pList = self.new_proxy(DerivedList([1, 2]))
        pList[-2:] = [3, 4]
        self.assertEqual(pList, [3, 4])
        pList = self.new_proxy(DerivedList([1, 2]))
        pList[-3:] = [3, 4]
        self.assertEqual(pList, [3, 4])


class Test_isProxy(unittest.TestCase):

    def _callFUT(self, *args):
        from zope.proxy import isProxy
        return isProxy(*args)

    def test_bare_instance(self):
        class C(object):
            pass
        c = C()
        self.assertFalse(self._callFUT(c))

    def test_proxy_no_class(self):
        from zope.proxy import ProxyBase
        class P1(ProxyBase):
            pass
        class C(object):
            pass
        c = C()
        p1 = P1(c)
        self.assertTrue(self._callFUT(p1))

    def test_proxy_w_same_class(self):
        from zope.proxy import ProxyBase
        class P1(ProxyBase):
            pass
        class C(object):
            pass
        c = C()
        p1 = P1(c)
        self.assertTrue(self._callFUT(p1, P1))

    def test_proxy_w_other_class(self):
        from zope.proxy import ProxyBase
        class P1(ProxyBase):
            pass
        class P2(ProxyBase):
            pass
        class C(object):
            pass
        c = C()
        p1 = P1(c)
        self.assertFalse(self._callFUT(p1, P2))


class Test_getProxiedObject(unittest.TestCase):

    def _callFUT(self, *args):
        from zope.proxy import getProxiedObject
        return getProxiedObject(*args)

    def test_no_proxy(self):
        class C(object):
            pass
        c = C()
        self.assertTrue(self._callFUT(c) is c)

    def test_simple_proxy(self):
        from zope.proxy import ProxyBase
        class C(object):
            pass
        c = C()
        p = ProxyBase(c)
        self.assertTrue(self._callFUT(p) is c)

    def test_nested_proxy(self):
        from zope.proxy import ProxyBase
        class C(object):
            pass
        c = C()
        p = ProxyBase(c)
        p2 = ProxyBase(p)
        self.assertTrue(self._callFUT(p2) is p)


class Test_ProxyIterator(unittest.TestCase):

    def _callFUT(self, *args):
        from zope.proxy import ProxyIterator
        return ProxyIterator(*args)

    def test_no_proxy(self):
        class C(object):
            pass
        c = C()
        self.assertEqual(list(self._callFUT(c)), [c])

    def test_w_simple_proxy(self):
        from zope.proxy import ProxyBase
        class C(object):
            pass
        c = C()
        p = ProxyBase(c)
        self.assertEqual(list(self._callFUT(p)), [p, c])

    def test_w_nested_proxies(self):
        from zope.proxy import ProxyBase
        class C(object):
            pass
        c = C()
        p = ProxyBase(c)
        p2 = ProxyBase(p)
        p3 = ProxyBase(p2)
        p4 = ProxyBase(p3)
        self.assertEqual(list(self._callFUT(p4)), [p4, p3, p2, p, c])


class Test_removeAllProxies(unittest.TestCase):

    def _callFUT(self, *args):
        from zope.proxy import removeAllProxies
        return removeAllProxies(*args)

    def test_no_proxy(self):
        class C(object):
            pass
        c = C()
        self.assertTrue(self._callFUT(c) is c)

    def test_simple_proxy(self):
        from zope.proxy import ProxyBase
        class C(object):
            pass
        c = C()
        p = ProxyBase(c)
        self.assertTrue(self._callFUT(p) is c)

    def test_nested_proxy(self):
        from zope.proxy import ProxyBase
        class C(object):
            pass
        c = C()
        p = ProxyBase(c)
        p2 = ProxyBase(p)
        self.assertTrue(self._callFUT(p2) is c)


class Test_queryProxy(unittest.TestCase):

    def _callFUT(self, *args):
        from zope.proxy import queryProxy
        return queryProxy(*args)

    def test_bare_instance(self):
        class C(object):
            pass
        c = C()
        self.assertEqual(self._callFUT(c), None)

    def test_proxy_no_class(self):
        from zope.proxy import ProxyBase
        class P1(ProxyBase):
            pass
        class C(object):
            pass
        c = C()
        p1 = P1(c)
        self.assertTrue(self._callFUT(p1) is p1)

    def test_proxy_w_same_class(self):
        from zope.proxy import ProxyBase
        class P1(ProxyBase):
            pass
        class C(object):
            pass
        c = C()
        p1 = P1(c)
        self.assertTrue(self._callFUT(p1, P1) is p1)
        self.assertTrue(self._callFUT(p1, P1, 42) is p1)

    def test_proxy_w_other_class(self):
        from zope.proxy import ProxyBase
        class P1(ProxyBase):
            pass
        class P2(ProxyBase):
            pass
        class C(object):
            pass
        c = C()
        p1 = P1(c)
        self.assertEqual(self._callFUT(p1, P2), None)
        self.assertEqual(self._callFUT(p1, P2, 42), 42)

    def test_proxy_w_base_class(self):
        from zope.proxy import ProxyBase
        class P1(ProxyBase):
            pass
        class P2(ProxyBase):
            pass
        class C(object):
            pass
        c = C()
        p1 = P1(c)
        self.assertTrue(self._callFUT(p1, ProxyBase) is p1)
        self.assertTrue(self._callFUT(p1, ProxyBase, 42) is p1)


class Test_queryInnerProxy(unittest.TestCase):

    def _callFUT(self, *args):
        from zope.proxy import queryInnerProxy
        return queryInnerProxy(*args)

    def test_bare_instance(self):
        class C(object):
            pass
        c = C()
        self.assertEqual(self._callFUT(c), None)

    def test_proxy_no_class(self):
        from zope.proxy import ProxyBase
        class P1(ProxyBase):
            pass
        class C(object):
            pass
        c = C()
        p1 = P1(c)
        self.assertTrue(self._callFUT(p1) is p1)

    def test_proxy_w_same_class(self):
        from zope.proxy import ProxyBase
        class P1(ProxyBase):
            pass
        class C(object):
            pass
        c = C()
        p1 = P1(c)
        self.assertTrue(self._callFUT(p1, P1) is p1)
        self.assertTrue(self._callFUT(p1, P1, 42) is p1)

    def test_nested_proxy(self):
        from zope.proxy import ProxyBase
        class P1(ProxyBase):
            pass
        class P2(ProxyBase):
            pass
        class C(object):
            pass
        c = C()
        p1 = P1(c)
        p2 = P2(p1)
        self.assertTrue(self._callFUT(p2, P1) is p1)
        self.assertTrue(self._callFUT(p2, P1, 42) is p1)
        self.assertTrue(self._callFUT(p2, P2) is p2)
        self.assertTrue(self._callFUT(p2, P2, 42) is p2)

    def test_re_nested_proxy(self):
        from zope.proxy import ProxyBase
        class P1(ProxyBase):
            pass
        class P2(ProxyBase):
            pass
        class C(object):
            pass
        c = C()
        p1 = P1(c)
        p2 = P2(p1)
        p3 = P1(p2)
        self.assertTrue(self._callFUT(p3, P1) is p1)
        self.assertTrue(self._callFUT(p3, P1, 42) is p1)
        self.assertTrue(self._callFUT(p3, P2) is p2)
        self.assertTrue(self._callFUT(p3, P2, 42) is p2)


class Test_sameProxiedObjects(unittest.TestCase):

    def _callFUT(self, *args):
        from zope.proxy import sameProxiedObjects
        return sameProxiedObjects(*args)

    def test_bare_instance_identical(self):
        class C(object):
            pass
        c1 = C()
        self.assertTrue(self._callFUT(c1, c1))

    def test_bare_instances_different(self):
        class C(object):
            pass
        c1 = C()
        c2 = C()
        self.assertFalse(self._callFUT(c1, c2))
        self.assertFalse(self._callFUT(c2, c1))

    def test_proxy_and_same_bare(self):
        from zope.proxy import ProxyBase
        class C(object):
            pass
        c1 = C()
        self.assertTrue(self._callFUT(ProxyBase(c1), c1))
        self.assertTrue(self._callFUT(c1, ProxyBase(c1)))

    def test_proxy_and_other_bare(self):
        from zope.proxy import ProxyBase
        class C(object):
            pass
        c1 = C()
        c2 = C()
        self.assertFalse(self._callFUT(ProxyBase(c1), c2))
        self.assertFalse(self._callFUT(c2, ProxyBase(c1)))

    def test_proxies_w_same_bare(self):
        from zope.proxy import ProxyBase
        class C(object):
            pass
        c1 = C()
        self.assertTrue(self._callFUT(ProxyBase(c1), ProxyBase(c1)))

    def test_proxies_w_other_bare(self):
        from zope.proxy import ProxyBase
        class C(object):
            pass
        c1 = C()
        c2 = C()
        self.assertFalse(self._callFUT(ProxyBase(c1), ProxyBase(c2)))
        self.assertFalse(self._callFUT(ProxyBase(c2), ProxyBase(c1)))

    def test_nested_proxy_and_same_bare(self):
        from zope.proxy import ProxyBase
        class C(object):
            pass
        c1 = C()
        self.assertTrue(self._callFUT(ProxyBase(ProxyBase(c1)), c1))
        self.assertTrue(self._callFUT(c1, ProxyBase(ProxyBase(c1))))

    def test_nested_proxy_and_other_bare(self):
        from zope.proxy import ProxyBase
        class C(object):
            pass
        c1 = C()
        c2 = C()
        self.assertFalse(self._callFUT(ProxyBase(ProxyBase(c1)), c2))
        self.assertFalse(self._callFUT(c2, ProxyBase(ProxyBase(c1))))


class Test_nonOverridable(unittest.TestCase):

    def test_it(self):
        from zope.proxy import ProxyBase
        from zope.proxy import non_overridable
        class Proxy(ProxyBase):
            def who(self):
                return 'PROXY'
            @non_overridable
            def what(self):
                return 'PROXY'
        class Foo(object):
            def who(self):
                return 'FOO'
            def what(self):
                return 'FOO'
        proxy = Proxy(Foo())
        self.assertEqual(proxy.who(), 'FOO')
        self.assertEqual(proxy.what(), 'PROXY')


class Thing:
    """This class is expected to be a classic class."""


class Comparable(object):
    def __init__(self, value):
        self.value = value

    def __eq__(self, other):
        if hasattr(other, "value"):
            other = other.value
        return self.value == other

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if hasattr(other, "value"):
            other = other.value
        return self.value < other

    def __ge__(self, other):
        return not self.__lt__(other)

    def __le__(self, other):
        if hasattr(other, "value"):
            other = other.value
        return self.value <= other

    def __gt__(self, other):
        return not self.__le__(other)

    def __repr__(self):
        return "<Comparable: %r>" % self.value


def test_suite():
    from doctest import DocTestSuite
    return unittest.TestSuite((
        unittest.makeSuite(ModuleConformanceCase),
        unittest.makeSuite(ProxyBaseTestCase),
        unittest.makeSuite(Test_isProxy),
        unittest.makeSuite(Test_getProxiedObject),
        unittest.makeSuite(Test_ProxyIterator),
        unittest.makeSuite(Test_removeAllProxies),
        unittest.makeSuite(Test_queryProxy),
        unittest.makeSuite(Test_queryInnerProxy),
        unittest.makeSuite(Test_sameProxiedObjects),
        unittest.makeSuite(Test_nonOverridable),
        DocTestSuite(),
    ))
