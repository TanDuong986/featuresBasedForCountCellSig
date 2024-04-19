import numpy as np
import matplotlib.pyplot as plt

y=np.ones(1000,dtype=float)
x=0.001
x_list=[]
for i in range(1000):
    x_ini=x*i
    x_list.append(x_ini)

plt.plot(x_list,y,'o')
plt.show()


