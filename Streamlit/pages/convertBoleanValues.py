def convertBoleanValues(dataFrame):
    dsBv = dataFrame.copy()
    boolcolumns = ['genderless', 'baby_pokemon', 'legendary', 'mythical', 'is_default', 'forms_switchable', 'can_evolve']

    for i in range(len(boolcolumns)):
        dsBv[boolcolumns[i]] = dsBv[boolcolumns[i]].astype(int)
    
    return dsBv[boolcolumns]