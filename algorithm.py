import time

def simpleAlg(kredits, bets):
    ratio = 1.3
    bet = bets[-1] if bets else None
    if bet:
        is_won = bet.is_won
    else: is_won = None

    if is_won == True or is_won == None:
        user_gave = kredits * 0.2 if kredits > 30 else kredits
    else: user_gave = 0


    bet = {'ratio': ratio, 'user_gave': user_gave}
    return bet

def last2LotAlg(kredits, bets):
    pass