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
    aantalPunten: int

    @property
    def maaswijdte(self) -> float:
        """Ook wel h genoemd"""
        return (self.S-self.L)/self.aantalPunten  

    @property
    def roosterPunten(self)->np.array:
        """roosterPunten exlusief L en S"""
        return np.arange(self.L,self.S,self.maaswijdte)[1:]

    # beginvoorwaarden
    def begint0(self,s)->float:
        return max(s-self.strike,0)

    def beginL(self, t)->float:
        return 0

    def beginS(self,t)->float:
        return self.S - exp(- self.rente * t) * self.strike

    #notatie
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
        for j in range(self.aantalPunten):
            for _ in range(3):
                row.append(j)

        col = []    # [0,1,2, 1,2,3, ...]
        for j in range(self.aantalPunten):
            for i in range(3):
                col.append(j+i)

        data = []   # alle coëfficiënten Dj aan mekaar 
        for j in range(self.aantalPunten):
            for Djk in self.D(j):
                data.append(Djk)

        # sparse matrix constructie
        return csc_matrix((data, (row, col)), shape = (self.aantalPunten, self.aantalPunten+2)).toarray()
        



def parametersOpgave(aantalPunten:int = 100):
   par = Model(
           rente = 0.01,
           volatiliteit = 0.25,
           looptijd = 2,
           strike = 100,
           L = 80,
           S = 300,
           aantalPunten = aantalPunten) 
   return par

def testModelBegin0():
    par = parametersOpgave()
    x = par.roosterPunten
    y = [par.begint0(xi) for xi in x ]
    plt.plot(x,y)
    plt.show()

def testModelD():
    par = parametersOpgave()
    print(par.D(3))

def testAd(dim):
    par = parametersOpgave(dim)
    par.Ad()

if __name__ == "__main__":
    testAd(10000)
