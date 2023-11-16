from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich import box
from db2 import *
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
        # Layout(name="indicar",size=30),
        Layout(name="shortcuts")
    )
    layout["main"].split_row(
        Layout(name="sidebar", size=30),
        Layout(name="listas", ),
        Layout(name="stats",size=mainSize)
    )
    layout["sidebar"].split_column(
        Layout(name="menu"),
        Layout(name="user")
    )

    layout["header"].update(
            Panel(
                Align.center("[bold][#feff6e]♪ TOCADISCOS[/#feff6e][/bold]"),
                border_style=tema["panel_border"],
            )
    )
    layout["shortcuts"].update(
            Panel(
                
                Align.left(
                    "[bold][#feff6e]<-- Escrever e depois selecionar opcao                              .(limpar input) t(Voltar ao inicio) q(fechar programa)[/#feff6e][/bold]"
                ), #Pre(v) (P)lay/Pause (S)top (N)ext  (R)epeat  (Q)uit (+)Vol (-)Vol 
                # title="Controls",
                border_style=tema["panel_border"],
            )
    )
    layout["user"].update(
            Panel(
                Align.center("\n\n\nUtilizador: Teste\nTipo: Teste"),
                border_style=tema["panel_border"],
                title="Utilizador",
            )
    )
    layout["menu"].update(menu_inicial(layout))
    layout["listas"].update(
            Panel(
                Align.center(""),
                border_style=tema["panel_border"],
                title="",
            )
    )
    global countArtistas,countAlbuns,countMusicas
    countArtistas,countAlbuns,countMusicas=estatisticas()
    layout["stats"].update(
            Panel(
                Align.center("\n\n\n\n\n\n\nArtistas: "+str(countArtistas)+"\nAlbuns: "+str(countAlbuns)+"\nMusicas: "+str(countMusicas)),
                border_style=tema["panel_border"],
                title="Estatisticas",
            )
    )
    layout["input"].update(
        Panel(Align.left(user_input, vertical='top'), box=box.ROUNDED, title_align='left', title='Input',border_style=tema["panel_border"],)
    )
    # layout["indicar"].update(
    #     Panel(Align.left("", vertical='top'), box=box.ROUNDED,border_style=tema["panel_border"],)
    # )
    return layout
#receber input user
def get_user_input(live, layout, mensagem):
    global user_input
    user_input = ""
    if mensagem is not None:
        mensagem_layout_listas(live,layout,mensagem)
    while True:
        event1 = kb.read_event() 
        if event1.event_type == kb.KEY_DOWN and event1.name == "enter":
            final_input=user_input
            user_input=""
            update_input_panel(live, layout)
            return final_input
        elif event1.event_type == kb.KEY_DOWN and event1.name == "backspace":
            user_input = user_input[:-1]
            update_input_panel(live, layout)
        elif event1.event_type == kb.KEY_DOWN and event1.name != "enter" and len(event1.name) == 1:
            user_input += event1.name
            update_input_panel(live, layout)
def mensagem_layout_listas(live,layout, mensagem):#Escrever as perguntas no layout
    layout["listas"].update(
            Panel(
                Align.center("\n\n"+mensagem),
                border_style=tema["panel_border"],
                title="",
            )
    )
    live.refresh()
    
def mensagem_layout_input(live,layout, mensagem):#Escrever as perguntas no layout
    layout["input"].update(
            Panel(
                Align.center(""),
                border_style=tema["panel_border"],
                title=mensagem,
            )
    )
    live.refresh()
#live input
def update_input_panel(live,layout):
    global live_input
    global user_input
    global menu
    layout["input"].update(
        Panel(Align.left(user_input, vertical='top'), box=box.ROUNDED, title_align='left', title='Input',border_style=tema["panel_border"],)
    )
    live.refresh()
       

    
#Apresentar lista de artistas
def listaArtistas(layout):
    global menu
    global countArtistas
    global mainSize
    lista = lista_artistas()
    table = Table(
        show_lines=False,
        box=box.SIMPLE,
        border_style=tema["panel_border"],
    )
    if lista!="empty":
        #se a lista for maior que 20 aumenta o tamanho do layout para caberem todos os artistas
        #vai ate 52 entradas, depois disso buga o layout
        if countArtistas>20:
            layout["main"].size = mainSize+(countArtistas-mainSize)+5
        table.add_column("ID", justify="center")
        table.add_column("Nome", justify="left",no_wrap=False)
        table.add_column("Nacionalidade", justify="center", style="green" )
        table.add_column("Direitos Editoriais", justify="center", )
        table.add_column("Albuns", justify="center")
        id=0
        for linha in lista:
            if len(linha)<5:
                table.add_row(linha[0],linha[1],linha[2],linha[3])
            else: table.add_row(linha[0],linha[1],linha[2],linha[3],str(int((linha[4].count("|"))+1)))

        layout["menu"].update(menu_lista_artistas(layout))    
        return Panel(
            Align.center(table),
            border_style=tema["panel_border"],
            title="[#feff6e]Lista de Artistas",
        )
    else:
        layout["menu"].update(menu_inicial(layout))
        return Panel(
            Align.center("\n\nAinda nao adicionou nenhum artista!"),
            border_style=tema["panel_border"],
        )

