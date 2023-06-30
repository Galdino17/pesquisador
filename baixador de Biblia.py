import requests
import random
import time
import os

caminho_arquivo = "listas_da_biblia.json"

livrosComCapitulos = [
    (1, 'Gênesis', 50),
    (2, 'Êxodo', 40),
    (3, 'Levítico', 27),
    (4, 'Números', 36),
    (5, 'Deuteronômio', 34),
    (6, 'Josué', 24),
    (7, 'Juízes', 21),
    (8, 'Rute', 4),
    (9, '1 Samuel', 31),
    (10, '2 Samuel', 24),
    (11, '1 Reis', 22),
    (12, '2 Reis', 25),
    (13, '1 Crônicas', 29),
    (14, '2 Crônicas', 36),
    (15, 'Esdras', 10),
    (16, 'Neemias', 13),
    (17, 'Ester', 10),
    (18, 'Jó', 42),
    (19, 'Salmos', 150),
    (20, 'Provérbios', 31),
    (21, 'Eclesiastes', 12),
    (22, 'Cânticos', 8),
    (23, 'Isaías', 66),
    (24, 'Jeremias', 52),
    (25, 'Lamentações de Jeremias', 5),
    (26, 'Ezequiel', 48),
    (27, 'Daniel', 12),
    (28, 'Oséias', 14),
    (29, 'Joel', 3),
    (30, 'Amós', 9),
    (31, 'Obadias', 1),
    (32, 'Jonas', 4),
    (33, 'Miquéias', 7),
    (34, 'Naum', 3),
    (35, 'Habacuque', 3),
    (36, 'Sofonias', 3),
    (37, 'Ageu', 2),
    (38, 'Zacarias', 14),
    (39, 'Malaquias', 4),
    (40, 'Mateus', 28),
    (41, 'Marcos', 16),
    (42, 'Lucas', 24),
    (43, 'João', 21),
    (44, 'Atos dos Apóstolos', 28),
    (45, 'Romanos', 16),
    (46, '1 Coríntios', 16),
    (47, '2 Coríntios', 13),
    (48, 'Gálatas', 6),
    (49, 'Efésios', 6),
    (50, 'Filipenses', 4),
    (51, 'Colossenses', 4),
    (52, '1 Tessalonicenses', 5),
    (53, '2 Tessalonicenses', 3),
    (54, '1 Timóteo', 6),
    (55, '2 Timóteo', 4),
    (56, 'Tito', 3),
    (57, 'Filemom', 1),
    (58, 'Hebreus', 13),
    (59, 'Tiago', 5),
    (60, '1 Pedro', 5),
    (61, '2 Pedro', 3),
    (62, '1 João', 5),
    (63, '2 João', 1),
    (64, '3 João', 1),
    (65, 'Judas', 1),
    (66, 'Apocalipse', 22)
]


#self.url = "https://data.bcdn.in/v20/bibles/{version}/40/11.xml"

class Baixador:

	def __init__(self):
		self.version = ''
		self.url = f"https://data.bcdn.in/v20/bibles/{self.version}"
		self.tempo_pausa = 0

	def set_url(self):
		self.url = f"https://data.bcdn.in/v20/bibles/{self.version}"

	def set_version(self, version):
		self.version = version
		self.set_url()

	def gerar_pausa(self, add=0):
		if self.pausa:
			# Gera uma pausa aleatória entre 100 e 5000 milissegundos
			self.tempo_pausa = random.randint(100+add, 500+add) / 1000
			# Pausa o código pelo tempo gerado em milissegundos
			time.sleep(self.tempo_pausa)

	def arquivo_existe(self, nome_arquivo):

		diretorio = os.path.dirname(nome_arquivo)
		if not os.path.exists(diretorio):
			os.makedirs(diretorio)

		if os.path.exists(nome_arquivo):
			 tamanho_arquivo = os.path.getsize(nome_arquivo)
			 if tamanho_arquivo > 0:
			 	return True
			 else:
			 	return False
		return False


	def salvar_biblia(self, numero_do_livro, capitulo, arquivo_output):
		# Faz a solicitação HTTP ao site
		link_get = f'{self.url}/{numero_do_livro}/{capitulo}.xml'

		response = requests.get(link_get)

		if response.status_code == 404:
			print(f"o {link_get} não contém na dataBase")
			return True


		# Verifica se a solicitação foi bem-sucedida
		if response.status_code == 200:
		    # Obtém o conteúdo do XML
		    xml_content = response.content

		    # Salva o conteúdo do XML em um arquivo
		    with open(arquivo_output, "wb") as file:
		        file.write(xml_content)
		    
		    print(f"O arquivo {arquivo_output} foi salvo com sucesso. Depois de uma pausa de {self.tempo_pausa}")
		    return True
		else:
			self.gerar_pausa(15000)
			print(f"Falha ao acessar o link {link_get}. O código de status da resposta foi:", response.status_code)
			return False

	def download(self, version, pausa=True):
		self.pausa = pausa
		self.set_version(version)
		for livro in livrosComCapitulos:
			nome_do_livro = livro[1]
			numero_do_livro = livro[0]
			quantidade_de_capitulos = livro[2]
			self.gerar_pausa(20000)

			for capitulo in range(quantidade_de_capitulos):
				
				arquivo_output = f"./{self.version}/{nome_do_livro}_{capitulo+1}.xml"
				while not self.arquivo_existe(arquivo_output):
					self.gerar_pausa()
					if self.salvar_biblia(numero_do_livro, capitulo+1, arquivo_output):
						break


downloader = Baixador()

listaVersoes =['ara', 'aa', 'arc', 'acf', 'naa', 'nvt', 'ol', 'rc69', 'nvi', 'tb', 'vc', 'rv', 'bdc', 'kjv', 'niv', 'kjf', 'receptus', 'alep']

for versao in listaVersoes:
	downloader.download(versao, False)

