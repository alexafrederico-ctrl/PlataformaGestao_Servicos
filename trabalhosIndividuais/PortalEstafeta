def aceitarRecusar(tarefas, anomalia, timestamps, estado, estadoAtual, contadorSucesso, contadorTarefas):
    var_return = 0
    print("Existem as seguintes encomendas atribuídas com os IDs no ínicio e contacto no final:")
    for i in range(0, len(tarefas) - 1 + 1, 1):
        print(str(1 + i) + ") " + tarefas[i])
    while True:    #This simulates a Do Loop
        print("Qual o ID da encomenda que pretende aceitar ou trocar de estado?(No caso de querer recusar digite outro número qualquer)")
        idTarefa = int(input())
        if idTarefa == 1 or idTarefa == 2 or idTarefa == 3 or idTarefa == 4:
            print("Qual operação pretende executar:" + chr(13) + "1-Aceitar atribuição;" + chr(13) + "2- Trocar estado operacional da encomenda;")
            x = int(input())
            if x == 1:
                print("O estado da sua tarefa está em recolha.")
                estadoAtual[idTarefa - 1] = estado[0]
                contadorTarefas[idTarefa - 1] = 1
            else:
                if x == 2:
                    print("Digite para que estado pretende alterar a tarefa escolhida:")
                    for i in range(0, len(estado) - 1 + 1, 1):
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
            for i in range(0, len(anomalia) - 1 + 1, 1):
                print(str(i + 1) + ")" + anomalia[i])
            motivo = int(input())
            print("Introduza a data e hora no formato DD/MM/AAAA HH:MM.")
            timestamp = input()
            print("O motivo pela qual a encomenda não vai ser entregue é o seguinte: " + anomalia[motivo - 1] + " E a data e hora que o estafeta relatou a anomalia foi: " + timestamp)
            timestamps[idTarefa - 1] = timestamp
        print("Se pretender aceitar/ recusar/ trocar de estado alguma outra encomenda, digite 1.")
        var_return = int(input())
        if var_return != 1: break

def menu():
    print("----MENU----")
    print("1) Lista de tarefas atribuídas;")
    print("2) Aceitar e recusar atribuição e trocar estado operacional de encomenda;")
    print("3) Registar localização;")
    print("4) Reportar anomalias;")
    print("5) Consultar dados pessoais;")
    print("6) Sair;")
    opcao = int(input())
    
    return opcao

def tarefasAtribuidas(tarefas):
    print("---Lista de tarefas atribuídas---")
    for i in range(0, len(tarefas) - 1 + 1, 1):
        print(str(i + 1) + ") " + tarefas[i])

# Main
contadorTarefas = [0] * (4)
contadorSucesso = [0] * (4)
timestamps = [""] * (4)
anomalia = [""] * (5)
estadoAtual = [""] * (4)
localizacao = [""] * (4)
tarefas = [""] * (4)
estado = [""] * (4)

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
for i in range(0, len(contadorTarefas) - 1 + 1, 1):
    contadorTarefas[i] = 0
for i in range(0, len(contadorSucesso) - 1 + 1, 1):
    contadorSucesso[i] = 0
idTarefa = 0
while True:    #This simulates a Do Loop
    opcao = menu()
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
