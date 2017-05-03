#!/usr/bin/python
# -*- coding: utf-8 -*
from time import ctime,sleep
import functools
def timeit(func):
	@functools.wraps(func)
	def wrapper():
		print '[%s] %s is called' % (ctime(),func.__name__)
	func()	
	return wrapper
@timeit
def foo():
	"""function foo()"""
	print "in foo()"
if __name__ == '__main__':
	for x in range(3):
		sleep(1)
		foo()
	str=("[sdfsdf]")
	print type(str[4]),str[4]