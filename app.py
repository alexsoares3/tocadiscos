from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich import box
from db import *
import keyboard as kb


#cor do programa
tema = {"panel_border": "red",}

#global
global menu
menu="menu_inicial"
global user_input
global mainSize
mainSize=25

#User Interface
def draw_ui(layout):   
    
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main",size=25),
        Layout(name="footer", size=3),
    )
    layout["footer"].split_row(
        Layout(name="input",size=30),
        Layout(name="shortcuts")
    )
    layout["main"].split_row(
        Layout(name="sidebar", size=30),
        Layout(name="listas", ),
        Layout(name="stats",size=mainSize)
    )
    layout["sidebar"].split_column(
        Layout(name="menu"),
        Layout(name="indicar",size=5)
    )
    layout["header"].update(
            Panel(
                Align.center("[bold][#feff6e]♪ TOCADISCOS[/#feff6e][/bold]"),
                border_style=tema["panel_border"],
            )
    )
    layout["shortcuts"].update(
            Panel(   
                Align.center(
                    "[bold][#feff6e].(refresh) t(Voltar ao inicio) q(fechar programa)[/#feff6e][/bold]"
                ), #Pre(v) (P)lay/Pause (S)top (N)ext  (R)epeat  (Q)uit (+)Vol (-)Vol 
                # title="Controls",
                border_style=tema["panel_border"],
            )
    )
    layout["indicar"].update(
            Panel(
                Align.center(""),
                border_style=tema["panel_border"],
                title="Indicacoes",
            )
    )
    layout["menu"].update(menu_inicial())
    layout["listas"].update(
            Panel(
                Align.center(""),
                border_style=tema["panel_border"],
                title="",
            )
    )
    
    stats(layout)
    layout["input"].update(
        Panel(Align.left(user_input, vertical='top'), box=box.ROUNDED, title_align='left', title='Input',border_style=tema["panel_border"],)
    )
    
    return layout
def stats(layout):
        countArtistas,countAlbuns,countMusicas=estatisticas()
        layout["stats"].update(
            Panel(
                Align.center("\n\n\n\n\n\n\n\n\nArtistas: "+str(countArtistas)+"\nAlbuns: "+str(countAlbuns)+"\nMusicas: "+str(countMusicas)),
                border_style=tema["panel_border"],
                title="Estatisticas",
            )
        )
#receber input user
def get_user_input(live, layout, mensagem):
    global user_input
    user_input = ""
    if mensagem != None:
        mensagem_layout_indicar(live,layout,mensagem)
    while True:
        event1 = kb.read_event() 
        if event1.event_type == kb.KEY_DOWN and event1.name == "enter": #define o input final quando clica no enter
            final_input=user_input
            user_input=""
            update_input_panel(live, layout)
            mensagem_layout_indicar(live,layout, None)
            live.refresh()
            return final_input
        elif event1.event_type == kb.KEY_DOWN and event1.name == "backspace": #apagar quando clica no backspace
            user_input = user_input[:-1]
            update_input_panel(live, layout)
        elif event1.event_type == kb.KEY_DOWN and event1.name != "enter" and len(event1.name) == 1:  #len == 1 para prevenir inputs como tab e shift
            user_input += event1.name
            update_input_panel(live, layout)

def mensagem_layout_indicar(live,layout, mensagem):#Escrever as perguntas no layout
    if mensagem != None:
        layout["indicar"].update(
                Panel(
                    Align.center(mensagem),
                    border_style=tema["panel_border"],
                    title="Indicacoes",
                )
        )
    else:
        layout["indicar"].update(
                Panel(
                    Align.center(""),
                    border_style=tema["panel_border"],
                    title="Indicacoes",
                )
        )
    live.refresh()
    
#escrever input no painel 
def update_input_panel(live,layout):
    global menu
    layout["input"].update(
        Panel(Align.left(user_input, vertical='top'), box=box.ROUNDED, title_align='left', title='Input',border_style=tema["panel_border"],)
    )
    live.refresh()
          
