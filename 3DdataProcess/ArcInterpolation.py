#!/usr/bin/python
# -*- coding: utf-8 -*
import numpy as np
from read_iges import *
from LineAreaProcess import *
import traceback
import common
from numpy import pi
from math import sin,cos,asin,acos
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
thresholdRaduis=5  #if raduis<5,interpolate by degree
perStepLength=2  #if raduis>5,interpolate by length
perStepDegree=pi/360  #0.5degree,interpolate by degree
def TransArcPoint(MyEntity):
	""""return TransArcList what storage TransARC"""
	transArcLineList=[]
	for transMatrix,arc in zip(MyEntity.transMatrixList ,MyEntity.arcList):
		matrix=np.array(transMatrix.matrix).reshape(3,3)
		matrixT=np.array(transMatrix.T).reshape(3,1)
		print matrix,matrixT
		for line in arc.interPolationList:
			startPoint=np.array(line.point1.point).reshape(3,1)
			endPoint=np.array(line.point2.point).reshape(3,1)
			startPoint=(matrix.dot(startPoint)+matrixT).reshape(1,3)
			endPoint=(matrix.dot(endPoint)+matrixT).reshape(1,3)
			#type transed [[endPoint]],[[startPoint]]
			point1=point(list(startPoint[0]))
			point2=point(list(endPoint[0]))
			print "transpoint1 :%s,transpoint2： %s" % (point1.point,point2.point)
			transArcLineList.append(Line(point1, point2))
	return transArcLineList
#interpolate before Trans
def interpolateArc(MyEntity):
	for arc in MyEntity.arcList:
		raduis=common.GetTwoPointDistance(arc.centerPoint, arc.startPoint)
		if raduis<thresholdRaduis:
			interpolateByDegree(arc,raduis,arc.startPoint)
		else :
			byLengthStepDegree=asin(perStepLength/raduis)
			interpolateByLength(arc,raduis,arc.startPoint,byLengthStepDegree)
def interpolateByLength(arc,raduis,currentPoint,byLengthStepDegree):
	normal1=[y-x for x,y in zip(arc.centerPoint,currentPoint)]
	normal2=[y-x for x,y in zip(arc.centerPoint,arc.endPoint)]
	if acos(common.NormalCos(normal1, normal2))>byLengthStepDegree:
		print common.GetTwoPointDistance(arc.endPoint, currentPoint)
		alpha=acos(currentPoint[0]/raduis)
		nextPoint=[]
		nextPoint.append(arc.centerPoint[0]+raduis*cos(alpha+byLengthStepDegree))
		nextPoint.append(arc.centerPoint[1]+raduis*sin(alpha+byLengthStepDegree))
		nextPoint.append(arc.centerPoint[2])
		point1=point(currentPoint)
		point2=point(nextPoint)
		arc.interPolationList.append(Line(point1,point2))
		interpolateByLength(arc, raduis, nextPoint,byLengthStepDegree)
	else:
		point1=point(currentPoint)
		point2=point(arc.endPoint)
		arc.interPolationList.append(Line(point1,point2))

def interpolateByDegree(arc,raduis,currentPoint):
	normal1=[y-x for x,y in zip(arc.centerPoint,currentPoint)]
	normal2=[y-x for x,y in zip(arc.centerPoint,arc.endPoint)]
	print arc.centerPoint,arc.endPoint,currentPoint
	if acos(common.NormalCos(normal1, normal2))>perStepDegree:
		alpha=acos(currentPoint[0]/raduis)
		print alpha
		nextPoint=[]
		nextPoint.append(arc.centerPoint[0]+raduis*cos(alpha+perStepDegree))
		nextPoint.append(arc.centerPoint[1]+raduis*sin(alpha+perStepDegree))
		nextPoint.append(arc.centerPoint[2])								#shiftZ
		point1=point(currentPoint)
		point2=point(nextPoint)
		arc.interPolationList.append(Line(point1,point2))
		interpolateByDegree(arc, raduis, nextPoint)
	else:
		point1=point(currentPoint)
		point2=point(arc.endPoint)
		arc.interPolationList.append(Line(point1,point2))
def getProcessArea(LineList):
	x=[x.point1.point[0] for x in LineList ]
	x=x+[x.point2.point[0] for x in LineList ]
	y=[y.point1.point[1] for y in LineList ]
	y=y+[y.point2.point[1] for y in LineList ]
	z=[z.point1.point[2] for z in LineList]
	z=z+[z.point2.point[2] for z in LineList]
	return [min(x),max(x),min(y),max(y),min(z),max(z)]
if __name__ == '__main__':
	filePath="C:/Users/wu/Documents/catia/gradCircle.IGS"
	MyEntity=entity()
	readIges(filePath, MyEntity)
	print len(MyEntity.arcList)
	for arc in MyEntity.arcList:
		print "centerpoint:%s startpoint:%s endpoint%s " % (arc.centerPoint,arc.startPoint,arc.endPoint)
	interpolateArc(MyEntity)
	fig=plt.figure()
	ax=plt.gca(projection='3d')
	for arc in MyEntity.arcList:
		for line in arc.interPolationList:
			#print "point1:%s point2:%s" % (line.point1.point,line.point2.point)
			x=np.array([line.point1.point[0],line.point2.point[0]])
			y=np.array([line.point1.point[1],line.point2.point[1]])
			z=np.array([line.point1.point[2],line.point2.point[2]])
			ax.plot(x,y,z)
	plt.show()
	#trans over the arcInterpolationList
	TransArcLineList=TransArcPoint(MyEntity)
	edgeXYZ=getProcessArea(TransArcLineList)
	print "edgeXYZ:",edgeXYZ
	#assgin the region	
	'''regionSet=set()
	sameRegionList=[]
	for line in TransArcLineList:
		left,right,bottom,top=edgeXYZ[0],edgeXYZ[1],edgeXYZ[2],edgeXYZ[3]
		getRegion(line.point1, left, right, bottom, top)
		getRegion(line.point2, left, right, bottom, top)
		#print line.point1.region,line.point2.region
		if line.point1.regionX!=line.point2.regionX and line.point1.regionY!=line.point2.regionY:
			processDifferentRegionLine(line,sameRegionList,left,bottom)
		elif line.point1.region==line.point2.region:
			continue
		else:
			processOneInSameRegionLine(line,sameRegionList,left,bottom)
		
	for line in sameRegionList:
		print line.point1.region,line.point2.region	
	for line in cutlineList:
		if line.point1.region==line.point2.region:
			sameRegionList.append(line)
	print "print end"
	plotLine(sameRegionList)'''
	fig=plt.figure()
	ax=plt.gca(projection='3d')
	for line in TransArcLineList:
		x=np.array([line.point1.point[0],line.point2.point[0]])
		y=np.array([line.point1.point[1],line.point2.point[1]])
		z=np.array([line.point1.point[2],line.point2.point[2]])
		ax.plot(x,y,z)
	plt.show()

