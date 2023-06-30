
import re
import os
import timeit


r'''
Explicação desse regex
r = Inicio de regex python
</ = procura por esse padrão
[^>] = Tudo exceto o > será incluído aqui
> = Valor final para fechar o regex
(?!v) = Ele garante que o conteúdo entre < e > não comece com a letra v.
\b = fronteira de palavra, ou seja, só retorna s, se tivesse <sample, <sol, <sub ele não consideraria mesmo iniciando com <s
.*? = busca não gulosa se fosse assim: <s> tesat </s> <o>asdasd</o> <s>outa</> com o guloso .* ele substituiria também o <o>{}</o>

(\w+): Isso cria um grupo de captura e corresponde 
		a uma ou mais ocorrências de caracteres alfanuméricos (letras maiúsculas e minúsculas, dígitos de 0 a 9 e sublinhados). 
		O + indica que deve haver pelo menos um caractere.
'''

siglas  = {
    'GÊNESIS': 'Gn',
    'ÊXODO': 'Êx',
    'LEVÍTICO': 'Lv',
    'NÚMEROS': 'Nm',
    'DEUTERONÔMIO': 'Dt',
    'JOSUÉ': 'Js',
    'JUÍZES': 'Jz',
    'RUTE': 'Rt',
    '1 SAMUEL': '1 Sm',
    '2 SAMUEL': '2 Sm',
    '1 REIS': '1 Rs',
    '2 REIS': '2 Rs',
    '1 CRÔNICAS': '1 Cr',
    '2 CRÔNICAS': '2 Cr',
    'ESDRAS': 'Ed',
    'NEEMIAS': 'Ne',
    'ESTER': 'Et',
    'JÓ': 'Jó',
    'SALMOS': 'Sl',
    'PROVÉRBIOS': 'Pv',
    'ECLESIASTES': 'Ec',
    'CÂNTICOS': 'Ct',
    'ISAÍAS': 'Is',
    'JEREMIAS': 'Jr',
    'LAMENTAÇÕES DE JEREMIAS': 'Lm',
    'EZEQUIEL': 'Ez',
    'DANIEL': 'Dn',
    'OSÉIAS': 'Os',
    'JOEL': 'Jl',
    'AMÓS': 'Am',
    'OBADIAS': 'Ob',
    'JONAS': 'Jn',
    'MIQUÉIAS': 'Mq',
    'NAUM': 'Na',
    'HABACUQUE': 'Hc',
    'SOFONIAS': 'Sf',
    'AGEU': 'Ag',
    'ZACARIAS': 'Zc',
    'MALAQUIAS': 'Ml',
    'MATEUS': 'Mt',
    'MARCOS': 'Mc',
    'LUCAS': 'Lc',
    'JOÃO': 'Jo',
    'ATOS DOS APÓSTOLOS': 'At',
    'ROMANOS': 'Rm',
    '1 CORÍNTIOS': '1 Co',
    '2 CORÍNTIOS': '2 Co',
    'GÁLATAS': 'Gl',
    'EFÉSIOS': 'Ef',
    'FILIPENSES': 'Fp',
    'COLOSSENSES': 'Cl',
    '1 TESSALONICENSES': '1 Ts',
    '2 TESSALONICENSES': '2 Ts',
    '1 TIMÓTEO': '1 Tm',
    '2 TIMÓTEO': '2 Tm',
    'TITO': 'Tt',
    'FILEMOM': 'Fm',
    'HEBREUS': 'Hb',
    'TIAGO': 'Tg',
    '1 PEDRO': '1 Pe',
    '2 PEDRO': '2 Pe',
    '1 JOÃO': '1 Jo',
    '2 JOÃO': '2 Jo',
    '3 JOÃO': '3 Jo',
    'JUDAS': 'Jd',
    'APOCALIPSE': 'Ap'
}


