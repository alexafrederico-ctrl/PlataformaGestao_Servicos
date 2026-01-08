import csv
from datetime import datetime
import os

# ================= CONSTANTES =================

ESTADO_PENDENTE   = "pendente"
ESTADO_APROVADA   = "aprovada"
ESTADO_REJEITADA  = "rejeitada"
ESTADO_CANCELADA  = "cancelada"
ESTADO_ATRIBUIDA  = "atribuida"

ESTADOS = [
    ESTADO_PENDENTE,
    ESTADO_APROVADA,
    ESTADO_REJEITADA,
    ESTADO_CANCELADA,
    ESTADO_ATRIBUIDA
]

COL_ENCOMENDAS = [
    "id", "idOriginal", "idCliente", "origem", "destino", "dataCriacao",
    "janelaInicio", "janelaFim", "duracaoEstimadaMin",
    "zona", "prioridade", "estado", "idEstafeta", "produto"
]

COL_EVENTOS = ["ClienteID", "Evento", "Produto", "Status", "Destino", "Timestamp"]
COL_ATRIBUICOES = ["idAtribuicao", "idPedido", "idEstafeta", "dataAtribuicao"]
COL_ESTAFETAS = ["idEstafeta", "nome", "zona", "disponibilidade", "carga_trabalho"]

# ================= CSV =================

def criar_csv(nome, colunas):
    if not os.path.exists(nome):
        with open(nome, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=colunas)
            writer.writeheader()

