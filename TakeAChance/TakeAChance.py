"""
Created on Sat Dec 29 23:06:48 2018

@author: David Paipa

TAKE A CHANCE
"""
import numpy as np
import matplotlib.pyplot as plt
import collections as cl
#============================
#FUNCIONES MAESTRAS
#============================
def TakeAChance(n):#valor entre 0 y 1
    k=np.random.random()
    if(k<=n):
        return 1
    else:
        return 0
    
def check(n,CUT=10):
    if(n<=CUT): 
        return int(n)
    elif(n<0):
        return 0
    else:
        return CUT

ACCEPTED=["y","s","si","yes"]
DENIED=["n","no"]

def readin(txt):
    inmsg=input(txt+" : \n >").lower()
    if(inmsg in ACCEPTED):
        return 1
    elif(inmsg in DENIED):
        return 0
    else:
        return readin(txt)

perso=["David",86,8,8,4]


class persona:
    #Parametros de accion caracteristicos
    C,B,R,N=0,0,0,0
    #Paramtros de entrono
    NEEDS,C_MASS=0,0
    AFECTOS={}
    #Vriables de estado fisico
    status=1
    hybernate=0
    desangrando=0
    Health=100

    #Variables de sueño
    D_atrapado=1
    H_despierto=0
    H_dormido=0
    eventualidades=0
    Dsincomer=0
    
    #LOGS
    log_H=[100]#salud
    log_S=[100]#Sanidad
    
    
    def __init__(self, name,gender,corporal_mass,needs,acertivity,lovely,vanity):
        self.NAME=name
        self.GENDER=gender
        self.C_MASS=corporal_mass
        self.NEEDS=needs
        self.A=acertivity
        self.L=lovely
        self.V=vanity
        self.DsinAgua=0
        self.adit=['a','o'][gender] 
        
        
        
        self.C=check((self.A-self.V)/2+5) #coward
        self.B=check((self.A+self.L/2)/2) #Balance 
        self.R=check(((self.A+self.L+self.V)/15)+np.random.randint(8)) #Random
        self.N=check((self.V+self.A/2)/3 + self.R/2) #Nuts
        self.ALVCBRN=np.array([self.A,self.L,self.V,self.C,self.B,self.R,self.N])
        self.AFECTOS={}
        self.H_despierto=0
        self.H_dormido=0
        self.Dsincomer=0
        self.DsinAgua=0
        
        self.Health=100
        self.desangrando=0
        
        self.hybernate=0
        self.status=1
        
        
        
        
        
    def Actualizar(self):
        self.ALVCBRN=np.array([self.A,self.L,self.V,self.C,self.B,self.R,self.N])
    
    def CualAfecto(self,Name):
        if Name in self.AFECTOS:
            return self.AFECTOS[Name]
        else:
            return 0
    def mood(self):
        dd=0
        for a in self.AFECTOS:
            dd=dd+self.AFECTOS[a]
        return dd
        
    def cordura(self,n): #n = 1 ,-1 
        self.B=check(self.B+2*n*np.random.random())
        self.N=check(self.N-2*n*np.random.random())
        self.C=check(self.C-(n/np.abs(n)))
        self.Actualizar()
        self.eventualidades=self.eventualidades+n
        
        
    def Recibir_ataque(self,name,intensity):
        self.Herir(intensity)
        
    def Atribuir(self,name,val):
        if(name in self.AFECTOS):
            n_bef=self.AFECTOS[name]
            n_now=check(self.AFECTOS[name]+val)
            if((n_bef>0)and(n_now<0)):
                print("Ahora "+self.NAME+" odia a "+name)
                if(n_now<=-8):
                    print(self.NAME+" odia a "+name+" a muerte.")
            if((n_bef<0)and(n_now>0)):
                print("Ahora "+self.NAME+" esta en buenos terminos con "+name)
                if(n_now>=8):
                    print(self.NAME+" ama a "+name)
            self.AFECTOS[name]=check(self.AFECTOS[name]+val)
            
            
        
        else:
            
            if(val<=-8):
                print(self.NAME+" odia a "+name+" a muerte.")
            if(val>=8):
                print(self.NAME+" ama a "+name)
            else:
                if(val<0):
                    print(self.NAME+" odia a "+name)
                if(val>0):
                    print(self.NAME+" esta en buenos terminos con "+name)

                
        
            self.AFECTOS[name]=val
        
     
    def Avance(self):
        if(self.status==1):
            n=0
            if(self.eventualidades!=0):
                n=self.eventualidades/np.abs(self.eventualidades)#+1,-1
            self.C=check(self.C+(2*TakeAChance(0.5+n*0.25)-1)*TakeAChance(0.1*self.R))
            self.B=check(self.B+(2*TakeAChance(0.5+n*0.25)-1)*TakeAChance(0.1*self.R))
            self.R=check(self.R+(2*TakeAChance(0.5+n*0.25)-1)*TakeAChance(0.1*self.R))
            self.N=check(self.N+(2*TakeAChance(0.5+n*0.25)-1)*TakeAChance(0.1*self.R))
            
            self.C,self.B,self.R,self.N=np.abs(self.C),np.abs(self.B),np.abs(self.R),np.abs(self.N)
            
            self.D_atrapado=self.D_atrapado+1
            
            delir=(self.N+self.DsinAgua+self.Dsincomer)*self.D_atrapado/300
            if(self.hybernate==0):
                if(TakeAChance(delir)==1):
                    
                    print(self.NAME+" esta delirando")
                    
                if((self.N>6)and(self.mood()<1)and(TakeAChance(delir)==1)and((self.DsinAgua+self.Dsincomer)>4)):
                
                    print("Dadas las circunstancias y la presion, "+self.NAME+ " decide suicidarse.")
                    self.muerto()
            
            
            
            
            
            if(self.desangrando==1):
                self.Herir(1)
                print(self.NAME+ " ha perdido mucha sangre.")
            
            if(self.hybernate==0):
                self.H_despierto=self.H_despierto+1
                self.dormir_maybe()
                
            else:
                self.H_dormido=self.H_dormido+1
                self.despertar_maybe()
                
            if(self.H_despierto>10):
                self.cordura(-1)
            self.eventualidades=0
            self.Actualizar()
            
            if(self.Dsincomer>1):
                self.cordura(-1)
                self.N=check(self.N+1)
                
            if(self.DsinAgua>1):
                self.cordura(-1)
                self.N=check(self.N+1)
            if(self.Health>100):
                self.Health=100
                
            
            
            if(self.Dsincomer>2):
                prob=0.1+np.random.random()+(self.Dsincomer-2)*0.1
                if(TakeAChance(prob)==1):
                    self.muerto()
                    print(self.NAME+" ha muerto por inanicion.")
                else:
                    print(self.NAME + " lucha por mantenerse con vida a pesar de no tener comida")
                    if(TakeAChance(self.Dsincomer/20)==1):
                        print(self.NAME + " se siente debil por no poder comer nada.")
                        self.desmayar()
                        
            if(self.DsinAgua>3):
                prob=0.1+np.random.random()-(self.DsinAgua-3)*0.1
                if(TakeAChance(prob)==1):
                    self.muerto()
                    print(self.NAME+" ha muerto por deshidratacion.")        
                else:
                    print(self.NAME + " no ha bebido agua en dias")
                    if(TakeAChance(self.DsinAgua/20)==1):
                        print(self.NAME + " se siente debil por la deshidratacion.")
                        self.desmayar()
    def comer(self):
        self.Health=check(self.Health+2,CUT=100)
        self.DsinAgua=check(self.DsinAgua-1)
        self.cordura(1)
        self.N=self.N-TakeAChance(1/2)
        self.Dsincomer=0
        
    def remNeeds(self,need):
        nn=[]
        for n in self.NEEDS:
            if(n!=need):
                nn.append(n)
        self.NEEDS=nn
        print(self.NAME+" ya no necesita más "+need)
    def AdNeeds(self,need):
        self.NEEDS.append(need)
    def dormir(self):
        if(self.hybernate==0):
            self.hybernate=1
            self.H_despierto=0
            self.H_dormido=1
            print(self.NAME+" se ha dormido.")
            self.cordura(1)
    def despertar(self):
        if(self.hybernate==1):
            self.hybernate=0
            self.H_despierto=1
            self.H_dormido=1
            print(self.NAME+" se ha despertado.")
            
    def Coke(self):
        
        self.N=9
        self.B=self.B-1
        self.H_despierto=0
        
        if(self.Dsincomer<4):
            self.Dsincomer=self.Dsincomer-1
            self.DsinAgua=self.DsinAgua+1
        
        self.H_dormido=10
        pos=["  tiene mucha energia"," tiene ansiedad absoluta"," esta espectante", "  se siente con poder"]
        
        print(self.NAME+np.random.choice(pos))
        
        
        
            
    def dormir_maybe(self):
        p=self.H_despierto/30
        if(TakeAChance(p)==1):
            self.dormir()
    def despertar_maybe(self):
        p=self.H_dormido/(15-self.N)
        if(TakeAChance(p)==1):
            self.despertar()
    def muerto(self):
        self.status=0
        self.Health=0
        
        print(self.NAME+" ha fallecido.")
    
    def Herir(self,n): # n entre 0 y 5 depende de la intensidad
        daño=(n**2)*np.random.random()*2
        if(TakeAChance(daño/200)==1):
            self.AdNeeds("Medicina")
            print("El dolor hace que "+self.NAME+" tenga que tomar medicina")
        self.cordura(-1)
        if((self.Health-daño)<=0):
            self.muerto()
        else:
            self.Health=int(self.Health-daño)
            print(self.NAME+" pierde salud.")
    def desangrar(self,n): #0,1
        self.desangrando=n
        if(n==1):
            self.eventualidades=self.eventualidades-1
            print(self.NAME + " está perdiendo sangre.")
    def desmayar(self):
        if(self.hybernate==0):
            self.hybernate=1
            self.H_despierto=0
            self.H_dormido=1
            print(self.NAME+" se ha desmayado.")
    def chill(self):
        for a in self.AFECTOS:
            self.AFECTOS[a]=self.AFECTOS[a]+1
    def grumpy(self):
        for a in self.AFECTOS:
            self.AFECTOS[a]=self.AFECTOS[a]-1
    
    def MakeIt_BrutalOn(self,name):
        af=check((self.CualAfecto(name)-5)/-2)
        chance=af+((self.N*self.R-self.C*self.L)/10)+self.N-np.random.randint(-1,4)+self.D_atrapado+2-(100-self.Health)/40
        self.cordura(-1)
        if ((chance+1<=0)or(self.D_atrapado<6)):
            return 0
        else:
            
            return 1
        
    def MakeIt_HeroOn(self,name):
        af=check((self.CualAfecto(name)-5)/2)
        chance=af+((self.L*self.R-2*self.C*self.V)/10)+self.B*self.Health/200+np.random.randint(-4,1)
        if ((chance+2<=0)):
            return 0
        else:
            
            return 1