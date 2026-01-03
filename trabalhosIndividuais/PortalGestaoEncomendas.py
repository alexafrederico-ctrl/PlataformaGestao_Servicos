import csv
from datetime import datetime
import os

# ---------- Funções de criação inicial dos CSVs ----------
def criar_csv_eventos():
    if not os.path.exists("eventos_pedido.csv"):
        with open("eventos_pedido.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["idEvento", "idPedido", "estado", "utilizador", "timestamp"])
            writer.writeheader()

def criar_csv_atribuicoes():
    if not os.path.exists("atribuicoes.csv"):
        with open("atribuicoes.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["idAtribuicao", "idPedido", "idEstafeta", "dataAtribuicao"])
            writer.writeheader()

# ---------- Funções de apoio ----------
def importar_pedidos_para_encomendas():
    pedidos_file = "pedidos.csv"
    encomendas_file = "encomendas.csv"

    colunas_encomendas = [
        "id", "idCliente", "produto", "quantidade", "origem", "destino", 
        "dataCriacao", "janelaInicio", "janelaFim", "duracaoEstimadaMin",
        "zona", "prioridade", "estado", "idEstafeta"
    ]

    pedidos = []
    if os.path.exists(pedidos_file):
        with open(pedidos_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pedidos.append(row)

    encomendas = []
    for i, p in enumerate(pedidos, start=1):
        encomenda = {
            "id": i,
            "idCliente": p.get("ClienteID", ""),
            "produto": p.get("Produto", "N/A"),
            "quantidade": p.get("Quantidade", "0"),
            "origem": "Loja",
            "destino": p.get("Destino", ""),
            "dataCriacao": p.get("Data", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
            "janelaInicio": "",
            "janelaFim": "",
            "duracaoEstimadaMin": "",
            "zona": p.get("Destino", ""),
            "prioridade": "Normal",
            "estado": "pendente",
            "idEstafeta": ""
        }
        encomendas.append(encomenda)

    if encomendas:
        with open(encomendas_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=colunas_encomendas)
            writer.writeheader()
            writer.writerows(encomendas)

    print(f"✓ {len(encomendas)} pedidos importados para {encomendas_file}")


def gerar_id_csv(csv_file, campo_id):
    try:
        with open(csv_file, "r") as f:
            reader = csv.DictReader(f)
            ids = [int(row[campo_id]) for row in reader if row[campo_id]]
            return max(ids) + 1 if ids else 1
    except FileNotFoundError:
        return 1

def criar_evento(idPedido, estado, utilizador):
    criar_csv_eventos()
    idEvento = gerar_id_csv("eventos_pedido.csv", "idEvento")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("eventos_pedido.csv", "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["idEvento", "idPedido", "estado", "utilizador", "timestamp"])
        writer.writerow({"idEvento": idEvento, "idPedido": idPedido, "estado": estado, "utilizador": utilizador, "timestamp": timestamp})

def ler_encomendas():
    """Lê encomendas.csv (não pedidos.csv)"""
    encomendas_file = "encomendas.csv"
    if not os.path.exists(encomendas_file):
        return []

    with open(encomendas_file, "r") as f:
        reader = csv.DictReader(f)
        encomendas = [row for row in reader]
    return encomendas

def atualizar_encomenda(idPedido, novo_estado, idEstafeta=""):
    encomendas_file = "encomendas.csv"
    encomendas = ler_encomendas()
    for e in encomendas:
        if str(e.get("id", "")) == str(idPedido):
            e["estado"] = novo_estado
            if idEstafeta:
                e["idEstafeta"] = str(idEstafeta)
    if encomendas:
        with open(encomendas_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=encomendas[0].keys())
            writer.writeheader()
            writer.writerows(encomendas)

# ---------- Funções principais do Gestor ----------
def consultar_encomendas_pendentes():
    encomendas = ler_encomendas()
    pendentes = [e for e in encomendas if e["estado"].lower() == "pendente"]
    if not pendentes:
        print("Não existem encomendas pendentes.")
        return
    for e in pendentes:
        print(f"Cliente: {e.get('idCliente','N/A')} | Produto: {e.get('produto','N/A')} | Qtde: {e.get('quantidade','N/A')} | Estado: {e.get('estado','N/A')}")

def aprovar_encomendas(zonasAtendidas, estafetas):
    encomendas = ler_encomendas()
    for e in encomendas:
        if e["estado"].lower() != "pendente":
            continue

        # Verifica zona
        if e.get("Destino", "") not in zonasAtendidas:
            print(f'Encomenda do cliente {e.get("ClienteID")} REJEITADA: Zona não atendida')
            atualizar_encomenda(e.get("ClienteID"), "rejeitado")
            criar_evento(e.get("ClienteID"), "Rejeitada", "gestor")
            continue

        # Verifica stock
        try:
            quantidade = float(e.get("Quantidade", 0))
        except:
            quantidade = 0
        try:
            preco = float(e.get("Preço_Unitário", 0))
        except:
            preco = 0
        if quantidade <= 0:
            print(f'Encomenda do cliente {e.get("ClienteID")} REJEITADA: Quantidade inválida')
            atualizar_encomenda(e.get("ClienteID"), "rejeitado")
            criar_evento(e.get("ClienteID"), "Rejeitada", "gestor")
            continue

        # Aprovada
        print(f'Encomenda do cliente {e.get("ClienteID")} APROVADA')
        atualizar_encomenda(e.get("ClienteID"), "aprovada")
        criar_evento(e.get("ClienteID"), "Aprovada", "gestor")

        # Atribuição de estafeta
        zona = e.get("Destino", "")
        estafeta_disponivel = next((est for est in estafetas if est["zona"] == zona and est["livre"]), None)
        if estafeta_disponivel:
            atualizar_encomenda(e.get("ClienteID"), "atribuida", idEstafeta=estafeta_disponivel["idEstafeta"])
            estafeta_disponivel["livre"] = False
            criar_evento(e.get("ClienteID"), "Atribuída", "gestor")
            idAtribuicao = gerar_id_csv("atribuicoes.csv", "idAtribuicao")
            criar_csv_atribuicoes()
            with open("atribuicoes.csv", "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=["idAtribuicao", "idPedido", "idEstafeta", "dataAtribuicao"])
                writer.writerow({"idAtribuicao": idAtribuicao, "idPedido": e.get("ClienteID"), "idEstafeta": estafeta_disponivel["idEstafeta"], "dataAtribuicao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
            print(f'Encomenda atribuída ao Estafeta {estafeta_disponivel["idEstafeta"]}')
        else:
            print(f'Encomenda aguarda atribuição (nenhum estafeta disponível)')

# ---------- Função para filtrar encomendas por zona ----------
def filtrar_encomendas_por_zona():
    encomendas = ler_encomendas()
    if not encomendas:
        print("Não existem encomendas registadas.")
        return

    zona = input("Indique a zona para filtrar: ").strip()
    filtradas = [e for e in encomendas if e.get("Destino", "").lower() == zona.lower()]

    if not filtradas:
        print(f"Não existem encomendas na zona '{zona}'.")
        return

    print(f"\nEncomendas na zona '{zona}':")
    for e in filtradas:
        print(f"ID Pedido: {e.get('idPedido', 'N/A')} | Cliente: {e.get('ClienteID','N/A')} | Produto: {e.get('Produto','N/A')} | Quantidade: {e.get('Quantidade','N/A')} | Estado: {e.get('estado','N/A')} | Estafeta: {e.get('idEstafeta','N/A')}")

# ---------- Menu ----------
def menu_gestor():
    zonasAtendidas = ["Braga", "Guimarães"]
    estafetas = [
        {"idEstafeta": 1, "zona": "Guimarães", "livre": True},
        {"idEstafeta": 2, "zona": "Guimarães", "livre": False},
        {"idEstafeta": 3, "zona": "Braga", "livre": True}
    ]

    while True:
        print("\n***** MENU GESTOR *****")
        print("1 - Consultar encomendas pendentes")
        print("2 - Aprovar e atribuir encomendas")
        print("3 - Filtrar encomendas por zona")
        print("4 - Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == "1":
            consultar_encomendas_pendentes()
        elif escolha == "2":
            aprovar_encomendas(zonasAtendidas, estafetas)
        elif escolha == "3":
            filtrar_encomendas_por_zona()
        elif escolha == "4":
            print("Sistema finalizado.")
            break
        else:
            print("Opção inválida. Escolha 1, 2, 3 ou 4.")

# ---------- Execução ----------
if __name__ == "__main__":
    importar_pedidos_para_encomendas() 
    menu_gestor()
