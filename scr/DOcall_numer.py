from Model import Model

from scipy.sparse import eye
from scipy.sparse.linalg import splu
import numpy as np
from math import floor


def MLDOCall(M:Model)->"list of U's on different times": 
    # merk op dat Model sommige dinges niet cached 
    A = M.A()
    g = M.g
    Utime = [M.beginU()]

    I = eye(M.plaatsPunten, format = "csc")
    LU = splu(I-0.5*M.tau * A)

    # dit is niet de beste manier om deze for loop te doen
    for t in M.tijdDiscretisatie[:-1]:
        # hier los ik dat ijl stelsel op 
        U = Utime[-1]
        rechtsIjlStelsel = U + 0.5* M.tau * (A.dot(U)+ g(t)+ g(t + M.tau))
        Unew = LU.solve(rechtsIjlStelsel)
        Utime.append(Unew)
    
    return Utime 

# ik weet dat ik hier beter een klas voor gebruik ...
def interpolatie(s:"plaats",T:"tijd", Utime, M:Model)-> float:
    """
    Deze functie dient om een schatting van de oplossing 
    buiten het discretisatie rooster te krijgen.
    """
    if not(M.L <= s <= M.S):
        raise Exception("s moet tussen L en S liggen")

    if not(0 <= T <= M.looptijd):
        raise Exception("T moet tussen 0 en looptijd liggen")

    indexClosestPointUnder = floor((s-M.L)/M.maaswijdte)
    indexClosetPointBefore = floor(T/M.tau)
    if indexClosestPointUnder == M.plaatsPunten:
        return Utime[indexClosetPointBefore][M.plaatsPunten-1] 
    else:
        return Utime[indexClosetPointBefore][indexClosestPointUnder] 

def interpolatieRooster(rooster, T:"tijd",Utime,M:Model)-> np.array:
    return  np.array([interpolatie(s,T,Utime,M) for s in rooster])



