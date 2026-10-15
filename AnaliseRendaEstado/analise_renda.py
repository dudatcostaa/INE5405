import pandas as pd
import matplotlib.pyplot as plt

ARQUIVO = 'dataset_final.xlsx'

RENDA = 'Renda (R$) acumulada'
REGIOES = {
    'AC': 'Norte', 'AP': 'Norte', 'AM': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste',
    'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MT': 'Centro-Oeste', 'MS': 'Centro-Oeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul',
}

def preparar_renda(data):
    d = data.copy()
    d[RENDA] = pd.to_numeric(d[RENDA], errors='coerce')
    d['Região'] = d['UF'].map(REGIOES) 
    return d

def analise_renda(data, grupo):
    d = data.dropna(subset=[grupo, RENDA])
    d = d[d[grupo] != 'ND']

    tab = d.groupby(grupo)[RENDA].agg(
        Filmes='count', Total='sum', Média='mean', Mediana='median', Desvio='std', Máximo='max'
    ).sort_values('Total', ascending=False)
    tab['% da renda total'] = (tab['Total'] / tab['Total'].sum() * 100).round(2)
    tab['% dos filmes'] = (tab['Filmes'] / tab['Filmes'].sum() * 100).round(2)

    print(f'\nRenda por {grupo}')
    print(tab.round(2).to_markdown())
    tab.round(2).to_excel(f'renda_por_{grupo}.xlsx')
    return tab

def grafico_renda_total(tab, grupo):
    plt.figure(figsize=(12, 6))
    barras = plt.bar(tab.index.astype(str), tab['Total'] / 1e6, color='mediumblue')
    plt.bar_label(barras, labels=[f'{p:.1f}%' for p in tab['% da renda total']], padding=3, fontsize=8)
    plt.ylim(0, (tab['Total'] / 1e6).max() * 1.1)
    plt.title(f'Renda total acumulada por {grupo}')
    plt.xlabel(grupo)
    plt.ylabel('Renda (milhões de R$)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'renda_total_por_{grupo}.png')
    plt.show()

def boxplot_renda_por_grupo(data, grupo):
    d = data.dropna(subset=[grupo, RENDA])
    d = d[(d[grupo] != 'ND') & (d[RENDA] > 0)]
    ordem = d.groupby(grupo)[RENDA].median().sort_values(ascending=False).index
    grupos = [d.loc[d[grupo] == g, RENDA] for g in ordem]

    plt.figure(figsize=(12, 6))
    plt.boxplot(grupos, tick_labels=list(ordem))
    plt.yscale('log')
    plt.title(f'Renda por filme segundo {grupo} (escala logarítmica)')
    plt.xlabel(grupo)
    plt.ylabel('Renda (R$)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'boxplot_renda_por_{grupo}.png')
    plt.show()


def main():
    if ARQUIVO.endswith('.csv'):
        data = pd.read_csv(ARQUIVO)
    else:
        data = pd.read_excel(ARQUIVO)
    data = preparar_renda(data)

    tab_uf = analise_renda(data, 'UF')
    grafico_renda_total(tab_uf, 'UF')
    boxplot_renda_por_grupo(data, 'UF')

    tab_reg = analise_renda(data, 'Região')
    grafico_renda_total(tab_reg, 'Região')
    boxplot_renda_por_grupo(data, 'Região')


if __name__ == '__main__':
    main()