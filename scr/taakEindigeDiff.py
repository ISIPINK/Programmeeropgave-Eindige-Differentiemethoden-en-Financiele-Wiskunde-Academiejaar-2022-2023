from parametersOpgave import parametersOpgave        

from scipy.linalg import expm, norm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plotnine import ggplot, geom_point, aes


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




if __name__ == "__main__":
    grafiekMatrixExpA()
