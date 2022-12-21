from Model import Model
from DOcall_numer import MLDOCall, interpolatie
from DOcall_exact import utime, uLaatste
from parametersOpgave import parametersOpgave

import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
from math import log,exp

def testLog() -> "grafiek log":
    x = np.arange(0.2, 100, 0.1)
    y = [log(xi) for xi in x] 
    plt.title("ln(x)")
    plt.plot(x, y)
    plt.show()

    z = [exp(log(xi)) for xi in x]
    plt.title("exp(ln(x))")
    plt.plot(x, z)
    plt.show()

def testN()-> "grafiek N":
    N = norm(0,1).cdf
    x = np.arange(-3, 3, 0.1)
    y = [N(xi) for xi in x]
    plt.title("verdelings functie standaard normaal")
    plt.plot(x, y)
    plt.show()

def testMLDOCall(aantalPlotLijnen=4, plaatsPunten=1000, tijdPunten=1000):
    par = parametersOpgave(plaatsPunten=plaatsPunten, tijdPunten=tijdPunten)
    Utime = MLDOCall(par)

    for i in range(0,len(Utime),len(Utime)//(aantalPlotLijnen-1)):
        Ut = Utime[i]
        plt.plot(par.roosterPunten, Ut, label = f"tijd:{par.tijdDiscretisatie[i]}")
    plt.xlabel("plaats")
    plt.ylabel("prijs")
    plt.title("numeriek voor verschillende tijden")
    plt.legend()
    plt.show()

def testutime(aantalPlotLijnen=4, plaatsPunten=100, tijdPunten=100):
    par = parametersOpgave(plaatsPunten=plaatsPunten, tijdPunten=tijdPunten)
    uTime = utime(par)

    for i in range(0,len(utime),len(utime)//(aantalPlotLijnen-1)):
        ut = uTime[i]
        plt.plot(par.roosterPunten, ut, label = f"tijd:{par.tijdDiscretisatie[i]}")
    plt.title("exact voor verschillende tijden")
    plt.xlabel("plaats")
    plt.ylabel("prijs")
    plt.legend()
    plt.show()


def testuLaatste(plaatsPunten=100, tijdPunten=100):
    par = parametersOpgave(plaatsPunten=plaatsPunten, tijdPunten=tijdPunten)
    plt.plot(par.roosterPunten, uLaatste(par,par.looptijd), label ="exact")
    plt.plot(par.roosterPunten,MLDOCall(par)[-1], label="numeriek")
    plt.legend()
    plt.title("exact vs numeriek")
    plt.xlabel("plaats")
    plt.ylabel("prijs")
    plt.show()

def testuLaatsteDisretisatie(plaatsPuntenLijst:list = [20,50,100]):
    for plaatsPunten in plaatsPuntenLijst:
        par = parametersOpgave(plaatsPunten=plaatsPunten, tijdPunten=10000)
        plt.plot(par.roosterPunten,MLDOCall(par)[-1], label=f"num:{plaatsPunten}")

    ex =parametersOpgave(plaatsPunten=plaatsPuntenLijst[-1], tijdPunten=1000)
    plt.plot(ex.roosterPunten, uLaatste(ex,ex.looptijd), label ="exact")
    plt.legend()
    plt.title("exact vs numeriek(discretiasaties)")
    plt.xlabel("plaats")
    plt.ylabel("prijs")
    plt.show()

def testinterpolatie():
    par = parametersOpgave(20,1000)
    Uts = MLDOCall(par)
    x = np.arange(par.L,par.S,(par.S-par.L)/100)
    y = [interpolatie(xi,par.looptijd,Uts,par) for xi in x]

    plt.scatter(x,y)
    plt.show()
    
    

    


def alleTesten():
    testMLDOCall()
    testN()
    testLog()
    # is traag en klopt toch niet
    #testutime()  
    testuLaatste()
    testuLaatsteDisretisatie()

if __name__ == "__main__":
    testuLaatste()
    
