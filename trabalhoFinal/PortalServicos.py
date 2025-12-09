def consultarEncomendas(iD, materiaisRequeridos, materiaisRequeridosQtd, zonaEncomendas):
    i = 0
    while i <= 2:
        print("As encomendas pendentes são: " + chr(13) + str(iD[i]) + " - O material pedido foi " + materiaisRequeridos[i] + " com a quantidade de " + str(materiaisRequeridosQtd[i]) + ".")
        i = i + 1

def consultarEstafetas(profissionalZona, profissionalLivre):
    i = 0
    while i <= 2:
        if profissionalLivre[i] == True:
            print("O Estafeta " + str(i) + " encontra-se na zona " + profissionalZona[i] + ".")
        i = i + 1

def consultarZonas(zonasAtendidas):
    i = 0
    while i <= 1:
        print("As zonas atendidas são: " + chr(13) + zonasAtendidas[i] + ".")
        i = i + 1

def encomendasAprovadas():
    materialsName = [""] * (10)
    materialsQtd = [0] * (10)
    materialsPrice = [0] * (10)
    orderMaterialQtd = [0] * (5)

    materialsName[0] = "Tintas"
    materialsName[1] = "Parafusos"
    materialsName[2] = "Martelos"
    materialsName[3] = "Pinceis"
    materialsName[4] = "Verniz"
    materialsName[5] = "Nivelador"
    materialsName[6] = "Lixa"
    materialsName[7] = "Aparafusadora"
    materialsName[8] = "Fita-metrica"
    materialsName[9] = "Serra"
    materialsQtd[0] = 10
    materialsQtd[1] = 100
    materialsQtd[2] = 6
    materialsQtd[3] = 10
    materialsQtd[4] = 7
    materialsQtd[5] = 15
    materialsQtd[6] = 150
    materialsQtd[7] = 33
    materialsQtd[8] = 57
    materialsQtd[9] = 0
    materialsPrice[0] = 11
    materialsPrice[1] = 1.6
    materialsPrice[2] = 5
    materialsPrice[3] = 9
    materialsPrice[4] = 14
    materialsPrice[5] = 23
    materialsPrice[6] = 1
    materialsPrice[7] = 55
    materialsPrice[8] = 3
    materialsPrice[9] = 7
    encomendas = [0] * (3)
    iD = [0] * (3)
    zonaEncomendas = [""] * (3)
    estadoEncomenda = [""] * (3)
    materiaisRequeridos = [""] * (3)
    materiaisRequeridosQtd = [0] * (3)
    zonasAtendidas = [""] * (2)
    profissionalZona = [""] * (3)
    profissionalLivre = [False] * (3)

    zonasAtendidas[0] = "Braga"
    zonasAtendidas[1] = "Guimarães"
    iD[0] = 1001
    estadoEncomenda[0] = "Pendente"
    zonaEncomendas[0] = "Braga"
    materiaisRequeridos[0] = "Nivelador"
    materiaisRequeridosQtd[0] = 10
    iD[1] = 1002
    estadoEncomenda[1] = "Pendente"
    zonaEncomendas[1] = "Faro"
    materiaisRequeridos[1] = "Aparafusadora"
    materiaisRequeridosQtd[1] = 2
    iD[2] = 1003
    estadoEncomenda[2] = "Pendente"
    zonaEncomendas[2] = "Guimarães"
    materiaisRequeridos[2] = "Serra"
    materiaisRequeridosQtd[2] = 5
    tamanhoProfissionais = 3
    profissionalZona[0] = "Guimarães"
    profissionalZona[1] = "Guimarães"
    profissionalZona[2] = "Braga"
    profissionalLivre[0] = True
    profissionalLivre[1] = False
    profissionalLivre[2] = True
    i = 0
    tamanhoEncomendas = 3
    while i < tamanhoEncomendas:

        # Testar as zonas
        zona = False
        j = 0
        while j < 2:
            if zonaEncomendas[i] == zonasAtendidas[j]:
                zona = True
            j = j + 1
            stock = False
            p = 0

            # Testar os nomes dos materiais e a quantidade disponível de cada um
            while p < 9 and zona == True:
                if materiaisRequeridos[i] == materialsName[p]:
                    if materiaisRequeridosQtd[i] <= materialsQtd[p]:
                        stock = True
                        p = 1000
                    else:
                        p = 10000
                else:
                    p = p + 1
        if zona == True and stock == True:
            print("Encomenda " + str(iD[i]) + ": APROVADA")
            estadoEncomenda[i] = "Aprovado"
        else:
            print("Encomenda " + str(iD[i]) + ": REJEITADA")
            estadoEncomenda[i] = "Rejeitado"
        i = i + 1
        i = 0
        while i < tamanhoEncomendas:
            if estadoEncomenda[i] == "Aprovado":
                atribuido = False
                k = 0

                # Atribuição de Profissionais/Estafetas
                while k < tamanhoProfissionais and atribuido == False:
                    if zonaEncomendas[i] == profissionalZona[k] and profissionalLivre[k] == True:
                        print("Encomenda " + str(iD[i]) + ": Atribuída ao Profissional " + str(k))
                        estadoEncomenda[i] = "Em Processamento"
                        profissionalLivre[k] = False
                        atribuido = True
                    else:
                        k = k + 1
                if atribuido == False:
                    print("Encomenda " + str(iD[i]) + ": NENHUM Estafeta DISPONÍVEL (Aguardar Atribuição)")
                    estadoEncomenda[i] = "Aguardar Atribuição"
            else:
                i = i + 1
    i = i + 1

