import math
import common
from read_iges import *
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
def getProcessArea(MyEntity):
	x=[x.point1.point[0] for x in MyEntity.line ]
	x=x+[x.point2.point[0] for x in MyEntity.line ]
	y=[y.point1.point[1] for y in MyEntity.line ]
	y=y+[y.point2.point[1] for y in MyEntity.line ]
	z=[z.point1.point[2] for z in MyEntity.line ]
	z=z+[z.point2.point[2] for z in MyEntity.line ]
	return [min(x),max(x),min(y),max(y),min(z),max(z)]
if __name__ == '__main__':
	MyEntity=entity()
	filePath="C:/Users/wu/Documents/catia/planeLine.IGS"
	readIges(filePath, MyEntity)
	edgeXYZ=getProcessArea(MyEntity)
	print edgeXYZ