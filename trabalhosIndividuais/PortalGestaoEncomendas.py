import csv
from datetime import datetime
import os

# ================= CONSTANTES E CONFIGURAÇÃO =================

ESTADOS_FINAIS = ["rejeitada", "cancelada", "concluida"]

COL_ENCOMENDAS = [
    "id", "idOriginal", "idCliente", "origem", "destino", "dataCriacao",
    "janelaInicio", "janelaFim", "duracaoEstimadaMin",
    "zona", "prioridade", "estado", "idEstafeta"
]

COL_EVENTOS = ["idEvento", "idPedido", "estado", "utilizador", "timestamp"]
COL_ATRIBUICOES = ["idAtribuicao", "idPedido", "idEstafeta", "dataAtribuicao"]
COL_ESTAFETAS = ["idEstafeta", "nome", "zona", "disponibilidade", "carga_trabalho"]

# ================= FUNÇÕES DE PERSISTÊNCIA (CSV) =================

def garantir_csv(nome, colunas):
    if not os.path.exists(nome):
        with open(nome, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=colunas)
            writer.writeheader()

def ler_csv(nome):
    if not os.path.exists(nome): return []
    with open(nome, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def guardar_csv(nome, colunas, dados):
    with open(nome, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(dados)

def obter_proximo_id(ficheiro, campo):
    dados = ler_csv(ficheiro)
    if not dados: return 1
    ids = []
    for d in dados:
        valor = d.get(campo)
        if valor and str(valor).isdigit():
            ids.append(int(valor))
    return max(ids) + 1 if ids else 1

# ================= GESTÃO DE EVENTOS E IMPORTAÇÃO =================

def registar_evento(idPedido, novo_estado):
    garantir_csv("eventos_pedido.csv", COL_EVENTOS)
    eventos = ler_csv("eventos_pedido.csv")
    novo_id = obter_proximo_id("eventos_pedido.csv", "idEvento")
    
    eventos.append({
        "idEvento": novo_id,
        "idPedido": idPedido,
        "estado": novo_estado,
        "utilizador": "Gestor",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    guardar_csv("eventos_pedido.csv", COL_EVENTOS, eventos)

def importar_pedidos_do_cliente():
    if not os.path.exists("pedidos.csv"): return

    pedidos = ler_csv("pedidos.csv")
    encomendas = ler_csv("encomendas.csv")
    
    ids_originais_processados = [e.get("idOriginal") for e in encomendas if e.get("idOriginal")]
    next_id = obter_proximo_id("encomendas.csv", "id")
    alterou = False

    for p in pedidos:
      
        id_origem = p.get("PedidoID") or p.get("Data")
        
        if id_origem not in ids_originais_processados:
            nova = {
                "id": next_id,
                "idOriginal": id_origem,
                "idCliente": p.get("ClienteID", "Desconhecido"),
                "origem": "Loja",
                "destino": p.get("Destino", ""),
                "dataCriacao": p.get("Data", datetime.now().strftime("%Y-%m-%d")),
                "janelaInicio": "09:00", #nao sei o que colocar aqui
                "janelaFim": "18:00",#nao sei o que colocar aqui
                "duracaoEstimadaMin": "30",#nao sei o que colocar aqui
                "zona": p.get("Destino", ""),
                "prioridade": "Normal",
                "estado": "pendente",
                "idEstafeta": ""
            }
            encomendas.append(nova)
            registar_evento(next_id, "pendente")
            ids_originais_processados.append(id_origem)
            next_id += 1
            alterou = True

    if alterou:
    
        guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)

# ================= FUNCIONALIDADES PRINCIPAIS =================

def listar_todas():
    encomendas = ler_csv("encomendas.csv")
    if not encomendas:
        print("\n[!] Não existem encomendas registadas.")
        return

    header = (f"{'ID':<3} | {'Cliente':<8} | {'Zona':<10} | {'Estado':<10} | {'Prioridade':<11} | {'Data':<20} | {'Estafeta'}")
    print("\n" + "="*50)
    print(header)
    print("-" * 50)
    for e in encomendas:
        print(f"{e.get('id',''):<3} | {e.get('idCliente',''):<8} | "
           
              f"{e.get('zona',''):<10} | {e.get('estado',''):<10} | "
              f"{e.get('prioridade',''):<11} | {e.get('dataCriacao',''):<20} "
              f"| {e.get('idEstafeta','') if e.get('idEstafeta') else '---'}")
    print("="*50)
def aprovar_rejeitar_pedidos(zonas_atendidas):
    while True:
        encomendas = ler_csv("encomendas.csv")
        catalogo = ler_csv("catalogo.csv")
        pendentes = [e for e in encomendas if e["estado"] == "pendente"]

        if not pendentes:
            print("\n[!] Não existem encomendas pendentes.")
            break

        print("\n--- ENCOMENDAS PENDENTES ---")
        print(f"{'ID':<4} | {'Produto':<12} | {'Zona':<12} | {'Sugestão'}")
        
        for e in pendentes:
       
            item_catalogo = next((item for item in catalogo if item["nome"] == e.get("produto")), None)
            
  
            tem_stock = item_catalogo and int(item_catalogo["stock"]) > 0
            if e["zona"] in zonas_atendidas and tem_stock:
                sug = "APROVAR"
            elif not tem_stock:
                sug = "SEM STOCK"
            else:
                sug = "FORA DE ZONA"
                
            print(f"{e['id']:<4} | {e.get('produto','?'):<12} | {e['zona']:<12} | {sug}")

        escolha = input("\nIntroduza o ID para tratar (ou '3' para sair): ").strip()
        if escolha == "3": break

        encomenda_alvo = next((e for e in pendentes if str(e["id"]) == escolha), None)

        if encomenda_alvo:
         
            item_catalogo = next((item for item in catalogo if item["nome"] == encomenda_alvo.get("produto")), None)
            stock_atual = int(item_catalogo["stock"]) if item_catalogo else 0

            decisao = input(f"Aprovar ID {escolha}? (1-aprovar, 2-rejeitar, 3-voltar): ").lower()
            
            if decisao == '1':
                if stock_atual > 0:
                    encomenda_alvo["estado"] = "aprovada"
           
                    item_catalogo["stock"] = str(stock_atual - 1)
                    guardar_csv("catalogo.csv", ["idItem","tipo","nome","categoria","preco","duracaoPadraoMin","stock","ativo"], catalogo)
                    
                    registar_evento(encomenda_alvo["id"], "aprovada")
                    guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)
                    print(f"Encomenda aprovada! Stock de {encomenda_alvo.get('produto')} atualizado para {int(stock_atual)-1}.")
                else:
                    print(f"[!] Erro: Impossível aprovar. O produto '{encomenda_alvo.get('produto')}' está esgotado!")
            
            elif decisao == '2':
                encomenda_alvo["estado"] = "rejeitada"
                registar_evento(encomenda_alvo["id"], "rejeitada")
                guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)
                print("A encomenda foi rejeitada!")
        else:
            print("ID inválido.")

def atribuir_estafetas():
    encomendas = ler_csv("encomendas.csv")
    estafetas = ler_csv("estafetas.csv")
    atribuicoes = ler_csv("atribuicoes.csv")
    
    if not estafetas:
        print("Erro: Ficheiro estafetas.csv vazio ou inexistente.")
        return

    proximo_id_atrib = obter_proximo_id("atribuicoes.csv", "idAtribuicao")
    alterou = False

    for e in encomendas:
        if e["estado"] == "aprovada":
   
            elegiveis = [s for s in estafetas if s["zona"].lower() == e["zona"].lower() 
                         and s["disponibilidade"].lower() == "true"]
            
            if elegiveis:
                escolhido = min(elegiveis, key=lambda x: int(x["carga_trabalho"]))
                
                e["estado"] = "atribuida"
                e["idEstafeta"] = escolhido["idEstafeta"]
                escolhido["carga_trabalho"] = str(int(escolhido["carga_trabalho"]) + 1)
                
                atribuicoes.append({
                    "idAtribuicao": proximo_id_atrib,
                    "idPedido": e["id"],
                    "idEstafeta": escolhido["idEstafeta"],
                    "dataAtribuicao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                proximo_id_atrib += 1
                registar_evento(e["id"], "atribuida")
                alterou = True
                print(f"[+] ID {e['id']} atribuído ao estafeta {escolhido['nome']} ({escolhido['idEstafeta']})")

    if alterou:
        guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)
        guardar_csv("estafetas.csv", COL_ESTAFETAS, estafetas)
        guardar_csv("atribuicoes.csv", COL_ATRIBUICOES, atribuicoes)
    else:
        print("[!] Nenhuma atribuição nova foi possível.")

def cancelar_editar_encomenda():
    encomendas = ler_csv("encomendas.csv")
    if not encomendas:
        print("\n[!] Não existem encomendas registadas para gerir.")
        return

    id_alvo = input("\nIntroduza o ID da encomenda que deseja gerir: ").strip()
    
    encomenda = next((e for e in encomendas if str(e["id"]) == id_alvo), None)

    if not encomenda:
        print(f"[!] Erro: A encomenda com o ID {id_alvo} não foi encontrada.")
        return

    if encomenda["estado"] != "pendente":
        print(f"\n[!] Operação Negada: A encomenda está no estado '{encomenda['estado']}'.")
        print("Só é possível cancelar ou editar encomendas que ainda estejam 'pendente'.")
        return

    print(f"\n" + "-"*30)
    print(f"GESTÃO DA ENCOMENDA ID: {id_alvo} (PENDENTE)")
    print(f"Zona Atual:   {encomenda['zona']}")
    print(f"Prioridade:   {encomenda['prioridade']}")
    print("-"*30)
    print("1. Cancelar encomenda")
    print("2. Editar Detalhes (Zona/Prioridade)")
    print("3. Voltar ao Menu Principal")
    
    opcao = input("\nEscolha uma opção: ")

    if opcao == "1":
        encomenda["estado"] = "cancelada"
        guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)
        registar_evento(id_alvo, "cancelada")
        print(f"[V] Sucesso: Encomenda {id_alvo} marcada como 'cancelada'.")

    elif opcao == "2":
        print("\n(Deixe vazio para manter o valor atual)")
        nova_zona = input(f"Nova Zona [{encomenda['zona']}]: ").strip()
        nova_prio = input(f"Nova Prioridade [{encomenda['prioridade']}]: ").strip()

        alterou = False
        if nova_zona: 
            encomenda["zona"] = nova_zona
            alterou = True
        if nova_prio: 
            encomenda["prioridade"] = nova_prio
            alterou = True
        
        if alterou:
            guardar_csv("encomendas.csv", COL_ENCOMENDAS, encomendas)
            print("[V] Detalhes atualizados com sucesso.")
        else:
            print("[*] Nenhuma alteração foi efetuada.")

    elif opcao == "3":
        return
    else:
        print("[!] Opção inválida.")

def filtrar_encomendas():
    print("\n--- FILTRAR ENCOMENDAS ---")
    print("1-Estado | 2-Zona | 3-Cliente | 4-Data (AAAA-MM-DD) | 5-Prioridade")
    op = input("Opção: ")
    
    mapeamento = {
        "1": "estado", 
        "2": "zona", 
        "3": "idCliente", 
        "4": "dataCriacao", 
        "5": "prioridade"
    }
    
    campo = mapeamento.get(op)
    
    if not campo:
        print("[!] Opção inválida.")
        return

    valor = input(f"Procurar {campo} por: ").strip().lower()
    
    encomendas = ler_csv("encomendas.csv")
 
    resultados = [e for e in encomendas if valor in e.get(campo, "").lower()]
    
    if resultados:
        header = (f"{'ID':<3} | {'Cliente':<8} | {'Zona':<10} | {'Estado':<10} | {'Data':<11} | {'Prioridade'}")
        print("\n" + "="*75)
        print(header)
        print("-" * 75)
        for e in resultados:
            print(f"{e.get('id',''):<3} | {e.get('idCliente',''):<8} | "
                  f"{e.get('zona',''):<10} | {e.get('estado',''):<10} | "
                  f"{e.get('dataCriacao',''):<11} | {e.get('prioridade','')}")
        print("="*75)
        print(f"Total encontrado: {len(resultados)} encomendas.")
    else:
        print(f"\n[!] Sem resultados para {campo} = '{valor}'.")

def menu():
    garantir_csv("encomendas.csv", COL_ENCOMENDAS)
    garantir_csv("eventos_pedido.csv", COL_EVENTOS)
    garantir_csv("atribuicoes.csv", COL_ATRIBUICOES)
    garantir_csv("estafetas.csv", COL_ESTAFETAS)
    
    ZONAS_ATENDIDAS = ["Braga", "Guimarães", "Famalicão"]

    while True:
        importar_pedidos_do_cliente()
        print("\n" + "="*40)
        print("      SISTEMA DE GESTÃO LOGÍSTICA")
        print("="*40)
        print("1. Aprovar/Rejeitar Pedidos")
        print("2. Atribuir Estafetas")
        print("3. Cancelar/Editar Encomenda")
        print("4. Filtrar Encomendas")
        print("5. Listar Todas as Encomendas")
        print("6. Sair")
        
        op = input("\nOpção: ")
        if op == "1": aprovar_rejeitar_pedidos(ZONAS_ATENDIDAS)
        elif op == "2": atribuir_estafetas()
        elif op == "3": cancelar_editar_encomenda()
        elif op == "4": filtrar_encomendas()
        elif op == "5": listar_todas()
        elif op == "6": break
     

if __name__ == "__main__":
    menu()