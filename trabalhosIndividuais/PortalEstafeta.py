import csv
import os
from datetime import datetime

# ------------------- CONFIGURAÇÃO DE CSV -------------------
COL_ATRIBUICOES = ["idAtribuicao", "idPedido", "idEstafeta", "dataAtribuicao", "decisao"]
COL_ENCOMENDAS = ["id", "idOriginal", "idCliente", "origem", "destino", "dataCriacao", "janelaInicio", "janelaFim", "duracaoEstimadaMin", "zona", "prioridade", "estado", "idEstafeta"]
COL_EVENTOS = ["idEvento", "idPedido", "estado", "utilizador", "idEstafeta", "localizacao", "timestamp"]
COL_ESTAFETAS = ["idEstafeta", "nome", "zona", "disponibilidade", "carga_trabalho"]
COL_ANOMALIAS = ["idAnomalia", "idPedido", "idEstafeta", "motivo", "descricao", "timestamp"]
COL_MENSAGENS = ["ClienteID", "Tipo", "Mensagem", "Timestamp"]
COL_METRICAS = ["idEstafeta", "nome", "tarefas_atribuidas", "aceites", "concluidas", "falhadas", "entregas_hoje", "entregas_mes", "taxa_sucesso", "media_estimativa_min", "media_actual_min", "media_tempo_min", "timestamp"]


def garantir_csv(nome, colunas):
    if not os.path.exists(nome):
        with open(nome, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=colunas)
            writer.writeheader()


