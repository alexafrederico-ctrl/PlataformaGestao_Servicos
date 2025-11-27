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
            print("Boa escolha")
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
    print("5 - Sair")
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
            voltar = 0
        else:
            print("Insira um número entre 1-5")
            voltar = 1
        if voltar != 1:
            break
    print("Sistema finalizado com sucesso")

def main():
    produtosNome, produtosQtd, produtosPreco = init_inventario()
    while True:
        print("Escolha o portal:")
        print("1 - Portal Gestor")
        print("2 - Portal Cliente")
        print("3 - Sair")
        escolha = int(input())
        if escolha == 1:
            gestor_main(produtosNome, produtosQtd, produtosPreco)
        elif escolha == 2:
            cliente_main(produtosNome, produtosQtd, produtosPreco)
        elif escolha == 3:
            break
        else:
            print("Escolha inválida")
    print("Aplicação terminada")

if __name__ == '__main__':
    main()
