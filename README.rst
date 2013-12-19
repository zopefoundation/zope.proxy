===========================
Generic Transparent Proxies
===========================

Proxies are special objects which serve as mostly-transparent
wrappers around another object, intervening in the apparent behavior of
the wrapped object only when necessary to apply the policy (e.g., access
checking, location brokering, etc.) for which the proxy is responsible.

zope.proxy is implemented via a C extension module, which lets it do things
like lie about its own ``__class__`` that are difficult in pure Python (and
were completely impossible before metaclasses).  It also proxies all the
internal slots (such as `__int__`/`__str__`/`__add__`).

Editorial note:

   Unfortunately, we don't have separate documentation for `zope.proxy`
   at this time.  This is a shame because they are generically useful.
   We are publishing this release without documentation mainly because
   it is a dependency of other releases.
