from dataclasses import dataclass
from math import exp
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csc_matrix

@dataclass
class Model:
    rente:float
    volatiliteit:float
    looptijd:float 
    strike: float
    # L is ondergrens van de discretisatie
    L: float
    # S is bovengrens van de discretisatie
    S: float
    plaatsPunten: int

    @property
    def maaswijdte(self) -> float:
        """Ook wel h genoemd"""
        return (self.S-self.L)/(self.plaatsPunten+1)  

    @property
    def roosterPunten(self)->np.array:
        """roosterPunten exlusief L en S (de s_j's)"""
        return np.arange(self.L,self.S,self.maaswijdte)[1:]

    # beginvoorwaarden
    def begint0(self,s)->float:
        return max(s-self.strike,0)

    def beginL(self, t)->float:
        return 0

    def beginS(self,t)->float:
        return self.S - exp(- self.rente * t) * self.strike

    #notatie (oef1)
    """Dit is allemaal notatie voor uitleg kijk verslag"""
    def c0(self, s)-> float:
        return self.rente

    def c1(self, s)-> float:
        return self.rente * s

    def c2(self, s)-> float:
        return 0.5 * self.volatiliteit**2 * s**2
    
    def D(self,j)->np.array:
        # dit kan efficiënter (redundancy)
        sj = self.roosterPunten[j-1]  # python telt van 0
        D0 = self.c2(sj)/(self.maaswijdte**2) + self.c1(sj)/(2*self.maaswijdte)
        D1 = -2*self.c2(sj)/(self.maaswijdte**2) - self.c0(sj)
        D2 = self.c2(sj)/(self.maaswijdte**2) - self.c1(sj)/(2*self.maaswijdte)
        return np.array([D0, D1, D2])
    
    def Ad(self):
        row = []    # [0,0,0, 1,1,1, ...]
        for j in range(self.plaatsPunten):
            for _ in range(3):
                row.append(j)

        col = []    # [0,1,2, 1,2,3, ...]
        for j in range(self.plaatsPunten):
            for i in range(3):
                col.append(j+i)

        data = []   # alle coëfficiënten Dj aan mekaar 
        for j in range(self.plaatsPunten):
            for Djk in self.D(j):
                data.append(Djk)

        # sparse matrix constructie
        return csc_matrix((data, (row, col)), shape = (self.plaatsPunten, self.plaatsPunten+2)).toarray()

    def A(self):
        return self.Ad()[:,1:self.plaatsPunten+1]

    def g(self,t)->float:
        g1 = self.D(1)[0]*self.beginL(t) # altijd 0 in dit model
        gm = self.D(self.plaatsPunten)[2] * self.beginS(t)    
        data = [g1,gm]
        row = [0, self.plaatsPunten-1]  #python telt van 0
        col = [0, 0]                    #python telt van 0
        return csc_matrix((data, (row, col)), shape = (self.plaatsPunten, 1)).toarray()



def parametersOpgave(plaatsPunten:int = 100):
    if plaatsPunten > 10**4:
        raise Exception("Zoveel punten (>10**4) kunnen mijn geheugen niet aan")

    par = Model(
           rente = 0.01,
           volatiliteit = 0.25,
           looptijd = 2,
           strike = 100,
           L = 80,
           S = 300,
           plaatsPunten = plaatsPunten) 
    return par


def testroosterpunten(aantal=10):
    par = parametersOpgave(aantal)
    print("aantal:", len(par.roosterPunten))
    print(par.roosterPunten)

def testBegin0():
    par = parametersOpgave()
    x = par.roosterPunten
    y = [par.begint0(xi) for xi in x ]
    plt.plot(x,y)
    plt.show()

def testD():
    par = parametersOpgave()
    print(par.D(3))

def testAd(dim):
    par = parametersOpgave(dim)
    Ad = par.Ad()
    print(Ad)

def testA(dim):
    print("Some sanity checks:")
    Pdif = parametersOpgave(dim)
    Pdif.c0 = lambda x : 0
    Pdif.c1 = lambda x : 0
    Pdif.c2 = lambda x : 1
    A = Pdif.A()* Pdif.maaswijdte**2
    print("pure diffusie orde 2:")
    print(A)

    Pcon = parametersOpgave(dim)
    Pcon.c0 = lambda x : 0
    Pcon.c1 = lambda x : 1
    Pcon.c2 = lambda x : 0
    A = 2* Pcon.A()* Pcon.maaswijdte
    print("pure convectie orde 2:")
    print(A)

def testg(dim):
    par = parametersOpgave(dim)
    g = par.g
    print("g(0):")
    print(g(0))
    print("g(2):")
    print(g(2))


if __name__ == "__main__":
    testg(4)
