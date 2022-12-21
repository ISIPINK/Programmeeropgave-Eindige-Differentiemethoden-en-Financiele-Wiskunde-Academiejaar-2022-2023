from parametersOpgave import parametersOpgave
from Model import Model

from foutanalyse import indexBuurtRooster, buurt2Fout, buurt2FoutNumeriek

from DOcall_numer import MLDOCall
from DOcall_exact import utime, uLaatste


import matplotlib.pyplot as plt

def testindexBuurtRooster(alpha=0.3,M:Model=parametersOpgave()):
    e,l = indexBuurtRooster(alpha,M)

    BuurtRooster = M.roosterPunten[e:l]
    uLaatsteBuurt = uLaatste(M,M.looptijd)[e:l]
    ULaatsteBuurt = MLDOCall(M)[-1][e:l]
    
    plt.plot(BuurtRooster,uLaatsteBuurt,label = "exact") 
    plt.plot(BuurtRooster,ULaatsteBuurt, label = "numeriek") 
    plt.legend()
    plt.title("exact vs numeriek in buurt")
    plt.show()

def testbuurt2Fout(alpha=0.3,M:Model = parametersOpgave()):
    print("buurt2fout=",buurt2Fout(alpha,M)) 

def testbuurt2FoutNumeriek(alpha=0.3,M:Model = parametersOpgave()):
    print("buurt2foutNumeriek=",buurt2FoutNumeriek(alpha,M)) 

def testbuurt2FoutDiscretisatie(alpha=0.3,plaatsPuntenLijst:list = range(5,180,5)):
    fouten = [buurt2Fout(alpha,parametersOpgave(plaatsPunten,tijdPunten=1000))
            for plaatsPunten in plaatsPuntenLijst ]
    plt.scatter(plaatsPuntenLijst,fouten)
    plt.title("buurtfout vs plaatspunten (exact)")
    plt.show()

def testbuurt2FoutNumeriekDiscretisatie(alpha=0.3,plaatsPuntenLijst:list = range(21,280,20)):
    fouten = [buurt2FoutNumeriek(alpha,parametersOpgave(plaatsPunten,tijdPunten=1000))
            for plaatsPunten in plaatsPuntenLijst ]
    plt.scatter(plaatsPuntenLijst,fouten)
    plt.title("buurtfout vs plaatspunten (numeriek)")
    plt.show()

def alleTesten():
    testindexBuurtRooster()
    testbuurt2Fout()
    testbuurt2FoutNumeriek()
    testbuurt2FoutDiscretisatie()
    testbuurt2FoutNumeriekDiscretisatie()
    
if __name__ == "__main__":
    alleTesten()
