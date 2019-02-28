"""
Created on Thu Oct  4 16:00:26 2018

@author: david
"""
import numpy as np
import matplotlib.pyplot as plt
#from astropy.convolution import Gaussian2DKernel,convolve
#import scipy.linalg as linalg
#from mpl_toolkits.mplot3d import Axes3D


#Parametros ALV-CBRN
#Acertivity,Lovely,Vanity # 0,10
#Coward,Balance,Random,Nuts # 0,10


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
    
    


class persona:
    #Parametros de accion caracteristicos
    C,B,R,N,ALVCBRN=0,0,0,0,0
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
    
    def __init__(self, name,corporal_mass,needs,acertivity,lovely,vanity):
        self.NAME=name
        self.C_MASS=corporal_mass
        self.NEEDS=needs
        self.A=acertivity
        self.L=lovely
        self.V=vanity
        self.DsinAgua=0
        
        
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
        
        
#     
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
        
        
        


class mascota:
    


    def __init__(self,especie,nombre,A,L,V,pre=''):
        self.PRE=pre
        self.NAME=nombre
        self.SPEC=especie
        self.A=A
        self.L=L
        self.V=V
        self.AFECTOS={}
        self.H_despierto=0
        self.H_dormido=0
        self.Dsincomer=0
        self.DsinAgua=0
        
        self.Health=100
        self.desangrando=0
        
        self.hybernate=0
        self.status=1
        
        
#     



    def comer(self):
        
        
        













    
    
    
    
    
