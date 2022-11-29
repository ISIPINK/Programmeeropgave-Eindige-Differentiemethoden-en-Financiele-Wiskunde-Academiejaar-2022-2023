from PlaatsModel import PlaatsModel

def parametersOpgave(plaatsPunten:int = 100):
    if plaatsPunten > 10**4:
        raise Exception("Zoveel punten (>10**4) kunnen mijn geheugen niet aan")

    par = PlaatsModel(
           rente = 0.01,
           volatiliteit =0.25,
           looptijd = 2,
           strike = 100,
           L = 80,
           S = 300,
           plaatsPunten = plaatsPunten) 
    return par
