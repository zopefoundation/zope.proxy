***************************
Generic Transparent Proxies
***************************

Proxies are special objects which serve as mostly-transparent
wrappers around another object, intervening in the apparent behavior of
the wrapped object only when necessary to apply the policy (e.g., access
checking, location brokering, etc.) for which the proxy is responsible.

Editorial note:

   Unfortunately, we don't have separate documentation for zope.proxy
   at this time.  This is a shame because the are generically useful.
   We are publishing this release without documentation mainly because
   it is a dependency of other releases.

Changes
*******

3.4.0 (2007/07/12)
==================

New Features
------------

Added a decorator module that supports declaring interfaces on proxies
that get blended with the interfaces of the things they proxy.

3.3.0 (2006/12/20)
==================

Corresponds to the verison of the zope.proxy package shipped as part of
the Zope 3.3.0 release.


3.2.0 (2006/01/05)
==================

Corresponds to the verison of the zope.proxy package shipped as part of
the Zope 3.2.0 release.


3.0.0 (2004/11/07)
==================

Corresponds to the verison of the zope.proxy package shipped as part of
the Zope X3.0.0 release.
