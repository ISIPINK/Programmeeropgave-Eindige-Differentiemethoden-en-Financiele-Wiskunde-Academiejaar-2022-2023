from parametersOpgave import parametersOpgave        

from scipy.linalg import expm, norm
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plotnine import *


def grafiekMatrixExpA(alleM:"lijst van m" = [5,10,20,50,100]):
    p = parametersOpgave(0)
    t = np.arange(0,p.looptijd, p.looptijd/200)

    df = pd.DataFrame({"time":[], "m":[], "n2expM":[]})

    for m in alleM:
        par = parametersOpgave(m)
        for time in t:
            row = pd.Series([time,m, norm(expm(par.A()*time),2)],index = df.columns)
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

    print(df.head())
    plot = (
    ggplot(df) 
    + geom_line(aes(x="m",y= "mu"), color = "blue") 
    + geom_line(aes(x="m",y= "ass"),color = "red") 
    + scale_y_continuous(trans='log10') 
    + scale_x_continuous(trans='log10')
    )
    plot.save("../verslag/oefening3.png",dpi = 300)


if __name__ == "__main__":
    print("lol")