#Apresentar lista de artistas
def listaArtistas(layout):
    lista = lista_artistas()
    table = Table(
        show_lines=False,
        box=box.SIMPLE,
        border_style=tema["panel_border"],
    )
    if lista!=None:
        #se a lista for maior que 20 aumenta o tamanho do layout para caberem todos os artistas
        #vai ate 52 entradas, depois disso buga o layout
        #if countArtistas>20: layout["main"].size = mainSize+(countArtistas-mainSize)+5

        table.add_column("ID", justify="center")
        table.add_column("Nome", justify="left",no_wrap=False)
        table.add_column("Nacionalidade", justify="center", style="green" )
        table.add_column("Direitos Editoriais", justify="center", )
        table.add_column("Albuns", justify="center")

        for linha in lista:
            if linha[4] == "":
                table.add_row(linha[0],linha[1],linha[2],linha[3]+"€","0")
            elif linha[4] != "" and linha[4].count("|") == 0:
                table.add_row(linha[0],linha[1],linha[2],linha[3]+"€","1")
            else: table.add_row(linha[0],linha[1],linha[2],linha[3]+"€",str(int((linha[4].count("|")))))


        update_menu(layout,menu_lista_artistas())  
        return Panel(
            Align.center(table),
            border_style=tema["panel_border"],
            title="[#feff6e]Lista de Artistas"
        )
    else:
        return Panel(
            Align.center("\n\nAinda nao adicionou nenhum artista!"),
            border_style=tema["panel_border"],
            title="[#feff6e]Lista de Artistas"
        )

def adicionarArtista(live,layout):
    update_menu(layout,limpar_menu())
    nome=get_user_input(live,layout,"Insira o nome do artista:")
    live.refresh()
    nacionalidade=get_user_input(live,layout,"Insira nacionalidade:")
    live.refresh()
    direitos=get_user_input(live,layout,"Insira os direitos: (Valor em percentagem)")
    live.refresh()
    adicionar_artista(nome,nacionalidade,direitos)
    mensagem_layout_indicar(live,layout,"Artista adicionado com sucesso!") 
    update_menu(layout,menu_lista_artistas())
    update_listas(layout,listaArtistas(layout))
    stats(layout)
    live.refresh()

def removerArtista(live,layout):
    update_menu(layout,limpar_menu())
    id_artista=get_user_input(live,layout,"Insira o id do artista\n      a remover")
    live.refresh()
    confirmar=get_user_input(live,layout,"Tem a certeza que quer remover esse artista? (s/n) ID:"+id_artista)
    live.refresh()
    if confirmar.upper() == "S":
        if remover_artista(id_artista) == None:
            mensagem_layout_indicar(live,layout, "Nao existe um artista com o ID "+id_artista)
            update_menu(layout,menu_lista_artistas())
            update_listas(layout,listaArtistas(layout))
            live.refresh()
            return
        remover_artista(id_artista)
        mensagem_layout_indicar(live,layout, "Artista foi removido")
        update_menu(layout,menu_lista_artistas())
        update_listas(layout,listaArtistas(layout))
        stats(layout)
        live.refresh()
    else:
        mensagem_layout_indicar(live,layout, "Artista nao foi removido")
        update_menu(layout,menu_lista_artistas())
        live.refresh()
    

def gerirArtista(layout,id):
    lista = lista_albuns(id)

    table = Table(
        show_lines=False,
        box=box.SIMPLE,
        border_style=tema["panel_border"]
    )
    #Nome,Genero Musical,Data de Lancamento,Unidades Vendidas,Preco,Lista de Musicast
    table.add_column("Nome", justify="center")
    table.add_column("Genero Musical", justify="left",no_wrap=False)
    table.add_column("Data de Lancamento", justify="center" )
    table.add_column("Unidades Vendidas", justify="center", )
    table.add_column("Preco", justify="center")
    table.add_column("Nr de Musicas", justify="center")

    if lista!=None :
        for linha in lista:
            if linha[6] == "":
                countMusicas = "0"
            else:
                musicas = linha[6].split("|")
                print(musicas)
                countMusicas = str(len(musicas))
            table.add_row(linha[1],linha[2],linha[3],linha[4]+" Un.",linha[5]+" €",countMusicas)

    update_menu(layout,limpar_menu())

    return Panel(
        Align.center(table),
        border_style=tema["panel_border"],
        title="[#feff6e]Lista de Albuns",
    )

