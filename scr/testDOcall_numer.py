from Model import Model
from DOcall_numer import MLDOCall
from parametersOpgave import parametersOpgave
import matplotlib.pyplot as plt

def testMLDOCall(aantalPlotLijnen=4, plaatsPunten=100, tijdPunten=100):
    par = parametersOpgave(plaatsPunten=plaatsPunten, tijdPunten=tijdPunten)
    Utime = MLDOCall(par)

    for i in range(0,len(Utime),tijdPunten//(aantalPlotLijnen-1)):
        Ut = Utime[i]
        plt.plot(par.roosterPunten, Ut, label = f"tijd:{par.tijdDiscretisatie[i]}")
    plt.xlabel("plaats")
    plt.ylabel("prijs")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    testMLDOCall()
