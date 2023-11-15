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
tema = {
        "panel_border": "red",
    }

#global
global menu
menu=0
global mainSize
mainSize=25
#AUMENTAR TAMANHO DO MAIN SE A LISTA FOR MAIOR QUE X
global user_input

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
                    "[bold][#feff6e]<-- Escrever e depois selecionar opcao                               t(Voltar ao inicio) q(fechar programa)[/#feff6e][/bold]"
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
    layout["menu"].update(
            Panel(
                Align.center("\n\n\n(x) Lista de Artistas\n(y) Pesquisar\n\n"),
                border_style=tema["panel_border"],
                title="MENU",
            )
    )
    layout["listas"].update(
            Panel(
                Align.center(""),
                border_style=tema["panel_border"],
                title="",
            )
    )
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

#Apresentar lista de artistas
def listaArtistas(layout):
    global menu
    lista = lista_artistas()
    table = Table(
        show_lines=False,
        box=box.SIMPLE,
        border_style=tema["panel_border"],
    )
    if lista!="empty":
        table.add_column("ID", justify="center")
        table.add_column("Nome", justify="left",no_wrap=False)
        table.add_column("Nacionalidade", justify="center", style="green" )
        table.add_column("Direitos Editoriais", justify="center", )
        table.add_column("Albuns", justify="center")
        id=0
        for linha in lista:
            id+=1
            #adicionar um ID para trabalhar localmente
            linha.insert(1,str(id))
            if len(linha)<6:
                table.add_row(linha[1],linha[2],linha[3],linha[4])
            else: table.add_row(linha[1],linha[2],linha[3],linha[4],linha[5])

        layout["menu"].update(menu1(layout))    
        return Panel(
            Align.center(table),
            border_style=tema["panel_border"],
            title="[#feff6e]Lista de Artistas",
        )
    else:
        layout["menu"].update(menu0(layout))
        return Panel(
            Align.center("Ainda nao adicionou nenhum artista!"),
            border_style=tema["panel_border"],
        )

def listaAlbunsPorID(layout,id):
    lista = lista_albuns(id)
    if lista=="empty":
        layout["menu"].update(menu0(layout))
        return Panel(
        Align.center("Esse artista nao tem albuns"),
        border_style=tema["panel_border"],
    )
    table = Table(
        show_lines=False,
        box=box.SIMPLE,
        border_style=tema["panel_border"],
    )
    #Nome,Genero Musical,Data de Lancamento,Unidades Vendidas,Preco,Lista de Musicas
    table.add_column("Nome", justify="center")
    table.add_column("Genero Musical", justify="left",no_wrap=False)
    table.add_column("Data de Lancamento", justify="center" )
    table.add_column("Unidades Vendidas", justify="center", )
    table.add_column("Preco", justify="center")
    table.add_column("Lista de Musicas", justify="center")
    for linha in lista:
        if len(linha)<=6:
            table.add_row(linha[1],linha[2],linha[3],linha[4],linha[5])
        else: table.add_row(linha[1],linha[2],linha[3],linha[4],linha[5],linha[6])
       
    return Panel(
        Align.center(table),
        border_style=tema["panel_border"],
        title="[#feff6e]Lista de Albuns",
    )

#Mudar opcoes do menu
def menu0(layout):
    global menu
    menu=0
    return Panel(
        Align.center("\n\n\n(x) Lista de Artistas\n(y) Pesquisar\n\n"),
        border_style=tema["panel_border"],
        title="MENU",
    )
def menu1(layout):
    global menu
    menu=1
    return Panel(
        Align.center("\n\n\n(x) Mostrar albuns \n    de x artista\n(y) Adicionar Artista\n(z) Remover Artista\n"),
        border_style=tema["panel_border"],
        title="MENU",
    )
def menu2(layout):
    global menu
    menu=2
    return Panel(
        Align.center("\n\n\n(x) Opcao 3\n(y) Opcao 2\n(z) Opcao 1\n"),
        border_style=tema["panel_border"],
        title="MENU",
    )

#live input
def update_input_panel(live,layout):
    global live_input
    global user_input
    if live_input:
        layout["input"].update(
            Panel(Align.left(user_input, vertical='top'), box=box.ROUNDED, title_align='left', title='Input',border_style=tema["panel_border"],)
        )
        live.refresh()
    else: pass

#Mostrar UI
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
            event = kb.read_event()
            #live input---------------------------------------------------
            if event.event_type == kb.KEY_DOWN and event.name == "enter":
                user_input = "" 
                update_input_panel(live,layout) 

            elif event.event_type == kb.KEY_DOWN and event.name == "backspace":
                # remover do input quando da backspace
                user_input = user_input[:-1]
                update_input_panel(live,layout) 

            elif event.event_type == kb.KEY_DOWN and event.name != "enter":
                # adicionar a user input quando escreve
                user_input += event.name
                update_input_panel(live,layout) 
            #live input--------------------------------------------------
            #opcoes menu-------------------------------------------------
            if event.event_type == kb.KEY_DOWN and event.name == 'x': #mudar menu/apresentar lista (x=Opcao 1)
                if menu==0:
                    layout["listas"].update(listaArtistas(layout))
                    user_input=""
                    live_input=True  
                    live.refresh()
                elif menu==1:
                    id=user_input[:-1]

                    user_input=""
                    update_input_panel(live,layout) 
                    layout["listas"].update(listaAlbunsPorID(layout,id))
                    live.refresh()
            if event.event_type == kb.KEY_DOWN and event.name == 'y': #menu2 (y=Opcao 2)
                layout["menu"].update(menu2(layout))
            if event.event_type == kb.KEY_DOWN and event.name == 'q': #(q=Fechar)
                break
            if event.event_type == kb.KEY_DOWN and event.name == 't': #(t=pagina inicial)
                user_input = ""
                live_input=False
                #update_input_panel(live,layout) 
                menu=0
                draw_ui(layout)
                live.refresh()
            if event.event_type == kb.KEY_DOWN and event.name == '.':
                user_input = ""
                #update_input_panel(live,layout) 
                #toggle_live_input()
            #opcoes menu-------------------------------------------------    

                      
if __name__ == "__main__":
    criar_csv_artistas()
    criar_csv_albuns()
    criar_csv_users()
    main()