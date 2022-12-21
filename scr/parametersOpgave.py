from Model import Model

def parametersOpgave(plaatsPunten:int = 100, tijdPunten:int = 100)->Model:
    if plaatsPunten > 10**4:
        raise Exception("Zoveel plaats punten (>10**4) kunnen mijn geheugen niet aan")

    if tijdPunten > 10**4:
        raise Exception("Zoveel tijd punten (>10**4) er moet ergens een limiet zijn")

    '''
    regels: die ik nog niet heb geimplementeerd
    L<strike<S 
    looptijd > 0 
    rente > 0 (denk ik)
    volatiliteit>0
    plaatsPunten en tijdPunten in \mathbb{N}
    
    '''
    par = Model(
           rente = 0.01,
           volatiliteit =0.25,
           looptijd = 2,
           strike = 100,
           L = 80,
           S = 300,
           plaatsPunten = plaatsPunten, # standaard 100
           tijdPunten = tijdPunten) # standaard 100 
    return par