def mENU():
    print("*****MENU*****")
    print("1 - Consultar encomendas pendentes")
    print("2 - Consultar zonas atendidas")
    print("3 - Consultar estafetas disponíveis")
    print("4 - Consultar encomendas aprovadas")
    print("5 - Sair")
    opçoes = 0
    opçoes = int(input())
    
    return opçoes
# We'll merge portalCliente into this file and provide a top-level role menu.

def init_inventario():
    # Shared product inventory (uses the larger set from gestor)
    produtosNome = [""] * 10
    produtosQtd = [0] * 10
    produtosPreco = [0] * 10

    produtosNome[0] = "Tintas"
    produtosNome[1] = "Parafusos"
    produtosNome[2] = "Martelos"
    produtosNome[3] = "Pinceis"
    produtosNome[4] = "Verniz"
    produtosNome[5] = "Nivelador"
    produtosNome[6] = "Lixa"
    produtosNome[7] = "Aparafusadora"
    produtosNome[8] = "Fita-metrica"
    produtosNome[9] = "Serra"

    produtosQtd[0] = 10
    produtosQtd[1] = 100
    produtosQtd[2] = 6
    produtosQtd[3] = 10
    produtosQtd[4] = 7
    produtosQtd[5] = 15
    produtosQtd[6] = 150
    produtosQtd[7] = 33
    produtosQtd[8] = 57
    produtosQtd[9] = 0

    produtosPreco[0] = 11
    produtosPreco[1] = 1.6
    produtosPreco[2] = 5
    produtosPreco[3] = 9
    produtosPreco[4] = 14
    produtosPreco[5] = 23
    produtosPreco[6] = 1
    produtosPreco[7] = 55
    produtosPreco[8] = 3
    produtosPreco[9] = 7

    return produtosNome, produtosQtd, produtosPreco

def load_materials_dataframe():
    """
    Load the `materials.csv` file (located next to this script) into a pandas DataFrame.

    Returns:
        pandas.DataFrame or list[dict]: DataFrame when pandas is available, otherwise a list
        of dicts (CSV rows) as a fallback.
    """
    import os
    import csv

    csv_path = os.path.join(os.path.dirname(__file__), 'materials.csv')
    try:
        import pandas as pd
        df = pd.read_csv(csv_path)
        return df
    except ImportError:
        # Fallback: read CSV with csv.DictReader and convert numeric fields
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = []
            for r in reader:
                # Convert Quantity to int
                try:
                    r['Quantity'] = int(r.get('Quantity', 0))
                except Exception:
                    r['Quantity'] = 0
                # Convert Price to float when possible
                try:
                    r['Price'] = float(r.get('Price', 0))
                except Exception:
                    r['Price'] = 0.0
                rows.append(r)
        print("pandas not installed; returning list of dicts. Install pandas with 'pip install pandas' to get a DataFrame.")
        return rows

