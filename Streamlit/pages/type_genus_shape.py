def type_genus_shape():
        #conversão dos tipos
        ds_type = pd.read_csv(path_to_dataset)
        ds_types = ds_type["typing"].unique()
        type_iterator = list()
        for type in ds_types:
            if not("~" in type):
                type_iterator.append(type)
        ds_type = pd.read_csv(path_to_dataset)
        ds_type.drop(['typing'], axis=1, inplace=True)

        for i in range(len(ds)):
            type_aux = type_iterator[:]
            # print(type_aux)
            if '~' in ds.loc[i,'typing']:

                pokemon_types = ds.loc[i,'typing'].split('~')
                ds_type.loc[i,pokemon_types[0]] = int(1)
                ds_type.loc[i, pokemon_types[1]] = int(1)
                type_aux.pop(type_aux.index(pokemon_types[0]))
                type_aux.pop(type_aux.index(pokemon_types[1]))

                for j in type_aux:
                    ds_type.loc[i,j] = int(0)
            else:

                mono_type = ds.loc[i,'typing']
                ds_type.loc[i,mono_type] = int(1)
                type_aux.pop(type_aux.index(mono_type))

                for k  in type_aux:
                    ds_type.loc[i,k] = int(0)

        st.dataframe(ds_type,None)

        #conversão genus
        ds_genus = ds_type['genus'].unique()
        genus_iterator = list()
        for genuslist in ds_genus:
            genus_iterator.append(genuslist)
        
        for index in range(len(ds)):
            genus_aux = genus_iterator[:]
            genus_class = ds_type.loc[index,'genus']
            ds_type.loc[index,genus_class] = 1
            genus_aux.pop(genus_aux.index(genus_class))
            for genus_i in genus_aux:
                ds_type.loc[index, genus_i] = 0

        ds_type.drop(['genus'], axis=1, inplace=True)
        st.dataframe(ds_type,None)

        #conversão de shape
        ds_shape = ds_type['shape'].unique()
        shape_iterator = [shapelist for shapelist in ds_shape]
         
        
        teste = list()

        for shapeIndex in range(len(ds)):
            shape_aux = shape_iterator[:]
            shape_class = ds_type.loc[shapeIndex,'shape']
            ds_type.loc[shapeIndex, shape_class] = 1 
            shape_aux.pop(shape_aux.index(shape_class))
            for shape_i in shape_aux:
                ds_type.loc[shapeIndex,shape_i] = 0
        ds_type.drop(['shape'], axis=1, inplace=True)
        st.dataframe(ds_type,None)