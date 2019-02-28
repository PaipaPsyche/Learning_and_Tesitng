"""
Created on Sun Sep  2 10:55:28 2018

@author: David Paipa
"""
import numpy as np
#import matplotlib.pyplot as plt
#from astropy.convolution import Gaussian2DKernel,convolve
#import scipy.linalg as linalg
#from mpl_toolkits.mplot3d import Axes3D
data=[]
with open('listado.txt', 'r') as myfile:
    data=myfile.read().replace('\n', ' ')
data=data.split()
data=np.array(data)
inicial=data.copy()
n_words=len(data)
for i in range(n_words):
    inicial[i]=list(data[i])[0]

def darListadoConInicial(a):
    ii=(inicial==a)
    return data[ii]

def genRanIndex(n):
    return int(n*np.random.random())+1

def NpalabrasCon(N,a):
    ans=[]
    lista=darListadoConInicial(a)
    for i in range (N):
        ans.append(np.random.choice(lista))
    return np.array(ans)

def  NrandWords(N, pr=False):
    r=[]
    for i in range (N):
        aa=data[genRanIndex(n_words)]
        if (pr==True):
            print(aa)
        r.append(aa)
    return np.array(r)

def find(word):
    ind=np.where(data==word)[0]
    if(ind.size==0):
        print('La palabra no existe en el registro.')
    else:
        print("La palabra '"+word+"' fue hallada en la posición "+str(ind[0])+" del arreglo de datos.")
        



