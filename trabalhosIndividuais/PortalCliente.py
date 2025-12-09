def apresentacaoProd(produtosNome, produtosPreco):
    print("Lista de Produtos")
    for i in range(0, len(produtosNome) - 1 + 1, 1):
        print(str(i + 1) + "- " + produtosNome[i] + "(" + str(produtosPreco[i]) + " eur/uni)")

def avaliacao():
    print("1- Experiência Boa")
    print("2- Experiência intermédia")
    print("3- Experiência Má")
    ava = int(input())
    
    return ava

def calcTotal(encomendas, produtoPreco):
    total = 0
    for i in range(0, len(encomendas) - 1 + 1, 1):
        total = total + encomendas[i] * produtoPreco[i]
    
    return total

def consultaPed(produtosNome, encomendas, produtosPreco, avaliacoes, t, td, destinos):
    for i in range(0, len(encomendas) - 1 + 1, 1):
        print(produtosNome[i] + " com a quantidade de " + str(encomendas[i]) + " e com o preço de " + str(encomendas[i] * produtosPreco[i]))
    print("---Avalições---")
    for a in range(0, t - 1 + 1, 1):
        print("Avalição " + str(a + 1) + "--> " + str(avaliacoes[a]))
    print("---Destino da Encomenda---")
    for d in range(0, td - 1 + 1, 1):
        print("Destino " + str(d + 1) + ": " + destinos[d])

def consultaStock(produtosNome, produtosQtd, produtosPreco):
    for r in range(0, len(produtosNome) - 1 + 1, 1):
        print(produtosNome[r] + " - " + str(produtosQtd[r]) + " unidades | " + str(produtosPreco[r]) + "eur/uni")

def criacaoPedido(produtosNome, encomendas, produtosPreco):
    repeat = 0
    while True:    #This simulates a Do Loop
        apresentacaoProd(produtosNome, produtosPreco)
        produtoSelecionado = int(input())
        if produtoSelecionado > len(produtosNome) or produtoSelecionado == 0:
            print("Escolha inválida")
        else:
            print("Indique a quantidade")
            qtd = float(input())
            encomendas[produtoSelecionado - 1] = encomendas[produtoSelecionado - 1] + qtd
        print("Quer adicionar mais produtos? " + "Se sim, insere 1")
        repeat = int(input())
        if repeat == 1:
            pass
        else:
            print("Boa escolha")
        if repeat != 1: break

def escolherDestino(destinosOpcao):
    print("Escolha o destino: ")
    print("1 - " + destinosOpcao[0])
    print("2 - " + destinosOpcao[1])
    print("3 - " + destinosOpcao[2])
    escolha = int(input())
    
    return escolha

def menu():
    print("##### Menu Cliente #####")
    print("1 - Lista de produtos")
    print("2 - Fazer pedido de produto")
    print("3 - Consultar lista de produtos encomendados")
    print("4 - Sair")
    option = int(input())
    
    return option

def validacaoStock(produtosNome, produtosQtd, encomendas, produtosPreco, chamadaMenu):
    for i in range(0, len(encomendas) - 1 + 1, 1):
        if encomendas[i] > 0:
            if encomendas[i] > produtosQtd[i]:
                print("Encomendas-te " + produtosNome[i] + "(" + str(encomendas[i]) + "). A quantidade encomendada é superior à quantidade máxima do stock " + str(produtosQtd[i]))
                print("A sua encomenda poderá demorar mais tempo até obter o stock necessário!")
            else:
                produtosQtd[i] = produtosQtd[i] - encomendas[i]
                print(" - " + produtosNome[i] + " com a quantidade de " + str(encomendas[i]) + " e o preço de " + str(encomendas[i] * produtosPreco[i]))

# Main
avaliacoes = [0] * (3)
destinosOpcao = [""] * (3)
destinos = [""] * (3)
produtosNome = [""] * (3)
produtosQtd = [0] * (3)
produtosPreco = [0] * (3)
encomendas = [0] * (3)

destinosOpcao[0] = "Braga"
destinosOpcao[1] = "Fafe"
destinosOpcao[2] = "Guimarães"
produtosNome[0] = "Tintas"
produtosNome[1] = "Parafusos"
produtosNome[2] = "Martelos"
produtosQtd[0] = 10
produtosQtd[1] = 100
produtosQtd[2] = 6
produtosPreco[0] = 11
produtosPreco[1] = 1.6
produtosPreco[2] = 5
chamadaMenu = 0
td = 0
t = 0

# t = indice de Avaliação( 1, 2 ou 3)
print("PORTAL DO CLIENTE")
for i in range(0, len(encomendas) - 1 + 1, 1):
    encomendas[i] = 0
while True:    #This simulates a Do Loop
    opcao = menu()
    if opcao == 1:
        consultaStock(produtosNome, produtosQtd, produtosPreco)
        chamadaMenu = 1
    else:
        if opcao == 2:
            print("Qual o produto que escolhe?")
            criacaoPedido(produtosNome, encomendas, produtosPreco)
            print("Lista de produtos encomendados:")
            validacaoStock(produtosNome, produtosQtd, encomendas, produtosPreco, chamadaMenu)
            print("Indique o destino da encomenda: ")
            escolha = escolherDestino(destinosOpcao)
            destinos[td] = destinosOpcao[escolha - 1]
            td = td + 1
            total = calcTotal(encomendas, produtosPreco)
            print("Obrigado pela a encomenda" + " O total da encomenda é " + str(total) + " eur")
            print("Avalie o seu pedido")
            ava = avaliacao()
            avaliacoes[t] = ava
            t = t + 1
            chamadaMenu = 1
        else:
            if opcao == 3:
                consultaPed(produtosNome, encomendas, produtosPreco, avaliacoes, t, td, destinos)
                chamadaMenu = 1
            else:
                if opcao == 4:
                    chamadaMenu = 0
                else:
                    print("Opção inválida")
                    chamadaMenu = 1
    if chamadaMenu != 1: break
print("Continuação de um ótimo dia")