def load_cliente_pedidos():
    """
    Lê os pedidos salvos pelo PortalCliente (para sincronização)
    """
    try:
        import pandas as pd
        import os
        cliente_path = os.path.join(os.path.dirname(__file__), '..', 'trabalhosIndividuais', 'pedidos.csv')
        if os.path.exists(cliente_path):
            return pd.read_csv(cliente_path)
    except:
        pass
    return None

def load_cliente_eventos():
    """
    Lê os eventos/tracking salvos pelo PortalCliente
    """
    try:
        import pandas as pd
        import os
        cliente_path = os.path.join(os.path.dirname(__file__), '..', 'trabalhosIndividuais', 'eventos_pedido.csv')
        if os.path.exists(cliente_path):
            return pd.read_csv(cliente_path)
    except:
        pass
    return None

def load_cliente_mensagens():
    """
    Lê as mensagens salvos pelo PortalCliente (confirmações/avisos)
    """
    try:
        import pandas as pd
        import os
        cliente_path = os.path.join(os.path.dirname(__file__), '..', 'trabalhosIndividuais', 'mensagens.csv')
        if os.path.exists(cliente_path):
            return pd.read_csv(cliente_path)
    except:
        pass
    return None

# ------------------ Cliente functions (adapted) ------------------
def apresentacaoProd(produtosNome, produtosPreco):
    print("Lista de Produtos")
    for i in range(0, len(produtosNome)):
        print(str(i + 1) + "- " + produtosNome[i] + "(" + str(produtosPreco[i]) + " eur/uni)")

def avaliacao():
    print("1- Experiência Boa")
    print("2- Experiência intermédia")
    print("3- Experiência Má")
    ava = int(input())
    return ava

def calcTotal(encomendas, produtoPreco):
    total = 0
    for i in range(0, len(encomendas)):
        total = total + encomendas[i] * produtoPreco[i]
    return total

def consultaPed(produtosNome, encomendas, produtosPreco, avaliacoes, t, td, destinos):
    for i in range(0, len(encomendas)):
        print(produtosNome[i] + " com a quantidade de " + str(encomendas[i]) + " e com o preço de " + str(encomendas[i] * produtosPreco[i]))
    print("---Avalições---")
    for a in range(0, t):
        print("Avalição " + str(a + 1) + "--> " + str(avaliacoes[a]))
    print("---Destino da Encomenda---")
    for d in range(0, td):
        print("Destino " + str(d + 1) + ": " + destinos[d])

def consultaStock(produtosNome, produtosQtd, produtosPreco):
    for r in range(0, len(produtosNome)):
        print(produtosNome[r] + " - " + str(produtosQtd[r]) + " unidades | " + str(produtosPreco[r]) + "eur/uni")

def criacaoPedido(produtosNome, encomendas, produtosPreco):
    while True:
        apresentacaoProd(produtosNome, produtosPreco)
        produtoSelecionado = int(input())
        if produtoSelecionado > len(produtosNome) or produtoSelecionado == 0:
            print("Escolha inválida")
        else:
            print("Indique a quantidade")
            qtd = float(input())
            encomendas[produtoSelecionado - 1] = encomendas[produtoSelecionado - 1] + qtd
        print("Quer adicionar mais produtos? Se sim, insere 1")
        repeat = int(input())
        if repeat != 1:
            print("Boa escolha!")
            break

def escolherDestino(destinosOpcao):
    print("Escolha o destino: ")
    for i in range(0, len(destinosOpcao)):
        print(str(i+1) + " - " + destinosOpcao[i])
    escolha = int(input())
    return escolha

def cliente_menu():
    print("##### Menu Cliente #####")
    print("1 - Lista de produtos")
    print("2 - Fazer pedido de produto")
    print("3 - Consultar lista de produtos encomendados")
    print("4 - Sair")
    option = int(input())
    return option

def validacaoStock(produtosNome, produtosQtd, encomendas, produtosPreco):
    for i in range(0, len(encomendas)):
        if encomendas[i] > 0:
            if encomendas[i] > produtosQtd[i]:
                print("Encomendas-te " + produtosNome[i] + "(" + str(encomendas[i]) + "). A quantidade encomendada é superior à quantidade máxima do stock " + str(produtosQtd[i]))
                print("A sua encomenda poderá demorar mais tempo até obter o stock necessário!")
            else:
                produtosQtd[i] = produtosQtd[i] - encomendas[i]
                print(" - " + produtosNome[i] + " com a quantidade de " + str(encomendas[i]) + " e o preço de " + str(encomendas[i] * produtosPreco[i]))

