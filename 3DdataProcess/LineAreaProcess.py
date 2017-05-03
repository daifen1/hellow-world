#!/usr/bin/python
# -*- coding: utf-8 -*

import math
import common
from read_iges import *
import copy
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
sectionX=10
sectionY=10
#get the whole process area by edge of curve
def getProcessArea(MyEntity):
	x=[x.point1.point[0] for x in MyEntity.lineList ]
	x=x+[x.point2.point[0] for x in MyEntity.lineList ]
	y=[y.point1.point[1] for y in MyEntity.lineList ]
	y=y+[y.point2.point[1] for y in MyEntity.lineList ]
	z=[z.point1.point[2] for z in MyEntity.lineList]
	z=z+[z.point2.point[2] for z in MyEntity.lineList ]
	return [min(x),max(x),min(y),max(y),min(z),max(z)]
#get region numbers by sectionx,sectiony
def getRegionNum(edgeXYZ):
	xNum=(edgeXYZ[1]-edgeXYZ[0])/sectionX+1
	yNum=(edgeXYZ[3]-edgeXYZ[2])/sectionY+1
	return xNum*yNum
#cut lines that length is more than min(sectionx,sectiony)
def cutLine(line,cutlineList):
	if common.GetTwoPointDistance(line.point1.point[:2], line.point2.point[:2])>min([sectionX,sectionY]):
		tmp=[]
		tmp.append((line.point1.point[0]+line.point2.point[0])/2)
		tmp.append((line.point1.point[1]+line.point2.point[1])/2)
		tmp.append((line.point1.point[2]+line.point2.point[2])/2)
		midPoint=point(tmp)
		line1=Line(line.point1,midPoint)
		line2=Line(line.point2,midPoint)
		cutLine(line1, cutlineList)
		cutLine(line2, cutlineList)
		'''print "no error line1",line1.point1.point,line1.point2.point
		print "no error line2",line2.point1.point,line2.point2.point
		try:
			cutLine(line1,cutlineList)
			cutline(line2,cutlineList)
		except NameError:
			print "line1:",line1.point1.point,line1.point2.point
			print "line2:",line2.point1.point,line2.point2.point'''
	else:
		cutlineList.append(line)
#assgin the regionX by x of point,edge point included
def getRegionX(thePoint,left,right,minx):
	if right-left<=sectionX:
		thePoint.regionX=str(int((left-minx)/sectionX))
	else:
		mid=left+(int((right-left)/sectionX)+1)/2*sectionX
		if thePoint.point[0]>mid:
			getRegionX(thePoint, mid, right, minx)
		else:
			getRegionX(thePoint, left, mid, minx)
def getRegionY(thePoint,bottom,top,miny):
	if top-bottom<=sectionY:
		print thePoint.point
		thePoint.regionY=str(int((bottom-miny)/sectionY))
	else:
		mid=bottom+(int((top-bottom)/sectionY)+1)/2*sectionY
		if thePoint.point[1]>mid:
			getRegionY(thePoint, mid, top, miny)
		else:
			getRegionY(thePoint, bottom, mid, miny)	
def getRegion(thePoint,left,right,bottom,top):
	getRegionX(thePoint, left, right, left)			#left=minx
	getRegionY(thePoint, bottom, top, bottom)		#bottom=miny
	#print thePoint.regionY.point
	thePoint.region=thePoint.regionY+thePoint.regionX
def get2DGradient(line):
    if line.point1.point[1]==line.point2.point[1]:
        return "vertical"
    elif line.point1.point[0]==line.point2.point[0]:
    	return "horizontal"
    else:
        return (line.point1.point[1]-line.point2.point[1])/(line.point1.point[0]-line.point2.point[0])	
#3D line's gradient
def get3DGradient(smallPoint,bigPoint):
	x=bigPoint.point[0]-smallPoint.point[0]
	y=bigPoint.point[1]-smallPoint.point[1]
	z=bigPoint.point[2]-smallPoint.point[2]
	dist=math.sqrt(x**2+y**2+z**2)
	return [x/dist,y/dist,z/dist]
#process lines that is parraleln to x,y,including edgeline
def processOneInSameRegionLine(line,sameRegionList,left,bottom):
	if line.point1.region!=line.point2.region:
		#print "OneInSameRegionLine %s:%s"%(line.point1.region,line.point2.region)
		if line.point1.point[0]==line.point2.point[0]:
			#can't use the result of cmp to judge
			if cmp(line.point1.point[1],line.point2.point[1])>0: 
				bigPoint=line.point1
				smallPoint=line.point2
			else:
				bigPoint=line.point2
				smallPoint=line.point1
			regeionNum=int((bigPoint.point[1]-bottom)/sectionY)
			edgeY=bottom+regeionNum*sectionY
			D3Grad=get3DGradient(smallPoint,bigPoint)
			#D3Grad may be is smaller than zero
			length=(bigPoint.point[1]-edgeY)/D3Grad[1]
		else:
			if cmp(line.point1.point[0],line.point2.point[0])>0:
				bigPoint=line.point1
				smallPoint=line.point2
			else:
				bigPoint=line.point2
				smallPoint=line.point1
			regeionNum=int((bigPoint.point[0]-left)/sectionX)
			edgeX=left+regeionNum*sectionX
			D3Grad=get3DGradient(smallPoint, bigPoint)
			length=(bigPoint.point[0]-edgeX)/D3Grad[0]

		tmpPoint=[]
		tmpPoint.append(bigPoint.point[0]-length*D3Grad[0])
		tmpPoint.append(bigPoint.point[1]-length*D3Grad[1])
		tmpPoint.append(bigPoint.point[2]-length*D3Grad[2])
		#print "gradient is :%s,length is:%s,regionNum is:%s"% (D3Grad,length,regeionNum)
		#print line.point1.point,line.point2.point,tmpPoint,bigPoint.point
		addCrossRegionLine(line, tmpPoint, sameRegionList)
