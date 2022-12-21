from parametersOpgave import parametersOpgave        
from foutanalyse import indexBuurtRooster, buurt2Fout, buurt2FoutNumeriek
from DOcall_exact import uLaatste

from scipy.linalg import expm, norm
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plotnine import *

def grafiekMatrixExpA(alleM:"lijst van m" = [5,10,20,50,100]):
    looptijd = parametersOpgave(0).looptijd
    times = np.arange(0, looptijd, looptijd/200)

    df = pd.DataFrame({"time":[], "m":[], "n2expM":[]})

    for m in alleM:
        A = parametersOpgave(m).A()
        for time in times:
            row = pd.Series([time,m, norm(expm(A.toarray()*time),2)],index = df.columns)
            df = df.append(row, ignore_index = True)

    plot = ggplot(df) + aes(x="time",y= "n2expM",color="m") + geom_point(size = 0.5)
    plot.save("../verslag/oefening2.png",dpi = 300)


def lognorm2(A):
    #de grootste eigen waarde van 0.5(A+Atranspose:)
    return eigsh(0.5* (A + A.transpose()), k = 1, which = 'LA')[0][0]

def grafiekMuA(alleM:"lijst van m" = list(range(5,50))+ list(range(50,100,5))+ list(range(100,1000,100))):
    df = pd.DataFrame({"m":[], "mu":[], "ass":[]})
    for m in alleM:
        A = parametersOpgave(m).A()
        row = pd.Series([m,lognorm2(A),m**2],index = df.columns)
        df = df.append(row, ignore_index = True)

    plot = (
    ggplot(df) 
    + geom_line(aes(x="m",y= "mu"), color = "blue") 
    + geom_line(aes(x="m",y= "ass"),color = "red") 
    + scale_y_continuous(trans='log10') 
    + scale_x_continuous(trans='log10')
    )
    plot.save("../verslag/oefening3.png",dpi = 300)

def grafiekExacte50():
    par = parametersOpgave(50)
    onderliggende = par.roosterPunten
    prijs = uLaatste(par,par.looptijd)
    df = pd.DataFrame(onderliggende,prijs )
    plot = (
    ggplot(df, aes(x="onderliggende", y="prijs")) 
    + geom_line() 
    + ggtitle("exacte oplossing m = 50")
    )
    plot.save("../verslag/oefening6.png",dpi = 300)

def grafiekBuurtFout(alpha=0.3,plaatsPunten:list = range(5,180,5)):
    buurtfouten = [buurt2Fout(alpha,parametersOpgave(pp,tijdPunten=1000))
            for pp in plaatsPunten ]
    df = pd.DataFrame(plaatsPunten,buurtfouten)
    plot = (
    ggplot(df, aes(x="plaatsPunten", y="buurtfouten")) 
    + geom_point() 
    + ggtitle("m vs buurtfout")
    )
    plot.save("../verslag/oefening8e.png",dpi = 300)

def grafiekBuurtFoutNumeriek(alpha=0.3,plaatsPunten:list = range(10,500,31)):
    buurtfouten = [buurt2FoutNumeriek(alpha,parametersOpgave(pp,tijdPunten=1000))
            for pp in plaatsPunten ]
    df = pd.DataFrame(plaatsPunten,buurtfouten)
    plot = (
    ggplot(df, aes(x="plaatsPunten", y="buurtfouten")) 
    + geom_point() 
    + ggtitle("m vs buurtfout numeriek")
    + scale_y_continuous(trans='log10') 
    + scale_x_continuous(trans='log10')
    )
    plot.save("../verslag/oefening8n.png",dpi = 300)

def alleGrafieken():
    grafiekMatrixExpA()
    grafiekMuA()
    grafiekExacte50()

if __name__ == "__main__":
    grafiekBuurtFout()
    grafiekBuurtFoutNumeriek()

