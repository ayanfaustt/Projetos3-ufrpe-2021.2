def boxPlotPoke(dataset,hp,attack,defense,speed,special_attack,special_defense,height,weight,normal_attack_effectiveness,
fire_attack_effectiveness,water_attack_effectiveness,electric_attack_effectiveness,grass_attack_effectiveness,ice_attack_effectiveness,
fighting_attack_effectiveness,poison_attack_effectiveness,bug_attack_effectiveness,ground_attack_effectiveness,fly_attack_effectiveness,
psychic_attack_effectiveness,rock_attack_effectiveness,ghost_attack_effectiveness,dragon_attack_effectiveness,dark_attack_effectiveness,
steel_attack_effectiveness,fairy_attack_effectiveness,base_experience,capture_rate,number_pokemon_with_typing,
egg_cycles,base_happiness,female_rate):
    ds = pd.read_csv(dataset)
    ds.boxplot(column=[hp, attack, defense, speed, special_attack, special_defense]
    ,fontsize=11, figsize=(10,10))
    ds.boxplot(column=[height, weight], fontsize=16, figsize=(30,30))

    ds.boxplot(column=[normal_attack_effectiveness, fire_attack_effectiveness,
                   water_attack_effectiveness, electric_attack_effectiveness,
                  grass_attack_effectiveness,ice_attack_effectiveness,
                   fighting_attack_effectiveness], fontsize=16, figsize=(30,30))

    ds.boxplot(column=[poison_attack_effectiveness,bug_attack_effectiveness,
                   ground_attack_effectiveness,fly_attack_effectiveness,
                   psychic_attack_effectiveness,rock_attack_effectiveness], fontsize=16, figsize=(30,30))

    ds.boxplot(column=[ghost_attack_effectiveness,dragon_attack_effectiveness,
                   dark_attack_effectiveness,steel_attack_effectiveness,
                   fairy_attack_effectiveness], fontsize=16, figsize=(25,25))

    ds.boxplot(column=[base_experience,capture_rate,number_pokemon_with_typing,egg_cycles,base_happiness,female_rate], fontsize=16, figsize=(10,10))

    st.write("""Alguns gráficos apresentam um boxplot um pouco diferente dos outros, por exemplo o de base_happiness, 
    onde há um um valor que a maioria dos dados se encontram, e há alguns que apresentam um valor maior, e outros com um valor
    menor.
    """)
    st.write("""Os outliers encontrados, principalmente nos status, são provenientes de um determinado pokemon 
        ser especial, ou por ser do tipo lendario, que por si só irá possuir uma base de status mais forte do que 
        outros pokemons "normais" ou so por ser um pokemon forte e possuir aquele atributo alto.
        E em relação aos multiplicadores de dano que um pokemon recebe de outro, quase sempre haverá um tipo muito forte
        ou muito fraco contra, causando também um outlier. 
    """)