from Model import Model

def parametersOpgave(plaatsPunten:int = 100, tijdPunten:int = 100)->Model:
    if plaatsPunten > 10**3:
        raise Exception("Zoveel plaats punten (>10**4) kunnen mijn geheugen niet aan")

    if tijdPunten > 10**3:
        raise Exception("Zoveel tijd punten (>10**3) er moet ergens een limiet zijn")

    par = Model(
           rente = 0.01,
           volatiliteit =0.25,
           looptijd = 2,
           strike = 100,
           L = 80,
           S = 300,
           plaatsPunten = plaatsPunten,
           tijdPunten = tijdPunten) 
    return par
