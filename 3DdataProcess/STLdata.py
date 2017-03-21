#!/usr/bin/python
# -*- coding: utf-8 -*
import math
from math import cos, sin, atan
import numpy as np
import common as common
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
# import common.Triangle as Triangle

'''class Triangle(object):
    """docstring for Triangle"""

    def __init__(self, vecter, vertexA, vertexB, vertexC):
        super(Triangle, self).__init__()
        self.vecter = vecter
        self.vertexA = vertexA
        self.vertexB = vertexB
        self.vertexC = vertexC'''


class Union(object):
    """docstring for Union"""

    def __init__(self, Triangle, Area, Region, regionX, regionY, Index):
        super(Union, self).__init__()
        self.Triangle = Triangle
        self.Area = Area
        self.Region = Region
        self.regionX = regionX
        self.regionY = regionY
        self.Index = Index
# Sava STLdata in Triangle list,including vector,vertex and Area
# remove the '\n' firstly can delete the unnessceary space
regionLength = 20
fittingArea = 1
# 装入所有union的LIST
RegionList = []  # 按region装入union的LIST
RegionNum = set()  # 装入所有不含有#的Region编号
RegionNumList = []  # Region编号按顺序存储
NormalList = []  # Region 法矢存储链表
RotationAngleList = []  # 各region旋转到[0,0,1]需要的角度[angle1,angleC]
# getSTLdata(file)                       读取STL文件，将数据保存至Union当中
# removeBottomTriangle(union)            STL为封闭图形，去掉最底层的平面(z==0)
# GetMinandMax(UnionList)                得到整个STL数据的xyz边界
# fittingTriangle(triangle, Area)        根据面积，判断三角形是否需要分割
# devideToEnd(union)                     将需要分割的三角形一直分割，知道面积满足要求
# judgeRegionX(union, left, right, minX) 判断三顶点的x坐标，判断是否属于同一块x区域
# judgeRegionY(union, left, right, minX) 判断三顶点的x坐标，判断是否属于同一块x区域

#得到符合要求的三角形list
def GetTriangleUninList(filePath,UnionList):
    file=open(filePath,'r+')
    getSTLdata(file, UnionList)
    removeBottomTriangle(UnionList)
    for union in UnionList:
        devideToEnd(union, UnionList)

def getSTLdata(file, UnionList):
    STLfile = file.read()
    # sava everyLine as a List
    # remove the '\n'at the end of line
    STLlist = STLfile.split('\n')
    STLSplitList = []
    for line in STLlist:
        STLSplitList.append(line.split())

    # Sava the data UnionList
    # TriangleList = []
    # UnionList = []
    for n in range(len(STLSplitList)):
        if n % 7 == 1 and n != len(STLSplitList) - 2:
            myTriangle = common.Triangle([], [], [], [])
        if n % 7 == 1 and n != len(STLSplitList) - 2:
            myTriangle.vecter.append(float(STLSplitList[n][2]))
            myTriangle.vecter.append(float(STLSplitList[n][3]))
            myTriangle.vecter.append(float(STLSplitList[n][4]))
        if n % 7 == 3:
            myTriangle.vertexA.append(float(STLSplitList[n][1]))
            myTriangle.vertexA.append(float(STLSplitList[n][2]))
            myTriangle.vertexA.append(float(STLSplitList[n][3]))
        if n % 7 == 4:
            myTriangle.vertexB.append(float(STLSplitList[n][1]))
            myTriangle.vertexB.append(float(STLSplitList[n][2]))
            myTriangle.vertexB.append(float(STLSplitList[n][3]))
        if n % 7 == 5:
            myTriangle.vertexC.append(float(STLSplitList[n][1]))
            myTriangle.vertexC.append(float(STLSplitList[n][2]))
            myTriangle.vertexC.append(float(STLSplitList[n][3]))

        if n % 7 == 0 and n > 1:
            # TriangleList.append(myTriangle)
            Area = common.GetTriangleArea(myTriangle)
            myUnion = Union(myTriangle, Area, '##', '#', '#', 0)
            UnionList.append(myUnion)
    return UnionList


