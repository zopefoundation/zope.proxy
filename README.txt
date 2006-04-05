zope.proxy Package Readme
=========================

Overview
--------

In Zope3, proxies are special objects which serve as mostly-transparent
wrappers around another object, intervening in the apparent behavior of
the wrapped object only when necessary to apply the policy (e.g., access
checking, location brokering, etc.) for which the proxy is responsible.
Zope 2 uses acquisition wrappers liberally, to impose a policy that
attribute lookups which failed on the "self" instance could be delegated
to the "parent" instance.

Changes
-------

See CHANGES.txt.

Installation
------------

See INSTALL.txt.


Developer Resources
-------------------

- Subversion browser:

  http://svn.zope.org/zope.proxy/

- Read-only Subversion checkout:

  $ svn co svn://svn.zope.org/repos/main/zope.proxy/trunk

- Writable Subversion checkout:

  $ svn co svn://svn.zope.org/repos/main/zope.proxy/trunk

- Note that the 'src/zope/proxy' package is acutally a 'svn:externals' link
  to the corresponding package in the Zope3 trunk (or to a specific tag,
  for released versions of the package).
