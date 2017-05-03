#!/usr/bin/python
# -*- coding: utf-8 -*
import re
from genData import genData
if __name__ == '__main__':
	strlist=[]
	weekMap={'Mon':0,'Tue':0,'Wed':0,'Thu':0,'Fri':0,'Sat':0,'Sun':0}
	genData(strlist)
	weekdays="(Mon|Tue|Wed|Thu|Fri|Sat|Sun)"
	time=".+(/d+:/d+:/d+ /d+)"
	m=re.compile(time)
	for str in strlist:
		print m.search(str)