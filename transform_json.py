import json
import os

def cria_se_nao_existe(arquivo):
		local = os.path.dirname(arquivo)
		if not os.path.exists(local):
				os.makedirs(local)

with open('listas_da_biblia.txt', "r", encoding='utf-8') as file: 
    linhas = file.read()


caminho_arquivo = './listas_da_biblia.json'
cria_se_nao_existe(caminho_arquivo)

# Salvar o conteúdo no arquivo JSON
with open(caminho_arquivo, 'w') as arquivo:
    json.dump(linhas, arquivo)

with open(caminho_arquivo, "r", encoding='utf-8') as arquivo: 
        tupla_recuperada = json.load(arquivo)
    
print(tupla_recuperada)
