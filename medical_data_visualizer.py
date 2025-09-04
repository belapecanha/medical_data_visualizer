# Importa as bibliotecas usadas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1 - Le o arquivo CSV
df = pd.read_csv("medical_examination.csv")

# 2 - Calcula o BMI e cria uma coluna chamada overweight com todos que tem um BMI maior que 25
df['overweight'] = ((df['weight'] / (df['height']/100)**2)>25).astype(int)

# 3 - Normaliza as colunas 'cholesterol' e 'gluc' trocando os valores >1 para 1 e = 1 para 0
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

# 4 - Define a função que cria o gráfico de barras
def draw_cat_plot():
    # 5
    colunas= ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight']
    df_cat = pd.melt(df, id_vars=['cardio'], value_vars=colunas)

    # 6 - Conta a frequência de cada combinação e cria uma coluna 'total'
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    # 7 - Define a ordem desejada e cria um gráfico de barras
    ordem = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke']
    grafico = sns.catplot(data=df_cat, x ='variable', y='total', hue='value', col='cardio', kind = 'bar', order=ordem)


    # 8 - Armazena a figura 
    fig = grafico.fig


    # 9 - Salva e retorna a figura
    fig.savefig('catplot.png')
    return fig


# 10 - Define a função que cria o mapa de calor
def draw_heat_map():
    # 11 - Filtra os dados 
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) & (df['height'] >= df['height'].quantile(0.025)) & (df['height'] <= df['height'].quantile(0.975)) &
    (df['weight'] >= df['weight'].quantile(0.025)) & (df['weight'] <= df['weight'].quantile(0.975) )]

    # 12 - Calcula a matriz de correlação entre as variáveis
    corr = df_heat.corr()

    # 13 - Cria uma máscara 
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # 14 - Cria uma nova figura e eixo com tamanho 12x10
    fig, ax = plt.subplots(figsize=(12,10))

    # 15 - Desenha o mapa de calor
    sns.heatmap(corr, mask=mask, annot=True, fmt='.1f', cmap='coolwarm', square=True, ax=ax)


    # 16 - Salva e retorna a figura
    fig.savefig('heatmap.png')
    return fig