class situacion:
    #OBJ={name:kind} kinds=Filoso,Punta,Contundente,Heavy
    catastrofe_eventos,personas=0,0
    OBJ={}
    proviciones={}
    dias_inside=1
    corpse=[]
    agot={}
    y=0
    
    brut=0
    desesp=0
    prob=0
    suicid=0
    def __init__(self,personas,objetos,catastrofe_n,catastrofe_eventos,dias,proviciones):
        pp={}
        
        for p in personas:
            pp[p.NAME]=p
        self.personas=pp
        self.maxdays=dias
        self.proviciones=proviciones
        self.OBJ=objetos
        self.catastrofe_name=catastrofe_n[0]
        self.catastrofe_descripcion=catastrofe_n[1]
        self.place=catastrofe_n[2]
        self.MakingHeader()
        

        
        self.catastrofe_eventos=catastrofe_eventos
    
    def MakingHeader(self):
        print("-----------------------")
        print(self.catastrofe_name)
        print("-----------------------")
        print(self.catastrofe_descripcion)
        n=len(self.personas)
        per=[]
        st=""
        for p in self.personas:
            per.append(self.personas[p].NAME)
        for  i in range(n-2):
            st+=per[i]
            st+=" , "
        st+=per[-2]+" y "
        st+=per[-1] +" se encuentran encerrados en "+self.place+"."
        rand=round(np.random.random()*100,2)
        self.prob=rand
        print("............................................................")
      
        print("Asumiendo correctos los parametros proporcionados")
        
        print("este escenario es posible en un "+str(rand)+"% de los casos.")
            
        print("===================== DIA 1 =====================")    

    
    
    
    def darHealth(self):
        for pers in self.personas:
            persona=self.personas[pers]
            print(persona.NAME + " tiene "+str(persona.Health)+"/100 de salud")
    def ElegirObjeto(self,kind):
        obj=[]
        for x in self.OBJ:
            if(self.OBJ.get(x)==kind):
                obj.append(x)
        o=np.random.choice(obj)
        return o
    
    def consumir(self,prov):
        
        sup=self.proviciones[prov]
        if (sup==0):
            return 0
        else:
            self.proviciones[prov]=self.proviciones[prov]-1
            if(self.proviciones[prov]==0):
                print("Se agotaron las reservas de "+prov)
                self.agot[prov]=self.dias_inside-1
            return 1
        
            
            
    
    def TomarRacion(self,pers,prov):
        if(self.consumir(prov)==1):
            
            print(pers.NAME + " consume una racion de "+prov)
            if(prov=="Agua"):
                pers.DsinAgua=0
            elif(prov=="Comida"):
                pers.comer()
                pers.Dsincomer=0
            elif(prov=="Medicina"):
                pers.Health=pers.Health+5
                if(((TakeAChance(1/5))==1)and(pers.desangrando==1)):
                    pers.desangrando=0
                    pers.remNeeds("Medicina")
                    print(pers.NAME+" finalmente ha controlado su hemorragia con medicina")
                
            elif(prov=="Cocaina"):
                pers.Coke()
                
            elif(prov=="Yerba"):
                pers.N=check(pers.N-1)
                pers.B=check(pers.B+1)
                pers.chill()
                pers.chill()
                print(pers.NAME+" se relaja un poco.")
        else:
            if(prov=="Agua"):
                
                if((self.dias_inside>10)and(pers.DsinAgua>2)and(TakeAChance(15/19)==1)):
                    print(pers.NAME+" siente demasiada sed y se ve en la necesidad de beber su propia orina")
                    pers.DsinAgua=1
                else:
                    pers.DsinAgua=pers.DsinAgua+1
                    
            
            elif(prov=="Comida"):

                pers.Dsincomer=pers.Dsincomer+1
                
            elif(prov=="Yerba"):
                pers.N=check(pers.N+1)
                pers.R=check(pers.R+1)
                pers.C=check(pers.C+1)
                pers.B=check(pers.B-1)
                print(pers.NAME+" siente ansiedad.")
            
            print(pers.NAME + " no puede consumir una racion de "+prov+ " por la escasez")
            if(prov=="Medicina"):
                pers.Herir(1)
                print("La falta de medicina debilita a "+pers.NAME)
    def todosToman(self):
        for p in self.personas:
            pers=self.personas[p]
            for n in pers.NEEDS:
                prob=np.random.random()
                if((prob>0.75)and(pers.hybernate==0)):
                    self.TomarRacion(pers,n)
                
    def interceptor(self,victima):
        if(np.random.random()>0.4):
            candidatos=[]
            for pers in self.personas:
                persona=self.personas[pers]
                a=persona.CualAfecto(victima.NAME)
                
                if ((a>0)and(persona.NAME!=victima.NAME)):
                    candidatos.append(persona)
            if (len(candidatos)==0):
                return 0
            else:
                return np.random.choice(candidatos)
        else:
            return 0
             
    
    def Ataque(self,atacante,victima):
        self.despertarTodos()
        M_factor=((atacante.C_MASS-victima.C_MASS)/6)
        Prob=(check(M_factor-victima.A+atacante.A)/10)
    
        p=TakeAChance(Prob+0.3)
        if(p==1):
            
            if(atacante.MakeIt_BrutalOn(victima.NAME)==1):
                T="H"
                if(TakeAChance(1/2)==1):
                    T="C"
                objeto_kind=np.random.choice(["F","P","C",T])
                intensidad=int(M_factor*np.random.random())+1
                objeto=self.ElegirObjeto(objeto_kind)
                
                acciones={"C":"golpear","P":"apuñalar","F":"cortar","H":"arremeter salvajemente conta"}
                
                if(objeto_kind in ["P","F"]):
                    intensidad=3  
                if(objeto_kind in ["H"]):
                    intensidad=4
                
                
                
                veces=int(3*np.random.random())+1
                                
                self.brut=self.brut+1
                print(atacante.NAME + " decide "+acciones[objeto_kind]+" a " + victima.NAME + " con "+objeto +" "+ str(veces)+" veces")
                self.despertarTodos()
                interc=self.interceptor(victima)
               
                if((interc==0)):
                   
                    if(objeto_kind in ["P","F"]):    
                        victima.desangrar(1)    
                    victima.Atribuir(atacante.NAME,-veces*intensidad)
                    victima.Herir(intensidad*veces)
                else:
                     if((interc.NAME!=victima.NAME)and(interc.NAME!=atacante.NAME)):
                        self.despertarTodos()
                        print(interc.NAME+" intercede en el ataque.")
                        interc.Herir(intensidad)     
                        interc.Atribuir(atacante.NAME,-3)
                        victima.Atribuir(atacante.NAME,-3)
                        victima.Atribuir(interc.NAME,3)
                        atacante.Atribuir(interc.NAME,-3)
                    
            
            else:
                print(atacante.NAME + " esta considerando atacar a " + victima.NAME +" , pero es incapaz de hacerlo.")
        else:
            if(TakeAChance(2/5)==0):
                self.despertarTodos()
                print(atacante.NAME + " intenta atacar a " + victima.NAME + " a golpes")# , pero "+victima.NAME+" se defiende.")
                if((TakeAChance(atacante.C_MASS/victima.C_MASS)-0.2)==1):
                    n_golpes=np.random.randint(4)+3*TakeAChance(1/3)
                    print(atacante.NAME+" golpea a "+victima.NAME+" en la cara "+str(n_golpes)+" veces" )
                    if(n_golpes>=4):
                        print("el ataque es brutal")
                        victima.desangrar(1)
                    victima.Herir(n_golpes)
                else:
                    print(victima.NAME+" se defiende de la agresion de "+atacante.NAME)
                    atacante.Herir(1)
                    victima.Atribuir(atacante.NAME,-3)
                    atacante.desmayar()
                    if(TakeAChance(1/2)==1):
                        self.Ataque(victima,atacante)
            else:
                print(atacante.NAME+ " está pensando en hacerle daño a otra persona")
                if(TakeAChance(1/4)==1):
                    print("En un ataque de ansiendad, "+atacante.NAME+" decide hacerse daño con "+self.ElegirObjeto("F"))
                    if(TakeAChance(9/10)==1):
                        
                        atacante.Herir(1)
                        self.despertarTodos()
                    else:
                        print(atacante.NAME+" logra suicidarse")
                        self.suicid=self.suicid+1
                        self.Muerte(atacante)
            self.checkDead()
        
    def RandomAwake(self):
        dd=[]
        for x in self.personas:
            dd.append(x)
        if(len(dd)>0):
            dead=self.personas.get(np.random.choice(dd))
            return dead
        else:
            return 0
        
    def randomFeels(self):
        p=self.RandomAwake()
        feels=["aburrimiento","ganas de llorar","pensamientos agresivos","frustracion","esperaza","pensamientos alegres","dudas sobre su rol en esta situacion"]

        if(p!=0):
            f=np.random.choice(feels)
            print(p.NAME+" tiene "+f)
            if(f=="pensamientos agresivos"):
                self.goneNuts(p)
            
    
    
    def detectarRaye(self):
        rayes={}
        for p in self.personas:
            for q in self.personas:
                p1=self.personas[p]
                p2=self.personas[q]
                
                if((p1.CualAfecto(p2.NAME)<0)and(p1.NAME!=p2.NAME)):
                    rayes[p1]=p2
        
        if(len(rayes)>0):
            rand=np.random.choice([x for x in rayes])
            rand2=rayes[rand]
            return rand,rand2
            
        else:
            return 0,0
    def ranchill(self):
        j=self.RandomAwake()
        if(j!=0):
            j.chill()
        
    def simpleAvanzar(self):
        pp=[]
        for pers in self.personas:
            Persona=self.personas[pers]
            pp.append(Persona)
        for per in pp:
            per.Avance()
            self.checkDead()
    def despertarTodos(self):
        for p in self.personas:
            self.personas[p].despertar()


    def eventoAleatorio(self):
        evento=np.random.choice(list(self.catastrofe_eventos.keys()))
        print(evento)
        self.despertarTodos()
        tipo = self.catastrofe_eventos[evento][1]
        if(tipo=="ME"):
            if(TakeAChance(1/8)==1):
                dd=[]
                for x in self.personas:
                    dd.append(x)
                if(len(dd)>0):
                    dead=self.personas.get(np.random.choice(dd))
                    print(self.catastrofe_eventos[evento][2]+dead.NAME)
                    self.Muerte(dead)
                #MAtar y sacar
            else:
                print("Afortunadamente no sucede nada grave")
        elif(tipo=="T"):
            dd=[]
            for x in self.personas:
                dd.append(x)
            if(len(dd)>=1):
                p=self.personas.get(np.random.choice(dd))
                print(self.catastrofe_eventos[evento][2]+p.NAME)
                p.cordura(2)
                p.chill()
        elif(tipo=="MV"):
            dd=[]
            for x in self.personas:
                dd.append(x)
            if(len(dd)>0):
                p=self.personas.get(np.random.choice(dd))
                p.grumpy()
                print(self.catastrofe_eventos[evento][2]+p.NAME)
                p.cordura(-2)
        elif(tipo=="RD"):

            dd=[]
            for x in self.personas:
                dd.append(x)
            if(len(dd)>0):
                for pers in dd:
                    if(TakeAChance(1/2)==1):
                        print(self.catastrofe_eventos[evento][2]+self.personas[pers].NAME)
                        self.personas[pers].Herir(4)
                        if(TakeAChance(1/2)==1):
                            self.personas[pers].desangrar(1)
                        
                    
                    
            

        if(self.catastrofe_eventos[evento][0]=="N"):
            self.catastrofe_eventos.pop(evento)
        self.checkDead()
      
    def RandomTregua(self):
        if(TakeAChance(self.dias_inside*0.2/10+0.1)==1):
            dd=[]
            for x in self.personas:
                if(self.personas[x].hybernate==0):
                    dd.append(x)
            if(len(dd)>2):
                p1=self.personas[np.random.choice(dd)]
                cand=[]
                for af in p1.AFECTOS:
                    if((p1.CualAfecto(af)<0)and(af in self.personas)):
                        cand.append(af)
                if(len(cand)>=1):
                    rc=np.random.choice(cand)
                    th=np.random.choice(["la situacion en la que se encuentran "," mejorar sus posibilidades de sobrevivir"," su amistad "," sus altercados previos "])
                    print(p1.NAME+" y " + rc + " tienen una larga charla sobre "+th+" y deciden que estar discutiendo es inutil")
                    self.personas[rc].Atribuir(p1.NAME,5)
                    p1.Atribuir(rc,5)
      


        
        
    def RandomTalk(self):
        dd=[]
        for x in self.personas:
            if(self.personas[x].hybernate==0):
                dd.append(x)
        if(len(dd)>2):
            p1,p2=np.random.choice(dd,2,replace=False)
            p1,p2=self.personas[p1],self.personas[p2]
            
            temas=["Temas personales","Actualidad","Libros","Videojuegos","Politica","Musica"]
            
            th=np.random.choice(temas)
            bm=["mal","bien"][TakeAChance(1/2)]
            print(p1.NAME+" y "+p2.NAME+" tienen una charla casual sobre "+th+ " y resulta "+bm)
            if(bm=="mal"):
                p1.grumpy()
                p2.grumpy()
            else:
                p1.chill()
                p2.chill()
            
        
    def checkDead(self):
        dead=[]
        for x in self.personas:
            if(self.personas[x].status==0):
                dead.append(x)
        for y in dead:
            self.personas.pop(y)
    
    
        
    def Muerte(self,Persona):
        Persona.muerto()
        self.personas.pop(Persona.NAME)
        self.addOBJ("el cadaver de "+Persona.NAME,"H")
        self.corpse.append("el cadaver de "+Persona.NAME)
        for pers in self.personas:
            self.personas[pers].cordura(-2)
            if(self.personas[pers].CualAfecto(Persona.NAME)>0):
                print(self.personas[pers].NAME+" se aflige por la muerte de "+Persona.NAME)
                self.personas[pers].cordura(-1)
                self.personas[pers].grumpy()
    def Altercado(self,persona1,persona2):
        self.despertarTodos()
        print(persona1.NAME + " y " +persona2.NAME +  " tienen un altercado.")
        persona1.Atribuir(persona2.NAME,-1)
        persona2.Atribuir(persona1.NAME,-1)
        if(TakeAChance(1/4)==1):
            self.Ataque(persona1,persona2)
        
    def cuantosDespiertos(self):
        c=0
        for x in self.personas:
           if(self.personas[x].hybernate==0):
               c+=1
        return c
    def AltercadoAleatorio(self):
        if(self.cuantosDespiertos()>=2):    
            dd=[]
            for x in self.personas:
                if(self.personas[x].hybernate==0):
                    dd.append(x)
            p1,p2=np.random.choice(dd,2,replace=False)
            p1,p2=self.personas[p1],self.personas[p2]
            self.Altercado(p1,p2)
        
    
    def Tension(self):
        t=[0]
        for x in self.personas:
            p=self.personas[x]
            for c in p.AFECTOS:
                if(p.hybernate==0):
                    t.append(p.AFECTOS[c])
        return int(-np.mean(t)+self.dias_inside/10)
    
    
    def goneNuts(self,pers):
         dd=[]
         for x in self.personas:
            if(self.personas[x].hybernate==0 and self.personas[x].NAME!=pers.NAME):
                dd.append(x)
         if(len(dd)>1):
            pp=self.personas[np.random.choice(dd)]
            aflic=["desesperacion","ansiedad","panico","ira"]
            print(pers.NAME+" tiene un ataque de "+np.random.choice(aflic)+" y piede el control")
            #print("<><><><><><><><><><><><><><><><><><><><><><>")
            self.Ataque(pers,pp)
            
            
        
    def addOBJ(self,name,kind):
        self.OBJ[name]=kind
    def Dia(self):
        dia=["alt"]
        self.yummy()
        self.todosToman()
        T=self.Tension()
        if(T>0):
            for i in range(T):
                dia.append("atq")
                dia.append("rc")
                dia.append("rc")
                dia.append("rantal")
                dia.append("atq")
                dia.append("rc")
                dia.append("rc")
                dia.append("rantal")
                dia.append("rtruce")
        for i in range (int(self.dias_inside/5)):
            dia.append("rtruce")
        dia.append("rtruce")       
        dia.append("atq")
        dia.append("rc") 
        dia.append("rc") 
        dia.append("eval")
        dia.append("rantal")
        dia.append("rantal")
        n_eventos=np.random.randint(5)
        for i in range(n_eventos):
            
            ev=np.random.choice(dia)
            if(ev=="alt"):
                self.AltercadoAleatorio()
            elif(ev=="atq"):
                ata,vic=self.detectarRaye()
                
                if (ata!=0):
                    at=ata
                    vc=vic
                    self.Ataque(at,vc)
            elif(ev=="eval"):
                self.eventoAleatorio()
            elif(ev=="rantal"):
                self.RandomTalk()
            elif(ev=="rc"):
                self.ranchill()
            elif(ev=="rtruce"):
                self.RandomTregua()
            for xx in range(5):
                if(TakeAChance(1/20)==1):
                    self.randomFeels()
               
        self.simpleAvanzar()
    

    def darStatsInteraccion(self):
        return str("Suicidios = "+str(self.suicid)+" | Brutalidad = "+str(self.brut)+" | Desesperacion = "+str(self.desesp))
        
    def yummy(self):
        
        n_personas=len(self.personas)
        dias=0
        bal=0
        cow=0
        if((self.dias_inside>10)and(len(self.corpse)>=1)and(self.proviciones["Comida"]==0)):
            for pp in self.personas:
                perso=self.personas[pp]
                dias=dias+perso.Dsincomer
                bal=bal+perso.B
                cow=cow+perso.C
                
            if((dias/n_personas>3)and(TakeAChance((n_personas*20-np.abs(cow+bal))/5)==1)):
                co=self.corpse.pop()
                print("Se decide por unanimidad que "+co+" será usado como comida puesto que hay escasez")
                self.OBJ.pop(co)
                self.proviciones["Comida"]=8
                self.desesp=self.desesp+1
                print("*")
                self.y=self.y+1
                for ppp in self.personas:
                    self.TomarRacion(self.personas[ppp],"Comida")
                    self.personas[ppp].cordura(-1)
    def Avanzar(self):
        
        perso=[]
        for pp in self.personas:
            perso.append(pp)
        for p in perso:
            if(p in self.personas):
                self.personas[p].Health=self.personas[p].Health-int(self.personas[p].Dsincomer*TakeAChance(1/3))
                if((self.personas[p].N+self.personas[p].R>10)and(TakeAChance(1/10)==1)):
                    self.goneNuts(self.personas[p])
        
        self.dias_inside=self.dias_inside+1
        
        self.Dia()
        self.checkDead()
        
        print("===================== DIA "+str(int(self.dias_inside))+" =====================")
        
                
    
        
        
                
