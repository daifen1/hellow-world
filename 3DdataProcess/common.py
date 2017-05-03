# -*- coding: utf-8 -*
# give two point,return the distance

import math
import numpy as np
from numpy import pi
'''
GetLineLength(vertexA, vertexB)    计算两点之间的距离

GetTriangleArea(myTriangle)        计算三角形的面积
GetLongesSide(triangle)            得到三角形的最长边
devideTriangle                     按照最长边，分割三角形，返回两个三角形
NormalCos(vecter1, vecter2)        计算两法矢的cos值
quickSort(num, l, r)               快速排序，r=len(num)-1,以下标来计算
GetRotationAngle(Normal)           计算将法向量旋转到(0,0,1)的A、C角
TransArcToDegree(arc)              将弧度转化为角度
GetTwoVertexDistance(vertex1,vertex1)  计算两顶点的欧氏距离
'''


class Triangle(object):
    """docstring for Triangle"""

    def __init__(self, vecter, vertexA, vertexB, vertexC):
        super(Triangle, self).__init__()
        self.vecter = vecter
        self.vertexA = vertexA
        self.vertexB = vertexB
        self.vertexC = vertexC


def GetTwoPointDistance(vertexA, vertexB):
    
    if len(vertexA)==3:
        sum = (vertexA[0] - vertexB[0]) * (vertexA[0] - vertexB[0]) + (vertexA[1] - vertexB[1]) * \
        (vertexA[1] - vertexB[1]) + (vertexA[2] -
                                     vertexB[2]) * (vertexA[2] - vertexB[2])
        return math.sqrt((vertexA[0] - vertexB[0])**2 + (vertexA[1] - vertexB[1])**2 + (vertexA[2] - vertexB[2])**2)
    elif len(vertexA)==2:
        sum=(vertexA[0] - vertexB[0]) **2 + (vertexA[1] - vertexB[1]) **2
        return math.sqrt(sum)
# give the Triangle,retuan the Area of triangle


def GetTriangleArea(myTriangle):
    a = GetLineLength(myTriangle.vertexA, myTriangle.vertexB)
    b = GetLineLength(myTriangle.vertexA, myTriangle.vertexC)
    c = GetLineLength(myTriangle.vertexB, myTriangle.vertexC)
    # calculate the Area by QingJiushao Algorithm
    m = (a + b + c) / 2
    return math.sqrt(m * (m - a) * (m - b) * (m - c))
# give a triangle,return the longest side in type of two vertex


def GetLongesSide(triangle):
    if GetLineLength(triangle.vertexA, triangle.vertexB) > GetLineLength(triangle.vertexA, triangle.vertexC):
        if GetLineLength(triangle.vertexA, triangle.vertexB) > GetLineLength(triangle.vertexB, triangle.vertexC):
            return [triangle.vertexA, triangle.vertexB]
        else:
            return [triangle.vertexB, triangle.vertexC]
    elif GetLineLength(triangle.vertexA, triangle.vertexC) > GetLineLength(triangle.vertexB, triangle.vertexC):
        return [triangle.vertexA, triangle.vertexC]
    else:
        return [triangle.vertexB, triangle.vertexC]
# give a triangle and two vertex of its longest side,return two triangle


def devideTriangle(triangle, twoPoint):
    point1 = np.array(twoPoint[0])
    point2 = np.array(twoPoint[1])
    point = (point1 + point2) / 2
    setpoint1 = set(twoPoint[0])
    setpoint2 = set(twoPoint[1])
    if (len(set(triangle.vertexA) | setpoint1) != 3)and(len(set(triangle.vertexA) | setpoint2) != 3):
        triangle1 = Triangle(
            triangle.vecter, triangle.vertexA, twoPoint[0], point)
        triangle2 = Triangle(
            triangle.vecter, triangle.vertexA, twoPoint[1], point)
        return [triangle1, triangle2]
    elif(len(set(triangle.vertexB) | setpoint1) != 3)and(len(set(triangle.vertexB) | setpoint2) != 3):
        triangle1 = Triangle(
            triangle.vecter, triangle.vertexB, twoPoint[0], point)
        triangle2 = Triangle(
            triangle.vecter, triangle.vertexB, twoPoint[1], point)
        return [triangle1, triangle2]
    else:
        triangle1 = Triangle(
            triangle.vecter, triangle.vertexC, twoPoint[0], point)
        triangle2 = Triangle(
            triangle.vecter, triangle.vertexC, twoPoint[1], point)
        return [triangle1, triangle2]
# give two Normal,return their cos


def NormalCos(vecter1, vecter2):

    array1 = np.array(vecter1)
    array2 = np.array(vecter2)
    array = array1 * array2
    sumary1 = math.sqrt(array1[0] * array1[0] +
                        array1[1] * array1[1] + array1[2] * array1[2])
    sumary2 = math.sqrt(array2[0] * array2[0] +
                        array2[1] * array2[1] + array2[2] * array2[2])
    return np.sum(array) / (sumary1 * sumary2)

# give a list,listIndex,edge of index,return sorted list,listIndex


def quickSort(num, l, r):
    if l >= r:  # 如果只有一个数字时，结束递归
        return
    flag = l
    for i in range(l + 1, r + 1):  # 默认以第一个数字作为基准数，从第二个数开始比较，生成索引时要注意右部的值
        if num[flag] > num[i]:
            tmp = num[i]
            del num[i]
            num.insert(flag, tmp)

            flag += 1
    quickSort(num,  l, flag - 1)  # 将基准数前后部分分别递归排序
    quickSort(num,  flag + 1, r)
# give the Normal,return the needed angleA and angleC that rotate to
# Normal(0,0,1)


def GetRotationAngle(Normal):
    if Normal[2] < 0:
        print "out of range,can't GetRotationAngle!"
    angleA = math.acos(Normal[2])

    if Normal[0] == 0 and Normal[1] == 0:
        angleA = 0
        angleC = 0
    elif Normal[1] == 0:
        if Normal[0] > 0:
            angleC = math.pi / 2
        else:
            angleC = -math.pi / 2
    elif Normal[0] == 0 and Normal[1] < 0:
        angleC = math.pi
    else:
        angleC = math.atan(Normal[0] / Normal[1])  # (-pi/2,pi/2)
        if Normal[0] < 0 and Normal[1] < 0:
            angleC = angleC - math.pi
        if Normal[0] > 0 and Normal[1] < 0:
            angleC = angleC + math.pi
    # 不需要返回角度，而是用弧度
    if angleC != math.pi / 2 and angleC != -math.pi / 2:
        angleA = angleA * 180 / math.pi
        angleC = angleC * 180 / math.pi
    return [angleA, angleC]


def TransArcToDegree(Arc):
    for x in range(len(Arc)):
        Arc[x] = Arc[x] * 180 / math.pi


def TransDegreeToArc(Degree):
    for x in range(len(Degree)):
        Degree[x] = Degree[x] / 180 * math.pi
if __name__ == '__main__':

    Arc = [math.pi / 4, math.pi / 2]
    TransArcToDegree(Arc)
    print Arc
