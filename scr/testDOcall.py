from Model import Model
from DOcall_numer import MLDOCall
from parametersOpgave import parametersOpgave
from DOcall_exact import utime, uLaatste

import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np
from math import log

def testLog() -> "grafiek log":
    x = np.arange(0.2, 100, 0.1)
    y = [log(xi) for xi in x]
    plt.title("ln(x)")
    plt.plot(x, y)
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

    for i in range(0,len(Utime),par.tijdPunten//(aantalPlotLijnen-1)):
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

    for i in range(0,len(uTime),tijdPunten//(aantalPlotLijnen-1)):
        ut = uTime[i]
        plt.plot(par.roosterPunten, ut, label = f"tijd:{par.tijdDiscretisatie[i]}")
    plt.title("exact voor verschillende tijden")
    plt.xlabel("plaats")
    plt.ylabel("prijs")
    plt.legend()
    plt.show()


def testuLaatste(plaatsPunten=100, tijdPunten=100):
    par = parametersOpgave(plaatsPunten=plaatsPunten, tijdPunten=tijdPunten)
    plt.plot(par.roosterPunten, uLaatste(par), label ="exact")
    plt.plot(par.roosterPunten,MLDOCall(par)[-1], label="numeriek")
    plt.legend()
    plt.title("exact vs numeriek")
    plt.xlabel("plaats")
    plt.ylabel("prijs")
    plt.show()


def testMLDOCallDiscretisatie(plaatsPunten=20, tijdPunten=100):
    ruw = parametersOpgave(plaatsPunten=plaatsPunten, tijdPunten=tijdPunten)
    fijn = parametersOpgave(plaatsPunten=1000, tijdPunten=1000)

    plt.plot(ruw.roosterPunten, MLDOCall(ruw)[-1], label="ruw")
    plt.plot(fijn.roosterPunten, MLDOCall(fijn)[-1], label="fijn")
    plt.legend()
    plt.title("ruw vs fijn")
    plt.xlabel("plaats")
    plt.ylabel("prijs")
    plt.show()

def alleTesten():
    testMLDOCall()
    testN()
    testLog()
    testutime()
    testuLaatste()

if __name__ == "__main__":
    testMLDOCallDiscretisatie()
