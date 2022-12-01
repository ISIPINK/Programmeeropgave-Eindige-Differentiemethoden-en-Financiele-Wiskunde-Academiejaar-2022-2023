from Model import Model

from scipy.sparse import eye
from scipy.sparse.linalg import splu


def MLDOCall(M:Model)->"list of U's on different times": 
    # merk op dat Model sommige dinges niet cached 
    A = M.A()
    g = M.g
    Utime = [M.beginU()]

    LU = splu(eye(M.plaatsPunten, format = "csc")-0.5*M.tau * A)

    # dit is niet de beste manier om deze for loop te doen
    for t in M.tijdDiscretisatie[:-1]:
        # hier los ik dat ijl stelsel op 
        U = Utime[-1]
        rechtsIjlStelsel = U + 0.5* M.tau * (A.dot(U)+ g(t)+ g(t + M.tau))
        Unew = LU.solve(rechtsIjlStelsel)
        Utime.append(Unew)
    
    return Utime 