class Transpilador:

	def __init__(self):
		self.arquivo_saida = ''
		self.arquivo_input = ''

		self.regex_close_tag = r"</[^>]+>"
		self.regex_tags_iniciais = r"<(?!v)[^>]*>"
		self.regex_titulos = r"<s\b[^>]*>.*?</s>"

		self.extrator_de_versiculo  = r'<v n="(\d+)" .*?/>'
		self.extrator_de_capitulo  = r'.*/([\w\s]+).xml'
		self.extrator_de_livro = r'.*/([\w\s]+)_.*?l'

		self.versoes = {}
		self.sigla = ''
		self.load_versoes()
		

	def set_input(self, arquivo_input):
		self.arquivo_input = arquivo_input
		self.set_livro()
		self.set_capitulo()

	def set_livro(self):
		self.livro = re.sub(self.extrator_de_livro, r'\1', self.arquivo_input).upper()

	def set_capitulo(self):
		capitulo = re.sub(self.extrator_de_capitulo, r'\1', self.arquivo_input)
		self.capitulo = f' {capitulo.upper().replace("_", " ")}'

	def get_capitulo(self):
		return self.capitulo

	def get_livro(self):
		return self.livro

	def transpilar_com_regex(self):
		with open(self.arquivo_input, "r", encoding='utf-8') as file:
			linha = file.read()

			linha_sem_titulos = re.sub(self.regex_titulos, " ", linha)
			linha_sem_close_tags = re.sub(self.regex_close_tag, " ", linha_sem_titulos) 
			linha_sem_tags = re.sub(self.regex_tags_iniciais, " ", linha_sem_close_tags) 
			linha_com_espacos_ajustados = ' '.join(linha_sem_tags.strip().split())
			linha_com_versiculos = re.sub(self.extrator_de_versiculo, fr'\n#{self.sigla}{self.capitulo.split()[-1]}-\1: ', linha_com_espacos_ajustados)
				
			return linha_com_versiculos

	def load_versoes(self, versoes=None):
		if not versoes is None:
			self.versoes = {}
			for versao in versoes:
				self.versoes[versao] = []
		else:
			for arquivo in os.listdir():
				if '.' in arquivo or arquivo=='biblias':
					pass
				else:
					self.versoes[arquivo] = []
		self.load_capitulos()

	def load_capitulos(self):
		
		for versao in self.versoes:
			pasta_versao = f'./{versao}'
			arquivos = os.listdir(pasta_versao)

			arquivos_ordenados = sorted(arquivos, key=lambda x: os.path.getmtime(os.path.join(pasta_versao, x)))
			for arquivo in arquivos_ordenados:
				self.versoes[versao].append(f'{pasta_versao}/{arquivo}')
		
	def cria_se_nao_existe(self, arquivo):
		local = os.path.dirname(arquivo)
		if not os.path.exists(local):
				os.makedirs(local)

	def get_nome_arquivo(self, versao):
		return f"./biblias/biblia{versao.upper()}.md"

	def esta_ordenada(self, lista):
		
		lista_int = list(map(int, lista))
		ordenada = sorted(lista_int)
		return ordenada == lista_int
				
	def escrever_arquivo(self):

		for versao, capitulos in self.versoes.items():
			caminho_saida = self.get_nome_arquivo(versao)
			self.cria_se_nao_existe(caminho_saida)
			print(f'Criando Biblia da versão: {versao}')

			with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
				livro_atual = ''
				numeros_capitulos = []

				for capitulo in capitulos:
					numeros_capitulos.append(capitulo.split('_')[1].split('.')[0])

					self.set_input(capitulo)
					if livro_atual != self.get_livro():
						if livro_atual!='':
							if not self.esta_ordenada(numeros_capitulos[:-1]):
								print(numeros_capitulos[:-1])
								break
								break

						livro_atual = self.livro
						self.sigla = siglas[self.livro]


						numeros_capitulos = ['1']
						arquivo_saida.write(f'\n{self.get_livro()}')
					arquivo_saida.write(f'\n{self.get_capitulo()}')
					arquivo_saida.write(self.transpilar_com_regex())
				
					





		
	def teste(self):
		self.load_versoes()
		tempo_execucao = timeit.timeit(self.escrever_arquivo, number=1)
		print("Tempo de execução:", tempo_execucao, "segundos")

transpilador = Transpilador()

transpilador.teste()