#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

# Python Embedded DSL simple test.
# Copyright 2013 Grigory Petrov
# See LICENSE for details.

from pyedsl import pd, xml

with xml.Tag( 'foo', o_parent = None ) as oXml:
  with xml.Tag( 'bar' ):
    pass
  pd.o.build()

assert oXml.o( 'bar' ).dparent.dname == 'foo'

##  Usage with third-party classes.
class Foo( object ): pass
class Bar( object ): pass

with pd.wrap( Foo() ):
  print( pd.o )
  with pd.wrap( Bar() ):
    print( pd.o )
  print( pd.o )

