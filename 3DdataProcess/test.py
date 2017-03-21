#!/usr/bin/python
# -*- coding: utf-8 -*
import sys
#系统模块默认'utf-8'编码
default_encoding="utf-8"
if(default_encoding!=sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import os,os.path
import re
file=open("e:/STLdata.txt",'r+')
allLines=(line.strip() for line in file )
for line in allLines:
	if line=='':
		pass
	elif line[0]=='#':
		pass
	elif '#' in line:
		#print line+'     this is line'
		if '\''in line or '\"' in line:
			count=0
			scount=0
			dcount=0
			splitline=line.split('#')
			for line in splitline:
				for letter in line:
					if letter=='\'':
						scount+=1
					elif letter=='\"':
						dcount+=1
				if scount%2==0 and dcount%2==0:
					break
				count+=1
			str=splitline[0]
			for x in range(1,count+1):
				str+='#'+splitline[x]
			print str
		else :
			print line.split('#')[0]
	else :
		print line