def removeBottomTriangle(UnionList):
    for x in range(len(UnionList) - 1, -1, -1):
        union = UnionList[x]
        if union.Triangle.vertexA[2] == union.Triangle.vertexB[2] == union.Triangle.vertexC[2] < 2e-14:
            UnionList.remove(union)
        # print len(UnionList)
# get the edge of UnionList


def GetMinandMax(UnionList):
    minMax = []
    x = []
    y = []
    z = []
    for union in UnionList:
        triangle = union.Triangle
        x.extend([triangle.vertexA[0], triangle.vertexB[0], triangle.vertexC[0]])
        y.extend([triangle.vertexA[1], triangle.vertexB[1], triangle.vertexC[1]])
        z.extend([triangle.vertexA[2], triangle.vertexB[2], triangle.vertexC[2]])
    minMax.append(min(x))
    minMax.append(max(x))
    minMax.append(min(y))
    minMax.append(max(y))
    minMax.append(min(z))
    minMax.append(max(z))
    return minMax


def fittingTriangle(triangle, Area):
    if Area < fittingArea:
        triangle2 = common.Triangle([], [], [], [])
        return [triangle, triangle2]
    else:
        twoPoint = common.GetLongesSide(triangle)
        return common.devideTriangle(triangle, twoPoint)

# process the bigArea Triangle until it meet the expectation


def devideToEnd(union, UnionList):

    [triangle1, triangle2] = fittingTriangle(
        union.Triangle, union.Area)
    if triangle2.vecter != []:
        Area1 = common.GetTriangleArea(triangle1)
        Area2 = common.GetTriangleArea(triangle2)
        union1 = Union(triangle1, Area1, '##', '#', '#', 0)
        union2 = Union(triangle2, Area2, '##', '#', '#', 0)
        UnionList.append(union1)
        UnionList.append(union2)
        devideToEnd(union1, UnionList)
        devideToEnd(union2, UnionList)


# assgin x to its region,if three x of the triangle belong to the same XRegion


def judgeRegionX(union, left, right, minX):
    if right - left <= regionLength:
        if union.Triangle.vertexB[0] < right and union.Triangle.vertexB[0] > left:
            if union.Triangle.vertexC[0] < right and union.Triangle.vertexC[0] > left:
                regionXNum = int((left - minX) / regionLength)
                union.regionX = str(regionXNum)
    else:
        middle = left + (int((right - left) / regionLength) +
                         1) / 2 * regionLength
        # print "x:%s  left:%s  middle:%s  right%s" %
        # (union.Triangle.vertexA[0], left, middle, right)
        if union.Triangle.vertexA[0] < middle:
            judgeRegionX(union, left, middle, minX)
        else:
            judgeRegionX(union, middle, right, minX)

# assgin Y to its region,if three y of the triangle belong to the same YRegion


def judgeRegionY(union, left, right, minY):
    if right - left <= regionLength:
        # print "right-left:%s" % (right - left)
        if union.Triangle.vertexB[1] < right and union.Triangle.vertexB[1] > left:
            if union.Triangle.vertexC[1] < right and union.Triangle.vertexC[1] > left:
                regionYNum = int((left - minY) / regionLength)
                union.regionY = str(regionYNum)
    else:
        middle = left + (int((right - left) / regionLength) +
                         1) / 2 * regionLength
        if union.Triangle.vertexA[1] < middle:
            judgeRegionY(union, left, middle, minY)
        else:
            judgeRegionY(union, middle, right, minY)

# Create LIst to storage union by union.Region
# create list to storage Region,the number of List depend on the edge of x,y


def CreateRegionListList(minX, maxX, minY, maxY):
    xNum = int((maxX - minX) / regionLength) + 1
    yNum = int((maxY - minY) / regionLength) + 1
    num = xNum * yNum
    # print num
    for x in range(num + 1):  # 4*4+1
        RegionList.append([])
    # print RegionList
# 返回按大小顺序存储的Region编号


