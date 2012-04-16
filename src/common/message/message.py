#!/usr/bin/env python
# -*- coding:utf-8 -*-

from copy import copy

from collections import defaultdict as dd
from collections import Hashable

__all__ = [
		'Broker',
		'sub',
		'unsub',
		'pub',
		'declare',
		'retract',
		'get_declarations',
		'has_declaration',
		]

class Context(object):
	def __init__(self):
		self.discontinued = False

class Broker(object):
	def __init__(self):
		self._router = dd(list)
		self._board = {}
	
	def sub(self, topic, func, front = False):
		assert isinstance(topic, Hashable)
		assert callable(func)
		if func in self._router[topic]:
			return
		if front:
			self._router[topic].insert(0, func)
		else:
			self._router[topic].append(func)
		if topic in self._board:
			a, kw = self._board[topic]
			func(Context(), *a, **kw)
	
	def unsub(self, topic, func):
		assert isinstance(topic, Hashable)
		assert callable(func)
		if topic not in self._router:
			return
		try:
			self._router[topic].remove(func)
		except ValueError:
			pass
		
	def pub(self, topic, *a, **kw):
		assert isinstance(topic, Hashable)
		if topic not in self._router:
			return
		removed = []
		context = Context()
		for func in copy(self._router[topic]):
			if func:
				func(context, *a, **kw)
			else:
				removed.append(func)
			if context.discontinued:
				break
		for i in removed:
			try:
				self._router[topic].remove(i)
			except ValueError:
				pass
	
	def declare(self, topic, *a, **kw):
		assert isinstance(topic, Hashable)
		self._board[topic] = (a, kw)
		return pub(topic, *a, **kw)
	
	def retract(self, topic):
		assert isinstance(topic, Hashable)
		try:
			self._board.pop(topic)
		except KeyError:
			pass
	
	def get_declarations(self):
		return self._board.keys()
	
	def has_declaration(self, topic):
		assert isinstance(topic, Hashable)
		return topic in self._board

_broker = Broker()
sub = _broker.sub
unsub = _broker.unsub
pub = _broker.pub
declare = _broker.declare
retract = _broker.retract
get_declarations = _broker.get_declarations
has_declaration = _broker.has_declaration

if __name__ == '__main__':
	def greet(context, name):
		print 'hello, %s.'%name
	
	sub('greet', greet)
	pub('greet', 'lai')
	pub('greet', 'smallfish')
	pub('greet', 'guido')
	unsub('greet', greet)
	unsub('not existed', greet)
	pub('greet', 'world')
	print '*' * 30
	sub('greet', greet)
	declare('greet', 'world')
	assert get_declarations()
	
	def greet2(context, name):
		print 'hello, %s. greet2'%name
	
	sub('greet', greet2)

	pub('greet', 'spring')
	
	retract('greet')

	def greet3(context, name):
		print 'hello, %s. greet3'%name
	
	sub('greet', greet3)

	print '*' * 30
	def greet4(context, name):
		print 'hello, %s. greet4'%name
		unsub('greet', greet4)
	sub('greet', greet4, front = True)
	pub('greet', 'lv')
	pub('greet', 'ma')
	
	print '*' * 30
	class Foo(object):
		def foo(self, ctx, name):
			print 'Foo.foo, hello %s.'%name

	foo = Foo()
	sub('lai', foo.foo)
	pub('lai', 'lai')