# Cliente main (keeps its own state for orders/evaluations)
def cliente_main(produtosNome, produtosQtd, produtosPreco):
    avaliacoes = [0] * 3
    destinosOpcao = [""] * 3
    destinos = [""] * 3
    encomendas = [0] * len(produtosNome)

    destinosOpcao[0] = "Braga"
    destinosOpcao[1] = "Fafe"
    destinosOpcao[2] = "Guimarães"

    chamadaMenu = 0
    td = 0
    t = 0

    print("PORTAL DO CLIENTE")
    while True:
        opcao = cliente_menu()
        if opcao == 1:
            consultaStock(produtosNome, produtosQtd, produtosPreco)
            chamadaMenu = 1
        elif opcao == 2:
            print("Qual o produto que escolhe?")
            criacaoPedido(produtosNome, encomendas, produtosPreco)
            print("Lista de produtos encomendados:")
            validacaoStock(produtosNome, produtosQtd, encomendas, produtosPreco)
            print("Indique o destino da encomenda: ")
            escolha = escolherDestino(destinosOpcao)
            destinos[td] = destinosOpcao[escolha - 1]
            td = td + 1
            total = calcTotal(encomendas, produtosPreco)
            print("Obrigado pela a encomenda" + " O total da encomenda é " + str(total) + " eur")
            print("Avalie o seu pedido")
            ava = avaliacao()
            if t < len(avaliacoes):
                avaliacoes[t] = ava
                t = t + 1
            chamadaMenu = 1
        elif opcao == 3:
            consultaPed(produtosNome, encomendas, produtosPreco, avaliacoes, t, td, destinos)
            chamadaMenu = 1
        elif opcao == 4:
            chamadaMenu = 0
        else:
            print("Opção inválida")
            chamadaMenu = 1
        if chamadaMenu != 1:
            break
    print("Continuação de um ótimo dia")

# ------------------ Gestor functions (adapted to use shared inventory) ------------------
def encomendasAprovadas(produtosNome, produtosQtd, produtosPreco):
    # This function uses a sample set of orders (like original) and the shared inventory.
    encomendas = [0] * 3
    iD = [0] * 3
    zonaEncomendas = [""] * 3
    estadoEncomenda = [""] * 3
    materiaisRequeridos = [""] * 3
    materiaisRequeridosQtd = [0] * 3
    zonasAtendidas = [""] * 2
    profissionalZona = [""] * 3
    profissionalLivre = [False] * 3

    zonasAtendidas[0] = "Braga"
    zonasAtendidas[1] = "Guimarães"
    iD[0] = 1001
    estadoEncomenda[0] = "Pendente"
    zonaEncomendas[0] = "Braga"
    materiaisRequeridos[0] = "Nivelador"
    materiaisRequeridosQtd[0] = 10
    iD[1] = 1002
    estadoEncomenda[1] = "Pendente"
    zonaEncomendas[1] = "Faro"
    materiaisRequeridos[1] = "Aparafusadora"
    materiaisRequeridosQtd[1] = 2
    iD[2] = 1003
    estadoEncomenda[2] = "Pendente"
    zonaEncomendas[2] = "Guimarães"
    materiaisRequeridos[2] = "Serra"
    materiaisRequeridosQtd[2] = 5
    tamanhoProfissionais = 3
    profissionalZona[0] = "Guimarães"
    profissionalZona[1] = "Guimarães"
    profissionalZona[2] = "Braga"
    profissionalLivre[0] = True
    profissionalLivre[1] = False
    profissionalLivre[2] = True

    i = 0
    tamanhoEncomendas = 3

    while i < tamanhoEncomendas:
        zona = False
        j = 0
        while j < len(zonasAtendidas):
            if zonaEncomendas[i] == zonasAtendidas[j]:
                zona = True
            j = j + 1
        stock = False
        p = 0

        while p < len(produtosNome) and zona == True:
            if materiaisRequeridos[i] == produtosNome[p]:
                if materiaisRequeridosQtd[i] <= produtosQtd[p]:
                    stock = True
                    break
                else:
                    break
            p = p + 1

        if zona == True and stock == True:
            print("Encomenda " + str(iD[i]) + ": APROVADA")
            estadoEncomenda[i] = "Aprovado"
        else:
            print("Encomenda " + str(iD[i]) + ": REJEITADA")
            estadoEncomenda[i] = "Rejeitado"
        i = i + 1

    i = 0
    while i < tamanhoEncomendas:
        if estadoEncomenda[i] == "Aprovado":
            atribuido = False
            k = 0
            while k < tamanhoProfissionais and atribuido == False:
                if zonaEncomendas[i] == profissionalZona[k] and profissionalLivre[k] == True:
                    print("Encomenda " + str(iD[i]) + ": Atribuída ao Profissional " + str(k))
                    estadoEncomenda[i] = "Em Processamento"
                    profissionalLivre[k] = False
                    atribuido = True
                else:
                    k = k + 1
            if atribuido == False:
                print("Encomenda " + str(iD[i]) + ": NENHUM Estafeta DISPONÍVEL (Aguardar Atribuição)")
                estadoEncomenda[i] = "Aguardar Atribuição"
        i = i + 1

