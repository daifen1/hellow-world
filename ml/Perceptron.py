#!/usr/bin/python
# -*- coding: utf-8 -*
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
	iterNum=1000
	alpha=0.1

	train_x=np.array([[1,1.5,1],[1.5,3,1],[2,2.4,1],[2.5,3.8,1],[3,3.9,1]])
	train_y=np.array([-1,1,-1,1,-1])
	w0,w1,w2=0,0,0
	param=np.array([w1,w2,w0])
	param.reshape(3,1)
	#print train_x[1].dot(param),type(train_x[1])
	length=len(train_x)
	#cal the J(w)
	for iter in range(iterNum):
		for x in range(len(train_x)):
			#print "train_x[x].dot(param)*train_y[x]",train_x[x].dot(param)*train_y[x]
			if train_x[x].dot(param)*train_y[x]<=0:
				w1=w1+alpha*train_x[x][0]*train_y[x]
				w2=w2+alpha*train_x[x][1]*train_y[x]
				w0=w0+alpha*train_y[x]
				param=np.array([w1,w2,w0]).reshape(3,1)
				#print "x",x,param
	x=np.linspace(0,5,100)
	y=x*(-w1/w2)+(-w0/w2)
	fig=plt.figure()
	ax=plt.subplot(111)
	ax.scatter(x,y)
	y=np.array([x[1] for x in train_x])
	x=np.array([x[0] for x in train_x])
	print len(x),len(y)
	ax.scatter(x,y,'b',lw=3)
	plt.show()
