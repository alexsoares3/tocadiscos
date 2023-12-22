import csv
import os
import difflib
import pygame


# verifica se o ficheiro existe, caso nao exista cria bd dos artistas com os campos necessario
def criar_csv_artistas():
    if os.path.isfile("db_artistas.csv"):
        pass
    else:
        campos = ["ID", "Nome", "Nacionalidade", "Direitos Editoriais", "Albuns"]
        with open("db_artistas.csv", "w", newline="") as file:
            escrever_csv = csv.writer(file, delimiter=",")
            escrever_csv.writerow(campos)


# verifica se o ficheiro existe, caso nao exista cria bd de albuns com os campos necessario
def criar_csv_albuns():
    if os.path.isfile("db_albuns.csv"):
        pass
    else:
        campos = [
            "ID_Artista",
            "Nome",
            "Genero Musical",
            "Data de Lancamento",
            "Unidades Vendidas",
            "Preco",
            "Lista de Musicas",
        ]
        with open("db_albuns.csv", "w", newline="") as file:
            escrever_csv = csv.writer(file, delimiter=",")
            escrever_csv.writerow(campos)

# verifica se o ficheiro existe, caso nao exista cria bd dos users com os campos necessario
def criar_csv_users():
    if os.path.isfile("db_users.csv"):
        pass
    else:
        campos = ["user", "password"]
        with open("db_users.csv", "w", newline="") as file:
            escrever_csv = csv.writer(file, delimiter=",")
            escrever_csv.writerow(campos)
        
# adicionar artista a db de artistas
def adicionar_artista(nome, nacionalidade, direitos_editoriais):  
    with open("db_artistas.csv", 'r', newline="",) as arquivo_csv:
        
        ler_csv = csv.reader(arquivo_csv)
        # avanca a primeira linha com o cabecalho
        next(ler_csv)
        #ID que o primeiro artista vai ter
        id_artista = 1 
        # Itera sobre as linhas para encontrar o ultimo ID, se nao encontrar id na primeira linha, define como 1
        for linha in ler_csv:
            if linha==[]:
                break
            else:
                ultimo_id = linha[0] 
                id_artista = int(ultimo_id)+1
            
    campos = [
        id_artista,
        nome,
        nacionalidade,
        direitos_editoriais,
    ]
    with open("db_artistas.csv", "a", newline="") as file:
        escrever_csv = csv.writer(file, delimiter=",")
        escrever_csv.writerow(campos)

# adicionar album a db de albuns
def adicionar_album(id_artista, nome, genero_musical, data_lancamento, unidades_vendidas, preco, musicas):
    lista_musicas = "|".join(musicas)
    campos = [
        id_artista,
        nome,
        genero_musical,
        data_lancamento,
        unidades_vendidas,
        preco,
        lista_musicas,
    ]
    with open("db_albuns.csv", "a", newline="") as file:
        escrever_csv = csv.writer(file, delimiter=",")
        escrever_csv.writerow(campos)
    atualizar_albuns_artista(id_artista, nome)

# ao adicionar album na bd de albums, associa tambem o nome do album ao artista na bd de artistas 
def atualizar_albuns_artista(id_artista, nomeAlbum):
    with open("db_artistas.csv", "r", newline="") as file:
        ler_csv = csv.reader(file, delimiter=",")
        linhas = list(ler_csv)
    for linha in linhas:
        if linha[0] == id_artista:
            if len(linha) < 5:
                linha.append(nomeAlbum)
            else:
                linha[-1] += "|" + nomeAlbum

    with open("db_artistas.csv", "w", newline="") as file:
        escrever_csv = csv.writer(file, delimiter=",")
        escrever_csv.writerows(linhas)


# remover artista da db_artistas
def remover_artista(id_artista):
    with open("db_artistas.csv", "r", newline="") as file:
        ler_csv = csv.reader(file)
        linhas = list(ler_csv)
    countLinhas = -1
    for linha in linhas:
        countLinhas +=1
        if linha[0] == id_artista:
            del linhas[countLinhas]

        with open("db_artistas.csv", "w", newline="") as file:
            escrever_csv = csv.writer(file)
            escrever_csv.writerows(linhas)
    remover_albuns_artista(id_artista)


# remover albuns do artista da db_albuns
def remover_albuns_artista(id_artista):
    linhas_a_remover = []
    with open("db_albuns.csv", "r", newline="") as file:
        ler_csv = csv.reader(file)
        linhas = list(ler_csv)
    countLinhas = -1
    for linha in linhas:
        countLinhas += 1
        if linha[0] == id_artista:
            linhas_a_remover.append(countLinhas)
    for index in reversed(linhas_a_remover):
        del linhas[index]

    with open("db_albuns.csv", "w", newline="") as file:
        escrever_csv = csv.writer(file)
        escrever_csv.writerows(linhas)