def gestor_menu():
    print("*****MENU*****")
    print("1 - Consultar encomendas pendentes")
    print("2 - Consultar zonas atendidas")
    print("3 - Consultar estafetas disponíveis")
    print("4 - Consultar encomendas aprovadas")
    print("5 - Consultar pedidos do cliente (CSV)")
    print("6 - Consultar eventos de pedidos (tracking)")
    print("7 - Consultar mensagens (confirmações/avisos)")
    print("8 - Sair")
    opcoes = int(input())
    return opcoes

def consultarEncomendas(iD, materiaisRequeridos, materiaisRequeridosQtd, zonaEncomendas, zonasAtendidas):
    i = 0
    while i < len(iD):
        print("As encomendas pendentes são: " + chr(13) + str(iD[i]) + " - O material pedido foi " + materiaisRequeridos[i] + " com a quantidade de " + str(materiaisRequeridosQtd[i]) + ".")
        i = i + 1

def consultarEstafetas(profissionalZona, profissionalLivre):
    i = 0
    while i < len(profissionalZona):
        if profissionalLivre[i] == True:
            print("O Estafeta " + str(i) + " encontra-se na zona " + profissionalZona[i] + ".")
        i = i + 1

def consultarZonas(zonasAtendidas):
    i = 0
    while i < len(zonasAtendidas):
        print("As zonas atendidas são: " + chr(13) + zonasAtendidas[i] + ".")
        i = i + 1

def gestor_main(produtosNome, produtosQtd, produtosPreco):
    # Local gestor state (sample orders/professionals)
    zonasAtendidas = ["Braga", "Guimarães"]
    iD = [1001, 1002, 1003]
    estadoEncomenda = ["Pendente"] * 3
    zonaEncomendas = ["Braga", "Faro", "Guimarães"]
    materiaisRequeridos = ["Nivelador", "Aparafusadora", "Serra"]
    materiaisRequeridosQtd = [10, 2, 5]
    profissionalZona = ["Guimarães", "Guimarães", "Braga"]
    profissionalLivre = [True, False, True]

    print("Bem-vindo, qual o seu nome?")
    nome = input()
    while True:
        opcoes = gestor_menu()
        if opcoes == 1:
            consultarEncomendas(iD, materiaisRequeridos, materiaisRequeridosQtd, zonaEncomendas, zonasAtendidas)
            print("******************************")
            voltar = 1
        elif opcoes == 2:
            consultarZonas(zonasAtendidas)
            print("******************************")
            voltar = 1
        elif opcoes == 3:
            consultarEstafetas(profissionalZona, profissionalLivre)
            print("******************************")
            voltar = 1
        elif opcoes == 4:
            encomendasAprovadas(produtosNome, produtosQtd, produtosPreco)
            print("******************************")
            voltar = 1
        elif opcoes == 5:
            # Carregar e exibir pedidos do cliente
            df_pedidos = load_cliente_pedidos()
            if df_pedidos is not None and not df_pedidos.empty:
                print("\n=== PEDIDOS DO CLIENTE ===")
                print(df_pedidos.to_string(index=False))
            else:
                print("Nenhum pedido do cliente encontrado.")
            print("******************************")
            voltar = 1
        elif opcoes == 6:
            # Carregar e exibir eventos de pedidos
            df_eventos = load_cliente_eventos()
            if df_eventos is not None and not df_eventos.empty:
                print("\n=== EVENTOS DE PEDIDOS (TRACKING) ===")
                print(df_eventos.to_string(index=False))
            else:
                print("Nenhum evento de pedido encontrado.")
            print("******************************")
            voltar = 1
        elif opcoes == 7:
            # Carregar e exibir mensagens
            df_mensagens = load_cliente_mensagens()
            if df_mensagens is not None and not df_mensagens.empty:
                print("\n=== MENSAGENS (CONFIRMAÇÕES/AVISOS) ===")
                print(df_mensagens.to_string(index=False))
            else:
                print("Nenhuma mensagem encontrada.")
            print("******************************")
            voltar = 1
        elif opcoes == 8:
            voltar = 0
        else:
            print("Insira um número entre 1-8")
            voltar = 1
        if voltar != 1:
            break
    print("Sistema finalizado com sucesso")


