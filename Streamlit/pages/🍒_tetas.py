from re import A
import streamlit as st
import pandas as pd
import os
import statsmodels.api as sm
import pylab


st.set_page_config(
    page_title="Tetinhas",
    page_icon="🍒",
)

def main():
    path_to_dataset = os.path.join(os.getcwd(),os.pardir)+"/pokemon.parquet"
    ds = pd.read_parquet(path_to_dataset)

    valores_quantitativos = ['vida',
                'ataque',
                'defesa',
                'ataque_especial',
                'defesa_especial',
                'velocidade',
                'altura',
                'peso',
                'taxa_de_femeas',
                'xp_basico',
                'taxa_de_captura',
                'ciclo_de_ovo',
                'felicidade_base',
                'total_pokemons_do_mesmo_tipo',
                'vulnerabilidade_normal',
                'vulnerabilidade_fogo',
                'vulnerabilidade_agua',
                'vulnerabilidade_eletrico',
                'vulnerabilidade_planta',
                'vulnerabilidade_gelo',
                'vulnerabilidade_lutador',
                'vulnerabilidade_venenoso',
                'vulnerabilidade_terrestre',
                'vulnerabilidade_voador',
                'vulnerabilidade_pisiquico',
                'vulnerabilidade_inseto',
                'vulnerabilidade_pedra',
                'vulnerabilidade_fantasma',
                'vulnerabilidade_dragao',
                'vulnerabilidade_sombrio',
                'vulnerabilidade_aco',
                'vulnerabilidade_fada',
                'geracao']
    colunas = ['nome',
               'n_pokedex',
               'habilidades',
               'tipo',
               'vida',
               'ataque',
               'defesa',
               'ataque_especial',
               'defesa_especial',
               'velocidade',
               'altura',
               'peso',
               'genero',
               'geracao',
               'taxa_de_femeas',
               'sem_genero',
               'bebe_pokemon',
               'lendario',
               'mitico',
               'padrao',
               'forma_temporaria',
               'xp_basico',
               'taxa_de_captura',
               'grupo_de_ovo',
               'ciclo_de_ovo',
               'felicidade_base',
               'evoluivel',
               'evolui_de',
               'cor_primaria',
               'forma',
               'total_pokemons_do_mesmo_tipo',
               'vulnerabilidade_normal',
               'vulnerabilidade_fogo',
               'vulnerabilidade_agua',
               'vulnerabilidade_eletrico',
               'vulnerabilidade_planta',
               'vulnerabilidade_gelo',
               'vulnerabilidade_lutador',
               'vulnerabilidade_venenoso',
               'vulnerabilidade_terrestre',
               'vulnerabilidade_voador',
               'vulnerabilidade_pisiquico',
               'vulnerabilidade_inseto',
               'vulnerabilidade_pedra',
               'vulnerabilidade_fantasma',
               'vulnerabilidade_dragao',
               'vulnerabilidade_sombrio',
               'vulnerabilidade_aco',
               'vulnerabilidade_fada']
    ds.columns = colunas

    st.title("Tetinhas")   
    st.markdown(
        """
        ## Teste de distribuição de dados
        """
    )

    st.write("Esta seção será dedicada a testagem da distribuição dos dados das colunas quantitavivas do dataset, a fim de descobrir se será necessário normalizar ou não esses dados.")
    st.write('Abaixo encontra-se um overview das colunas que serão testadas:')
    st.write('\n')

    st.dataframe(ds[valores_quantitativos])

    colunaSelecionada = st.multiselect(
            'Selecione coluna para ver sua distribuição', valores_quantitativos)

    if st.button('Gerar gráficos'):
        plt.title(f"Histograma dos dados da coluna {colunaSelecionada[0]}")
        plt.hist(ds[colunaSelecionada], rwidth=0.9)
        st.pyplot(plt, clear_figure=True)

        sm.qqplot(ds[colunaSelecionada[0]], line = "r")
        st.pyplot(plt, clear_figure=True)


if __name__ == '__main__':
    main()