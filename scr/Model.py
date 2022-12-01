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
    tijdPunten: int

    @property
    def maaswijdte(self) -> float:
        """Ook wel h genoemd"""
        return (self.S-self.L)/(self.plaatsPunten+1)  

    @property
    def tau(self) -> float:
        return  self.looptijd/self.tijdPunten

    @property
    def tijdDiscretisatie(self)-> np.array:
        return np.arange(0, self.looptijd+self.tau, self.tau)
        
    @property
    def roosterPunten(self)->np.array:
        """roosterPunten exlusief L en S (de s_j's)"""
        return np.arange(self.L,self.S,self.maaswijdte)[1:]

    # beginvoorwaarden
    def begint0(self,s)->float:
        return max(s-self.strike,0)

    # cell averaging
    def beginU(self)->float:
        return np.array(
                [self.begint0(sj) 
                if abs(sj-self.strike) > self.maaswijdte/2 
                else 0.5*((sj + self.maaswijdte*0.5) - self.strike) 
                for sj in self.roosterPunten]
                )


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
        return csc_matrix((data, (row, col)), shape = (self.plaatsPunten, self.plaatsPunten+2))

    def A(self):
        row = []    # [0,0,0, 1,1,1, ...]
        for j in range(self.plaatsPunten):
            for _ in range(3):
                row.append(j)

        col = []    # [0,1,2, 1,2,3, ...]
        for j in range(self.plaatsPunten):
            for i in range(3):
                col.append(j+i-1) # -1 omdat ik de eerst kolom laat wegvallen

        data = []   # alle coëfficiënten Dj aan mekaar 
        for j in range(self.plaatsPunten):
            for Djk in self.D(j):
                data.append(Djk)

        # sparse matrix constructie
        return csc_matrix((data[1:-1], (row[1:-1], col[1:-1])), shape = (self.plaatsPunten, self.plaatsPunten))

    def g(self,t)->float:
        g = [0]*self.plaatsPunten
        
        g[0] = self.D(1)[0]*self.beginL(t) # altijd 0 in dit model
        g[-1]= self.D(self.plaatsPunten)[2] * self.beginS(t)    

        return np.array(g)
