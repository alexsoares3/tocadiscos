import csv
import os
import difflib


# verifica se o ficheiro existe, caso nao exista cria bd dos artistas com os campos necessario
def criar_csv_artistas():
    if os.path.isfile("db_artistas.csv"):
        pass
    else:
        campos = [
            "ID", 
            "Nome", 
            "Nacionalidade", 
            "Direitos Editoriais", 
            "Albuns"
        ]
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
def criar_pasta_artistas():
    nome_pasta = "artistas"
    # obter caminho da pasta atual
    pasta_atual = os.getcwd()

    # criar caminho completo para a pasta
    caminho_pasta = os.path.join(pasta_atual,nome_pasta)

    # verificar se a pasta existe
    if not os.path.exists(caminho_pasta):
        # criar pasta
        os.makedirs(caminho_pasta)
        
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

    nome_pasta = nome
    # obter caminho da pasta atual
    pasta_atual = os.getcwd()

    # criar caminho completo para a pasta
    caminho_pasta = os.path.join(pasta_atual,"artistas", nome_pasta)

    # verificar se a pasta existe
    if not os.path.exists(caminho_pasta):
        # criar pasta
        os.makedirs(caminho_pasta)

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
    # Read the existing data
    with open("db_artistas.csv", "r", newline="") as file:
        ler_csv = csv.reader(file)
        header = next(ler_csv)  # Save the header
        linhas = list(ler_csv)

    # Identify the index of the line to be removed
    index_a_remover = -1
    for idx, linha in enumerate(linhas):
        if linha and linha[0] == id_artista:
            index_a_remover = idx
            break

    if index_a_remover == -1:
        return "empty"

    # Remove the line
    del linhas[index_a_remover]

    # Write back the modified data
    with open("db_artistas.csv", "w", newline="") as file:
        escrever_csv = csv.writer(file)
        escrever_csv.writerow(header)  # Write back the header
        escrever_csv.writerows(linhas)

    remover_albuns_artista(id_artista)

# remover albuns do artista da db_albuns
def remover_albuns_artista(id_artista):
    linhas_a_remover = []
    header = None  # Variable to store the header

    # Read existing data and find lines to remove
    with open("db_albuns.csv", "r", newline="") as file:
        leitor_csv = csv.reader(file)
        header = next(leitor_csv)  # Save the header
        linhas = list(leitor_csv)

    # Identify the index of the line to be removed
    for idx, linha in enumerate(linhas):
        if linha[0] == id_artista:
            linhas_a_remover.append(idx)

    # Remove lines from the data
    for index in reversed(linhas_a_remover):
        del linhas[index]

    # Write back the modified data
    with open("db_albuns.csv", "w", newline="") as file:
        escritor_csv = csv.writer(file)
        escritor_csv.writerow(header)  # Write back the header
        escritor_csv.writerows(linhas)


def remover_album(id_artista,nome_album):
    # Lista para armazenar os dados do CSV
    dados_csv = []
    existe = False

    # Lê os dados do arquivo CSV e os armazena na lista dados_csv
    with open("db_artistas.csv", 'r') as file:
        ler_csv = csv.DictReader(file)
        next(ler_csv)
        dados_csv = list(ler_csv)  # Populate dados_csv with the data read from the file
    
    # Procura o álbum a ser removido e o remove da lista
    for linha in dados_csv:
        if linha['ID'] == id_artista and nome_album in linha['Albuns']:
            # Remove o álbum da lista
            albuns = linha['Albuns'].split('|')
            albuns.remove(nome_album)
            linha['Albuns'] = '|'.join(albuns)
            existe=True

    # Escreve os dados atualizados de volta no arquivo CSV
    with open("db_artistas.csv", 'w', newline='') as file:
        campos = ['ID', 'Nome', 'Nacionalidade', 'Direitos Editoriais', 'Albuns']
        escrever_csv = csv.DictWriter(file, fieldnames=campos)
        escrever_csv.writeheader()
        escrever_csv.writerows(dados_csv)

    # Lista para armazenar os dados do CSV
    dados_csv1 = []
    # Lê os dados do arquivo CSV e os armazena na lista dados_csv1
    with open("db_albuns.csv", 'r') as file:
        ler_csv = csv.DictReader(file)
        next(ler_csv)
        dados_csv1 = list(ler_csv)  # Populate dados_csv1 with the data read from the file

    # Cria uma nova lista excluindo a linha com o ID_Artista e Nome correspondentes
    dados_csv1 = [linha for linha in dados_csv1 if linha['ID_Artista'] != id_artista or linha['Nome'] != nome_album]

    # Escreve os dados atualizados de volta no arquivo CSV
    with open("db_albuns.csv", 'w', newline='') as file:
        campos = ['ID_Artista', 'Nome', 'Genero Musical', 'Data de Lancamento', 'Unidades Vendidas', 'Preco', 'Lista de Musicas']
        escrever_csv = csv.DictWriter(file, fieldnames=campos)
        escrever_csv.writeheader()
        escrever_csv.writerows(dados_csv1)
    if existe == False:
        return "empty"

