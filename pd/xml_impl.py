#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python DSL
# Copyright 2012 Grigory Petrov
# See LICENSE for details.

from pd_impl import pd

class Tag( pd.Item ) :

  def build( self, offset = 0 ) :
    print( " " * offset + "<{0}>".format( self.name ) )
    for oChild in self.children :
      oChild.build( offset + 2 )
    print( " " * offset + "</{0}>".format( self.name ) )

