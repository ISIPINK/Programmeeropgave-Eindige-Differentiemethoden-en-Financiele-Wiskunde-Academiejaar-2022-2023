from parametersOpgave import parametersOpgave
from Model import Model


from DOcall_numer import MLDOCall, interpolatieRooster
from DOcall_exact import utime, uLaatste


import matplotlib.pyplot as plt
from math import sqrt

def indexBuurtRooster(alpha: float, M: Model) -> (int,int):
    '''
    geeft de eerste en laatste index van de "buurtrooster" om
    plaatst discretisatie te slicen
    '''
    # in deze berekening kijk in naar de hoeveelheid
    # punten wat overeen komt met de lengte

    totaleLengte = M.S - M.L

    onder = max((1-alpha)*M.strike, M.L)
    lengteOnder = onder-M.L
    eerste = int((lengteOnder/totaleLengte) * M.plaatsPunten) 

    boven = min(M.S, (1+alpha)*M.strike)
    lengteBoven = boven - M.L
    laatste = int((lengteBoven/totaleLengte) * M.plaatsPunten) 
    
    return (eerste, laatste)


def buurt2Fout(alpha:float,M:Model):
    e,l = indexBuurtRooster(alpha,M)

    BuurtRooster = M.roosterPunten[e:l]
    uLaatsteBuurt = uLaatste(M)[e:l]
    ULaatsteBuurt = MLDOCall(M)[-1][e:l]
    
    s = sum((u-U)**2 for u, U in zip(uLaatsteBuurt, ULaatsteBuurt))
    
    return sqrt(s/M.plaatsPunten)
    

def buurt2FoutNumeriek(alpha:float,M:Model):
    e,l = indexBuurtRooster(alpha,M)
    BuurtRooster = M.roosterPunten[e:l]
    par = parametersOpgave(1000,1000)
    
    UrefLaatsteBuurt = interpolatieRooster(BuurtRooster,M.looptijd,MLDOCall(par),par)
    ULaatsteBuurt = MLDOCall(M)[-1][e:l]
    
    s = sum((Uref-U)**2 for Uref, U in zip(UrefLaatsteBuurt, ULaatsteBuurt))
    
    return sqrt(s/max(l-e,1))