def ler_csv(nome):
    if not os.path.exists(nome):
        return []
    try:
        with open(nome, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            return [{k.strip(): v.strip() for k, v in linha.items() if k is not None} for linha in reader]
    except:
        return []

def guardar_csv(nome, colunas, dados):
    with open(nome, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(dados)

def obter_proximo_id(ficheiro, campo):
    dados = ler_csv(ficheiro)
    ids = [int(d[campo]) for d in dados if d.get(campo, "").isdigit()]
    return max(ids) + 1 if ids else 1

# ================= EVENTOS =================

def registar_evento(idPedido, novo_estado):
    criar_csv("eventos_pedido.csv", COL_EVENTOS)

    eventos = ler_csv("eventos_pedido.csv")
    encomendas = ler_csv("encomendas.csv")

    enc = next((e for e in encomendas if str(e["id"]) == str(idPedido)), {})

    eventos.append({
        "ClienteID": enc.get("idCliente", "N/A"),
        "Evento": f"Gestor: {novo_estado.upper()}",
        "Produto": enc.get("produto", "N/A"),
        "Status": novo_estado,
        "Destino": enc.get("zona", "N/A"),
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    guardar_csv("eventos_pedido.csv", COL_EVENTOS, eventos)

# ================= IMPORTAÇÃO =================

def importar_pedidos_do_cliente():
    if not os.path.exists("pedidos.csv"):
        return

    pedidos_brutos = ler_csv("pedidos.csv")
    encomendas_atuais = ler_csv("encomendas.csv")

    processados = [e.get("idOriginal") for e in encomendas_atuais]
    next_id = obter_proximo_id("encomendas.csv", "id")
    alterou = False

    for p in pedidos_brutos:
        id_unico = f"{p.get('Produto')}_{p.get('Data')}"

        if id_unico not in processados:
            encomendas_atuais.append({
                "id": next_id,
                "idOriginal": id_unico,
                "idCliente": p.get("ClienteID", "Desconhecido"),
                "produto": p.get("Produto", "N/A"),
                "origem": "Loja Online",
                "destino": p.get("Destino", ""),
                "dataCriacao": p.get("Data", datetime.now().strftime("%Y-%m-%d")),
                "janelaInicio": "09:00",
                "janelaFim": "18:00",
                "duracaoEstimadaMin": "30",
                "zona": p.get("Destino", "N/A"),
                "prioridade": "Normal",
                "estado": ESTADO_PENDENTE,
                "idEstafeta": ""
            })

            registar_evento(next_id, ESTADO_PENDENTE)
            processados.append(id_unico)
            next_id += 1
            alterou = True

    if alterou:
        guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas_atuais)

# ================= FUNCIONALIDADES =================

def listar_todas():
    encomendas = ler_csv("encomendas.csv")
    if not encomendas:
        print("\nNão existem encomendas registadas.")
        return

    print("\n" + "=" * 110)
    header = f"{'ID':<4} | {'Cliente':<10} | {'Produto':<12} | {'Zona':<12} | {'Estado':<10} | {'Prioridade':<10} | {'Estafeta'}"
    print(header)
    print("-" * 110)

    for e in encomendas:
        estafeta = e.get("idEstafeta") if e.get("idEstafeta") else "---"
        print(f"{e['id']:<4} | {e['idCliente']:<10} | {e['produto']:<12} | "
              f"{e['zona']:<12} | {e['estado']:<10} | {e['prioridade']:<10} | {estafeta}")

    print("=" * 110)

def aprovar_rejeitar_pedidos(zonas_atendidas):
    while True:
        encomendas = ler_csv("encomendas.csv")
        pendentes = [e for e in encomendas if e["estado"] == ESTADO_PENDENTE]

        if not pendentes:
            print("\nNenhum pedido pendente.")
            break

        print("\n--- PEDIDOS PENDENTES ---")
        for e in pendentes:
            sug = "APROVAR" if e["zona"] in zonas_atendidas else "ZONA FORA"
            print(f"ID: {e['id']} | Produto: {e['produto']} | Zona: {e['zona']} | Sugestão: {sug}")

        escolha = input("\nID para tratar (ou 's' para sair): ").strip()
        if escolha.lower() == 's':
            break

        alvo = next((e for e in pendentes if str(e["id"]) == escolha), None)
        if not alvo:
            print("ID inválido.")
            continue

        op = input("1-Aprovar, 2-Rejeitar, 3-Voltar: ")
        if op == "1":
            alvo["estado"] = ESTADO_APROVADA
            registar_evento(alvo["id"], ESTADO_APROVADA)
        elif op == "2":
            alvo["estado"] = ESTADO_REJEITADA
            registar_evento(alvo["id"], ESTADO_REJEITADA)

        guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)

def cancelar_editar_encomenda():
    encomendas = ler_csv("encomendas.csv")
    if not encomendas:
        return

    id_alvo = input("\nID da encomenda a gerir: ").strip()
    enc = next((e for e in encomendas if str(e["id"]) == id_alvo), None)

    if not enc:
        print("ID não encontrado.")
        return

    if enc["estado"] not in [ESTADO_PENDENTE]:
        print(f"Não pode editar uma encomenda '{enc['estado']}'.")
        return

    print("\n1. Cancelar Encomenda\n2. Editar (Zona/Prioridade)\n3. Voltar")
    opcao = input("Opção: ")

    if opcao == "1":
        enc["estado"] = ESTADO_CANCELADA
        registar_evento(id_alvo, ESTADO_CANCELADA)
        print("✓ Cancelada.")
    elif opcao == "2":
        nova_zona = input(f"Nova Zona [{enc['zona']}]: ").strip()
        nova_prio = input(f"Nova Prioridade [{enc['prioridade']}]: ").strip()
        if nova_zona:
            enc["zona"] = nova_zona
        if nova_prio:
            enc["prioridade"] = nova_prio
        print("✓ Atualizada.")

    guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)

def filtrar_encomendas():
    encomendas = ler_csv("encomendas.csv")
    print("\nFiltrar por: 1-Estado | 2-Zona | 3-Cliente | 4-Produto")
    op = input("Opção: ")

    mapeamento = {"1": "estado", "2": "zona", "3": "idCliente", "4": "produto"}
    campo = mapeamento.get(op)

    if campo:
        valor = input(f"Valor para {campo}: ").strip().lower()
        resultados = [e for e in encomendas if valor in e.get(campo, "").lower()]

        if resultados:
            print(f"\nEncontradas {len(resultados)} encomendas:")
            for r in resultados:
                print(f"ID {r['id']} | Nome {r['idCliente']} |  {r['produto']} | {r['zona']} | {r['estado']}")
        else:
            print("Nenhum resultado.")

def atribuir_estafetas():
    encomendas = ler_csv("encomendas.csv")
    estafetas = ler_csv("estafetas.csv")

    criar_csv("atribuicoes.csv", COL_ATRIBUICOES)
    atribuicoes = ler_csv("atribuicoes.csv")

    proximo_atrib = obter_proximo_id("atribuicoes.csv", "idAtribuicao")
    alterou = False

    for e in encomendas:
        if e["estado"] == ESTADO_APROVADA:
            elegiveis = [
                s for s in estafetas
                if s["zona"].lower() == e["zona"].lower()
                and s["disponibilidade"].lower() == "true"
            ]

            if elegiveis:
                escolhido = min(elegiveis, key=lambda x: int(x["carga_trabalho"]))
                e["estado"] = ESTADO_ATRIBUIDA
                e["idEstafeta"] = escolhido["idEstafeta"]
                escolhido["carga_trabalho"] = str(int(escolhido["carga_trabalho"]) + 1)

                atribuicoes.append({
                    "idAtribuicao": proximo_atrib,
                    "idPedido": e["id"],
                    "idEstafeta": escolhido["idEstafeta"],
                    "dataAtribuicao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                registar_evento(e["id"], ESTADO_ATRIBUIDA)
                proximo_atrib += 1
                alterou = True

    if alterou:
        guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)
        guardar_csv("estafetas.csv", COL_ESTAFETAS, estafetas)
        guardar_csv("atribuicoes.csv", COL_ATRIBUICOES, atribuicoes)

# ================= MENU =================

def menu():
    criar_csv("encomendas.csv", COL_ENCOMENDAS)
    criar_csv("eventos_pedido.csv", COL_EVENTOS)

    ZONAS_ATENDIDAS = ["Braga", "Guimarães", "Famalicão", "Fafe"]

    while True:
        importar_pedidos_do_cliente()

        print("\n" + "=" * 40)
        print("     SISTEMA DE GESTÃO DE ENCOMENDAS")
        print("=" * 40)
        print("1. Aprovar/Rejeitar Pedidos")
        print("2. Atribuir Estafetas")
        print("3. Cancelar/Editar Encomenda")
        print("4. Filtrar Encomendas")
        print("5. Consultar todas as Encomendas")
        print("6. Sair")

        op = input("\nOpção: ")

        if op == "1":
            aprovar_rejeitar_pedidos(ZONAS_ATENDIDAS)
        elif op == "2":
            atribuir_estafetas()
        elif op == "3":
            cancelar_editar_encomenda()
        elif op == "4":
            filtrar_encomendas()
        elif op == "5":
            listar_todas()
        elif op == "6":
            break

if __name__ == "__main__":
    menu()