#pesquisar por palavras parecidas
def pesquisa(tipo_pesquisa, search):
    resultados = []

    if tipo_pesquisa == "artista":
        with open("db_artistas.csv", "r", newline="") as file:
            ler_csv = csv.reader(file)
            linhas = list(ler_csv)
        lista_palavras = [linha[1] for linha in linhas]
        closest_matches = difflib.get_close_matches(
            search, lista_palavras, n=10, cutoff=0.5
        )
        resultados = closest_matches

    elif tipo_pesquisa == "album" or tipo_pesquisa == "musica":
        with open("db_albuns.csv", "r", newline="") as file:
            ler_csv = csv.reader(file)
            linhas = list(ler_csv)

        if tipo_pesquisa == "album":
            lista_palavras = [linha[1] for linha in linhas]
            print(lista_palavras)
            closest_matches = difflib.get_close_matches(
                search, lista_palavras, n=15, cutoff=0.5
            )
            resultados = closest_matches

        elif tipo_pesquisa == "musica":
            lista_palavras = [
                coluna for linha in linhas for coluna in linha[6].split("|")
            ]
            print(lista_palavras)
            closest_matches = difflib.get_close_matches(
                search, lista_palavras, n=20, cutoff=0.5
            )

            resultados = closest_matches
    return resultados

#devolver lista com todos os artistas
def lista_artistas():
    with open("db_artistas.csv", "r") as file:
        ler_csv = csv.reader(file)
        next(ler_csv) #avanca a primeira linha com o cabecalho
        lista = []
        for linha in ler_csv:
            linha[3]=calculoDireitosAutorais(linha[0],linha[3])
            lista.append(linha)
    if len(lista)==0:
        lista="empty"
        return lista
    else: return lista

def calculoDireitosAutorais(idArtista,percentagem):
    #Ir buscar nrAlbuns vendidos, preco
    total=0
    with open("db_albuns.csv", "r") as file:
        ler_csv = csv.reader(file)
        next(ler_csv) #avanca a primeira linha com o cabecalho
        for linha in ler_csv:
            if linha[0]==str(idArtista):
                total+=float(linha[4])*float(linha[5])
    direitosAutorais=float(total)*float(percentagem)
    print(str(direitosAutorais))
    return str(direitosAutorais)


#devolver lista com todos os albuns de x artista
def lista_albuns(id_artista):
    with open("db_albuns.csv", "r") as file:
        ler_csv = csv.reader(file)
        next(ler_csv) #avanca a primeira linha com o cabecalho
        lista = []
        for linha in ler_csv:
            if linha[0]==id_artista:
                lista.append(linha)
    if len(lista)==0: return "empty"
    else: return lista

def criar_user(user,password):
    with open("db_users.csv", "r") as file:
        ler_csv = csv.reader(file)
        next(ler_csv) #avanca a primeira linha com o cabecalho
        #verificar se existe algum user com o mesmo nome
        for linha in ler_csv:
            if linha[0]==user:
                return print("Ja existe um utilizador com esse nome!")
    campos = [user,password]
    with open("db_users.csv", "a", newline="") as file:
        escrever_csv = csv.writer(file, delimiter=",")
        escrever_csv.writerow(campos)

def estatisticas():
    countArtistas=0
    countAlbuns=0
    countMusicas=0
    with open("db_artistas.csv", "r") as file:
        ler_csv = csv.reader(file)
        next(ler_csv) #avanca a primeira linha com o cabecalho
        for linha in ler_csv:
            if len(linha)==0: break
            countArtistas+=1
    with open("db_albuns.csv", "r") as file1:
        ler_csv1 = csv.reader(file1)
        next(ler_csv1)
        for linha in ler_csv1:
            if len(linha)==0: break
            countAlbuns+=1
            if len(linha)>6:
                musicas = linha[6].split("|")
                countMusicas += len(musicas)
    return countArtistas,countAlbuns,countMusicas 

#tocar a musica
def tocar_musica():
    #vai buscar a musica à base de dados
    ficheiro = open('db_musica.csv', 'rb')
    reader = csv.reader(ficheiro)
    for linha in reader:
        musica = linha;
    #inicio do modulo
    pygame.init()
    # caminho para a musica
    pasta_musica = "musicas"
    # variavel que faz o caminho completo da musica
    dar_play = [os.path.join(pasta_musica, musica)]
    # inicia o mixer do pygame
    pygame.mixer.init()
    # carrega a musica no pygame
    pygame.mixer.music.load(dar_play)
    # inicia a reprodução da musica
    pygame.mixer.music.play()
    # faz com que a musica toque até ao fim
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

# Testes das funcoes:
criar_csv_artistas()
criar_csv_albuns()
criar_csv_users()
#estatisticas()
# pesquisa("musica", "Mus")
#adicionar_artista("Alex", "Portuguesa", "DireitosArtista")
#adicionar_album("1", "Teste2", "GeneroMusical", "DataLancamento", "1000", "10.99", ["Musica1", "Musica2"])
# atualizar_albuns_artista("7c2eb476-e660-4b45-a179-40e126d5d153", "TESTE")
# remover_artista("ddd5b688-f221-4ae4-bbd5-36429b959392")
# lista_autores()
# lista_albuns("7e8e66b7-ea89-4dad-9bf0-fac7d2005e46")
#criar_user("alex","123")

#for x in range(20):
#    adicionar_artista("Alex", "Portuguesa", "DireitosArtista")