import os
import pandas as pd
from datetime import datetime


def apresentacaoProd(produtosNome, produtosPreco):
    print("Lista de Produtos")
    for i in range(0, len(produtosNome), 1):
        print(str(i + 1) + "- " + produtosNome[i] + "(" + str(produtosPreco[i]) + " eur/uni)")

def avaliacao():
    print("1- Experiência Boa")
    print("2- Experiência intermédia")
    print("3- Experiência Má")
    ava = int(input())
    
    return ava

def calcTotal(encomendas, produtoPreco):
    total = 0
    for i in range(0, len(encomendas), 1):
        total = total + encomendas[i] * produtoPreco[i]
    
    return total

def consultaPed(produtosNome, encomendas, produtosPreco, avaliacoes, t, td, destinos):
    for i in range(0, len(encomendas), 1):
        print(produtosNome[i] + " com a quantidade de " + str(encomendas[i]) + " e com o preço de " + str(encomendas[i] * produtosPreco[i]))
    print("---Avalições---")
    for a in range(0, t, 1):
        print("Avalição " + str(a + 1) + "--> " + str(avaliacoes[a]))
    print("---Destino da Encomenda---")
    for d in range(0, td, 1):
        print("Destino " + str(d + 1) + ": " + destinos[d])

def consultaStock(produtosNome, produtosQtd, produtosPreco):
    for r in range(0, len(produtosNome), 1):
        print(produtosNome[r] + " - " + str(produtosQtd[r]) + " unidades | " + str(produtosPreco[r]) + "eur/uni")

def criacaoPedido(produtosNome, encomendas, produtosPreco):
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
        if repeat != 1:
            break

def escolherDestino(destinosOpcao):
    print("Escolha o destino: ")
    for i in range(0, len(destinosOpcao)):
        print(str(i + 1) + " - " + destinosOpcao[i])
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

def validacaoStock(produtosNome, produtosQtd, encomendas, produtosPreco):
    for i in range(0, len(encomendas), 1):
        if encomendas[i] > 0:
            if encomendas[i] > produtosQtd[i]:
                print("Encomendas-te " + produtosNome[i] + "(" + str(encomendas[i]) + "). A quantidade encomendada é superior à quantidade máxima do stock " + str(produtosQtd[i]))
                print("A sua encomenda poderá demorar mais tempo até obter o stock necessário!")
            else:
                produtosQtd[i] = produtosQtd[i] - encomendas[i]
                print(" - " + produtosNome[i] + " com a quantidade de " + str(encomendas[i]) + " e o preço de " + str(encomendas[i] * produtosPreco[i]))


# --- CSV persistence helpers (pedidos.csv, eventos_pedido.csv, mensagens.csv) ---
CSV_PEDIDOS = os.path.join(os.getcwd(), 'pedidos.csv')
CSV_EVENTOS = os.path.join(os.getcwd(), 'eventos_pedido.csv')
CSV_MENSAGENS = os.path.join(os.getcwd(), 'mensagens.csv')


def ensure_csvs():
    # Create files with headers if they don't exist
    if not os.path.exists(CSV_PEDIDOS):
        df = pd.DataFrame(columns=['order_id', 'produto', 'quantidade', 'preco_unit', 'subtotal', 'destino', 'total', 'timestamp'])
        df.to_csv(CSV_PEDIDOS, index=False)
    if not os.path.exists(CSV_EVENTOS):
        df = pd.DataFrame(columns=['order_id', 'evento', 'timestamp'])
        df.to_csv(CSV_EVENTOS, index=False)
    if not os.path.exists(CSV_MENSAGENS):
        df = pd.DataFrame(columns=['order_id', 'mensagem', 'timestamp'])
        df.to_csv(CSV_MENSAGENS, index=False)


def save_order(order_id, items, destino, total):
    # items: list of dicts with keys produto, quantidade, preco_unit, subtotal
    ts = datetime.now().isoformat(sep=' ')
    rows = []
    for it in items:
        rows.append({
            'order_id': order_id,
            'produto': it['produto'],
            'quantidade': it['quantidade'],
            'preco_unit': it['preco_unit'],
            'subtotal': it['subtotal'],
            'destino': destino,
            'total': total,
            'timestamp': ts
        })
    df = pd.DataFrame(rows)
    df.to_csv(CSV_PEDIDOS, mode='a', header=not os.path.exists(CSV_PEDIDOS) or os.path.getsize(CSV_PEDIDOS) == 0, index=False)


def save_event(order_id, evento):
    ts = datetime.now().isoformat(sep=' ')
    df = pd.DataFrame([{'order_id': order_id, 'evento': evento, 'timestamp': ts}])
    df.to_csv(CSV_EVENTOS, mode='a', header=not os.path.exists(CSV_EVENTOS) or os.path.getsize(CSV_EVENTOS) == 0, index=False)


def save_message(order_id, mensagem):
    ts = datetime.now().isoformat(sep=' ')
    df = pd.DataFrame([{'order_id': order_id, 'mensagem': mensagem, 'timestamp': ts}])
    df.to_csv(CSV_MENSAGENS, mode='a', header=not os.path.exists(CSV_MENSAGENS) or os.path.getsize(CSV_MENSAGENS) == 0, index=False)

if __name__ == '__main__':
    # Main interactive client portal that persists to CSVs
    ensure_csvs()
    avaliacoes = [0] * 3
    destinosOpcao = [""] * 3
    destinos = [""] * 3
    produtosNome = [""] * 3
    produtosQtd = [0] * 3
    produtosPreco = [0] * 3
    encomendas = [0] * 3

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

    print("PORTAL DO CLIENTE")
    for i in range(0, len(encomendas), 1):
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
                validacaoStock(produtosNome, produtosQtd, encomendas, produtosPreco)
                print("Indique o destino da encomenda: ")
                escolha = escolherDestino(destinosOpcao)
                destino_escolhido = destinosOpcao[escolha - 1]
                destinos[td] = destino_escolhido
                td = td + 1
                total = calcTotal(encomendas, produtosPreco)
                print("Obrigado pela a encomenda" + " O total da encomenda é " + str(total) + " eur")
                print("Avalie o seu pedido")
                ava = avaliacao()
                avaliacoes[t] = ava
                t = t + 1

                # Persist order + events + message via pandas CSVs
                # Build order items list
                items = []
                for idx in range(0, len(encomendas)):
                    if encomendas[idx] > 0:
                        items.append({
                            'produto': produtosNome[idx],
                            'quantidade': encomendas[idx],
                            'preco_unit': produtosPreco[idx],
                            'subtotal': encomendas[idx] * produtosPreco[idx]
                        })
                order_id = datetime.now().strftime('%Y%m%d%H%M%S')
                save_order(order_id, items, destino_escolhido, total)
                save_event(order_id, 'Pedido criado')
                save_message(order_id, f'Pedido recebido. Total: {total} eur')

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
        if chamadaMenu != 1:
            break
    print("Continuação de um ótimo dia")