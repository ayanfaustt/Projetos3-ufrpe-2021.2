def typeConversion(dataFrame):
    unique_val = dataFrame["typing"].unique()
    
    type_iterator = list()
    for type in unique_val:
        if not("~" in type):
            type_iterator.append(type)

  
    
    for i in range(len(dataFrame)):
        type_aux = type_iterator[:]
        if '~' in dataFrame.loc[i,'typing']:
            pokemon_types = dataFrame.loc[i,'typing'].split('~')
            dataFrame.loc[i,pokemon_types[0]] = int(1)
            dataFrame.loc[i, pokemon_types[1]] = int(1)
            type_aux.pop(type_aux.index(pokemon_types[0]))
            type_aux.pop(type_aux.index(pokemon_types[1]))
            for j in type_aux:
                dataFrame.loc[i,j] = int(0)
        else:
            mono_type = dataFrame.loc[i,'typing']
            dataFrame.loc[i,mono_type] = int(1)
            type_aux.pop(type_aux.index(mono_type))
            for k  in type_aux:
                dataFrame.loc[i,k] = int(0)
    
    dataFrame.drop(['typing'], axis=1, inplace=True)

    return dataFrame


def colummConversion(dataFrame, col):
    
    unique_val = dataFrame[col].unique()

    var_iterator = [itemlist for itemlist in unique_val]
    for index in range(len(dataFrame)):
        varIterator_aux = var_iterator[:]
        current_val = dataFrame.loc[index,col]
        dataFrame.loc[index, current_val] = 1 
        varIterator_aux.pop(varIterator_aux.index(current_val))
        for index_i in varIterator_aux:
            dataFrame.loc[index,index_i] = 0
    
    dataFrame.drop([col], axis=1, inplace=True)

    return dataFrame
