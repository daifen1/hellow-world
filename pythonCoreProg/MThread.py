#!/usr/bin/python
# -*- coding: utf-8 -*
from time import ctime,clock,sleep
import threading
class MyThread(	threading.Thread):
	"""docstring for MyThread"""
	def __init__(self, func,args,name='',res=''):
		threading.Thread.__init__(self)
		self.name=name
		self.func=func
		self.args=args
		self.res=res
	def run(self):
		print "starting",self.name,"at ",ctime()
		self.res=apply(self.func,self.args)
		print self.name,"fininshed at", ctime()		
	def getResult(self):
		return self.res
	
def fib(x):
	sleep(0.005)
	if x<2:
		return 1
	return fib(x-1)+fib(x-2)

def fac(x):
	sleep(0.005)
	if x<2:
		return 1
	else :
		return x*fac(x-1)
def sumfac(x):
	sleep(0.005)
	if x<2:
		return 1
	else :
		return x+sumfac(x-1)
if __name__ == '__main__':
	funcs=[fib,fac,sumfac]
	nfuncs=range(len(funcs))
	n=12
	print "single thread start at ",ctime()
	for i in nfuncs:
		print funcs[i].__name__," start time is  ",ctime()
		print funcs[i](n)
		print funcs[i].__name__," end time is  ",ctime()

	print "single thread end at ",ctime()

	threads=[]
	for i in nfuncs:
		t=MyThread(funcs[i], (n, ),funcs[i].__name__)
		threads.append(t)
	for i in nfuncs:
		threads[i].start()

	for i in nfuncs:
		threads[i].join()
		print threads[i].getResult()
	