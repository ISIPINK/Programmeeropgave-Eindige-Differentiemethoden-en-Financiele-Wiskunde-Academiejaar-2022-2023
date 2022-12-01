from parametersOpgave import parametersOpgave   
import matplotlib.pyplot as plt

def testroosterPunten(plaatsPunten=10):
    roosterPunten = parametersOpgave(plaatsPunten = plaatsPunten).roosterPunten
    print("aantal plaatspunten:", len(roosterPunten))
    print("roosterPunten:")
    print(roosterPunten)

def testtijdDiscretisatie(tijdPunten=10):
    tijdDiscretisatie = parametersOpgave(tijdPunten=tijdPunten).tijdDiscretisatie
    print("aantal tijdPunten:", len(tijdDiscretisatie)-1) #ik tel laatste punt niet mee
    print("tijdDiscretisatie:")
    print(tijdDiscretisatie)

def testBegin0():
    par = parametersOpgave()
    x = par.roosterPunten
    y = [par.begint0(xi) for xi in x ]
    plt.plot(x,y)
    plt.title("testBegin0")
    plt.show()

def testBeginU(lijstPlaatsPunten = [20,50,100]):
    for plaatspunten in lijstPlaatsPunten:
        par = parametersOpgave(plaatspunten)
        x = par.roosterPunten
        y = par.beginU()
        plt.plot(x,y)
    plt.title(f"testBeginU plaatspunten={lijstPlaatsPunten} (cel averaging)")
    plt.show()

def testD():
    par = parametersOpgave()
    print("D_1:")
    print(par.D(1))

def testAd(dim=4):
    par = parametersOpgave(dim)
    Ad = par.Ad()
    print("Ad:")
    print("type:", type(Ad))
    print(Ad.toarray())

def testA(dim=4):
    print("Some sanity checks:")
    Pdif = parametersOpgave(dim)
    Pdif.c0 = lambda x : 0
    Pdif.c1 = lambda x : 0
    Pdif.c2 = lambda x : 1
    A = Pdif.A()* Pdif.maaswijdte**2
    print("pure diffusie orde 2:")
    print("type:", type(A))
    print(A.toarray())

    Pcon = parametersOpgave(dim)
    Pcon.c0 = lambda x : 0
    Pcon.c1 = lambda x : 1
    Pcon.c2 = lambda x : 0
    A = 2* Pcon.A()* Pcon.maaswijdte
    print("pure convectie orde 2:")
    print(A.toarray())

def testg(dim= 4):
    par = parametersOpgave(dim)
    g = par.g
    print("g(0):")
    print(g(0))
    print("g(2):")
    print(g(2))
    
def alleTesten():
    testroosterPunten()
    testtijdDiscretisatie()
    testBegin0()
    testBeginU()
    testD()
    testAd()
    testA()
    testg()

if __name__ == "__main__":
    alleTesten()   
