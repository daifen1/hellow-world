#!/usr/bin/python
# -*- coding: utf-8 -*
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn import datasets
from sklearn import linear_model
from sklearn import svm
from sklearn import naive_bayes
if __name__ == '__main__':
	iris=datasets.load_iris()
	x=iris.data
	y=iris.target
	
	#LinearRegression
	#linear=linear_model.LinearRegression()
	#linear.fit(x, y)
	
	#LogisticRegression/0.96
	#logistic=linear_model.LogisticRegression()
	#logistic.fit(x, y)
	#print logistic.score(x,y)
	#print logistic.coef_

	#svm/0.9866
	#classify=svm.SVC()
	#classify.fit(x,y)
	#print classify.score(x,y)

	#naive_bayes
	bayes=naive_bayes.GaussianNB()
	bayes.fit(x,y)
	print bayes.score(x,y)