# ------------------ Estafeta functions (imported/adapted from PortalEstafeta) ------------------
def aceitarRecusar(tarefas, anomalia, timestamps, estado, estadoAtual, contadorSucesso, contadorTarefas):
    var_return = 0
    print("Existem as seguintes encomendas atribuídas com os IDs no ínicio e contacto no final:")
    for i in range(0, len(tarefas)):
        print(str(1 + i) + ") " + tarefas[i])
    while True:    #This simulates a Do Loop
        print("Qual o ID da encomenda que pretende aceitar ou trocar de estado?(No caso de querer recusar digite outro número qualquer)")
        idTarefa = int(input())
        if 1 <= idTarefa <= len(tarefas):
            print("Qual operação pretende executar:" + chr(13) + "1-Aceitar atribuição;" + chr(13) + "2- Trocar estado operacional da encomenda;")
            x = int(input())
            if x == 1:
                print("O estado da sua tarefa está em recolha.")
                estadoAtual[idTarefa - 1] = estado[0]
                contadorTarefas[idTarefa - 1] = 1
            else:
                if x == 2:
                    print("Digite para que estado pretende alterar a tarefa escolhida:")
                    for i in range(0, len(estado)):
                        print(str(i + 1) + ")" + estado[i])
                    x = int(input())
                    estadoAtual[idTarefa - 1] = estado[x - 1]
                    print("A encomenda passou ao estado: " + estadoAtual[idTarefa - 1])
                    if estadoAtual[idTarefa - 1] == "Concluído.":
                        contadorSucesso[idTarefa - 1] = contadorSucesso[idTarefa - 1] + 1
                    else:
                        contadorSucesso[idTarefa - 1] = float(contadorSucesso[idTarefa - 1]) / 2
                        contadorTarefas[idTarefa - 1] = 1
        else:
            print("Qual tarefa pretende recusar?")
            idTarefa = int(input())
            print("Qual o motivo para recusar a encomenda?")
            for i in range(0, len(anomalia)):
                print(str(i + 1) + ")" + anomalia[i])
            motivo = int(input())
            print("Introduza a data e hora no formato DD/MM/AAAA HH:MM.")
            timestamp = input()
            print("O motivo pela qual a encomenda não vai ser entregue é o seguinte: " + anomalia[motivo - 1] + " E a data e hora que o estafeta relatou a anomalia foi: " + timestamp)
            timestamps[idTarefa - 1] = timestamp
        print("Se pretender aceitar/ recusar/ trocar de estado alguma outra encomenda, digite 1.")
        var_return = int(input())
        if var_return != 1: break

def tarefasAtribuidas(tarefas):
    print("---Lista de tarefas atribuídas---")
    for i in range(0, len(tarefas)):
        print(str(i + 1) + ") " + tarefas[i])

def estafeta_menu():
    print("----MENU ESTAFETA----")
    print("1) Lista de tarefas atribuídas;")
    print("2) Aceitar e recusar atribuição e trocar estado operacional de encomenda;")
    print("3) Registar localização;")
    print("4) Reportar anomalias;")
    print("5) Consultar dados pessoais;")
    print("6) Sair;")
    opcao = int(input())
    return opcao