#add cutCrossRegion line to cutLineList
def addCrossRegionLine(line,tmpPoint,sameRegionList):
	cutPoint1=point(tmpPoint)
	cutPoint1.regionX=line.point1.regionX
	cutPoint1.regionY=line.point1.regionY
	cutPoint1.region=line.point1.region
	cutPoint2=point(tmpPoint)
	cutPoint2.regionX=line.point2.regionX
	cutPoint2.regionY=line.point2.regionY
	cutPoint2.region=line.point2.region
	line1=Line(line.point1,cutPoint1)
	line2=Line(line.point2,cutPoint2)
	sameRegionList.append(line1)
	sameRegionList.append(line2)
	
def processDifferentRegionLine(line,sameRegionList,left,bottom):
	#print "DifferentRegionLine %s:%s"%(line.point1.region,line.point2.region)
	if cmp(line.point1.point[0], line.point1.point[1])>0:
		bigXpoint=line.point1
		smallXpoint=line.point2
	else:
		bigXpoint=line.point2
		smallXpoint=line.point1
	if cmp(line.point1.point[1], line.point2.point[1])>0:
		bigYpoint=line.point1
		smallYpoint=line.point2
	else:
		bigYpoint=line.point2
		smallYpoint=line.point1
	regionNumX=int(bigXpoint.point[0]-left)/sectionX
	regionNumY=int(bigYpoint.point[1]-bottom)/sectionY
	edgeX=left+regionNumX*sectionX
	edgeY=bottom+regionNumY*sectionY
	D3GradX=get3DGradient(smallXpoint, bigXpoint)
	D3GradY=get3DGradient(smallYpoint, bigYpoint)
	cutX,cutY=[],[]
	lengthX=(bigXpoint.point[0]-edgeX)/D3GradX[0]
	lengthY=(bigYpoint.point[1]-edgeY)/D3GradY[1]
	cutX.append(bigXpoint.point[0]-lengthX*D3GradX[0])
	cutX.append(bigXpoint.point[1]-lengthX*D3GradX[1])
	cutX.append(bigXpoint.point[2]-lengthX*D3GradX[2])
	cutY.append(bigYpoint.point[0]-lengthY*D3GradY[0])
	cutY.append(bigYpoint.point[1]-lengthY*D3GradY[1])
	cutY.append(bigYpoint.point[2]-lengthY*D3GradY[2])
	#get crossArea RegionNum
	midPoint=[]
	midPoint.append((cutX[0]+cutY[0])/2)
	midPoint.append((cutX[1]+cutY[1])/2)
	midPoint.append((cutX[2]+cutY[2])/2)
	midRegionX=str(int(midPoint[0]-left)/sectionX)
	midRegionY=str(int(midPoint[1]-bottom)/sectionY)
	pointX=point(cutX)
	pointY=point(cutY)
	#get the distance between point1,pointx,pointy,point2
	if common.GetTwoPointDistance(line.point1.point, pointX.point)<common.GetTwoPointDistance(line.point1.point, pointY.point):
		nearPoint=pointX
		longPoint=pointY
	else:
		nearPoint=pointY
		longPoint=pointX
	#line1
	nearPoint1=point(nearPoint.point)
	nearPoint1.regionX=line.point1.regionX
	nearPoint1.regionY=line.point1.regionY
	nearPoint1.region=line.point1.region
	line1=Line(line.point1,nearPoint1)
	#lineMid
	nearPointMid=point(nearPoint.point)
	nearPointMid.regionX=midRegionX
	nearPointMid.regionY=midRegionY
	nearPointMid.region=midRegionY+midRegionX
	longPointMid=point(longPoint.point)
	longPointMid.regionX=midRegionX
	longPointMid.regionY=midRegionY
	longPointMid.region=midRegionY+midRegionX
	lineMid=Line(nearPointMid,longPointMid)
	#line2
	longPoint2=point(longPoint.point)
	longPoint2.regionX=line.point2.regionX
	longPoint2.regionY=line.point2.regionY
	longPoint2.region=line.point2.region
	line2=Line(line.point2,longPoint2)
	sameRegionList.append(line1)
	sameRegionList.append(line2)
	sameRegionList.append(lineMid)
def plotLine(sameRegionList):
	fig=plt.figure()
	ax=plt.gca(projection='3d')
	for line in sameRegionList:
		x=np.array([line.point1.point[0],line.point2.point[0]])
		y=np.array([line.point1.point[1],line.point2.point[1]])
		z=np.array([line.point1.point[2],line.point2.point[2]])
		ax.plot(x,y,z)
	plt.show()
#def plotGrid():
if __name__ == '__main__':
	MyEntity=entity()
	filePath="C:/Users/wu/Documents/catia/planeLine.IGS"
	readIges(filePath, MyEntity)
	edgeXYZ=getProcessArea(MyEntity)
	#print edgeXYZ
	cutlineList=[]
	for line in MyEntity.line:
		cutLine(line, cutlineList)

	regionSet=set() 				#to get no-repeat region number
	sameRegionList=[]
	for line in cutlineList:
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
	plotLine(sameRegionList)
	