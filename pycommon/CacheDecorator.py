#!/usr/bin/python3
#
#	CacheDecorator - Simple timed cache decorator.
#	Copyright (C) 2011-2019 Johannes Bauer
#	
#	This file is part of pycommon.
#
#	pycommon is free software; you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation; this program is ONLY licensed under
#	version 3 of the License, later versions are explicitly excluded.
#
#	pycommon is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with pycommon; if not, write to the Free Software
#	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
#	Johannes Bauer <JohannesBauer@gmx.de>
#
#	File UUID 0a5de76f-52f7-4fe0-b0b7-41c4dbdf6983

import time

def cacheresult(timeout = None):
	def decorator(decoree):
		cache = { }	
		def decorated_function(*args, **kwargs):
			refresh = True
			if args in cache:
				(lasttime, result) = cache[args]
				refresh = (time.time() - lasttime) > timeout

			if refresh:
				result = decoree(*args, **kwargs)
				cache[args] = (time.time(), result)				
			return result
		return decorated_function

	return decorator


if __name__ == "__main__":
	@cacheresult(timeout = 2)
	def foo(a, b, c):
		print("a =", a)
		print("b =", b)
		print("c =", c)
		return a * b * c

	class MyClass():
		def __init__(self):
			self._x = 0

		@cacheresult(timeout = 2)
		def foo(self):
			self._x += 1
			return self._x

	mc = MyClass()
	while True:
#		print(foo(9, 6, 2))
#		print(foo(9, 6, 1))
		print(mc.foo())
		time.sleep(1)


