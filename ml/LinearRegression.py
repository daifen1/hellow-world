
# -*- coding: utf-8 -*
#!/usr/bin/python
import numpy as np
import pandas as pd
from sklearn import datasets
import random
import matplotlib.pyplot as plt
#get the database
x=np.linspace(0,5,50)
y=np.array([x+random.uniform(-0.2, 0.2) for x in x])
print type(y)
fig=plt.figure()
plt.plot(x,y)
plt.show()