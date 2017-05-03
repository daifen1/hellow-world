#!/usr/bin/python
# -*- coding: utf-8 -*
import os,os.path
def fileSearch(filePath,NoDocList,DocMap):
	'''分出那些py文件有__doc__，
	   将不存在__doc__的存入NoDocList,将存在
	   的存入DocMap
	'''
	for dir,directions,files in os.walk(filePath):
		for file in files:
			try:
				if file.split('.')[1]=='py':
					fileAbsPath=os.path.join(dir,file)
					try :
						pyfile=open(fileAbsPath,'r+')
					except IOError:
						filename=os.path.basename(filepath)
						print "%s open failed,file has been closed" % filename
						file.close()
					if pyfile.__doc__==' ':
						NoDocList.append(fileAbsPath)
					else :
						DocMap[fileAbsPath]=pyfile.__doc__
			except IndexError:
				pass

if __name__=="__main__":
	filePath="E:/Program Files/python2.7/Lib"
	NoDocList=[]
	DocMap={}
	fileSearch(filePath,NoDocList,DocMap)
	for file in NoDocList:
		print file
	for key in DocMap.keys():
		print "filepath is %s" % key
		print DocMap[key]