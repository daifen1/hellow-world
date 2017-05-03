#!/usr/bin/python
# -*- coding: utf-8 -*

class entity(object):
	"""Iges data_Type"""
	def __init__(self):
		self.lineList=[]
		self.arcList=[]
		self.transMatrixList=[]
		self.others=[]
class point(object):
	"""Iges_basicType:point"""
	def __init__(self, param):
		super(point, self).__init__()
		self.point=param
		self.regionX='#'
		self.regionY='#'
		self.region='##'
class Line(object):
	"""Iges_type:line"""
	def __init__(self, point1,point2):
		super(Line, self).__init__()
		self.point1=point1
		self.point2=point2

class arc(object):
	"""Iges_type:arc"""
	def __init__(self,param):
		super(arc, self).__init__()
		self.centerPoint=param[0:3]
		self.startPoint=param[3:6]
		self.endPoint=param[6:9]
		self.interPolationList=[]	

class transMatrix(object):
		"""iges_tytransMatrix"""
		def __init__(self, param):
			super(transMatrix, self).__init__()
			self.matrix=param[0:3]+param[4:7]+param[8:11]
			self.T=[param[3]]+[param[7]]+[param[11]]
				
def readIges(filePath,MyEntity):
	try:
		file=open(filePath,'r+')
	except IOError:
		print "file open failed"
		file.close()
	pLineSet=set()      #judge whether there is a Type that need tow paramline
	FirstLine=False	#judge whether is continuously first line
	line1,line2=[],[]
	catLine=[]
	param=[]
	entity_type=''
	for line in file.readlines():
		data=line[:80]
		id_code=line[72]

		#getdata in P
		if id_code=='P':
			#print "id_code",line
			lineIndex=data[65:72].strip()
			#print lineIndex
			if lineIndex not in pLineSet:
				#print "not in pLineSet",line
				if FirstLine==True:
					#print 'the second line'
					#print param
					#end of line has a 0.0;

					saveParam(param[:len(param)-1],entity_type,MyEntity)
					#print param
					param=[]

				pLineSet.add(lineIndex)
				line=line.strip(';')
				line=line.split(",")
				entity_type=line[0].strip()
				for x in line[1:len(line)-1]:
					#print x
					param.append(safeFloat(x))
				#print "whole firstLine",param
				FirstLine=True
			#the second line
			else:
				FirstLine=False
				if line!='0;':
					line=line.strip(';')
					line=line.split(',')
					for x in line[:len(line)-2]:
						#print x	
						param.append(safeFloat(x))
				print param     
				#print twoLine param
				saveParam(param,entity_type,MyEntity)
				param=[]
	#the last PLine not save
	saveParam(param, entity_type, MyEntity)
def saveParam(param,entity_type,MyEntity):
	if entity_type=='110':
		try:

			point1=point(param[0:3])
			point2=point(param[3:6])
			MyLine=Line(point1, point2)
		except :
			print "line class initial failed",param
		MyEntity.lineList.append(MyLine)
	elif entity_type=='100':
		try:
			changeParam=param[1:3]+[param[0]]+param[3:5]+[param[0]]+param[5:]+[param[0]]
			#print "+param:",param
			MyArc=arc(changeParam)
		except:
			print "Arc class initial failed",param
		MyEntity.arcList.append(MyArc)
	elif entity_type=='124':
		try:
			MyTransMatrix=transMatrix(param)
		except:
			print "TransMatrix initial failed",param
		MyEntity.transMatrixList.append(MyTransMatrix)
	else :
		MyEntity.others.append(param)
def safeFloat(x):
	try:
		return float(x)
	except TypeError:
		print 'TypeError:',type(x),x
	except ValueError:
		print 'ValueError',type(x),x 
if __name__=='__main__':
	filePath="C:/Users/wu/Documents/catia/planeCircle.IGS"
	MyEntity=entity()
	readIges(filePath, MyEntity)
	#print len(MyEntity.lineList)
	for line in MyEntity.lineList:
		#print [line.X1,line.Y1,line.Z1,line.X2,line.Y2,line.Z2]
		print 'line data:',line.point1.point,line.point2.point
	for arc in MyEntity.arcList:
		print 'arc data:',arc.centerPoint,arc.startPoint,arc.endPoint
		print arc.interPolationList
	for transMatrix in MyEntity.transMatrixList:
		print 'transMatrix data:',transMatrix.matrix,transMatrix.T
	for other in MyEntity.others:
		print "other lineType",other