def adicionarAlbum(live,layout,id_artista):
    update_menu(layout,limpar_menu())
    nome=get_user_input(live,layout, "Insira o Nome do Album: ")
    genero=get_user_input(live,layout, "Insira o Genero Musical: ")
    datalancamento=get_user_input(live,layout, "Insira a Data de Lançamento: ")
    unidades=get_user_input(live,layout, "Insira a Quantidade de Unidades Vendidas: ")
    preco=get_user_input(live,layout, "Insira o Preço: ")
    n=int(get_user_input(live,layout, "Quantas Músicas vai querer Inserir? : "))
    musicas=[]
    for i in range(n):
        nomemusica=get_user_input(live,layout, "Insira o nome da "+str(i+1)+"ª musica: ")
        live.refresh()
        #caminho=get_user_input(live,layout, "Insira o caminho ou arraste o ficheiro (mp3) : ")
        musicas.append(nomemusica)
    #for x in musicas:
    #    shutil.copyfile(x[1], 'artistas/w/destination.txt')
    #    musicas.remove(x[1])
    adicionar_album(id_artista,nome,genero,datalancamento,unidades,preco,musicas)
    mensagem_layout_indicar(live,layout,"Album adicionado com sucesso!") 
    update_listas(layout,gerirArtista(layout,id_artista))
    update_menu(layout,menu_gerir_artista())
    stats(layout)
    live.refresh()

def removerAlbum(live,layout,id_artista):
    update_menu(layout,limpar_menu())
    nome_album=get_user_input(live,layout,"Insira o nome do album\n      a remover")
    live.refresh()
    confirmar=get_user_input(live,layout,"Tem a certeza que quer remover esse album? (s/n) ID:"+nome_album)
    live.refresh()
    if confirmar.upper() == "S":
        if remover_album(id_artista,nome_album) == None:
            mensagem_layout_indicar(live,layout, "Nao existe um album com o nome "+nome_album)
            update_listas(layout,gerirArtista(layout,id_artista))
            update_menu(layout,menu_gerir_artista())
            live.refresh()
            return
        remover_album(id_artista,nome_album)
        mensagem_layout_indicar(live,layout, "Album foi removido")
        update_listas(layout,gerirArtista(layout,id_artista))
        update_menu(layout,menu_gerir_artista())
        stats(layout)
        live.refresh()
    else:
        mensagem_layout_indicar(live,layout, "Album nao foi removido")
        update_menu(layout,menu_lista_artistas())
        live.refresh()

def pesquisar(tipo_pesquisa,search):
    lista = pesquisa(tipo_pesquisa, search)
    if lista == None:
        return None
    table = Table(
        show_lines=False,
        box=box.SIMPLE,
        border_style=tema["panel_border"]
    )
    if tipo_pesquisa == "artista":
        table.add_column("ID", justify="center")
        table.add_column("Nome", justify="left",no_wrap=False)
        table.add_column("Nacionalidade", justify="center", style="green" )
        table.add_column("Direitos Editoriais", justify="center", )
        table.add_column("Albuns", justify="center")
        if lista!=None :
            for linha in lista:
                if linha[4] == "":
                    table.add_row(linha[0],linha[1],linha[2],linha[3]+"€","0")
                elif linha[4] != "" and linha[4].count("|") == 0:
                    table.add_row(linha[0],linha[1],linha[2],linha[3]+"€","1")
                else: table.add_row(linha[0],linha[1],linha[2],linha[3]+"€",str(int((linha[4].count("|")))))
    elif tipo_pesquisa == "album" or tipo_pesquisa == "musica":
        #ID_Artista,Nome,Genero Musical,Data de Lancamento,Unidades Vendidas,Preco,Lista de Musicas
        table.add_column("ID", justify="center")
        table.add_column("Nome", justify="left",no_wrap=False)
        table.add_column("Genero Musical", justify="center", style="green" )
        table.add_column("Data de Lancamento", justify="center", )
        table.add_column("Unidades Vendidas", justify="center")
        table.add_column("Preco", justify="center")
        table.add_column("Lista de Musicas", justify="center")
        if lista!=None :
            for linha in lista:
                table.add_row(linha[0],linha[1],linha[2],linha[3],linha[4],linha[5],linha[6])
    

    return Panel(
        Align.center(table),
        border_style=tema["panel_border"],
        title="[#feff6e]Pesquisa de Artistas",
    )


