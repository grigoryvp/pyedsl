#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Python DSL
# Copyright 2012 Grigory Petrov
# See LICENSE for details.

import threading
import re

##x |__enter__| that can be used with any class.
def enter( self ) :
  ##  Save current value of |pd.o| so |__exit__()| can restore it. This
  ##  is required to correctly handle hierarchical DSL construction.
  self.__dict__[ '__pyedsl_context' ] = pd.o
  pd.o = self
  return self

##x |__enter__| that can be used with any class.
def exit( self, * vargs ) :
  pd.o = self.__dict__[ '__pyedsl_context' ]
  if isinstance( self, Item ) :
    if self._Item__pyedsl_parent is not None :
      ##  User defined adder.
      if hasattr( self._Item__pyedsl_parent, 'dadd' ) :
        self._Item__pyedsl_parent.dadd( self )
      ##  Build-in adder that maintain tree for lookup.
      self._Item__pyedsl_parent._Item__pyedsl_add( self )

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
      self.__pyedsl_parent = pd.o
    else :
      assert parent is None or isinstance( parent, Item ), "Wrong parent."
      self.__pyedsl_parent = parent
    if name is not None :
      assert isinstance( name, basestring )
      self.__name = name
    else :
      self.__name = self.__class__.__name__.lower()
    self.__children = []

  def __enter__( self ) :
    return enter( self )

  def __exit__( self, * vargs ) :
    return exit( self, * vargs )

  @property
  ##x Shortage from "Dsl Parent". Not named "parent" since it will conflict
  ##  with |Tkinter| "parent" method.
  def dparent( self ) :
    return self.__pyedsl_parent

  ##x Shortage from "Dsl Name". Not named "name" since it will conflict
  ##  with something for sure.
  @property
  def dname( self ) :
    return self.__name

  ##x Shortage from "Dsl Children". Not named "children" since it will
  ##  conflict with something for sure.
  ##  Used in cases like building XML where gathering results from DSL
  ##  starts at root.
  @property
  def dchildren( self ) :
    return self.__children

  ##x Search children for item with {i name} and evalute to it or |None|.
  def o( self, name ) :
    for oChild in self.__children :
      if oChild.dname == name :
        return oChild
    for oChild in self.__children :
      oItem = oChild.o( name )
      if oItem is not None :
        return oItem
    return None

  ##x "DSL Add", name to prevent conflicts.
  def __pyedsl_add( self, child ) :
    self.__children.append( child )


class RegexpMatch( object ) :

  def __init__( self, match ) :
    self.__match = match

  @property
  def string( self ) :
    return self.__match.string

  @property
  def first( self ) :
    lGroups = self.__match.groups()
    if len( lGroups ) :
      return lGroups[ 0 ]
    else :
      return None

  def __getitem__( self, key ) :
    if isinstance( key, int ) :
      return self.__match.groups()( key )
    if isinstance( key, basestring ) :
      return self.__match.groupdict()( key )
    assert False, "Unknown key type."

class Pd( object ) :

  def __init__( self ) :
    self.Item = Item
    self.__tls = threading.local()

  ##  Shortcut to access regexp search result properties.
  def search( self, pattern, string ) :
    oMatch = re.search( pattern, string )
    if oMatch is not None :
      self.__tls.match = RegexpMatch( oMatch )
      return self.__tls.match
    return None

  ##  Wraps any object so it can be used inside 'with' and reference
  ##  to it will be available as |pd.o|.
  def wrap( self, object ) :
    object.__class__.__enter__ = enter
    object.__class__.__exit__ = exit
    return object

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

  @property
  def match( self ) :
    if hasattr( self.__tls, 'match' ) :
      return self.__tls.match
    else :
      return None


pd = Pd()

