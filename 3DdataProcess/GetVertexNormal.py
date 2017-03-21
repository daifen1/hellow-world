#!/usr/bin/python
# -*- coding: utf-8 -*
import STLdata as stl
import common
import read_iges as iges
from math import cos, sin, atan
import math
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def AddToVertexList(union, vertexSet):
    vertexList.append(union.Triangle.vertexA)
    vertexList.append(union.Triangle.vertexB)
    vertexList.append(union.Triangle.vertexC)

#删除三角形中重复的顶点，得到顶点集合
def GetNorepeatVertex(UnionList, vertexList, vertexset):
    for union in UnionList:
        AddToVertexList(union, vertexList)
    # print len(vertexList)
    for vertex in vertexList:
        string = str(vertex[0]) + '|' + str(vertex[1]) + '|' + str(vertex[2])
    vertexset.add(string)
    vertexStrList = list(vertexset)
    del vertexList
    vertexList = []
    for vertexstr in vertexStrList:
        string = vertexstr.split('|')
        vertexList.append(
            [float(string[0]), float(string[1]), float(string[2])])

#给定dot，顶点集合vertexList,得到dot最近的三个点，存入ThreeVertex
def GetNearestThreeVertex(dot,vertexList,ThreeVertex):
	nearestVertexMap = dict()
	for vertex in vertexList:
		vertexType = type(vertex)
		if vertexType.__name__ == 'ndarray':
			vertex = vertex.tolist()  # 之前生成数据有ndarray
		# print type(vertex)
		distance = math.sqrt((vertex[0] - dot[0])**2+(vertex[1] - dot[1])**2 + (vertex[2] -dot[2])**2)
		#distance=common.GetTwoPointDistance(vertex, testVertex)
		nearestVertexMap[distance] = vertex
		if len(nearestVertexMap)>3:
			keys=sorted(nearestVertexMap.keys())
			nearestVertexMap.pop(keys[3])
	keys=nearestVertexMap.keys()
	for key in keys:
		#print nearestVertexMap[key]
		ThreeVertex.append(nearestVertexMap[key])
		#print nearestVertexMap[key]
#计算三点所在平面法向量，并归一化
def GetNormal(ThreeVertex):
	ThreeVertex=np.array(ThreeVertex)
	#print ThreeVertex
	AB=ThreeVertex[0]-ThreeVertex[1]
	AC=ThreeVertex[0]-ThreeVertex[2]
    #print AB,AC 
	Normal=[AB[1]*AC[2]-AC[1]*AB[2],AC[0]*AB[2]-AB[0]*AC[2],AB[0]*AC[1]-AC[0]*AB[1]]
	Normal=np.array(Normal)
	Normal=Normal/math.sqrt(Normal[0]**2+Normal[1]**2+Normal[2]**2)
	return Normal
if __name__ == "__main__":
	#STL文件
	UnionList = []
	vertexstrertexList = []
	vertexset = set()
	vertexList=[]
	filePath="E:\\halfBall.STL"
	stl.GetTriangleUninList(filePath,UnionList)
	GetNorepeatVertex(UnionList, vertexList, vertexset)

	#Iges文件
	DotList=[]
	igesFilePath="C:/Users/wu/Documents/catia/lineDot.IGS"
	iges.readIges(igesFilePath,DotList)

	NormalList=[]
	for dot in DotList:
		ThreeVertex=[]
		GetNearestThreeVertex(dot, vertexList, ThreeVertex)
		NormalList.append(GetNormal(ThreeVertex))
		print GetNormal(ThreeVertex)