#pesquisar por palavras parecidas
def pesquisa(tipo_pesquisa, search):
    resultados = []

    if tipo_pesquisa == "artista":
        with open("db_artistas.csv", "r", newline="") as file:
            ler_csv = csv.reader(file)
            next(ler_csv)
            linhas = list(ler_csv)
        for linha in linhas:
            if linha and len(linha) > 1:
                palavra = linha[1]
                if difflib.SequenceMatcher(None, search, palavra).ratio() > 0.5:
                    resultados.append(linha)

    elif tipo_pesquisa == "album" or tipo_pesquisa == "musica":
        with open("db_albuns.csv", "r", newline="") as file:
            ler_csv = csv.reader(file)
            next(ler_csv)
            linhas = list(ler_csv)

        for linha in linhas:
            if linha and len(linha) > 1:
                if tipo_pesquisa == "album":
                    palavra = linha[1]
                elif tipo_pesquisa == "musica" and len(linha) > 6:
                    palavras = linha[6].split("|")
                    if any(difflib.SequenceMatcher(None, search, palavra).ratio() > 0.5 for palavra in palavras):
                        resultados.append(linha)

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
    direitosAutorais=float(total)*(float(percentagem)/100)
    #finalText = str(direitosAutorais)+"("+str(percentagem)+"%)"
    return str(direitosAutorais)


#devolver lista com todos os albuns de x artista
def lista_albuns(id_artista):
    with open("db_albuns.csv", "r") as file:
        ler_csv = csv.reader(file)
        next(ler_csv) #avanca a primeira linha com o cabecalho
        lista = []
        id_existe = False
        for linha in ler_csv:
            print(linha[0])
            if linha[0]==id_artista:
                id_existe = True
                lista.append(linha)
    if len(lista)==0 and id_existe==False: return "empty"
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

def check_if_exists(id_artista):
     with open("db_artistas.csv", "r") as file:
        ler_csv = csv.reader(file)
        next(ler_csv) #avanca a primeira linha com o cabecalho
        lista = []
        for linha in ler_csv:
            if linha[0]==id_artista:
                return True
        return False


# Testes das funcoes:
criar_csv_artistas()
criar_csv_albuns()
criar_csv_users()
criar_pasta_artistas()


#estatisticas()
#pesquisa("musica", "Mus")
#adicionar_artista("Alex", "Portuguesa", "DireitosArtista")
#adicionar_album("1", "Teste2", "GeneroMusical", "DataLancamento", "1000", "10.99", ["Musica1", "Musica2"])
# atualizar_albuns_artista("7c2eb476-e660-4b45-a179-40e126d5d153", "TESTE")
# remover_artista("ddd5b688-f221-4ae4-bbd5-36429b959392")
# lista_autores()
# lista_albuns("7e8e66b7-ea89-4dad-9bf0-fac7d2005e46")
#criar_user("alex","123")

#for x in range(15):
#    adicionar_artista("Alex", "Portuguesa", "10")