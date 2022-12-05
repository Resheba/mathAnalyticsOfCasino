

def simpleAlg(kredits):
    ratio = 1.5
    user_gave = kredits * 0.5 if kredits > 5 else kredits

    bet = {'ratio': ratio, 'user_gave': user_gave}
    return bet