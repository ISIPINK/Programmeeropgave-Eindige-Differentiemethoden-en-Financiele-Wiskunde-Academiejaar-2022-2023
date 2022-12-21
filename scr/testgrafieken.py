from scipy.linalg import expm, norm
from scipy.sparse.linalg import eigsh
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from grafieken import lognorm2

"""
Hier worden er een aantal functies getest dat in
de grafieken worden gebruikt
"""

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

def testlognorm2():
    I = np.eye(3)
    print("I=")
    print(I)
    print("lognorm2(I)=",lognorm2(I))

def alleTesten():
    testn2expM()
    testlognorm2()

if __name__ == "__main__":
    alleTesten()
    
