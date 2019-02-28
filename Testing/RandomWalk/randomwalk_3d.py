"""
Created on Wed Feb  6 23:09:34 2019

@author: david
"""
import numpy as np
import matplotlib.pyplot as plt
#from astropy.convolution import Gaussian2DKernel,convolve
#import scipy.linalg as linalg
#from mpl_toolkits.mplot3d import Axes3D

N=2000
FILENAME="randomwalk3d_"+str(N)+"_2.dat"

archivo=open(FILENAME,"w")


x=[0]
y=[0]
z=[0]

for i in range(N):
    dx=(np.random.random()-0.5)*2
    dy=(np.random.random()-0.5)*2
    dz=(np.random.random()-0.5)*2
    
    L=np.sqrt(dx**2+dy**2+dz**2)
    
    Dx=dx/L
    Dy=dy/L
    Dz=dz/L
    
    x.append(x[-1]+Dx)
    y.append(y[-1]+Dy)
    z.append(z[-1]+Dz)
    
    sep=" "
    archivo.write(str(x[i])+sep+str(y[i])+sep+str(z[i])+"\n")
    print(i)
archivo.close()
    
    
    