def estafeta_main():
    contadorTarefas = [0] * 4
    contadorSucesso = [0] * 4
    timestamps = [""] * 4
    anomalia = [""] * 5
    estadoAtual = [""] * 4
    localizacao = [""] * 4
    tarefas = [""] * 4
    estado = [""] * 4

    anomalia[0] = "Endereço incorreto."
    anomalia[1] = "Cliente ausente."
    anomalia[2] = "Avaria no veículo."
    anomalia[3] = "Condições metereológicas adversas."
    anomalia[4] = "Produto danificado."
    tarefas[0] = "Lisboa, Porto, 966607184"
    tarefas[1] = "Guimarães, Fafe, 93456064"
    tarefas[2] = "Bragança, Alentejo, 92349599"
    tarefas[3] = "Póvoa de Varzim, guimarães, 912345678"
    estado[0] = "Em recolha."
    estado[1] = "Em distribuição."
    estado[2] = "Concluído."
    estado[3] = "Falhado."
    menuCall = 0
    repeat = 0
    print("Seja bem vindo ao portal do estafeta, qual o seu nome?")
    nome = input()
    print("O que o/a " + nome + " deseja fazer?")
    for i in range(0, len(contadorTarefas)):
        contadorTarefas[i] = 0
    for i in range(0, len(contadorSucesso)):
        contadorSucesso[i] = 0
    idTarefa = 0
    while True:    #This simulates a Do Loop
        opcao = estafeta_menu()
        if opcao == 1:
            tarefasAtribuidas(tarefas)
            menuCall = 1
        else:
            if opcao == 2:
                aceitarRecusar(tarefas, anomalia, timestamps, estado, estadoAtual, contadorSucesso, contadorTarefas)
                print("Deseja fazer mais alguma operação? Se sim digite 1.")
                menuCall = int(input())
            else:
                if opcao == 3:
                    print("Qual o ID da tarefa que está a realizar?")
                    tarefasAtribuidas(tarefas)
                    idTarefa = int(input())
                    print("Qual a sua localização atual.")
                    loc = input()
                    print("A sua localização foi registada: " + loc)
                    tarefas[idTarefa - 1] = loc
                    print("Deseja fazer mais alguma operação? Se sim digite 1.")
                    menuCall = int(input())
                else:
                    if opcao == 4:
                        print("Qual o ID da sua tarefa?")
                        tarefasAtribuidas(tarefas)
                        idTarefa = int(input())
                        print("Qual o motivo da anomalia?")
                        textoLivre = input()
                        print("Deseja realizar mais alguma operação? Se sim digite 1.")
                        menuCall = int(input())
                    else:
                        if opcao == 5:
                            print("Qual o ID da sua tarefa?")
                            idTarefa = int(input())
                            contadorSucesso[idTarefa - 1] = float(contadorTarefas[idTarefa - 1]) / 2 * 100
                            print("Tarefas realizadas: " + str(contadorTarefas[idTarefa - 1]))
                            print("Taxa de sucesso: " + str(contadorSucesso[idTarefa - 1]) + "%")
                        else:
                            menuCall = 0
        if menuCall != 1: break
    print("Obrigado por trabalhar connosco!")


# ------------------ Portal Gestão de Produtos (adaptado de PortalGestaoProdutos) ------------------
def calcfinal_prod(pedidoprodutoQtd, materialsPrice):
    endcalc = 0
    for i in range(0, len(pedidoprodutoQtd)):
        endcalc = endcalc + pedidoprodutoQtd[i] * materialsPrice[i]
    return endcalc

def materialconsultation_prod(materialsName, materialsPrice, materialsQtd):
    for i in range(0, len(materialsName)):
        print(materialsName[i] + ": " + str(materialsPrice[i]) + "€ || stock : " + str(materialsQtd[i]))

def gestao_produtos_menu():
    print("Menu Gestão de Produtos:")
    print("1 - Consultar materiais")
    print("2 - Colocar materiais no carrinho")
    print("3 - Finalização do pedido")
    print("4 - Sair")
    option = int(input())
    return option