def update_menu(layout,content):
    layout["menu"].update(content)
def update_listas(layout,content):
    layout["listas"].update(content)

def limpar_listas():
    return Panel(
        Align.center(""),
        border_style=tema["panel_border"],
        title="",
    )
    
def limpar_menu():
    global menu
    menu="limpar_menu"
    return Panel(
        Align.center(""),
        border_style=tema["panel_border"],
        title="MENU",
    )
#Mudar opcoes do menu
def menu_inicial():
    global menu
    menu="menu_inicial"
    return Panel(
        Align.center("\n\n\n(x) Lista de Artistas\n(y) Pesquisar\n(z) Adicionar Artista\n(a) Login\n(b) Registar"),
        border_style=tema["panel_border"],
        title="MENU",
    )
def menu_lista_artistas():
    global menu
    menu="menu_lista_artistas"
    if menu!="limpar_menu":
        return Panel(
            Align.center("\n\n\n(x) Gerir/Mostrar albuns \n    de artista\n(y) Adicionar Artista\n(z) Remover Artista\n"),
            border_style=tema["panel_border"],
            title="MENU",
        )
def menu_gerir_artista():
    global menu
    menu="menu_gerir_artista"
    return Panel(
        Align.center("\n\n\n(x) Gerir Album\n(y) Adicionar Album\n(z) Remover Album\n"),
        border_style=tema["panel_border"],
        title="MENU",
    )
def menu_gerir_album():
    global menu
    menu="menu_gerir_album"
    return Panel(
        Align.center("\n\n\n(x) Adicionar Musica\n(y) Remover Musica\n"),
        border_style=tema["panel_border"],
        title="MENU",
    )
   
def menu_pesquisar():
    global menu
    menu="menu_pesquisar"
    return Panel(
        Align.center("\n\n\n(x) Pesquisar por autor\n(y) Pesquisar por album\n(z) Pesquisar por musica"),
        border_style=tema["panel_border"],
        title="MENU",
    )
       