def GetRegionNumList():
    for x in range(10):
        if ('0' + str(x)) in RegionNum:
            RegionNumList.append('0' + str(x))
    for x in range(10, 100):
        if str(x) in RegionNum:
            RegionNumList.append(str(x))
    common.quickSort(RegionNumList, 0, len(RegionNumList) - 1)

# 将每个union根据region分配给RegionList


def assginUnionToRegion(union):
    for x in range(len(RegionNumList)):
        if union.Region == RegionNumList[x]:
            RegionList[x].append(union.Index)
    if union.regionX == '#' or union.regionY == '#':
        RegionList[len(RegionList) - 1].append(union.Index)
# Assgin Triangle by three vertex in the same Region


def FirstAssginTriangleArea(minX, maxX, minY, maxY):
     # create list to storage Region,the number of List depend on the edge of
     # x,y
    CreateRegionListList(minX, maxX, minY, maxY)
    count = 0
    for union in UnionList:
        union.Index = count
        count += 1
        judgeRegionX(union, minX, maxX, minX)
        judgeRegionY(union, minY, maxY, minY)
        union.Region = union.regionY + union.regionX
        if (union.regionY != '#') and (union.regionX != '#'):
            RegionNum.add(union.Region)  # 将region编号存入set中
    GetRegionNumList()         # 按大小顺序存储region编号,但没33/#x,x#,##分配时，也将这些数据处理
    # print RegionNumList
    for union in UnionList:
        assginUnionToRegion(union)
# 得到各分区的法矢


def GetRegionNormal(x):
    sum = np.array([0, 0, 0])
    for index in RegionList[x]:
        # print UnionList[index].Triangle.vecter
        sum = sum + np.array(UnionList[index].Triangle.vecter) * \
            UnionList[index].Area
        # print np.array(UnionList[index].Triangle.vecter) *
        # UnionList[index].Area
    # print sum
    sqrtSum = math.sqrt(sum[0] * sum[0] + sum[1]
                        * sum[1] + sum[2] * sum[2])
    # print sqrtSum, sum
    NormalList.append((sum / sqrtSum).tolist())
# 旋转三角形一顶点的坐标


def RotationVertex(vertex, angleA, angleC):
    x = vertex[0] * cos(angleC) - vertex[1] * sin(angleC)
    y = vertex[0] * cos(angleA) * sin(angleC) + vertex[1] * \
        cos(angleA) * cos(angleC) - vertex[2] * sin(angleA)
    z = vertex[0] * sin(angleA) * sin(angleC) + vertex[1] * \
        sin(angleA) * cos(angleC) + vertex[2] * cos(angleA)
    return [x, y, z]
# 计算并打印旋转区域图


def RotaionRegion(num, xList, yList, zList):
    angleA = RotationAngleList[num][0]
    angleC = RotationAngleList[num][1]
    for Index in RegionList[1]:
        triangle = UnionList[Index].Triangle
        vertex = RotationVertex(triangle.vertexA, angleA, angleC)
        xList.append(vertex[0])
        yList.append(vertex[1])
        zList.append(vertex[2])
        vertex = RotationVertex(triangle.vertexB, angleA, angleC)
        xList.append(vertex[0])
        yList.append(vertex[1])
        zList.append(vertex[2])
        vertex = RotationVertex(triangle.vertexC, angleA, angleC)
        xList.append(vertex[0])
        yList.append(vertex[1])
        zList.append(vertex[2])
# 3Dplot


def plot(xList, yList, zList):
    xList = np.array(xList)
    yList = np.array(yList)
    zList = np.array(zList)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(xList, yList, zList, c='y')
    # ax.axis([-60, 60, -60, 60])
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()
# plot区域点状图


def plotOneRegion(num):

    x, y, z = [], [], []
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for Index in RegionList[num]:
        triangle = UnionList[Index].Triangle
        x.append(triangle.vertexA[0])
        x.append(triangle.vertexB[0])
        x.append(triangle.vertexC[0])
        y.append(triangle.vertexA[1])
        y.append(triangle.vertexB[1])
        y.append(triangle.vertexC[1])
        z.append(triangle.vertexA[2])
        z.append(triangle.vertexB[2])
        z.append(triangle.vertexC[2])
    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    ax.scatter(x, y, z, c='y')
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()
# plot全部region的点状图


