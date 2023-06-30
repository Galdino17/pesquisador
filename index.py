import flet as ft
import os
import json


DEFAULT_FLET_PATH = ''  # or 'ui/path'
DEFAULT_FLET_PORT = 3000

FONEMAS = {' ':' ','α':'a', 'β':'b', 'γ':'g', 'δ':'d', 'ε':'é', 'ζ':'dz', 'η':'ê', 'θ':'th', 'ι':'i', 'κ':'k', 'λ':'l', 'μ':'m', 'ν':'n', 'ξ':'x', 'ο':'o', 'π':'p', 'ρ':'r', 'σ':'s', 'ς':'s', 'τ':'t', 'υ':'ü', 'φ':'f', 'χ':'k', 'ψ':'ps', 'ω':'ó'}

def get_lista_livros():
    with open('livros.json', encoding='utf-8') as file:
        data = json.load(file)
    return data['livros']

LIVROS = get_lista_livros()

def transcrever_fonema(palavra):
	fonema = []
	for caracter in palavra:
		try:
			fonema.append(FONEMAS[caracter])
		except:
			fonema.append(caracter)

	return ''.join(fonema)

def adicionar_chave(meu_dicionario, chave, valor):
    meu_dicionario.setdefault(chave, []).append(valor)
    return meu_dicionario

def e_capitulo(linha):
    return linha[0] !='#'

def e_livro(linha):
    return linha[0] !='#' and linha[0] !=' '

def tem_o_texto(linha, texto_procurado):
    linha = linha.lower()
    if type(texto_procurado) == str:
        return texto_procurado.lower() in linha

    elif type(texto_procurado) == list:
        retorno = 1
        for texto in texto_procurado:
            retorno*= texto.lower() in linha

        return bool(retorno)


    return False
 
def e_NT(linha):
    return 'MATEUS' == linha[:6]

def esse_testamento(atual, procurado):
    return procurado=='Tudo' or procurado is None or atual==procurado

def indexar_referencias(referencias):
    # for referencia in referencias:
    return referencias

def retornar_referencia(referencias, caminho_arquivo):
    if len(referencias)==0:
        return []
    textos = []
    versiculo = referencias.pop(0)
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()
        for linha in linhas:
            if versiculo in linha:
                textos.append(linha)
                try:
                    versiculo = referencias.pop(0)
                except:
                    break

    return textos


def procurar_texto_arquivo(caminho_arquivo, texto_procurado, testamento):

    texto_procurado = texto_procurado.lower().split(' ')

    referencias = []
    testamento_atual = 'AT'

    print(testamento_atual, testamento)
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        linhas = arquivo.readlines()

    for num_linha, linha in enumerate(linhas, start=1):
        if e_livro(linha):
            if e_NT(linha):
                testamento_atual='NT'

        if esse_testamento(testamento_atual, testamento):
            if not e_capitulo(linha) and tem_o_texto(linha, texto_procurado):
                referencia = f'{linha.split(":")[0]}'
                referencias.append(referencia)

    
    return referencias

 

