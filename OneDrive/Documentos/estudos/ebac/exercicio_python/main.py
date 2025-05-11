import csv
import json
import os
import time
from random import random
from datetime import datetime
from sys import argv

import pandas as pd
import requests
import seaborn as sns
import matplotlib.pyplot as plt

URL = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados'

# Captando a taxa CDI do site do BCB
def extrair_taxa_cdi():
    print("Tentando extrair taxa CDI...")
    try:
        response = requests.get(url=URL)
        response.raise_for_status()
    except requests.HTTPError:
        print("Dado não encontrado, continuando.")
        return None
    except Exception as exc:
        print("Erro, parando a execução.")
        raise exc
    else:
        dado = json.loads(response.text)[-1]['valor']
        print(f"Taxa CDI extraída: {dado}")
        return dado

# Criando a variável data e hora e salvando no CSV
def gerar_csv():
    print("Iniciando geração do CSV...")
    dado = extrair_taxa_cdi()
    
    # Usando a pasta do usuário
    arquivo_csv = os.path.join(os.path.expanduser('~'), 'taxa_cdi.csv')
    print(f"Arquivo CSV será salvo em: {arquivo_csv}")

    # Limpar o arquivo se ele existir
    if os.path.exists(arquivo_csv):
        print("Removendo arquivo CSV existente...")
        os.remove(arquivo_csv)

    # Criar novo arquivo com cabeçalho
    print("Criando novo arquivo CSV...")
    with open(file=arquivo_csv, mode='w', encoding='utf8') as fp:
        fp.write('data,hora,taxa\n')

    for i in range(0, 10):
        data_e_hora = datetime.now()
        data = datetime.strftime(data_e_hora, '%Y/%m/%d')
        hora = datetime.strftime(data_e_hora, '%H:%M:%S')

        cdi = float(dado) + (random() - 0.5)

        with open(file=arquivo_csv, mode='a', encoding='utf8') as fp:
            fp.write(f'{data},{hora},{cdi}\n')
        
        print(f"Registro {i+1} de 10 adicionado ao CSV")
        time.sleep(1)

    print("CSV gerado com sucesso.")

# Salvando gráfico
def gerar_grafico(nome_grafico):
    print(f"Iniciando geração do gráfico {nome_grafico}...")
    arquivo_csv = os.path.join(os.path.expanduser('~'), 'taxa_cdi.csv')
    arquivo_grafico = os.path.join(os.path.expanduser('~'), f"{nome_grafico}.png")
    
    print(f"Lendo arquivo CSV de: {arquivo_csv}")
    # Verificar se o arquivo existe
    if not os.path.exists(arquivo_csv):
        print(f"Erro: Arquivo {arquivo_csv} não encontrado!")
        return

    # Ler o CSV e mostrar as colunas disponíveis
    df = pd.read_csv(arquivo_csv)
    print("Colunas disponíveis:", df.columns.tolist())
    
    # Verificar se as colunas necessárias existem
    if 'hora' not in df.columns or 'taxa' not in df.columns:
        print("Erro: Colunas 'hora' ou 'taxa' não encontradas no arquivo CSV!")
        return

    print("Criando gráfico...")
    # Criar o gráfico com configurações melhoradas
    plt.figure(figsize=(10, 6))  # Definir tamanho do gráfico
    grafico = sns.lineplot(x=df['hora'], y=df['taxa'])
    plt.xticks(rotation=90)  # Rotacionar labels do eixo x
    plt.title('Variação da Taxa CDI')  # Adicionar título
    plt.xlabel('Hora')  # Adicionar label do eixo x
    plt.ylabel('Taxa')  # Adicionar label do eixo y
    plt.tight_layout()  # Ajustar layout para evitar cortes
    
    print(f"Salvando gráfico em: {arquivo_grafico}")
    plt.savefig(arquivo_grafico)
    
    print("Exibindo gráfico...")
    plt.show()  # Mostrar o gráfico na tela
    plt.close()  # Fechar a figura para liberar memória
    
    print(f"Gráfico salvo como {nome_grafico}.png")

# Execução principal
def main():
    print("Iniciando execução do script...")
    if len(argv) < 2:
        print("Por favor, forneça o nome do gráfico como parâmetro.")
        return

    nome_grafico = argv[1]
    print(f"Nome do gráfico: {nome_grafico}")
    
    gerar_csv()
    gerar_grafico(nome_grafico)
    print("Script finalizado com sucesso!")

if __name__ == "__main__":
    main()