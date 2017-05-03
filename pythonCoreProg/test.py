#!/usr/bin/python
# -*- coding: utf-8 -*
import math
import time
def safe_input():
	try :
		string=raw_input("input please")
	except (EOFError,KeyboardInterrupt):
		return None
	return string
def safe_sqrt(num):
	try:
		math.sqrt(num)
	except ValueError:
		return complex(0,math.sqrt(abs(num)))
	except TypeError:
		return None

def ToTuple(x,y):
	return (x,y)
def jiecheng(N):
	if N==1:
		return N
	else :
		return N*jiecheng(N-1)
if __name__ == '__main__':
	num=range(5)
	string=['a','b','c','d','e']
	print map(ToTuple, string,num)
	N=int(raw_input("input a num"))
	print reduce(lambda x,y:x*y, range(1,N+1))
	print jiecheng(N)