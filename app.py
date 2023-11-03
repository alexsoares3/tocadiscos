from rich import print
from rich.layout import Layout
from rich.align import Align
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich import box
from rich.console import Group
import keyboard as kb

#cor do programa
tema = {
        "panel_border": "#d600ff",
    }

#User Interface
def draw_ui(layout):   
    
    layout.split(
            Layout(name="header", size=3),
            Layout(
                name="main",
                size=25
            ),
            Layout(name="footer", size=3),
    )
    layout["main"].split_row(
        Layout(name="sidebar", size=20),
        Layout(name="listas", ),
        Layout(name="stats",size=20)
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
    layout["footer"].update(
            Panel(
                Align.center(
                    "[bold][#feff6e]Pre(v) (P)lay/Pause (S)top (N)ext  (R)epeat  (Q)uit (+)Vol (-)Vol [/#feff6e][/bold]"
                ),
                # title="Controls",
                border_style=tema["panel_border"],
            )
    )
    layout["user"].update(
            Panel(
                Align.center(""),
                border_style=tema["panel_border"],
                title="Utilizador",
            )
    )
    layout["menu"].update(
            Panel(
                Align.center("\n\n\n(x) Opcao 1\n(y) Opcao 2\n(z) Opcao 3\n"),
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
    layout["stats"].update(
            Panel(
                Align.center(""),
                border_style=tema["panel_border"],
                title="Estatisticas",
            )
    )  

    return layout

#Input utilizador
def user_controls():
    kb.add_hotkey("x", x)
    kb.add_hotkey("y", y)
    kb.add_hotkey("z", z)
def x():
    print("LETRAx")
    global x
    x=1
def y():
    print("LETRAxy")
def z():
    print("LETRAxz")



#Gerar uma tabela
def listaAutores(layout):
    table = Table(
        show_lines=False,
        box=box.SIMPLE,
        border_style=tema["panel_border"],
    )
    table.add_column("File", justify="left",  no_wrap=False)
    table.add_column("Duration", justify="center", style="green" )
    table.add_column("Duration", justify="right", )

    for x in range(21):
        x=str(x)
        table.add_row(x,x+x,x+x+x)

    return Panel(
        table,
        border_style=tema["panel_border"],
        title="[#feff6e]Lista de Autores",
    )

#Mudar opcoes do menu
def menu1(layout):
    return Panel(
        Align.center("\n\n\n(x) Opcao 1\n(y) Opcao 2\n(z) Opcao 3\n"),
        border_style=tema["panel_border"],
        title="MENU",
    )



#Mostrar UI
def main():
    global x,layout
    x = 0
    layout = Layout()
    layout = draw_ui(layout)
    user_controls()
    with Live(layout, refresh_per_second=2):
        while True:
            layout["menu"].update(menu1(layout))
            layout["listas"].update(listaAutores(layout))
            input()
if __name__ == "__main__":
    main()