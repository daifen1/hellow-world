#!/usr/bin/python
# -*- coding: utf-8 -*
from time import ctime
import re
from sys import maxint
from random import randint,choice
from string import lowercase

def genData(strlist):
	doms=('com','edu','net','org','gov')
	for i in range(randint(5, 10)):
		dtint=randint(0, maxint-1)
		dastr=ctime(dtint)
		em=''
		shorter=randint(4, 7)
		for j in range(shorter):
			em+=choice(lowercase)
		longer=randint(shorter, 12)
		dn=''
		for j in range(longer):
			dn+=choice(lowercase)
		strlist.append("[ %s ]::%s@%s.%s::%d-%d-%d"% (dastr,em,dn,choice(doms),dtint,shorter,longer))
	return strlist