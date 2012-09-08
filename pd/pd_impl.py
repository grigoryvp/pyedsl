#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python DSL
# Copyright 2012 Grigory Petrov
# See LICENSE for details.

import threading

class Item( object ) :

  def __init__( self,
    ##i DSL item name. Used to lookup child item from parent item.
    name = None,
    ##i DSL item parent:
    ##  . |None| to define top level DSL item.
    ##  . 'auto' to implicitly use `current` parent stored in
    ##    thread-local |pd.o|. This allows to write nested |with|
    ##    statements without explicitly defining parents for each item.
    ##  . |pd.Item| subclass to continue DSL construction from existing
    ##    parent. Allows to define top level item as standalone class and
    ##    construct child DSL hierarchy in constructor.
    parent = 'auto'
  ) :
    if isinstance( parent, basestring ) and 'auto' == parent :
      assert pd.o is not None, "Auto parent top level item."
      self.__parent = pd.o
    else :
      assert parent is None or isinstance( parent, Item ), "Wrong parent."
      self.__parent = parent
    if name is not None :
      assert isinstance( name, basestring )
      self.__name = name
    else :
      self.__name = self.__class__.__name__.lower()
    self.__children = []

  def __enter__( self ) :
    ##  Save current value of |pd.o| so |__exit__()| can restore it. This
    ##  is required to correctly handle hierarchical DSL construction.
    self.__dict__[ '__o' ] = pd.o
    pd.o = self
    return self

  def __exit__( self, * vargs ) :
    pd.o = self.__dict__[ '__o' ]
    if self.parent is not None :
      ##  User defined adder.
      if hasattr( self.parent, 'add' ) :
        self.parent.add( self )
      ##  Build-in adder that maintain tree for lookup.
      self.parent.__add( self )

  @property
  def parent( self ) :
    return self.__parent

  @property
  def name( self ) :
    return self.__name

  @property
  def children( self ) :
    return self.__children

  ##x Search children for item with {i name} and evalute to it or |None|.
  def o( self, name ) :
    for oChild in self.__children :
      if oChild.name == name :
        return oChild
    for oChild in self.__children :
      oItem = oChild.o( name )
      if oItem is not None :
        return oItem
    return None

  def __add( self, child ) :
    self.__children.append( child )


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