#  print("<><><><><><><><><><><><><><><><><><><><><><>")
        
need=["Yerba","Comida","Agua","Cocaina"]        
        
David1=persona("David 1",90,need,8,7,6)
Mafe1=persona("Mafe 1",70,need,6,8,4)
Chris1=persona("Chris 1",80,need,8,7,9)
David2=persona("David 2",90,need,8,7,6)
Mafe2=persona("Mafe 2",70,need,6,8,4)
Chris2=persona("Chris 2",80,need,8,7,9)
David3=persona("David 3",90,need,8,7,6)
Mafe3=persona("Mafe 3",70,need,6,8,4)
Chris3=persona("Chris 3",80,need,8,7,9)
#Ceci=persona("Javier",80,need,9,4,5)
#Susi=persona("Susana",70,need,7,10,8)
David1.Atribuir("Mafe 1",3)
#Susi.Atribuir("David",3)
#Chris.Atribuir("Javier",-2)
Mafe1.Atribuir("David 1",3)
#Ceci.Atribuir("Susana",9)
Chris1.Atribuir("Mafe 1",6)
David1.Atribuir("Chris 1",3)
#Susi.Atribuir("Javier",9)
#Ceci.Atribuir("David",3)

ob={"una lampara":"C","un libro":"C","una silla":"H","un bisturi":"F","un lapiz":"P","un cuchillo":"P","unas tijeras":"P","una plancha":"H"}
c_ev={"Un sobrecarga de la energia daña algunos aparatos electronicos":["NR","RD","Uno de los aparatos al explotar le hace daño a "],"Se ecuchan disturbios en la calle":["R","MV","La sensacion de inseguridad sumada con la ausencia de sol están afectando la salud mental de "],"El frio se hace mas agresivo a medida que pasan más días sin que el sol salga":["R","MV","La falta de calor está desesperando a "],"Una señal de radio aparece despues de horas.":["R","T","Esto ha mejorado el animo de "],"Una fuga de gas en el edificio de al lado":["N","ME","Esto hay causado la asfixia de "],"Hay ruidos extraños en el pasillo":["R","MV","Esto le quita la tranquilidad a "],"La humedad se filtra por el techo y finalmente derriba parte del techo":["N","RD","Los escombros que caen del techo hieren a "],"Se escucha a un perro ladrar afuera":["N","T","Esto recupera la esperanza de "],"Se escuchan susurros que provienen de atrás de una pared":["R","MV","Para cuando los susurros se detienen, la ansiedad se apodera de "]}
n_rec=20
ck=100
sup={"Comida":n_rec,"Yerba":n_rec,"Medicina":n_rec,"Agua":n_rec,"Cocaina":ck}            
catast=["El sol ha desaparecido.","Son las 8 AM. Todos despiertan de una noche de ocio. Curiosamente no se ve el brillo del sol. Es plena mañana y todo afuera está oscuro, con algunas escasas edificaciones que aún tienen electricidad. ","la casa de javier"]
s=situacion([David1,Chris1,Mafe1,David2,Chris2,Mafe2,David3,Chris3,Mafe3],ob,catast,c_ev,30,sup)
#print(Mafe.Health)
d=1
ht1=[]
ht2=[]
ht3=[]
ht4=[]
ht5=[]
ht6=[]
ht7=[]
ht8=[]
ht9=[]
while((len(s.personas)>0)):
    s.Avanzar()
    
    d+=1
    if("Mafe 1" in s.personas):
        ht1.append(s.personas.get("Mafe 1").Health)

    else:
        ht1.append(0)
    if("David 1" in s.personas):
        ht2.append(s.personas.get("David 1").Health)
    else:
        ht2.append(0)
    if("Chris 1" in s.personas):
        ht3.append(s.personas.get("Chris 1").Health)
    else:
        ht3.append(0)
        
        
    if("Mafe 2" in s.personas):
        ht4.append(s.personas.get("Mafe 2").Health)

    else:
        ht4.append(0)
    if("David 2" in s.personas):
        ht5.append(s.personas.get("David 2").Health)
    else:
        ht5.append(0)
    if("Chris 2" in s.personas):
        ht6.append(s.personas.get("Chris 2").Health)
    else:
        ht6.append(0)
    if("Mafe 3" in s.personas):
        ht7.append(s.personas.get("Mafe 3").Health)

    else:
        ht7.append(0)
    if("David 3" in s.personas):
        ht8.append(s.personas.get("David 3").Health)
    else:
        ht8.append(0)
    if("Chris 3" in s.personas):
        ht9.append(s.personas.get("Chris 3").Health)
    else:
        ht9.append(0)
