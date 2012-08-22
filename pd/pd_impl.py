#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python DSL
# Copyright 2012 Grigory Petrov
# See LICENSE for details.

import threading

class Item( object ) :

  def __init__( self, parent = None, name = None ) :
    self.__parent = parent if parent is not None else pd.o
    sDefaultName = self.__class__.__name__.lower()
    self.__name = name if name is not None else sDefaultName

  def __enter__( self ) :
    ##  Save current value of |pd.o| so |__exit__()| can restore it. This
    ##  is required to correctly handle hierarchical DSL construction.
    self.__dict__[ '__o' ] = pd.o
    pd.o = self
    return self

  def __exit__( self, * vargs ) :
    pd.o = self.__dict__[ '__o' ]
    if self.parent is not None and hasattr( self.parent, 'add' ) :
      self.parent.add( self )

  @property
  def parent( self ) :
    return self.__parent

  @property
  def name( self ) :
    return self.__name


class Pd( object ) :

  def __init__( self ) :
    self.Item = Item
    self.__tls = threading.local()

  ##! |pd.o| holds current DSL item that is thread local and is auto
  ##  maintained  via |with| statements:
  ##  | with pu.Wnd() :
  ##  |   # 'with' sets pu.o to 'Wnd' instance for current thread.
  ##  |   with pu.Button() :
  ##  |     # Current pu.o is used as parent. 'with' sets pu.o for
  ##  |     # 'Button' instance.
  ##  |     pu.o.setText( "button" )
  ##  |   # pu.o is restored to 'Wnd' by leaving 'with' statement.
  ##  |   pu.o.setCaption( "window" )
  @property
  def o( self ) :
    if hasattr( self.__tls, 'o' ) :
      return self.__tls.o
    else :
      return None

  @o.setter
  def o( self, value ) :
    self.__tls.o = value

pd = Pd()

