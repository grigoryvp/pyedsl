#!/usr/bin/env python
# coding:utf-8 vi:et:ts=2

from pd import pd, xml

with xml.Tag( 'foo' ) as oXml :
  with xml.Tag( 'bar' ) :
    pass

oXml.build()