def stockupdate_prod(materialsQtd, pedidoprodutoQtd):
    for i in range(0, len(pedidoprodutoQtd)):
        materialsQtd[i] = materialsQtd[i] - pedidoprodutoQtd[i]

def validstock_prod(materialsQtd, pedidoprodutoQtd, materialsName):
    for i in range(0, len(pedidoprodutoQtd)):
        if pedidoprodutoQtd[i] > 0:
            if pedidoprodutoQtd[i] > materialsQtd[i]:
                print("A sua encomenda ultrapassa o nosso limite de stock de " + materialsName[i])
            else:
                print("A sua encomenda de " + materialsName[i] + " foi validada com sucesso")

def gestao_produtos_main():
    materialsName = [""] * 10
    materialsQtd = [0] * 10
    materialsPrice = [0] * 10
    pedidoprodutoQtd = [0] * 10

    for i in range(0, len(pedidoprodutoQtd)):
        pedidoprodutoQtd[i] = 0

    materialsName[0] = "Tintas"
    materialsName[1] = "Martelo"
    materialsName[2] = "Parafusos"
    materialsName[3] = "Pincéis"
    materialsName[4] = "Verniz"
    materialsName[5] = "Nivelador"
    materialsName[6] = "Lixa"
    materialsName[7] = "Aparafusador"
    materialsName[8] = "Fita métrica"
    materialsName[9] = "Serra"

    materialsQtd[0] = 10
    materialsQtd[1] = 100
    materialsQtd[2] = 6
    materialsQtd[3] = 6
    materialsQtd[4] = 10
    materialsQtd[5] = 15
    materialsQtd[6] = 150
    materialsQtd[7] = 3
    materialsQtd[8] = 57
    materialsQtd[9] = 5

    materialsPrice[0] = 11
    materialsPrice[1] = 1.6
    materialsPrice[2] = 5
    materialsPrice[3] = 9
    materialsPrice[4] = 14
    materialsPrice[5] = 23
    materialsPrice[6] = 1
    materialsPrice[7] = 55
    materialsPrice[8] = 3
    materialsPrice[9] = 7

    repeat = 0
    endcalc = 0
    menuCall = 0

    while True:
        option = gestao_produtos_menu()
        if option == 1:
            materialconsultation_prod(materialsName, materialsPrice, materialsQtd)
            menuCall = 1
        elif option == 2:
            while True:
                print("Indique o material desejado (número):")
                for i in range(0, len(materialsName)):
                    print(str(i) + " - " + materialsName[i])
                i = int(input())
                print("Que quantidade de " + materialsName[i] + " deseja?")
                pedidoprodutoQtd[i] = float(input())
                validstock_prod(materialsQtd, pedidoprodutoQtd, materialsName)
                stockupdate_prod(materialsQtd, pedidoprodutoQtd)
                print("Deseja adicionar mais artigos ao carrinho? Digite 1 para sim")
                repeat = int(input())
                if repeat != 1:
                    break
            endcalc = calcfinal_prod(pedidoprodutoQtd, materialsPrice)
            menuCall = 1
        elif option == 3:
            endcalc = calcfinal_prod(pedidoprodutoQtd, materialsPrice)
            print("O preço do seu carrinho é de " + str(endcalc) + "€")
            print("O seu pedido encontra-se finalizado, obrigado pelo seu voto de confiança.")
            menuCall = 0
        elif option == 4:
            menuCall = 0
        else:
            print("Opção inválida")
            menuCall = 1

        if menuCall != 1:
            break


def main():
    produtosNome, produtosQtd, produtosPreco = init_inventario()
    while True:
        print("Escolha o portal:")
        print("1 - Portal Gestor")
        print("2 - Portal Cliente")
        print("3 - Portal Estafeta")
        print("4 - Portal Gestão Produtos")
        print("5 - Sair")
        escolha = int(input())
        if escolha == 1:
            gestor_main(produtosNome, produtosQtd, produtosPreco)
        elif escolha == 2:
            cliente_main(produtosNome, produtosQtd, produtosPreco)
        elif escolha == 3:
            estafeta_main()
        elif escolha == 4:
            gestao_produtos_main()
        elif escolha == 5:
            break
        else:
            print("Escolha inválida")
    print("Aplicação terminada")

if __name__ == '__main__':
    main()
