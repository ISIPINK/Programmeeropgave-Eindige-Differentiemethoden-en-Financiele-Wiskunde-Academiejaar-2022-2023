from parametersOpgave import parametersOpgave        

from scipy.linalg import expm, norm
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plotnine import *

def testn2expM():
    I = np.eye(3)
    print("I=")
    print(I)
    print("expM(I)=")
    print(expm(I))
    print("n2expM(I)=")
    print(norm(expm(I),2))

    II = np.matrix([[1,1],[1,1]])
    print("II=")
    print(II)
    print("expM(II)=")
    print(expm(II))
    print("n2expM(II)=",norm(expm(II),2))
    



def grafiekMatrixExpA(alleM:"lijst van m" = [5,10,20,50,100]):
    looptijd = parametersOpgave(0).looptijd
    times = np.arange(0, looptijd, looptijd/200)

    df = pd.DataFrame({"time":[], "m":[], "n2expM":[]})

    for m in alleM:
        A = parametersOpgave(m).A()
        for time in times:
            row = pd.Series([time,m, norm(expm(A*time),2)],index = df.columns)
            df = df.append(row, ignore_index = True)

    plot = ggplot(df) + aes(x="time",y= "n2expM",color="m") + geom_point(size = 0.5)
    plot.save("../verslag/oefening2.png",dpi = 300)


def grafiekMuA(alleM:"lijst van m" = list(range(5,50))+ list(range(50,100,5))+ list(range(100,1000,100))):
    df = pd.DataFrame({"m":[], "mu":[], "ass":[]})
    for m in alleM:
        A = parametersOpgave(m).A()
        row = pd.Series([
            m,
            eigsh(0.5* (A + A.transpose()), k = 1, which = 'LA')[0][0],
            m**2
            ],index = df.columns)
        df = df.append(row, ignore_index = True)

    plot = (
    ggplot(df) 
    + geom_line(aes(x="m",y= "mu"), color = "blue") 
    + geom_line(aes(x="m",y= "ass"),color = "red") 
    + scale_y_continuous(trans='log10') 
    + scale_x_continuous(trans='log10')
    )
    plot.save("../verslag/oefening3.png",dpi = 300)

def alleGrafieken():
    grafiekMatrixExpA()
    grafiekMuA()

if __name__ == "__main__":
    testn2expM()

