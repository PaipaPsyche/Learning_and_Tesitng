# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 15:16:50 2018

@author: David
"""

import numpy as np
import matplotlib.pyplot as plt


n_time=500
step=1
m_range=16  

def weight(t):
    return gain*np.sin(t*np.pi/50)



plt.figure(figsize=(12,m_range*2))
for g in range (m_range):
    gain=g*(0.5/m_range)
    time=[]
    val=[]
    value=0
    for i in range (n_time):
        trend=0.5+weight(i)
        k=np.random.random()
        if(k<=trend):
            value=value-step
        else:
            value=value+step
        val.append(value)
        time.append(i)
        plt.subplot(m_range,2,g+1)
        plt.plot(time,val)