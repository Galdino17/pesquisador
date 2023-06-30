
with open('./biblias/bibliareceptus.md', "r", encoding='utf-8') as file:
	linhas = file.read()

palavras = {}
lista_palavras = linhas.split()
dez_mais = []

for palavra in lista_palavras:
	if palavra[0]=='#':
		continue
	try:
		palavras[palavra]+=1
	except:
		palavras[palavra]=1

ordenado = sorted(palavras.items(), key=lambda x: x[1])
lista_hoje = ordenado[len(ordenado)-10:len(ordenado)]

# caracteres = []
# for linha in linhas:
# 	if ':' in linha:
# 		texto = linha.split(':')[1]
# 		for caracter in texto:
# 			if not caracter in caracteres:
# 				caracteres.append(caracter)

# palavras_exemplo = {}

# for caracter in caracteres:
# 	for linha in linhas:
# 		if ':' in linha:
# 			texto = linha.split(':')[1]
# 			palavras = texto.split()
# 			for palavra in palavras:
# 				if caracter in palavra:
# 					palavras_exemplo[caracter] = palavra
# 					break
# 					break

caracteres = [ 'β', 'ι', 'λ', 'ο', 'ς', 'γ', 'ε', 'ν', 'σ', 'ω', 'η', 'υ', 'χ', 'ρ', 'τ', 'δ', 'α', 'μ', 'κ', 'φ', 'ζ', 'θ', 'π', 'ξ', 'ψ']
fonemas = {' ':' ', 'β':'v', 'ι':'i', 'λ':'l', 'ο':'o', 'ς':'s', 'γ':'g', 'ε':'e', 'ν':'n', 'σ':'s', 'ω':'ó', 'η':'ê', 'υ':'u', 'χ':'k', 'ρ':'r', 'τ':'t', 'δ':'d', 'α':'a', 'μ':'m', 'κ':'k', 'φ':'f', 'ζ':'z', 'θ':'th', 'π':'p', 'ξ':'x', 'ψ':'ps'}

print(fonemas)

def transcrever_fonema(palavra):
	fonema = []
	for caracter in palavra:
		fonema.append(fonemas[caracter])

	print(f"transcrição: {''.join(fonema)} palavra: {palavra}")
	

[transcrever_fonema(palavra[0]) for palavra in lista_hoje]

while True:

	palavra = input("\nDigite o termo grego: \n")
	transcrever_fonema(palavra)