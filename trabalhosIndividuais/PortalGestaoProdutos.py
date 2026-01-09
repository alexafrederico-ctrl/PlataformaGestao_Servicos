def calcfinal(pedidoprodutoQtd, materialsPrice):
    i = 0
    endcalc = 0
    for i in range(0, len(pedidoprodutoQtd) - 1 + 1, 1):
        endcalc = endcalc + pedidoprodutoQtd[i] * materialsPrice[i]
    
    return endcalc

def materialconsultation(materialsName, materialsPrice, materialsQtd):
    for i in range(0, len(materialsName) - 1 + 1, 1):
        print(materialsName[i] + ": " + str(materialsPrice[i]) + "€ || stock : " + str(materialsQtd[i]))

def menu():
    print("Menu:")
    print("1 - consultar materiais ")
    print("2 - Colocar materias no carrinho ")
    print("3 - Finalização do pedido")
    option = int(input())
    
    return option

def stockupdate(materialsQtd, pedidoprodutoQtd):
    i = 0
    for i in range(0, len(pedidoprodutoQtd) - 1 + 1, 1):
        materialsQtd[i] = materialsQtd[i] - pedidoprodutoQtd[i]

def validstock(materialsQtd, pedidoprodutoQtd, materialsName):
    i = 0
    for i in range(0, len(pedidoprodutoQtd) - 1 + 1, 1):
        if pedidoprodutoQtd[i] > 0:
            if pedidoprodutoQtd[i] > materialsQtd[i]:
                print(" A sua encomenda ultrapassa o  nosso  limite de stock de " + materialsName[i])
            else:
                print("A sua encomenda de " + materialsName[i] + " foi validada com sucesso")

# Main
materialsName = [""] * (10)
materialsQtd = [0] * (10)
materialsPrice = [0] * (10)
orderMaterialPrice = [0] * (10)
pedidoprodutoQtd = [0] * (10)

i = 0
for i in range(0, len(pedidoprodutoQtd) - 1 + 1, 1):
    pedidoprodutoQtd[i] = 0
materialsName[0] = "tintas"
materialsName[2] = "parafusos"
materialsName[1] = "martelo"
materialsName[3] = "pincéis"
materialsName[4] = "vernizes"
materialsName[5] = "nivelador"
materialsName[6] = "lixa"
materialsName[7] = "aparafusador"
materialsName[8] = "fita métrica"
materialsName[9] = "serra"
materialsQtd[0] = 10
materialsQtd[1] = 100
materialsQtd[2] = 6
materialsQtd[3] = 6
materialsQtd[4] = 10
materialsQtd[5] = 7
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
price = 0
menuCall = 0
option = 0
endcalc = 0
while True:    #This simulates a Do Loop
    option = menu()
    if option == 1:
        materialconsultation(materialsName, materialsPrice, materialsQtd)
        menuCall = 1
    else:
        if option == 2:
            while True:    #This simulates a Do Loop
                i = 0
                print("indique o material desejado")
                for i in range(0, len(materialsName) - 1 + 1, 1):
                    print(str(i) + " se desejar " + materialsName[i])
                i = int(input())
                print("Quanta quantidade de " + materialsName[i] + " que deseja?")
                pedidoprodutoQtd[i] = float(input())
                validstock(materialsQtd, pedidoprodutoQtd, materialsName)
                stockupdate(materialsQtd, pedidoprodutoQtd)
                print("Deseja adicionar mais artigos ao carinho? Digite 1 ")
                repeat = int(input())
                calcfinal(materialsPrice, pedidoprodutoQtd)
                if repeat != 1: break
            endcalc = calcfinal(materialsPrice, pedidoprodutoQtd)
            menuCall = 1
        else:
            menuCall = 0
    if menuCall != 1: break
endcalc = calcfinal(materialsPrice, pedidoprodutoQtd)
print(" o  preço do seu carinho é de " + str(endcalc) + "€")
print("O seu pedido encontra-se finalizados, obrigado pelo seu voto de confiança. ")
