"""
Created on Thu Aug 30 22:00:29 2018

@author: David Paipa
"""
#========================MOTIVATION==========================
#As you may know, being a programmer sometimes suck. And it sucks 
#because you keep doing mini functions that may save your ass a couple
#times. BUT as you may also know, you keep needing this tiny fuckers once
#in a while because your logic is used to it. This implies a very stressed
#version of you copying it from file to file, hoping to be right.

#I would like to avoid this by creating my own "function repository" in order
#to "make my life better" and eventually "kill myself" in peace as a decent
#undergraduate physics student.

#========================OBSERVATIONS============================


#======================DOCUMENTATION============================

#**********minmax2D**************************
#PARAM = [Mat]
#Mat = 2D Array 

#This function extracts the minimum (min) and maximum(max) value from 
#a 2D Array.
#RETURNS min , max
#********************isPrime****************************
#PARAM = [n,printingDescriptive]
#n = integer ( n>=0)
#printingDescriptive = Boolean (False by default)
#
#This fuction determines if n is (TRUE) a prime number or not (FALSE).
#printingDescriptive allows to print a descriptive message on the answer.
#RETURNS Boolean
#********************primesUntil************************
#PARAM = [N,printing]
#N = integer (N>=0)
#prinitng = Boolean (False by default)
#PrintingDescriptive = Boolean(False by Default)
#
#Returns the prime numbers smaller than N or equal to N.
#printing allows the fuction to print all prime numbers until N.
#printingDescriptive allows to print a descriptive message on every number
#from o to N-1.
#RETURNS integer array
#*******************statValues***************************
#PARAM = [Arr,printing]
#Arr = Array
#printing = Boolean(False by default)
#
#Returns relevant statistical values.
#In order : mean , median, mode , std deviation , variance
#printing allows the function to print a descriptive text on this values.
#RETURNS float , float , float , float , float 
#**********************CrossInPeriodicalCond***********************
#PARAM = [coords,sizes]
#coords = 1D Array
#sizes = 1D Array
#*Note:coords length must be the same as sizes length!
#
#Returns an array with the coordinates (in n dimensions) for the  
# 2n points adyacent(in a grid with dimensions sizes ) to a point 
# with coordinates coords. Inmediate Neighbors.
#RETURNS Array[2n,n]
#************************dice*************************************
#PARAM = [n_faces]
#n_faces = integer
#
#Returns the result of tossing a dice with n_faces faces. 
#RETURNS integer
#***************************distributionDices**********************
#PARAM = [N_dices,n_faces, toss]
#N_dices = integer
#n_dices = integer
#toss = integer (10000 by default)
#
#tosses 'N_dices' dices with 'n_faces' faces and sum up the results. this
#process 'toss' times. 
#returns an array with 'toss' results on it.
#RETURNS Array[toss]
#
#
#
#---------------WHY----------------------------------
#*********************killingit***********************
#Just dont.
#string i.e. "abababa" 
#a = write random word
#b = write random float
#string describes probability distribution
#
#===========================CODE================================
import numpy as np
#import matplotlib.pyplot as plt
#from astropy.convolution import Gaussian2DKernel,convolve
#import scipy.linalg as linalg
#from mpl_toolkits.mplot3d import Axes3D
#test_data=np.loadtxt("testData.txt")
#***********************************************************************
def minmax2D(Mat):
    mayor=0
    menor=0
    tamx=Mat.shape[0]
    tamy=Mat.shape[1]
    for i in range(int(tamx)):
        for j in range(int(tamy)):
            num=Mat[i,j]
            if(num<menor):
                menor=num
            if(num>mayor):
                mayor=num
    return menor , mayor
#***********************************************************************
def isPrime(n,printingDescriptive=False):
    r=True
    s=2

    if((n==0)or(n==1)):
        r=False
    while((s<n)and(r==True)):
        if((n/s)%1==0):
            r=False
        s+=1
    if(printingDescriptive):
        itis=" is "
        add=""
        if(r==False):
            itis=" is not "
            add=" For example, "+str(s-1)+" x "+str(int(n/(s-1)))+" = "+str(n)+" ."
        print("The number "+str(n)+itis+"a prime number."+add)
    return r
#***********************************************************************
def primesUntil(N,printing=False,printingDescriptive = False):
    ans =[]
    for i in range (N+1):
        if(isPrime(i,printingDescriptive)):
            ans.append(i)
    ans=np.array(ans)
    if(printing):
        for elem in ans:
            print (elem)
    return ans
#************************************************************************
def statValues(Arr,printing=False):
    m=np.mean(Arr)
    stdev=np.std(Arr)
    md=max(set(Arr), key=Arr.count)
    med=np.median(Arr)
    v=np.var(Arr)
    if(printing):
        print("For the Array : " )
        print(Arr)
        print("The mean value is "+str(m)+" . \n")
        print("The median is "+str(med)+" . \n")
        print("The mode is "+str(md)+" . \n")
        print("The standard deviation is "+str(stdev)+" . \n")
        print("The variance is "+str(v)+" . \n")
    
    return m , med , md , stdev , v
#************************************************************************

def CrossInPeriodicalCond(coords,sizes):
    dim_c=int(len(coords))
    dim_s=int(len(sizes))
    ans=np.zeros([2*dim_c,dim_c])
    if(dim_c!=dim_s):
        print("Coords and sizes must have equal length. Refer to Documentation.")
        return 0
    else:
        for i in range (dim_c):
            c_ant=(coords[i]-1)%sizes[i]
            c_post=(coords[i]+1)%sizes[i]
            newant=coords.copy()
            newpost=coords.copy()
            newant[i]=c_ant
            newpost[i]=c_post
            ans[i]=newant
            ans[i+dim_c]=newpost
    return ans
#************************************************************************

def dice(n_faces):
    return int(int(n_faces*np.random.random())+1)
#************************************************************************

def distributionDices(N_dices,n_faces,toss=10000):
    k=[]
    for i in range(toss):
        n=0
        for i in range (N_dices):
            n+=dice(n_faces)
        k.append(n)
    return np.array(k)
##########################################################
##########################################################
#===============GRID ANALYSIS============================#
##########################################################
##########################################################
def dar_vecinos_periodico(args,N):
    dim=len(args)
    n_vec=2*dim
    ANS=np.zeros([dim,n_vec])
    for d in range(dim):
        
        for v in range(n_vec):
            if (v==2*d):
                ANS[d,v]=args[d]-1
            elif(v==(2*d + 1)):
                ANS[d,v]=args[d]+1
            else:
                ANS[d,v]=args[d]
    return ANS
            
        
        






















#************************************************************************

#================================WHY====================================
    
#Try to uderstand my motivotions

#***********************************************************************    
def killingit(distribution="ab"):
    l=list(distribution)
    while(True):
        n=np.random.choice(l)
        if(n =='a'):
            print(np.random.choice(["better, indeed.","nice.","Give me "+str(np.random.randint(10))+" seconds to think about it.","I have a better idea...","try "+str(np.random.randint(10))+" . Better number.","DUDE, NO.","How about...","no","uhhh?","oh","WOOAAHHH","uh....","OHH","Dude.","youre killing it!","keep it.","Better."]))
        else:
            print(np.random.random()*np.random.normal())
        
        
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
