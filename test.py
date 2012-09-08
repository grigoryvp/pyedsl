#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

from pd import pd, xml

with xml.Tag( 'foo', parent = None ) as oXml :
  with xml.Tag( 'bar' ) :
    pass
  pd.o.build()

assert oXml.o( 'bar' ).parent.name == 'foo'