def ler_csv(nome):
    if not os.path.exists(nome):
        return []
    with open(nome, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def guardar_csv(nome, colunas, dados):
    with open(nome, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(dados)


def append_row(nome, colunas, row):
    garantir_csv(nome, colunas)
    rows = ler_csv(nome)
    rows.append(row)
    guardar_csv(nome, colunas, rows)


def obter_proximo_id(ficheiro, campo):
    dados = ler_csv(ficheiro)
    ids = [int(d[campo]) for d in dados if d.get(campo) and d[campo].isdigit()]
    return max(ids, default=0) + 1


def registar_evento(idPedido, novo_estado, utilizador="Estafeta", idEstafeta="", localizacao=""):
    novo_id = obter_proximo_id("eventos_pedido.csv", "idEvento")
    row = {
        "idEvento": str(novo_id),
        "idPedido": str(idPedido),
        "estado": novo_estado,
        "utilizador": utilizador,
        "idEstafeta": str(idEstafeta) if idEstafeta is not None else "",
        "localizacao": localizacao,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    append_row("eventos_pedido.csv", COL_EVENTOS, row)
    atualizar_estado_por_evento(idPedido, novo_estado, idEstafeta) 


def registar_anomalia(idPedido, idEstafeta, motivo, descricao=""):
    row = {
        "idAnomalia": str(obter_proximo_id("anomalias.csv", "idAnomalia")),
        "idPedido": str(idPedido),
        "idEstafeta": str(idEstafeta),
        "motivo": motivo,
        "descricao": descricao,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    append_row("anomalias.csv", COL_ANOMALIAS, row)


def registar_mensagem(cliente_id, tipo, mensagem):
    append_row("mensagens.csv", COL_MENSAGENS, {
        "ClienteID": cliente_id,
        "Tipo": tipo,
        "Mensagem": mensagem,
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


def atualizar_estado_por_evento(idPedido, evento_estado, idEstafeta=""):
    encomendas = ler_csv("encomendas.csv")
    encom = next((e for e in encomendas if str(e.get("id")) == str(idPedido)), None)
    if not encom:
        return
    s = str(evento_estado).lower()
    rules = [("aceite", "atribuida"), ("atribu", "atribuida"), ("conclu", "concluida"), ("entreg", "concluida"), ("falh", "falhada"), ("recus", "rejeitada"), ("rejeitada", "rejeitada"), ("aprov", "aprovada"), ("cancel", "cancelada")]
    novo = next((v for k, v in rules if k in s), None)
    if novo:
        encom["estado"] = novo
        if idEstafeta:
            encom["idEstafeta"] = str(idEstafeta)
        guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)


def calcular_metricas(idEstafeta):
    """Recalcula métricas a partir de eventos e encomendas (mais compacto)."""
    eventos = ler_csv("eventos_pedido.csv")
    encomendas = {str(e.get("id")): e for e in ler_csv("encomendas.csv")}
    evs = [e for e in eventos if str(e.get("idEstafeta", "")).strip() == str(idEstafeta)]

    from collections import defaultdict
    grupos = defaultdict(list)
    for e in evs:
        if e.get("idPedido"): grupos[e.get("idPedido")].append(e)

    tarefas_atribuidas = sum(1 for p, lst in grupos.items() if any("atribu" in (ev.get("estado","")) or "aceite" in (ev.get("estado","")) for ev in lst))
    aceites = sum(1 for e in evs if "aceite" in (e.get("estado","")))
    falhadas = sum(1 for e in evs if "falh" in (e.get("estado","")))

    today = datetime.now()
    entregas_hoje = entregas_mes = concluidas = 0
    tempos = []
    estimated = []

    for p, lst in grupos.items():
        t_aceite = next((datetime.strptime(e.get("timestamp"), "%Y-%m-%d %H:%M:%S") for e in lst if e.get("timestamp") and ("aceite" in e.get("estado","") or "atribu" in e.get("estado",""))), None)
        t_concl = next((datetime.strptime(e.get("timestamp"), "%Y-%m-%d %H:%M:%S") for e in lst if e.get("timestamp") and ("conclu" in e.get("estado","") or "entreg" in e.get("estado",""))), None)
        if t_concl:
            concluidas += 1
            if t_concl.date() == today.date(): entregas_hoje += 1
            if t_concl.year == today.year and t_concl.month == today.month: entregas_mes += 1
        if t_aceite and t_concl and t_concl >= t_aceite:
            tempos.append((t_concl - t_aceite).total_seconds() / 60.0)
        enc = encomendas.get(str(p))
        if enc and enc.get("duracaoEstimadaMin"):
            try: estimated.append(float(enc.get("duracaoEstimadaMin")))
            except Exception: pass

    media_tempo = sum(tempos)/len(tempos) if tempos else None
    media_estimativa = sum(estimated)/len(estimated) if estimated else None
    taxa_sucesso = (concluidas / tarefas_atribuidas * 100.0) if tarefas_atribuidas else None

    est = next((x for x in ler_csv("estafetas.csv") if str(x.get("idEstafeta")) == str(idEstafeta)), {})
    return {"idEstafeta": str(idEstafeta), "nome": est.get("nome",""), "tarefas_atribuidas": tarefas_atribuidas, "aceites": aceites, "concluidas": concluidas, "falhadas": falhadas, "entregas_hoje": entregas_hoje, "entregas_mes": entregas_mes, "taxa_sucesso": taxa_sucesso, "media_estimativa_min": media_estimativa, "media_actual_min": media_tempo, "media_tempo_min": media_tempo}


def mostrar_metricas(idEstafeta, gravar=False):
    m = calcular_metricas(idEstafeta)
    print("--- Métricas pessoais ---")
    print(f"Estafeta: {m.get('nome','(desconhecido)')} (id {m.get('idEstafeta')})")
    print(f"Tarefas atribuídas (únicas): {m.get('tarefas_atribuidas')}")
    print(f"Aceites: {m.get('aceites')}")
    print(f"Concluídas: {m.get('concluidas')}")
    print(f"Falhadas: {m.get('falhadas')}")
    print(f"Entregas hoje: {m.get('entregas_hoje')}")
    print(f"Entregas este mês: {m.get('entregas_mes')}")
    if m.get('taxa_sucesso') is not None:
        print(f"Taxa de sucesso: {m.get('taxa_sucesso'):.1f}%")
    else:
        print("Taxa de sucesso: N/A")
    if m.get('media_estimativa_min') is not None:
        print(f"Média estimada (min): {m.get('media_estimativa_min'):.1f} min")
    else:
        print("Média estimada: N/A")
    if m.get('media_actual_min') is not None:
        print(f"Média real (min) entre aceite e conclusão: {m.get('media_actual_min'):.1f} min")
    else:
        print("Média real: N/A")
    if m.get('media_tempo_min') is not None:
        print(f"Tempo médio (min) entre aceite e conclusão: {m.get('media_tempo_min'):.1f} min")
    else:
        print("Tempo médio: N/A")

    if gravar:
        garantir_csv("metricas_estafeta.csv", COL_METRICAS)
        metricas = ler_csv("metricas_estafeta.csv")
        registro = {
            "idEstafeta": m.get("idEstafeta"),
            "nome": m.get("nome"),
            "tarefas_atribuidas": str(m.get("tarefas_atribuidas") or 0),
            "aceites": str(m.get("aceites") or 0),
            "concluidas": str(m.get("concluidas") or 0),
            "falhadas": str(m.get("falhadas") or 0),
            "entregas_hoje": str(m.get("entregas_hoje") or 0),
            "entregas_mes": str(m.get("entregas_mes") or 0),
            "taxa_sucesso": f"{m.get('taxa_sucesso'):.2f}" if m.get('taxa_sucesso') is not None else "",
            "media_estimativa_min": f"{m.get('media_estimativa_min'):.2f}" if m.get('media_estimativa_min') is not None else "",
            "media_actual_min": f"{m.get('media_actual_min'):.2f}" if m.get('media_actual_min') is not None else "",
            "media_tempo_min": f"{m.get('media_tempo_min'):.2f}" if m.get('media_tempo_min') is not None else "",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        # atualizar ou adicionar
        existente = next((x for x in metricas if x.get("idEstafeta") == registro["idEstafeta"]), None)
        if existente:
            metricas = [registro if x.get("idEstafeta") == registro["idEstafeta"] else x for x in metricas]
        else:
            metricas.append(registro)
        guardar_csv("metricas_estafeta.csv", COL_METRICAS, metricas)
        print("Métricas gravadas em 'metricas_estafeta.csv'.")


# ------------------- OPERACIONAL DO ESTAFETA -------------------

anomalia = [
    "Endereço incorreto.",
    "Cliente ausente.",
    "Avaria no veículo.",
    "Condições metereológicas adversas.",
    "Produto danificado."
]

ESTADOS_POSIVEIS = [
    "em recolha",
    "em distribuição",
    "concluído",
    "falhado"
]


def encontrar_ou_criar_estafeta(nome):
    garantir_csv("estafetas.csv", COL_ESTAFETAS)
    estafetas = ler_csv("estafetas.csv")
    for e in estafetas:
        if e.get("nome", "").strip().lower() == nome.strip().lower():
            return e["idEstafeta"]

    novo_id = obter_proximo_id("estafetas.csv", "idEstafeta")
    novo = {"idEstafeta": str(novo_id), "nome": nome, "zona": "", "disponibilidade": "true", "carga_trabalho": "0"}
    estafetas.append(novo)
    guardar_csv("estafetas.csv", COL_ESTAFETAS, estafetas)
    return str(novo_id)


def tarefas_do_estafeta(idEstafeta):
    garantir_csv("atribuicoes.csv", COL_ATRIBUICOES)
    garantir_csv("encomendas.csv", COL_ENCOMENDAS)
    atribuicoes = ler_csv("atribuicoes.csv")
    encomendas = ler_csv("encomendas.csv")

    tarefas = []
    mapping = []  # same order: mapping[i] -> idPedido
    for a in atribuicoes:
        if a.get("idEstafeta") == str(idEstafeta):
            idPedido = a.get("idPedido")
            encom = next((x for x in encomendas if str(x.get("id")) == str(idPedido)), None)
            if encom:
                display = f"ID {encom.get('id')} | Destino: {encom.get('destino','')} | Estado: {encom.get('estado','')} | Atribuição: {a.get('dataAtribuicao','')} | Decisão: {a.get('decisao','') or 'N/A'}"
                tarefas.append(display)
                mapping.append(str(idPedido))
    return tarefas, mapping


def tarefasAtribuidas(tarefas):
    print("---Lista de tarefas atribuídas---")
    if not tarefas:
        print("(Não existem tarefas atribuídas.)")
        return
    for i, t in enumerate(tarefas, start=1):
        print(str(i) + ") " + t)


def aceitarRecusar(tarefas, mapping, idEstafeta):
    if not tarefas:
        print("Não tem tarefas atribuídas.")
        return

    garantir_csv("atribuicoes.csv", COL_ATRIBUICOES)
    garantir_csv("encomendas.csv", COL_ENCOMENDAS)
    garantir_csv("eventos_pedido.csv", COL_EVENTOS)

    atribuicoes = ler_csv("atribuicoes.csv")
    encomendas = ler_csv("encomendas.csv")

    while True:
        tarefasAtribuidas(tarefas)
        print("Escolha o número da tarefa que pretende gerir (0 para sair):")
        escolha = input().strip()
        if not escolha.isdigit() or int(escolha) == 0:
            break
        idx = int(escolha) - 1
        if idx < 0 or idx >= len(mapping):
            print("Escolha inválida.")
            continue

        idPedido = mapping[idx]
        encom = next((x for x in encomendas if str(x.get("id")) == str(idPedido)), None)
        atrib = next((x for x in atribuicoes if str(x.get("idPedido")) == str(idPedido) and x.get("idEstafeta") == str(idEstafeta)), None)

        print("Qual operação pretende executar:\n1 - Aceitar atribuição\n2 - Trocar estado operacional da encomenda\n3 - Recusar atribuição")
        op = input().strip()

        if op == "1":
            # Aceitar atribuicao -> marcar como atribuida
            encom["estado"] = "atribuida"
            if atrib:
                atrib["decisao"] = "aceite"
                atrib["dataAtribuicao"] = atrib.get("dataAtribuicao") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)
            guardar_csv("atribuicoes.csv", COL_ATRIBUICOES, atribuicoes)
            registar_evento(idPedido, "aceite", utilizador="Estafeta", idEstafeta=idEstafeta)
            print(f"Encomenda {idPedido} aceite e estado alterado para 'atribuida'.")

        elif op == "2":
            print("Digite para que estado pretende alterar a tarefa escolhida:")
            for i, s in enumerate(ESTADOS_POSIVEIS, start=1):
                print(f"{i}) {s}")
            x = input().strip()
            if x.isdigit() and 1 <= int(x) <= len(ESTADOS_POSIVEIS):
                novo = ESTADOS_POSIVEIS[int(x) - 1]
                encom["estado"] = novo
                guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)

                # Se o novo estado for recolha/entrega/falha, pedir localização para guardar no evento
                loc = ""
                if any(k in novo.lower() for k in ["recol", "conclu", "entreg", "falh"]):
                    loc = input("Introduza a localização (morada ou coordenadas) para registar no evento (deixe vazio para omitir): ").strip()

                registar_evento(idPedido, novo, utilizador="Estafeta", idEstafeta=idEstafeta, localizacao=loc)
                print(f"A encomenda passou ao estado: {novo}")
            else:
                print("Estado inválido.")

        elif op == "3":
            print("Qual o motivo para recusar a encomenda?")
            for i, m in enumerate(anomalia, start=1):
                print(f"{i}) {m}")
            motivo = input().strip()
            motivo_text = ""
            if motivo.isdigit() and 1 <= int(motivo) <= len(anomalia):
                motivo_text = anomalia[int(motivo) - 1]
            else:
                motivo_text = input("Descreva o motivo: ")

            encom["estado"] = "rejeitada"
            if atrib:
                atrib["decisao"] = "recusado"
            guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)
            guardar_csv("atribuicoes.csv", COL_ATRIBUICOES, atribuicoes)
            registar_evento(idPedido, f"recusado: {motivo_text}", utilizador="Estafeta", idEstafeta=idEstafeta)
            # Registar anomalia e notificar gestor
            registar_anomalia(idPedido, idEstafeta, motivo_text, descricao=motivo_text)
            registar_mensagem("gestor", "Anomalia", f"Anomalia reportada no pedido {idPedido} por estafeta {idEstafeta}: {motivo_text}")
            print(f"A encomenda {idPedido} foi recusada com motivo: {motivo_text}")

        else:
            print("Opção inválida.")

        cont = input("Se pretender gerir outra encomenda digite 1, caso contrário digite outro número: ")
        if cont.strip() != "1":
            break


# ------------------- MENU PRINCIPAL -------------------

def menu():
    garantir_csv("encomendas.csv", COL_ENCOMENDAS)
    garantir_csv("eventos_pedido.csv", COL_EVENTOS)
    garantir_csv("atribuicoes.csv", COL_ATRIBUICOES)
    garantir_csv("estafetas.csv", COL_ESTAFETAS)

    print("----MENU----")
    print("1) Lista de tarefas atribuídas;")
    print("2) Aceitar/Recusar atribuição ou trocar estado;")
    print("3) Registar localização (gera evento);")
    print("4) Reportar anomalias;")
    print("5) Consultar dados pessoais;")
    print("6) Sair;")
    print("7) Mostrar métricas pessoais;")
    opcao = input().strip()
    return opcao


if __name__ == '__main__':
    print("Seja bem vindo ao portal do estafeta, qual o seu nome?")
    nome = input().strip()
    idEstafeta = encontrar_ou_criar_estafeta(nome)
    print(f"Olá {nome} (id {idEstafeta})! O que desejas fazer?")

    while True:
        opc = menu()
        if opc == "1":
            tarefas, mapping = tarefas_do_estafeta(idEstafeta)
            tarefasAtribuidas(tarefas)

        elif opc == "2":
            tarefas, mapping = tarefas_do_estafeta(idEstafeta)
            aceitarRecusar(tarefas, mapping, idEstafeta)

        elif opc == "3":
            tarefas, mapping = tarefas_do_estafeta(idEstafeta)
            tarefasAtribuidas(tarefas)
            print("Qual o ID do pedido (número) que está a realizar?")
            idPedido = input().strip()
            loc = input("Qual a sua localização atual: ")
            registar_evento(idPedido, f"localizacao: {loc}", utilizador=nome, idEstafeta=idEstafeta, localizacao=loc)
            print("Localização registada.")

        elif opc == "4":
            tarefas, mapping = tarefas_do_estafeta(idEstafeta)
            tarefasAtribuidas(tarefas)
            print("Qual o ID do seu pedido?")
            idPedido = input().strip()
            motivo = input("Descreva a anomalia: ")
            registar_evento(idPedido, f"anomalia: {motivo}", utilizador=nome, idEstafeta=idEstafeta)
            # opcionalmente marcar como rejeitada
            encomendas = ler_csv("encomendas.csv")
            encom = next((x for x in encomendas if str(x.get("id")) == str(idPedido)), None)
            if encom:
                encom["estado"] = "rejeitada"
                guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)
                print("Encomenda marcada como rejeitada e evento registado.")

        elif opc == "5":
            estafetas = ler_csv("estafetas.csv")
            est = next((x for x in estafetas if x.get("idEstafeta") == str(idEstafeta)), None)
            tarefas, mapping = tarefas_do_estafeta(idEstafeta)
            print(f"Nome: {est.get('nome')}")
            print(f"Tarefas atribuídas: {len(tarefas)}")
            print(f"Carga de trabalho (registada): {est.get('carga_trabalho')}")

        elif opc == "6":
            print("Obrigado por trabalhar connosco!")
            break

        elif opc == "7":
            salvar = input("Deseja gravar métricas em 'metricas_estafeta.csv'? (s/n): ").strip().lower().startswith('s')
            mostrar_metricas(idEstafeta, gravar=salvar)

        else:
            print("Opção inválida. Tente novamente.")
