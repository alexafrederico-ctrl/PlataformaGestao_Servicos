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

# Main
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
voltar = 0
print("Bem-vindo, qual o seu nome?")
nome = input()
while True:    #This simulates a Do Loop
    opçoes = mENU()
    if opçoes == 1:
        consultarEncomendas(iD, materiaisRequeridos, materiaisRequeridosQtd, zonasAtendidas)
        print("******************************")
        voltar = 1
    else:
        if opçoes == 2:
            consultarZonas(zonasAtendidas)
            print("******************************")
            voltar = 1
        else:
            if opçoes == 3:
                consultarEstafetas(profissionalZona, profissionalLivre)
                print("******************************")
                voltar = 1
            else:
                if opçoes == 4:
                    encomendasAprovadas()
                    print("******************************")
                    voltar = 1
                else:
                    if opçoes == 5:
                        voltar = 0
                    else:
                        print("Insira um número entre 1-5")
    if voltar != 1: break
print("Sistema finalizado com sucesso")