#    if("Javier" in s.personas):
#        ht4.append(s.personas.get("Javier").Health)
#    else:
#        ht4.append(0)
#    if("Susana" in s.personas):
#        ht5.append(s.personas.get("Susana").Health)
#    else:
#        ht5.append(0)
print("El último superviviente muere después de "+str(d)+" dias ")
print(s.agot)
print(s.darStatsInteraccion())
plt.figure(figsize=[12,4])
ls=[["k",":"],["k","-."],["k","--"],["r",":"]]
i=0
#for prov in s.agot:
#    plt.axvline(s.agot[prov],c=ls[i][0],linestyle=ls[i][1],label="Agota "+prov)
#    i+=1
plt.plot(ht1,label="Mafe 1")
plt.plot(ht2,label="David 1")
plt.plot(ht3,label="Chris 1")
plt.plot(ht4,label="Mafe 2")
plt.plot(ht5,label="David 2")
plt.plot(ht6,label="Chris 2")
plt.plot(ht7,label="Mafe 3")
plt.plot(ht8,label="David 3")
plt.plot(ht9,label="Chris 3")
#4plt.plot(ht4,label="Javier")
#plt.plot(ht5,label="Susana")
plt.legend()
plt.title(s.darStatsInteraccion())
plt.grid()
plt.savefig("Eventos.png")
#5print(Mafe.Health)         
   