def plotAllRegion():

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    for num in range(len(RegionList) - 1, -1, -1):
        x, y, z = [], [], []

        for Index in RegionList[num]:
            x.append(UnionList[Index].Triangle.vertexA[0])
            x.append(UnionList[Index].Triangle.vertexB[0])
            x.append(UnionList[Index].Triangle.vertexC[0])
            y.append(UnionList[Index].Triangle.vertexA[1])
            y.append(UnionList[Index].Triangle.vertexB[1])
            y.append(UnionList[Index].Triangle.vertexC[1])
            z.append(UnionList[Index].Triangle.vertexA[2])
            z.append(UnionList[Index].Triangle.vertexB[2])
            z.append(UnionList[Index].Triangle.vertexC[2])
        x = np.array(x)
        y = np.array(y)
        z = np.array(z)
    # print len(x), len(y), len(z)
        ax.scatter(x, y, z, 'y')

        # plt.hold(False)
    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.show()
# the main function
if __name__ == "__main__":
    UnionList = []
    file = open("E:\\halfBall.STL", 'r+')
    getSTLdata(file, UnionList)

    # delete the BOttom Triangle

    removeBottomTriangle(UnionList)

    # process the Triangle,scatter it by divide its longest side
    for union in UnionList:
        devideToEnd(union, UnionList)
    # use 'for' to remove the LIST may result in error
    # 初始时不符合、处理时不符合的三角形并未删除,采用倒序删除
    for i in range(len(UnionList) - 1, -1, -1):
        if UnionList[i].Area > fittingArea:
            UnionList.remove(UnionList[i])

        # Get the edge of STLdata
    [minX, maxX, minY, maxY, minZ, maxZ] = GetMinandMax(UnionList)
    FirstAssginTriangleArea(minX, maxX, minY, maxY)
    # plotAllRegion()
    # 判断两个顶点是否在该区域

    # 得到各分区的拟合法矢,计算拟合法矢到[0,0,1]的旋转角度,默认为弧度，检查可以写一个角度函数
    for x in range(len(RegionList) - 2):
        GetRegionNormal(x)
        # print NormalList[x]
        RotationAngleList.append(common.GetRotationAngle(NormalList[x]))

    # 判断各区域是否有三角形矢量与拟合矢量角度过大
    for num in range(len(RegionList) - 2):
        for Index in RegionList[num]:
            if common.NormalCos(UnionList[Index].Triangle.vecter, NormalList[num]) < (math.sqrt(3) / 2):
                print UnionList[Index].Region
    #
    for num in range(len(RegionList) - 2):
        angleA = RotationAngleList[num][0]
        angleC = RotationAngleList[num][1]
        RotationRegionNormal = RotationVertex(NormalList[num], angleA, angleC)

        for Index in RegionList[num]:
            normal = UnionList[Index].Triangle.vecter
            normal = RotationVertex(normal, angleA, angleC)
            if common.NormalCos(normal, RotationRegionNormal) < (math.sqrt(3) / 2):
                print UnionList[Index].Region
    '''xList, yList, zList = [], [], []
    RotaionRegion(2, xList, yList, zList)
    plot(xList, yList, zList)'''
    '''nx, ny, nz = [], [], []
    for Index in RegionList[5]:
        vecter = UnionList[Index].Triangle.vecter
        NormalX = vecter[0] * math.cos(angleC) - vecter[1] * math.sin(angleC)
        NormalY = vecter[0] * math.cos(angleA) * math.sin(angleC) + vecter[1] * math.cos(
            angleA) * math.cos(angleC) - vecter[2] * math.sin(angleA)
        NormalZ = vecter[0] * math.sin(angleA) * math.sin(angleC) + vecter[1] * math.sin(
            angleA) * math.cos(angleC) + vecter[2] * math.cos(angleA)
        nx.append(NormalX)
        ny.append(NormalY)
        nz.append(NormalZ)
        # print[NormalX, NormalY, NormalZ]'''