def main(page: ft.Page):

    #textos_para_lista = []
    textos_para_lista = ft.Ref[ft.Text]()
    fonema_txt = ft.Ref[ft.Text]()
    ref_search_text = ft.Ref[ft.TextField]()
    ref_dd_capitulos = ft.Ref[ft.Dropdown]()
    ref_options = ft.Ref[ft.RadioGroup]()
    ref_dd_livros = ft.Ref[ft.Dropdown]()

    def listar_versoes(e=''):
        versoes_list = os.listdir(caminho_biblia.value)
        return [versao.replace('biblia','').replace('.md', '') for versao in versoes_list if not 'txt' in versao]

    def carregar_capitulos(e):
        
        livro = [item for item in LIVROS if item['nome']==e.control.value][0]
        ref_dd_capitulos.current.options = [ft.dropdown.Option(cap+1) for cap in range(livro['capitulos'])]
        ref_search_text.current.value = '#'+livro['sigla']
        listar('')

    def select_capitulo(e):
        ref_search_text.current.value += ref_dd_capitulos.current.value
        listar('')

    def change_testamento(e):
        ref_dd_livros.current.options = [ft.dropdown.Option(livro['nome']) for livro in LIVROS if esse_testamento(livro['testamento'], e.control.value)]
        page.update()

    def crescer_caminho(e):
        e.control.width = page.width*0.6
        page.update()
    
    def diminuir_caminho(e):
        e.control.width = page.width*0.05
        page.update()

    def get_caminho(versao):
        pasta = os.path.join(os.getcwd(), 'biblias')
        return  os.path.join(pasta, versao + '.' + 'md')

    page.title = "Pesquisador na Biblia"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    #page.bgcolor = ft.colors.ON_PRIMARY_CONTAINER
    page.theme_mode = 'DARK'

    cores_texto = ft.colors.TERTIARY

    txt_search = ft.TextField(value="#Mt", width=100, ref=ref_search_text)
    options = ft.RadioGroup(ref=ref_options, content=ft.Row([
              ft.Radio(value="NT", label="NT"),
              ft.Radio(value="AT", label="AT"),
              ft.Radio(value="Tudo", label="Tudo")]), on_change=change_testamento)
    
    caminho_biblia = ft.TextField(value=os.path.join(os.getcwd(), 'biblias') ,
     width=page.width*0.05, on_change=listar_versoes, text_align="right", on_focus=crescer_caminho, on_blur=diminuir_caminho)
    
    dd_livros = ft.Dropdown(options=[ft.dropdown.Option(livro['nome']) for livro in LIVROS], on_change=carregar_capitulos, ref=ref_dd_livros)
    dd_capitulos = ft.Dropdown(ref=ref_dd_capitulos, on_change=select_capitulo)
    

    textos_encontrados = ft.ListView(expand=True)
    textos_encontrados_versao2 = ft.ListView(expand=True)
    textos_referencias = ft.Row(spacing=5, wrap=True, run_spacing=10, height=page.height*0.2, scroll='auto')

    fonema = ft.Text(ref=fonema_txt, selectable=True)

    def texto_clicado(e):
        fonema_txt.current.value = f'{e.control.text} \n {transcrever_fonema(e.control.text)}'
        page.update()
    
    def atualizar_lista(texto):
        if not textos_para_lista.current.value is None:
            lista_local = [item for item in textos_para_lista.current.value]
            textos_versao = retornar_referencia(lista_local, get_caminho(versoes.value))
            versao_selecionada = versoes.value.split("\\biblia")[-1].split('.')[0]

            textos_encontrados.controls = []
            textos_encontrados.controls.append(ft.Text(f"Foram encontrados {len(textos_versao)} textos na versao {versao_selecionada}", color=cores_texto))
 
            if versao_selecionada=='RECEPTUS':
                for referencia in textos_versao:
                    textos_encontrados.controls.append(ft.Text("", selectable=True, color=cores_texto, spans=[ft.TextSpan(referencia, on_click=texto_clicado)]))
            else:
                text_view = ""
                for referencia in textos_versao:
                    text_view = text_view + referencia
                textos_encontrados.controls.append(ft.Text(text_view, selectable=True, color=cores_texto))

            page.update()

    versoes = ft.RadioGroup(content=ft.Row(
        [ft.Radio(value=versao, label=versao) for versao in listar_versoes()],
         scroll='auto', width=page.width*0.45
        ), on_change=atualizar_lista, value='RECEPTUS')
    
    
    
    def atualizar_lista_v2(textos):
        
        if not textos_para_lista.current.value is None:
            lista_local = [item for item in textos_para_lista.current.value]
            textos_versao_2 = retornar_referencia(lista_local, get_caminho(versoes_2.value) )
            versao_selecionada = versoes_2.value.split("\\biblia")[-1].split('.')[0]

            textos_encontrados_versao2.controls = []
            textos_encontrados_versao2.controls.append(ft.Text(f"Referencis correspondentes: {len(textos_versao_2)} na versao {versao_selecionada}", color=cores_texto))

            text_view = ""
            for referencia in textos_versao_2:
                text_view = text_view+ referencia + '\n' 
            
            textos_encontrados_versao2.controls.append(ft.Text(text_view, selectable=True, color=cores_texto))
            page.update()

    versoes_2 = ft.RadioGroup(content=ft.Row(
        [ft.Radio(value=versao, label=versao) for versao in listar_versoes()],
        scroll='auto', width=page.width*0.45
        ), on_change=atualizar_lista_v2)

    def click_button(e):
        texto_do_botao = e.control.text
        texto_local = []
        textos = textos_para_lista[0][0]

        if texto_do_botao=='*':
            atualizar_lista(textos)
        else:
            for texto in textos:
                if texto_do_botao.strip() in texto:
                    texto_local.append(texto)

            atualizar_lista(texto_local)
        page.update()


    def atualizar_grid(textos):
        textos_referencias.controls = []
        textos_referencias.controls.append(ft.ElevatedButton('*', on_click=click_button)) 

        for referencia in textos:
            textos_referencias.controls.append(ft.ElevatedButton(referencia, on_click=click_button)) 
                

    def listar(e):
        caminho_versao = get_caminho(versoes.value)

        textos_para_lista.current.value = procurar_texto_arquivo(caminho_versao, txt_search.value, options.value)
        atualizar_lista('')

        if not versoes_2.value is None:
            atualizar_lista_v2('')

        #atualizar_grid(textos_para_lista[1])

        page.update()

    page.add(
            ft.Column([
                ft.Row([ options, dd_livros, dd_capitulos,   txt_search, ft.IconButton(ft.icons.SEARCH, on_click=listar), 
                
                
                             ]),
                    ft.Row( [  
                        ft.Container(versoes, width=page.width*0.48, height=page.height*0.08),
                        ft.Divider(height=1, color="red"),
                        ft.Container(versoes_2, width=page.width*0.48, height=page.height*0.08)
                    ]),
                    ]),
                ft.Row(
                    [   
                        ft.Container(textos_encontrados, bgcolor=ft.colors.ON_TERTIARY, width=page.width*0.48, height=page.height*0.65),
                        ft.Divider(height=1, color="red"),
                        ft.Container(textos_encontrados_versao2, bgcolor=ft.colors.ON_TERTIARY, width=page.width*0.48, height=page.height*0.65)
                    ]
                    ),
                ft.Text(ref=textos_para_lista, height=1, width=1),
                fonema
                
        )


if __name__ == "__main__":
    ft.app(main)