#Mainloop
def main():
    
    global menu
    global user_input
    
    user_input=""
    
    layout = Layout()
    layout = draw_ui(layout)
    with Live(layout, auto_refresh=False) as live: 
        while True:
            #live input
            event = kb.read_event()
            #opcoes menu-------------------------------------------------
            if menu=="menu_inicial": #opcoes do menu inicial
                if event.event_type == kb.KEY_DOWN and (event.name == 'x' or event.name == 'X'): #Lista de Artistas
                    update_listas(layout,listaArtistas(layout))
                    live.refresh()
                    event.name=None
                if event.event_type == kb.KEY_DOWN and (event.name == 'y' or event.name == 'Y'): #Pesquisar
                    update_menu(layout,menu_pesquisar())
                    live.refresh()
                    event.name=None
                if event.event_type == kb.KEY_DOWN and (event.name == 'z' or event.name == 'Z'): #Adicionar artista
                    adicionarArtista(live,layout)
                    event.name=None
                if event.event_type == kb.KEY_DOWN and (event.name == 'b' or event.name == 'B'): #Registar User
                    user=get_user_input(live,layout, "Insira o nome de utilizador")
                    password=get_user_input(live,layout, "Insira a palavra passe")
                    if check_if_exists_user(user):
                        mensagem_layout_indicar(live,layout, "Ja existe um utilizador com esse nome!")
                    else:
                        criar_user(user,password)
                        mensagem_layout_indicar(live,layout, "Utilizador registado com sucesso!")
                    event.name=None
                if event.event_type == kb.KEY_DOWN and (event.name == 'a' or event.name == 'A'): #Logar User
                    user=get_user_input(live,layout, "Insira o nome de utilizador")
                    password=get_user_input(live,layout, "Insira a palavra passe")
                    if login_user(user,password):
                        mensagem_layout_indicar(live,layout, "Utilizador logado com sucesso!")
                    else: mensagem_layout_indicar(live,layout, "Utilizador ou password incorretos!")
                    event.name=None

            if menu=="menu_lista_artistas": #opcoes do menu lista de artistas       
                if event.event_type == kb.KEY_DOWN and (event.name == 'x' or event.name == 'X'): #gerir x artista
                    mensagem_layout_indicar(live,layout, "Insira o ID do artista")
                    id=get_user_input(live, layout, None) 
                    if check_if_exists_artista(id):   
                        update_listas(layout,gerirArtista(layout,id))
                        update_menu(layout,menu_gerir_artista())
                    else:
                        mensagem_layout_indicar(live,layout, "O ID inserido nao existe")
                        update_menu(layout,menu_lista_artistas())
                    live.refresh()
                    event.name=None

                if event.event_type == kb.KEY_DOWN and (event.name == 'y' or event.name == 'Y'): #Adicionar artista
                    adicionarArtista(live,layout)
                    event.name=None

                if event.event_type == kb.KEY_DOWN and (event.name == 'z' or event.name == 'Z'): #Remover artista
                    removerArtista(live,layout)
                    event.name=None


            if menu=="menu_gerir_artista": #opcoes do menu lista de artistas      
                if event.event_type == kb.KEY_DOWN and (event.name == 'x' or event.name == 'X'): #gerir album
                    event.name=None
                    pass
                if event.event_type == kb.KEY_DOWN and (event.name == 'y' or event.name == 'Y'): #adicionar album
                    event.name=None
                    adicionarAlbum(live,layout,id)
                if event.event_type == kb.KEY_DOWN and (event.name == 'z' or event.name == 'Z'): #remover album
                    event.name=None
                    removerAlbum(live,layout,id)
            

            if menu=="menu_pesquisar": #opcoes do menu lista de artistas 
                if event.event_type == kb.KEY_DOWN and (event.name == 'x' or event.name == 'X'): #pesquisar por artista
                    search=get_user_input(live,layout,"Qual o artista a pesquisar?")
                    if pesquisa("artista",search) != None:
                        update_listas(layout,pesquisar("artista",search))
                        live.refresh()
                    else: 
                        mensagem_layout_indicar(live,layout, "Nenhum resultado encontrado")
                        live.refresh()
                if event.event_type == kb.KEY_DOWN and (event.name == 'y' or event.name == 'Y'): #pesquisar por album
                    search=get_user_input("Qual o album a pesquisar?")
                    if pesquisa("album",search) != None:
                        update_listas(layout,pesquisar("album",search))
                        live.refresh()
                    else: 
                        mensagem_layout_indicar(live,layout, "Nenhum resultado encontrado")
                        live.refresh()
                if event.event_type == kb.KEY_DOWN and (event.name == 'z' or event.name == 'Z'): #pesquisar por musica
                    search=get_user_input(live,layout,"Qual a musica a pesquisar?")
                    if pesquisa("musica",search) != None:
                        update_listas(layout,pesquisar("musica",search))
                        live.refresh()
                    else: 
                        mensagem_layout_indicar(live,layout, "Nenhum resultado encontrado")
                        live.refresh()
            
            if event.event_type == kb.KEY_DOWN and (event.name == 'q' or event.name == 'Q'): #(q=Fechar)
                break
            if event.event_type == kb.KEY_DOWN and (event.name == 't' or event.name == 'T'): #(t=pagina inicial)
                menu="menu_inicial"
                draw_ui(layout)
                live.refresh()
            if event.event_type == kb.KEY_DOWN and event.name == '.': #refresh ao ecra
                live.refresh() 
            #opcoes menu-------------------------------------------------    

                      
if __name__ == "__main__":
    criar_pasta_database()
    criar_csv_artistas()
    criar_csv_albuns()
    criar_csv_users()
    criar_pasta_artistas()
    main()