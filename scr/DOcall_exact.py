from parametersOpgave import parametersOpgave
from Model import Model

from functools import partial
from math import log, exp, sqrt, pow
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm



# ik weet dat hier veel redundant termen staan ...

def d1(s: "plaats", T: "tijd", M: Model) -> float:
    p1 = log(s/M.strike)
    p2 = (M.rente + 0.5 * pow(M.volatiliteit,2)) * T
    p3 = M.volatiliteit * sqrt(T)
    return (p1 + p2)/p3

# require d1
def d2(s: "plaats", T: "tijd", M: Model) -> float:
    p3 = M.volatiliteit * sqrt(T)
    return d1(s, T, M) - p3

# in de plaats van lambda l
def l(M: Model):
    return (M.rente + 0.5 * M.volatiliteit**2) / M.volatiliteit**2

# require lambda
def y(s: "plaats", T: "tijd", M: Model) -> float:
    p3 = M.volatiliteit * sqrt(T)
    p4 = log(pow(M.L,2)/(s*M.strike))
    return p4/p3 + l(M) * p3


# require all functions
def u(s: "plaats", T: "tijd", M: Model) -> float:
    N = norm(0,1).cdf

    exprT = exp(-M.rente*T)
    Ls = M.L/s
    p3 = M.volatiliteit * sqrt(T)

    # ik splits in additieve termen
    a1 = s*N(d1(s,T,M))
    a2 = -M.strike*exprT* N(d2(s,T,M))
    a3 = -s*N(y(s,T,M))* pow(Ls, 2*l(M))
    a4 = M.strike * exprT *N(y(s,T,M)-p3)* pow(Ls,2*l(M)-2)

    return a1 + a2 + a3 + a4

# deze formule klopt enkel op de eindtijd (denk ik)
def utime(M:Model)-> "raar formaat":
    return [np.array(
        [u(s,t,M) for s in M.roosterPunten]
        )
        for t in M.tijdDiscretisatie + [M.looptijd]]

def uLaatste(M:Model)-> np.array:
    return np.array([u(s,M.looptijd,M) for s in M.roosterPunten])
        


