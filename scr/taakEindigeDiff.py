from parametersOpgave import parametersOpgave        

from scipy.linalg import expm, norm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from plotnine import ggplot, geom_point, aes


def grafiekMatrixExpA(l:"lijst van m" = [5,10,20,50,100]):
    p = parametersOpgave(0)
    t = np.arange(0,p.looptijd, p.looptijd/200)

    df = pd.DataFrame({"time":[], "m":[], "n2expM":[]})

    for m in l:
        par = parametersOpgave(m)
        for time in t:
            row = pd.Series([time,m, norm(expm(par.A()*time),2)],index = df.columns)
            df = df.append(row, ignore_index = True)

    tmp = ggplot(df) + aes(x="time",y= "n2expM",color="m") + geom_point(size = 0.5)
    tmp.save("oefening2.png")




if __name__ == "__main__":
