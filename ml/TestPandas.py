#!/usr/bin/python
# -*- coding: utf-8 -*
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from sklearn import datasets

if __name__ == '__main__':
	s=pd.Series([1,3,5,np.nan,6,8])
	dates=pd.date_range('20170502',periods=6)
	df=pd.DataFrame(np.random.randn(6,4),index=dates,columns=list('ABCD'))
	df2=pd.DataFrame({'A':1.,'B':pd.Timestamp('20170503'),'C':np.array([3]*5)})
	df2.head(2)
	df2.tail(2)
	df2.index  #纵坐标
	df2.columns 	#横坐标
	iris=datasets.load_iris()
	iris_df=pd.DataFrame(iris.data,columns=list(['x0','x1','x2','x3']))
	#前两行
	iris_df.head(2)
	#后两行
	iris_df.tail(2)
	#值
	iris_df.values
	#获得mean/min/std等
	iris_df.describe()
	#转置
	iris_df.T
	#改变columns排序
	iris_df.sort_index(axis=1,ascending=False)
	#这个版本没有
	#iris_df.sort_values(by='x0')


	#切片
	iris_df['x0']
	iris_df[0:3]


	#通过label索引
	#某行
	iris_df.loc[3]
	#某些行，某些列
	iris_df.loc[1:30,['x0','x3']]
	#单个元素
	iris_df.loc[2,'x0']
	iris_df.at[1,'x0']

	#整数position索引,即横坐标不用x0/x1而用整数
	iris_df.iloc[3]
	iris_df.iloc[3,2:4]
	#通过list，List中数字为Position
	iris_df.iloc[[1,2,4],[0,2]]
	iris_df.iloc[1:4,]

	#与iloc相似
	iris_df.iat[1,1]