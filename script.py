import pandas as pd
import matplotlib.pyplot as plt


# tabela de frequências
def calcular_frequencias(data, coluna):
    df = data[coluna].value_counts().reset_index()
    df.columns = [coluna, 'Quantidade']

    df['Frequência Relativa (%)'] = (df['Quantidade'] / df['Quantidade'].sum() * 100).round(2)

    print(f"\nTabela de Frequência: {coluna}")
    print(df.to_markdown(index=False))

    df.to_excel(f'freq_table_{coluna}.xlsx', index=False)

    return df


# salvar tabela de frequências como imagem
def salvar_tabela_frequencias_imagem(df, coluna):
    fig, ax = plt.subplots(figsize=(9, len(df) * 0.4 + 1.5))
    ax.axis('off')

    tabela = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', colWidths=[0.45, 0.25, 0.30], bbox=[0.02, 0.02, 0.96, 0.90])

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(10)

    for (linha, coluna_idx), celula in tabela.get_celld().items():
        celula.set_edgecolor('#E5E7EB')
        celula.set_linewidth(0.5)

        if linha == 0:
            celula.set_facecolor('#243B55')
            celula.set_text_props(color='white', weight='bold')
        elif linha % 2 == 0:
            celula.set_facecolor('#F1F5F9')
        else:
            celula.set_facecolor('white')

    fig.suptitle(f'Tabela de Frequência: {coluna}', fontsize=14, fontweight='bold', y=0.98)
    plt.savefig(f'freq_table_{coluna}.png', bbox_inches='tight', dpi=300)
    plt.show()

# medidas de tendência central
def calcular_medidas_centrais(data, coluna):
    valores = data[coluna].dropna()

    media = valores.mean()
    mediana = valores.median()
    moda = valores.mode()

    print(f'\nMedidas de Tendência Central: {coluna}')
    print(f'Média: {media:.2f}')
    print(f'Mediana: {mediana:.2f}')

    if valores.value_counts().max() == 1:
        print('Moda: não há')
    else:
        print(f'Moda: {moda.tolist()}')

    return media, mediana, moda

# gráfico de colunas
# gráfico de colunas (com porcentagem em cima de cada coluna)
def grafico_colunas(df, coluna):
    df = df.sort_values(by=coluna)

    categorias = df[coluna].astype(str)
    quantidades = df['Quantidade']
    percentuais = df['Frequência Relativa (%)']

    plt.figure(figsize=(12, 6))
    barras = plt.bar(categorias, quantidades, color='mediumblue')
    plt.bar_label(barras, labels=[f'{p:.1f}%' for p in percentuais], padding=3, fontsize=8)
    plt.ylim(0, quantidades.max() * 1.1)   # folga para o texto da maior coluna não cortar
    plt.title(f'{coluna} (Gráfico de Colunas)')
    plt.xlabel(coluna)
    plt.ylabel('Quantidade')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'grafico_colunas_{coluna}.png')
    plt.show()


# gráfico de barras
# gráfico de barras (com porcentagem ao lado de cada barra)
def grafico_barras(df, coluna):
    df = df.sort_values(by=coluna)

    categorias = df[coluna].astype(str)
    quantidades = df['Quantidade']
    percentuais = df['Frequência Relativa (%)']

    plt.figure(figsize=(10, 8))
    barras = plt.barh(categorias, quantidades, color='lightgreen')
    plt.bar_label(barras, labels=[f'{p:.1f}%' for p in percentuais], padding=3, fontsize=8)
    plt.xlim(0, quantidades.max() * 1.12)   # folga para o texto da maior barra não cortar
    plt.title(f'{coluna} (Gráfico de Barras)')
    plt.xlabel('Quantidade')
    plt.ylabel(coluna)
    plt.tight_layout()
    plt.savefig(f'grafico_barras_{coluna}.png')
    plt.show()


# gráfico de setores
def grafico_setores(df, coluna):
    categorias = df[coluna].astype(str)
    quantidades = df['Quantidade']

    plt.figure(figsize=(10, 10))
    plt.pie(quantidades, labels=categorias, autopct='%1.1f%%', startangle=90)
    plt.title(f'Proporção de {coluna} (Gráfico de Setores)')
    plt.tight_layout()
    plt.savefig(f'grafico_setores_{coluna}.png')
    plt.show()


# boxplot
def grafico_boxplot(data, coluna):
    plt.boxplot(data[coluna].dropna())
    plt.title(coluna)
    plt.show()


# histograma
def grafico_histograma(data, coluna):
    plt.hist(data[coluna].dropna(), bins=20, color='skyblue', edgecolor='black')
    plt.title(f'Histograma - {coluna}')
    plt.xlabel(coluna)
    plt.ylabel('Quantidade de Filmes (Frequência)')
    plt.savefig(f'histograma_{coluna}.png')
    plt.show()


def main():
    data = pd.read_excel('dataset_final.xlsx') # substituir pelo nome da planilha analisada

    # substituir o segundo parâmetro de cada função pela análise desejada

    # tabela de frequência
    df = calcular_frequencias(data, 'UF')
    salvar_tabela_frequencias_imagem(df, 'UF')

    # medidas de tendência central
    calcular_medidas_centrais(data, 'Minutos')

    # gráficos de frequência
    grafico_colunas(df, 'UF')
    grafico_barras(df, 'UF')
    grafico_setores(df, 'UF')

    # boxplot e histograma
    grafico_boxplot(data, 'UF')
    grafico_histograma(data, 'UF')


if __name__ == '__main__':
    main()