def adicionarArtista(live,layout):
    global user_input
    global live_input
    user_input = ""
    live_input=True
    # First question
    layout["menu"].update(limpar_menu(layout))
    nome=get_user_input(live,layout,"Insira o nome do artista:")
    live.refresh()
    nacionalidade=get_user_input(live,layout,"Insira nacionalidade:")
    live.refresh()
    direitos=get_user_input(live,layout,"Insira os direitos:")
    live.refresh()
    adicionar_artista(nome,nacionalidade,direitos)
    mensagem_layout_listas(live,layout,"Artista adicionado com sucesso!")
    
    

def listaAlbunsPorID(layout,id):
    lista = lista_albuns(id)
    if lista=="empty":
        layout["menu"].update(menu_inicial(layout))
        return Panel(
            Align.center("\n\nEsse artista nao tem albuns ou inseriu um ID invalido!"),
            border_style=tema["panel_border"],
        )
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
    table.add_column("Lista de Musicas", justify="center")
    for linha in lista:
        if len(linha)<=6:
            table.add_row(linha[1],linha[2],linha[3],linha[4],linha[5])
        else: table.add_row(linha[1],linha[2],linha[3],linha[4]+" Un.",linha[5]+" €",str(int((linha[6].count("|"))+1)))
       
    return Panel(
        Align.center(table),
        border_style=tema["panel_border"],
        title="[#feff6e]Lista de Albuns",
    )

#Mudar opcoes do menu
def limpar_menu(layout):
    global menu
    menu="limpar_menu"
    return Panel(
        Align.center(""),
        border_style=tema["panel_border"],
        title="MENU",
    )
def menu_inicial(layout):
    global menu
    menu="menu_inicial"
    return Panel(
        Align.center("\n\n\n(x) Lista de Artistas\n(y) Adicionar Artista\n\n"),
        border_style=tema["panel_border"],
        title="MENU",
    )
def menu_lista_artistas(layout):
    global menu
    menu="menu_lista_artistas"
    if menu!="limpar_menu":
        return Panel(
            Align.center("\n\n\n(x) Mostrar albuns \n    de x artista\n(y) Remover Artista\n"),
            border_style=tema["panel_border"],
            title="MENU",
        )
        



#Mainloop
def main():
    
    global live_input
    live_input=False
    global menu
    global user_input
    user_input=""
    
    layout = Layout()
    layout = draw_ui(layout)
    with Live(layout, auto_refresh=False) as live: 
        while True:
            #live input---------------------------------------------------
            event = kb.read_event()
            #opcoes menu-------------------------------------------------
            if menu=="menu_inicial": #opcoes do menu inicial
                if event.event_type == kb.KEY_DOWN and event.name == 'x': #Lista de Artistas
                    layout["listas"].update(listaArtistas(layout))
                    user_input=""
                    live_input=True  
                    live.refresh()
                    event.name=None
                if event.event_type == kb.KEY_DOWN and event.name == 'y':
                    adicionarArtista(live,layout)

            if menu=="menu_lista_artistas": #opcoes do menu lista de artistas
                
                if event.event_type == kb.KEY_DOWN and event.name == 'x': #mostrar albuns de artista por x ID
                    mensagem_layout_input(live,layout, "Insira o ID:")
                    id=get_user_input(live, layout, None)    
                    layout["listas"].update(listaAlbunsPorID(layout,id))
                    live.refresh()
                    event.name=None
            
            if event.event_type == kb.KEY_DOWN and event.name == 'q': #(q=Fechar)
                break
            if event.event_type == kb.KEY_DOWN and event.name == 't': #(t=pagina inicial)
                user_input = ""
                live_input=False
                menu="menu_inicial"
                draw_ui(layout)
                live.refresh()
            if event.event_type == kb.KEY_DOWN and event.name == '.' and live_input: #limpar imput
                user_input = ""
                update_input_panel(live,layout) 
            #opcoes menu-------------------------------------------------    

                      
if __name__ == "__main__":
    criar_csv_artistas()
    criar_csv_albuns()
    criar_csv_users()
    main()