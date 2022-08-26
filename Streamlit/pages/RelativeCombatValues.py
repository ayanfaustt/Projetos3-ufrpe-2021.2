def relativeCombatValues(dataFrame):
    dsEq = dataFrame.copy()
    colSum = ['hp', 'attack', 'defense', 'special_attack', 'special_defense', 'speed']

    for i in colSum:
        dsEq[i] = dataFrame[i]/dataFrame[colSum].sum(axis=1)
    
    return dsEq

