:mod:`zope.proxy` API
=====================

:mod:`zope.proxy.interfaces`
----------------------------

.. automodule:: zope.proxy.interfaces

  .. autointerface:: IProxyIntrospection
     :members:
     :member-order: bysource


:mod:`zope.proxy`
-----------------

.. automodule:: zope.proxy
   :members:


:mod:`zope.proxy.decorator`
---------------------------

.. automodule:: zope.proxy.decorator

   .. doctest::

      >>> from zope.interface import Interface
      >>> from zope.interface import directlyProvides
      >>> from zope.interface import implementer
      >>> class I1(Interface):
      ...     pass
      >>> class I2(Interface):
      ...     pass
      >>> class I3(Interface):
      ...     pass
      >>> class I4(Interface):
      ...     pass
      >>> from zope.proxy.decorator import SpecificationDecoratorBase
      >>> @implementer(I1)
      ... class D1(SpecificationDecoratorBase):
      ...   pass
      >>> @implementer(I2)
      ... class D2(SpecificationDecoratorBase):
      ...   pass
      >>> @implementer(I3)
      ... class X(object):
      ...   pass
      >>> x = X()
      >>> directlyProvides(x, I4)

   Interfaces of X are ordered with the directly-provided interfaces first.

   .. doctest::

      >>> from zope.interface import providedBy
      >>> [interface.getName() for interface in list(providedBy(x))]
      ['I4', 'I3']

   When we decorate objects, what order should the interfaces come
   in?  One could argue that decorators are less specific, so they
   should come last.

   .. doctest::

      >>> [interface.getName() for interface in list(providedBy(D1(x)))]
      ['I4', 'I3', 'I1']

      >>> [interface.getName() for interface in list(providedBy(D2(D1(x))))]
      ['I4', 'I3', 'I1', 'I2']

   SpecificationDecorators also work with old-style classes:

   .. doctest::

      >>> @implementer(I3)
      ... class X:
      ...   pass

      >>> x = X()
      >>> directlyProvides(x, I4)

      >>> [interface.getName() for interface in list(providedBy(x))]
      ['I4', 'I3']

      >>> [interface.getName() for interface in list(providedBy(D1(x)))]
      ['I4', 'I3', 'I1']

      >>> [interface.getName() for interface in list(providedBy(D2(D1(x))))]
      ['I4', 'I3', 'I1', 'I2']

   .. autoclass:: DecoratorSpecificationDescriptor
      :members:

   .. autoclass:: SpecificationDecoratorBase
