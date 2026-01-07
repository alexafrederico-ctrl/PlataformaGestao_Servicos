import os
import pandas as pd
from typing import Optional
from datetime import datetime

# Caminhos para os CSV do cliente
CLIENT_DIR = os.path.join(os.path.dirname(__file__), '..', 'trabalhosIndividuais')
PEDIDOS_CSV = os.path.join(CLIENT_DIR, 'pedidos.csv')
EVENTOS_CSV = os.path.join(CLIENT_DIR, 'eventos_pedido.csv')
MENSAGENS_CSV = os.path.join(CLIENT_DIR, 'mensagens.csv')
MATERIALS_CSV = os.path.join(os.path.dirname(__file__), 'materials.csv')
AVALIACOES_CSV = os.path.join(CLIENT_DIR, 'avaliacoes.csv')

# Estados possíveis para tracking
ESTADOS_PEDIDO = [
    'Criado',
    'Confirmado',
    'Aprovado',
    'Em Processamento',
    'Em Distribuição',
    'Entregue',
    'Falhado',
    'Cancelado'
]

#  Regra de cancelamento: permitido apenas se ainda NÃO foi atribuído
# (ou seja, se ainda NÃO está "Em Processamento" nem depois)
ESTADOS_NAO_CANCELAVEIS = {
    'Em Processamento',
    'Em Distribuição',
    'Entregue',
    'Falhado',
    'Cancelado'
}

#  Schema fixo do tracking (agora com coluna Tracking)
EVENTOS_SCHEMA = ['PedidoID', 'ClienteID', 'Estado', 'Descricao', 'Timestamp', 'Tracking']

#  Schema para pedidos (para permitir atualização em ficheiro)
PEDIDOS_SCHEMA = [
    'PedidoID',
    'ClienteID',
    'Produto',
    'Quantidade',
    'Preço_Unitário',
    'Preço_Total',
    'Destino',
    'Avaliação',
    'Data',
    'Estado'
]

AVALIACOES_SCHEMA = [
    'PedidoID',
    'ClienteID',
    'Rating',
    'Comentario',
    'Timestamp'
]


# Importacao tardia do PortalCliente para evitar pedidos de input no arranque
def _get_portal_cliente_module():
    """Tenta importar o modulo PortalCliente de forma tardia.

    Isto evita que o PortalCliente execute codigo de topo (por exemplo, inputs)
    no momento em que o PortalServicos e importado. Devolve o modulo ou None.
    """
    try:
        import sys as _sys, importlib as _importlib
        _pc_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'trabalhosIndividuais'))
        if _pc_path not in _sys.path:
            _sys.path.insert(0, _pc_path)
        return _importlib.import_module('PortalCliente')
    except Exception:
        return None


# DataFrames globais (em memoria para acesso rapido)
DF_PEDIDOS = pd.DataFrame()
DF_EVENTOS = pd.DataFrame()
DF_MENSAGENS = pd.DataFrame()


def consultarEncomendas(iD, materiaisRequeridos, materiaisRequeridosQtd, zonaEncomendas):
    i = 0
    while i <= 2:
        print(
            "As encomendas pendentes são: " + chr(13) + str(iD[i]) +
            " - O material pedido foi " + materiaisRequeridos[i] +
            " com a quantidade de " + str(materiaisRequeridosQtd[i]) + "."
        )
        i = i + 1


def consultarEstafetas(profissionalZona, profissionalLivre):
    i = 0
    while i <= 2:
        if profissionalLivre[i] is True:
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
            while p < 9 and zona is True:
                if materiaisRequeridos[i] == materialsName[p]:
                    if materiaisRequeridosQtd[i] <= materialsQtd[p]:
                        stock = True
                        p = 1000
                    else:
                        p = 10000
                else:
                    p = p + 1
        if zona is True and stock is True:
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
                while k < tamanhoProfissionais and atribuido is False:
                    if zonaEncomendas[i] == profissionalZona[k] and profissionalLivre[k] is True:
                        print("Encomenda " + str(iD[i]) + ": Atribuída ao Profissional " + str(k))
                        estadoEncomenda[i] = "Em Processamento"
                        profissionalLivre[k] = False
                        atribuido = True
                    else:
                        k = k + 1
                if atribuido is False:
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
    opçoes = int(input())
    return opçoes


def init_inventario():
    # Inventario partilhado de produtos (usa o conjunto maior do gestor)
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


def _read_csv_if_exists(path: str) -> pd.DataFrame:
    """
    Helper robusto: lê CSV sem converter valores para NaN,
    e tenta manter tudo como string para evitar "nan" no tracking.
    """
    try:
        if os.path.exists(path):
            df = pd.read_csv(
                path,
                dtype=str,
                keep_default_na=False,
                na_filter=False,
                encoding='utf-8'
            )

            # normalizar ClienteID
            if 'ClienteID' in df.columns:
                df['ClienteID'] = df['ClienteID'].astype(str).str.strip()
                df.loc[df['ClienteID'] == '', 'ClienteID'] = 'unknown'

            # normalizar PedidoID/Estado quando existirem
            if 'PedidoID' in df.columns:
                df['PedidoID'] = df['PedidoID'].astype(str).str.strip()
            if 'Estado' in df.columns:
                df['Estado'] = df['Estado'].astype(str).str.strip()

            return df
    except Exception as e:
        print(f"Erro ao ler {path}: {e}")
    return pd.DataFrame()


def load_all_client_csvs() -> None:
    """Carrega todos os CSV do cliente para DataFrames globais (DF_PEDIDOS, DF_EVENTOS, DF_MENSAGENS)."""
    global DF_PEDIDOS, DF_EVENTOS, DF_MENSAGENS
    DF_PEDIDOS = _read_csv_if_exists(PEDIDOS_CSV)
    DF_EVENTOS = _read_csv_if_exists(EVENTOS_CSV)
    DF_MENSAGENS = _read_csv_if_exists(MENSAGENS_CSV)


def load_pedidos() -> pd.DataFrame:
    """Devolve o DataFrame de pedidos (carrega do disco se necessario)."""
    global DF_PEDIDOS
    if DF_PEDIDOS.empty:
        load_all_client_csvs()
    return DF_PEDIDOS


def load_eventos() -> pd.DataFrame:
    """Devolve o DataFrame de eventos (carrega do disco se necessario)."""
    global DF_EVENTOS
    if DF_EVENTOS.empty:
        load_all_client_csvs()
    return DF_EVENTOS


def load_mensagens() -> pd.DataFrame:
    """Devolve o DataFrame de mensagens (carrega do disco se necessario)."""
    global DF_MENSAGENS
    if DF_MENSAGENS.empty:
        load_all_client_csvs()
    return DF_MENSAGENS


def load_cliente_pedidos():
    """Wrapper de compatibilidade usado noutros pontos do ficheiro."""
    return load_pedidos()


def load_cliente_eventos():
    return load_eventos()


def load_cliente_mensagens():
    return load_mensagens()


def load_materials_dataframe():
    """Carrega o ficheiro `materials.csv` (usa pandas).

    Devolve pandas.DataFrame ou list[dict] (fallback com parsing manual).
    """
    try:
        return _read_csv_if_exists(MATERIALS_CSV)
    except Exception:
        import csv
        rows = []
        if os.path.exists(MATERIALS_CSV):
            with open(MATERIALS_CSV, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    try:
                        r['Quantity'] = int(r.get('Quantity', 0))
                    except Exception:
                        r['Quantity'] = 0
                    try:
                        r['Price'] = float(r.get('Price', 0))
                    except Exception:
                        r['Price'] = 0.0
                    rows.append(r)
        return rows


# ============= SISTEMA DE tracking EM TEMPO REAL =============
def criar_evento_pedido(pedido_id: str, novo_estado: str, cliente_id: str, descricao: str = "") -> dict:
    """
    Cria um novo evento de tracking para um pedido.
     Agora também preenche a coluna "Tracking" no eventos_pedido.csv
    """
    if novo_estado not in ESTADOS_PEDIDO:
        print(f"⚠ Estado '{novo_estado}' não reconhecido. Estados válidos: {ESTADOS_PEDIDO}")
        novo_estado = 'Criado'

    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    evento = {
        'PedidoID': str(pedido_id).strip(),
        'ClienteID': str(cliente_id).strip() if cliente_id else 'unknown',
        'Estado': str(novo_estado).strip(),
        'Descricao': str(descricao) if descricao is not None else "",
        'Timestamp': ts,
        #  Coluna extra pedida: Tracking (texto pronto)
        'Tracking': f"{ts} → {str(novo_estado).strip()}"
    }
    return evento


def _normalizar_eventos_schema(df: pd.DataFrame) -> pd.DataFrame:
    """
    Garante que o DF de eventos tem as colunas do schema.
    Se vierem colunas diferentes (ex: de outro módulo), isto evita NaN.
     Inclui a coluna "Tracking".
    """
    if df is None or df.empty:
        return pd.DataFrame(columns=EVENTOS_SCHEMA)

    # criar colunas em falta
    for c in EVENTOS_SCHEMA:
        if c not in df.columns:
            df[c] = ""

    # manter apenas schema (ignora lixo)
    df = df[EVENTOS_SCHEMA].copy()

    # normalizar tipos/trim
    for c in EVENTOS_SCHEMA:
        df[c] = df[c].astype(str).str.strip()

    # evitar 'nan' literal
    df = df.replace({'nan': ''})
    df.loc[df['ClienteID'] == '', 'ClienteID'] = 'unknown'

    # se vier algum evento antigo sem tracking, tenta preencher de forma automática
    if 'Tracking' in df.columns:
        mask = df['Tracking'].astype(str).str.strip() == ""
        if mask.any():
            df.loc[mask, 'Tracking'] = df.loc[mask].apply(
                lambda r: f"{r.get('Timestamp','')} → {r.get('Estado','')}".strip(),
                axis=1
            )

    return df


def registar_evento_pedido(evento: dict) -> None:
    """
    Registra um evento de tracking no CSV de eventos.
    Cada mudança de estado cria uma entrada nova.
    CRIAÇÃO CSV'S CASO NÃO EXISTA! SE JÁ EXISTIR, APENAS ATUALIZA!
    """
    global DF_EVENTOS

    try:
        df_novo = pd.DataFrame([evento])
        df_novo = _normalizar_eventos_schema(df_novo)

        df_existentes = load_eventos()
        df_existentes = _normalizar_eventos_schema(df_existentes)

        df_final = pd.concat([df_existentes, df_novo], ignore_index=True)

        os.makedirs(os.path.dirname(EVENTOS_CSV) or '.', exist_ok=True)
        df_final.to_csv(EVENTOS_CSV, index=False, encoding='utf-8')

        DF_EVENTOS = df_final

        print(f"✓ Evento registado: {evento['Estado']} para pedido {evento['PedidoID']}")

    except Exception as e:
        print(f"✗ Erro ao registar evento: {e}")


def obter_estado_atual_pedido(pedido_id: str) -> str:
    """
    Obtém o estado atual de um pedido (último evento registado).
    """
    df_eventos = load_eventos()
    df_eventos = _normalizar_eventos_schema(df_eventos)

    if df_eventos.empty:
        return 'Desconhecido'

    pedido_id = str(pedido_id).strip()
    pedido_eventos = df_eventos[df_eventos['PedidoID'] == pedido_id]

    if pedido_eventos.empty:
        return 'Desconhecido'

    pedido_eventos = pedido_eventos.sort_values('Timestamp', ascending=True)
    ultimo_evento = pedido_eventos.iloc[-1]

    estado = str(ultimo_evento.get('Estado', '')).strip()
    if not estado or estado.lower() == 'nan':
        return 'Desconhecido'
    return estado


def obter_historico_pedido(pedido_id: str) -> pd.DataFrame:
    """
    Obtém o histórico completo de tracking de um pedido.
    """
    df_eventos = load_eventos()
    df_eventos = _normalizar_eventos_schema(df_eventos)

    if df_eventos.empty:
        return pd.DataFrame(columns=EVENTOS_SCHEMA)

    pedido_id = str(pedido_id).strip()
    pedido_eventos = df_eventos[df_eventos['PedidoID'] == pedido_id].copy()

    if not pedido_eventos.empty:
        pedido_eventos = pedido_eventos.sort_values('Timestamp', ascending=True)

    return pedido_eventos


# ================== PEDIDOS.CSV helpers (atualização em ficheiro) ==================
def _normalizar_pedidos_schema(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=PEDIDOS_SCHEMA)

    # cria colunas em falta
    for c in PEDIDOS_SCHEMA:
        if c not in df.columns:
            df[c] = ""

    # mantem schema
    df = df[PEDIDOS_SCHEMA].copy()

    # trim
    for c in PEDIDOS_SCHEMA:
        df[c] = df[c].astype(str).str.strip()

    df = df.replace({'nan': ''})
    df.loc[df['ClienteID'] == '', 'ClienteID'] = 'unknown'
    return df


def _normalizar_avaliacoes_schema(df: pd.DataFrame) -> pd.DataFrame:
    if df is None or df.empty:
        return pd.DataFrame(columns=AVALIACOES_SCHEMA)

    for c in AVALIACOES_SCHEMA:
        if c not in df.columns:
            df[c] = ""

    df = df[AVALIACOES_SCHEMA].copy()

    for c in AVALIACOES_SCHEMA:
        df[c] = df[c].astype(str).str.strip()

    return df.replace({'nan': ''})


def load_avaliacoes() -> pd.DataFrame:
    """Lê avaliações do ficheiro (retorna vazio se não existir)."""
    return _normalizar_avaliacoes_schema(_read_csv_if_exists(AVALIACOES_CSV))


def registar_avaliacao_servico(pedido_id: str, cliente_id: str, rating: int, comentario: str = "") -> bool:
    """Regista uma avaliação 1-5 em avaliacoes.csv depois de validar que o pedido está concluído."""
    try:
        rating_int = int(rating)
    except Exception:
        print("Avaliação inválida. Indique um número entre 1 e 5.")
        return False

    if rating_int < 1 or rating_int > 5:
        print("Avaliação inválida. Indique um número entre 1 e 5.")
        return False

    estado_atual = obter_estado_atual_pedido(pedido_id)
    estado_normalizado = estado_atual.lower()
    if not any(s in estado_normalizado for s in ["entregue", "conclu"]):
        print(f"Pedido {pedido_id} ainda não está concluído (estado atual: {estado_atual}).")
        return False

    registo = {
        'PedidoID': str(pedido_id).strip(),
        'ClienteID': str(cliente_id).strip() if cliente_id else 'unknown',
        'Rating': str(rating_int),
        'Comentario': str(comentario).strip(),
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    try:
        df_existentes = load_avaliacoes()
        df_novo = _normalizar_avaliacoes_schema(pd.DataFrame([registo]))
        df_final = pd.concat([df_existentes, df_novo], ignore_index=True)

        os.makedirs(os.path.dirname(AVALIACOES_CSV) or '.', exist_ok=True)
        df_final.to_csv(AVALIACOES_CSV, index=False, encoding='utf-8')
        return True
    except Exception as e:
        print(f"Erro ao registar avaliação: {e}")
        return False


def salvar_pedido_csv_local(
    pedido_id: str,
    cliente_id: str,
    produtos_nome: list,
    encomendas: list,
    produtos_preco: list,
    destino: str,
    avaliacao: str,
    estado: str,
) -> None:
    """
    Guarda o pedido no pedidos.csv com PedidoID + Estado (para permitir atualizar quando cancelar).
    Cria 1 linha por produto com quantidade > 0.
    """
    global DF_PEDIDOS

    try:
        now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        linhas = []
        for i in range(len(produtos_nome)):
            try:
                qtd = float(encomendas[i])
            except Exception:
                qtd = 0.0
            if qtd > 0:
                try:
                    pu = float(produtos_preco[i])
                except Exception:
                    pu = 0.0
                linhas.append({
                    'PedidoID': str(pedido_id).strip(),
                    'ClienteID': str(cliente_id).strip() if cliente_id else 'unknown',
                    'Produto': str(produtos_nome[i]),
                    'Quantidade': str(qtd),
                    'Preço_Unitário': str(pu),
                    'Preço_Total': str(qtd * pu),
                    'Destino': str(destino),
                    'Avaliação': str(avaliacao),
                    'Data': now_str,
                    'Estado': str(estado).strip()
                })

        if not linhas:
            return

        df_novo = pd.DataFrame(linhas)
        df_exist = load_pedidos()
        df_exist = _normalizar_pedidos_schema(df_exist)

        df_final = pd.concat([df_exist, _normalizar_pedidos_schema(df_novo)], ignore_index=True)

        os.makedirs(os.path.dirname(PEDIDOS_CSV) or '.', exist_ok=True)
        df_final.to_csv(PEDIDOS_CSV, index=False, encoding='utf-8')

        DF_PEDIDOS = df_final

    except Exception as e:
        print(f"✗ Erro ao salvar pedido em pedidos.csv: {e}")


def atualizar_estado_pedido_csv(pedido_id: str, novo_estado: str) -> None:
    """
    Atualiza pedidos.csv (coluna Estado) para todas as linhas do PedidoID.
    """
    global DF_PEDIDOS
    try:
        df = load_pedidos()
        df = _normalizar_pedidos_schema(df)
        if df.empty:
            return

        pid = str(pedido_id).strip()
        mask = df['PedidoID'].astype(str).str.strip() == pid
        if not mask.any():
            return

        df.loc[mask, 'Estado'] = str(novo_estado).strip()

        os.makedirs(os.path.dirname(PEDIDOS_CSV) or '.', exist_ok=True)
        df.to_csv(PEDIDOS_CSV, index=False, encoding='utf-8')
        DF_PEDIDOS = df
    except Exception as e:
        print(f"✗ Erro ao atualizar estado no pedidos.csv: {e}")


# ================== REGRA DE CANCELAMENTO ==================
def pedido_pode_ser_cancelado(pedido_id: str) -> bool:
    estado_atual = obter_estado_atual_pedido(pedido_id)
    if estado_atual in ESTADOS_NAO_CANCELAVEIS:
        return False
    return True


def cancelar_pedido(pedido_id: str, cliente_id: str, motivo: str = "") -> bool:
    """
    Cancela pedido:
      - só se NÃO estiver atribuído (não estar em "Em Processamento" nem depois)
      - cria evento "Cancelado"
      - atualiza pedidos.csv (Estado)
      - cria mensagem
    """
    try:
        pid = str(pedido_id).strip()
        if not pid:
            print("✗ PedidoID inválido.")
            return False

        estado_atual = obter_estado_atual_pedido(pid)
        if not pedido_pode_ser_cancelado(pid):
            print(f"✗ Não é possível cancelar. Estado atual: '{estado_atual}' (já atribuído ou finalizado).")
            return False

        desc = "Pedido cancelado pelo cliente."
        if motivo:
            desc += f" Motivo: {motivo}"

        ok = alterar_estado_pedido(pid, 'Cancelado', cliente_id, desc)
        if ok:
            atualizar_estado_pedido_csv(pid, 'Cancelado')
            return True
        return False
    except Exception as e:
        print(f"✗ Erro ao cancelar pedido: {e}")
        return False


def alterar_estado_pedido(pedido_id: str, novo_estado: str, cliente_id: str, descricao: str = "") -> bool:
    """
    Altera o estado de um pedido criando um novo evento.
     Integra regra de cancelamento: só cancela se não atribuído.
    """
    try:
        pedido_id = str(pedido_id).strip()
        novo_estado = str(novo_estado).strip()

        #  regra integrada
        if novo_estado == 'Cancelado':
            if not pedido_pode_ser_cancelado(pedido_id):
                estado_atual = obter_estado_atual_pedido(pedido_id)
                print(f"✗ Cancelamento bloqueado. Estado atual: '{estado_atual}' (já atribuído ou finalizado).")
                return False

        estado_anterior = obter_estado_atual_pedido(pedido_id)

        evento = criar_evento_pedido(pedido_id, novo_estado, cliente_id, descricao)
        registar_evento_pedido(evento)

        mensagem = f"Pedido {pedido_id}: Estado alterado de '{estado_anterior}' para '{novo_estado}'"
        if descricao:
            mensagem += f" - {descricao}"
        salvar_mensagem_tracking(cliente_id, 'Atualização de Estado', mensagem)

        #  Atualiza também pedidos.csv (se existir o PedidoID)
        try:
            atualizar_estado_pedido_csv(pedido_id, novo_estado)
        except Exception:
            pass

        return True

    except Exception as e:
        print(f"✗ Erro ao alterar estado: {e}")
        return False


def salvar_mensagem_tracking(cliente_id: str, tipo: str, mensagem: str) -> None:
    """
    Salva uma mensagem de tracking (confirmações, avisos, etc).
    """
    global DF_MENSAGENS

    try:
        msg_dict = {
            'ClienteID': str(cliente_id).strip() if cliente_id else 'unknown',
            'Tipo': tipo,
            'Mensagem': mensagem,
            'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        df_novo = pd.DataFrame([msg_dict])
        df_existentes = load_mensagens()

        if df_existentes.empty:
            df_final = df_novo
        else:
            df_final = pd.concat([df_existentes, df_novo], ignore_index=True)

        os.makedirs(os.path.dirname(MENSAGENS_CSV) or '.', exist_ok=True)
        df_final.to_csv(MENSAGENS_CSV, index=False, encoding='utf-8')

        DF_MENSAGENS = df_final

    except Exception as e:
        print(f"✗ Erro ao salvar mensagem: {e}")


# ================== OPÇÃO B ==================
def resolver_pedido_id(input_id: str) -> str:
    """
    Permite ao gestor/cliente escrever:
      - ID completo (ex: 1998_20251228213057) -> retorna igual
      - só ClienteID (ex: 1998) -> resolve para o PedidoID mais recente desse cliente (prefixo 1998_)
    """
    input_id = str(input_id).strip()
    if not input_id:
        return input_id

    if "_" in input_id:
        return input_id

    df_eventos = _normalizar_eventos_schema(load_eventos())
    if df_eventos.empty:
        return input_id

    prefixo = input_id + "_"
    candidatos = df_eventos[df_eventos["PedidoID"].astype(str).str.startswith(prefixo)].copy()
    if candidatos.empty:
        return input_id

    candidatos = candidatos.sort_values("Timestamp", ascending=True)
    return str(candidatos.iloc[-1]["PedidoID"]).strip()


# ------------------ Cliente functions (adapted) ------------------
def apresentacaoProd(produtosNome, produtosPreco):
    print("Lista de Produtos")
    for i in range(0, len(produtosNome)):
        print(str(i + 1) + "- " + produtosNome[i] + "(" + str(produtosPreco[i]) + " eur/uni)")


def avaliar_servico(cliente_id: Optional[str]):
    print("\n=== AVALIAR SERVIÇO ===")
    pedido_id_input = input("ID do pedido: ").strip()
    if not pedido_id_input:
        pedido_id_input = str(cliente_id).strip() if cliente_id else ""

    if not pedido_id_input:
        print("Nenhum pedido indicado.")
        return

    pedido_id = resolver_pedido_id(pedido_id_input)
    if pedido_id != pedido_id_input:
        print(f"PedidoID resolvido automaticamente: {pedido_id}")

    rating = input("Avaliação (1-5): ").strip()
    comentario = input("Comentário (opcional): ").strip()

    if registar_avaliacao_servico(pedido_id, cliente_id, rating, comentario):
        print("Avaliação registada com sucesso. Obrigado pelo feedback!")


def calcTotal(encomendas, produtoPreco):
    total = 0
    for i in range(0, len(encomendas)):
        total = total + encomendas[i] * produtoPreco[i]
    return total


def consultaPed(produtosNome, encomendas, produtosPreco, destinos, td):
    for i in range(0, len(encomendas)):
        print(produtosNome[i] + " com a quantidade de " + str(encomendas[i]) + " e com o preço de " + str(
            encomendas[i] * produtosPreco[i]))
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
            print("Boa escolha!")
            break


def escolherDestino(destinosOpcao):
    print("Escolha o destino: ")
    for i in range(0, len(destinosOpcao)):
        print(str(i + 1) + " - " + destinosOpcao[i])
    escolha = int(input())
    return escolha


def cliente_menu():
    print("##### Menu Cliente #####")
    print("1 - Lista de produtos")
    print("2 - Fazer pedido de produto")
    print("3 - Consultar lista de produtos encomendados")
    print("4 - Cancelar pedido")
    print("5 - Avaliar serviço")
    print("6 - Sair")
    option = int(input())
    return option


def validacaoStock(produtosNome, produtosQtd, encomendas, produtosPreco):
    for i in range(0, len(encomendas)):
        if encomendas[i] > 0:
            if encomendas[i] > produtosQtd[i]:
                print("Encomendas-te " + produtosNome[i] + "(" + str(
                    encomendas[i]) + "). A quantidade encomendada é superior à quantidade máxima do stock " + str(
                    produtosQtd[i]))
                print("A sua encomenda poderá demorar mais tempo até obter o stock necessário!")
            else:
                produtosQtd[i] = produtosQtd[i] - encomendas[i]
                print(" - " + produtosNome[i] + " com a quantidade de " + str(encomendas[i]) + " e o preço de " + str(
                    encomendas[i] * produtosPreco[i]))


# Cliente main
def cliente_main(produtosNome, produtosQtd, produtosPreco):
    destinosOpcao = [""] * 3
    destinos = [""] * 3
    encomendas = [0] * len(produtosNome)

    destinosOpcao[0] = "Braga"
    destinosOpcao[1] = "Fafe"
    destinosOpcao[2] = "Guimarães"

    chamadaMenu = 0
    td = 0

    print("PORTAL DO CLIENTE")
    try:
        CLIENT_ID = input("Insira o seu ID de cliente: ").strip()
    except Exception:
        CLIENT_ID = None

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

            # ===== tracking EM TEMPO REAL =====
            #  ID automático do pedido (ClienteID + timestamp)
            pedido_id = f"{CLIENT_ID}_{datetime.now().strftime('%Y%m%d%H%M%S')}"

            evento_criacao = criar_evento_pedido(
                pedido_id,
                'Criado',
                CLIENT_ID,
                f"Pedido criado com {sum(1 for e in encomendas if e > 0)} produtos para {destinos[td - 1]}"
            )
            registar_evento_pedido(evento_criacao)

            alterar_estado_pedido(
                pedido_id,
                'Confirmado',
                CLIENT_ID,
                f"Pedido confirmado. Total: {total}€"
            )

            #  Guardar também em pedidos.csv
            try:
                salvar_pedido_csv_local(
                    pedido_id=pedido_id,
                    cliente_id=CLIENT_ID,
                    produtos_nome=produtosNome,
                    encomendas=encomendas,
                    produtos_preco=produtosPreco,
                    destino=destinos[td - 1],
                    avaliacao="",
                    estado='Confirmado'
                )
            except Exception:
                pass

            # (Opcional) manter PortalCliente para mensagens
            try:
                pc = _get_portal_cliente_module()
                if pc is not None:
                    try:
                        pc.CLIENT_ID = CLIENT_ID
                    except Exception:
                        pass
                    try:
                        pc.salvar_mensagens_csv("Confirmação",
                                                f"Pedido confirmado para {destinos[td - 1]} - Total: {total}€")
                    except Exception:
                        pass
                    try:
                        load_all_client_csvs()
                    except Exception:
                        pass
            except Exception:
                pass

            chamadaMenu = 1

        elif opcao == 3:
            try:
                df_pedidos = load_cliente_pedidos()
                if df_pedidos is not None and not df_pedidos.empty and CLIENT_ID is not None and 'ClienteID' in df_pedidos.columns:
                    df_pedidos = _normalizar_pedidos_schema(df_pedidos)
                    df_my = df_pedidos.loc[df_pedidos['ClienteID'] == CLIENT_ID]
                    if not df_my.empty:
                        print("\n=== ENCOMENDAS ===")
                        print(df_my.to_string(index=False))

                        df_eventos = _normalizar_eventos_schema(load_eventos())
                        if not df_eventos.empty and CLIENT_ID:
                            df_eventos_cliente = df_eventos[df_eventos['ClienteID'] == CLIENT_ID]
                            if not df_eventos_cliente.empty:
                                print("\n=== Tracking EM TEMPO REAL ===")
                                df_eventos_cliente = df_eventos_cliente.sort_values('Timestamp', ascending=True)

                                for _, evento in df_eventos_cliente.iterrows():
                                    ts = str(evento.get('Timestamp', ''))
                                    est = str(evento.get('Estado', ''))
                                    desc = str(evento.get('Descricao', ''))
                                    pid = str(evento.get('PedidoID', ''))
                                    track = str(evento.get('Tracking', ''))
                                    print(f"  • {ts} → {est:20s} | {pid} | TRACK: {track} | ({desc[:60]})")

                                pedidos_unicos = df_eventos_cliente['PedidoID'].unique()
                                print("\n  ➤ ESTADO ATUAL:")
                                for pid in pedidos_unicos:
                                    estado = obter_estado_atual_pedido(pid)
                                    print(f"    {pid}: {estado}")
                            else:
                                print("\n  Sem eventos de Tracking ainda.")
                    else:
                        print("Nenhuma encomenda encontrada para o seu ID.")
                else:
                    consultaPed(produtosNome, encomendas, produtosPreco, destinos, td)
            except Exception as e:
                print(f"Erro ao consultar pedidos: {e}")
                consultaPed(produtosNome, encomendas, produtosPreco, destinos, td)
            chamadaMenu = 1

        elif opcao == 4:
            #  Cancelar pedido (só se não atribuído)
            print("\n=== CANCELAR PEDIDO ===")
            print("Podes inserir o ID.")
            pid_in = input("ID do pedido (ENTER para cancelar o mais recente): ").strip()

            if not pid_in:
                pid_in = str(CLIENT_ID).strip() if CLIENT_ID else ""

            pedido_id = resolver_pedido_id(pid_in)
            if pedido_id != pid_in:
                print(f"✓ PedidoID resolvido automaticamente: {pedido_id}")

            motivo = input("Motivo (opcional): ").strip()
            ok = cancelar_pedido(pedido_id, CLIENT_ID, motivo)
            if ok:
                print(f"✓ Pedido {pedido_id} cancelado com sucesso.")
            else:
                print(f"✗ Não foi possível cancelar o pedido {pedido_id}.")

            try:
                load_all_client_csvs()
            except Exception:
                pass

            chamadaMenu = 1

        elif opcao == 5:
            avaliar_servico(CLIENT_ID)
            chamadaMenu = 1

        elif opcao == 6:
            chamadaMenu = 0

        else:
            print("Opção inválida")
            chamadaMenu = 1

        if chamadaMenu != 1:
            break

    print("Continuação de um ótimo dia")


# ------------------ Gestor functions ------------------
def encomendasAprovadas(produtosNome, produtosQtd, produtosPreco):
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

        while p < len(produtosNome) and zona is True:
            if materiaisRequeridos[i] == produtosNome[p]:
                if materiaisRequeridosQtd[i] <= produtosQtd[p]:
                    stock = True
                    break
                else:
                    break
            p = p + 1

        if zona is True and stock is True:
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
            while k < tamanhoProfissionais and atribuido is False:
                if zonaEncomendas[i] == profissionalZona[k] and profissionalLivre[k] is True:
                    print("Encomenda " + str(iD[i]) + ": Atribuída ao Profissional " + str(k))
                    estadoEncomenda[i] = "Em Processamento"
                    profissionalLivre[k] = False
                    atribuido = True
                else:
                    k = k + 1
            if atribuido is False:
                print("Encomenda " + str(iD[i]) + ": NENHUM Estafeta DISPONÍVEL (Aguardar Atribuição)")
                estadoEncomenda[i] = "Aguardar Atribuição"
        i = i + 1


def gestor_menu():
    print("*****MENU*****")
    print("1 - Consultar encomendas pendentes")
    print("2 - Consultar zonas atendidas")
    print("3 - Consultar estafetas disponíveis")
    print("4 - Consultar encomendas aprovadas")
    print("5 - Consultar pedidos do cliente (CSV)")
    print("6 - Consultar eventos de pedidos (tracking)")
    print("7 - Consultar mensagens (confirmações/avisos)")
    print("8 - Alterar estado de um pedido")
    print("9 - Ver histórico de um pedido")
    print("10 - Listar pedidos filtrados (estado/zona)")
    print("11 - Sair")
    opcoes = int(input())
    return opcoes


def consultarEncomendas(iD, materiaisRequeridos, materiaisRequeridosQtd, zonaEncomendas, zonasAtendidas):
    i = 0
    while i < len(iD):
        print(
            "As encomendas pendentes são: " + chr(13) + str(iD[i]) +
            " - O material pedido foi " + materiaisRequeridos[i] +
            " com a quantidade de " + str(materiaisRequeridosQtd[i]) + "."
        )
        i = i + 1


def consultarEstafetas(profissionalZona, profissionalLivre):
    i = 0
    while i < len(profissionalZona):
        if profissionalLivre[i] is True:
            print("O Estafeta " + str(i) + " encontra-se na zona " + profissionalZona[i] + ".")
        i = i + 1


def consultarZonas(zonasAtendidas):
    i = 0
    while i < len(zonasAtendidas):
        print("As zonas atendidas são: " + chr(13) + zonasAtendidas[i] + ".")
        i = i + 1


def listar_pedidos_filtrados_estado_zona():
    """Lista pedidos com filtros opcionais por Estado e Destino (zona)."""
    df = load_cliente_pedidos()
    df = _normalizar_pedidos_schema(df)

    if df.empty:
        print("Nenhum pedido encontrado.")
        return

    coluna_avaliacao = None
    if 'Avaliação' in df.columns:
        coluna_avaliacao = 'Avaliação'
    elif 'AvaliaÇõÇœo' in df.columns:
        coluna_avaliacao = 'AvaliaÇõÇœo'

    if coluna_avaliacao:
        df_avaliacoes = load_avaliacoes()
        df_avaliacoes = _normalizar_avaliacoes_schema(df_avaliacoes)
        if not df_avaliacoes.empty:
            df_avaliacoes = df_avaliacoes.sort_values('Timestamp', ascending=True)
            mapa_avaliacoes = df_avaliacoes.groupby('PedidoID', as_index=False).last()
            mapa_avaliacoes = dict(zip(mapa_avaliacoes['PedidoID'], mapa_avaliacoes['Rating']))
            vazio = df[coluna_avaliacao].astype(str).str.strip() == ''
            if vazio.any():
                df.loc[vazio, coluna_avaliacao] = df.loc[vazio, 'PedidoID'].map(mapa_avaliacoes).fillna('')

    print("\n=== FILTRO DE PEDIDOS ===")
    print("Estados disponíveis:")
    for i, est in enumerate(ESTADOS_PEDIDO, 1):
        print(f"  {i} - {est}")
    estado_in = input("Estado (ENTER para todos ou escolha acima): ").strip()
    zona_in = input("Zona/Destino (ENTER para todas): ").strip()

    filtrado = df.copy()

    if estado_in:
        if estado_in.isdigit():
            idx = int(estado_in) - 1
            if 0 <= idx < len(ESTADOS_PEDIDO):
                estado_in = ESTADOS_PEDIDO[idx]
        filtrado = filtrado[filtrado['Estado'].str.lower() == estado_in.lower()]

    if zona_in:
        filtrado = filtrado[filtrado['Destino'].str.lower().str.contains(zona_in.lower(), na=False)]

    if filtrado.empty:
        print("Nenhum pedido encontrado com esses filtros.")
        return

    cols = [c for c in ['PedidoID', 'ClienteID', 'Produto', 'Quantidade', 'Destino', 'Estado', 'Data', 'Avaliação'] if
            c in filtrado.columns]
    print("\n=== RESULTADO ===")
    print(filtrado[cols].to_string(index=False))


def gestor_main(produtosNome, produtosQtd, produtosPreco):
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
        try:
            load_all_client_csvs()
        except Exception:
            pass

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
            df_pedidos = _normalizar_pedidos_schema(load_cliente_pedidos())
            if df_pedidos is not None and not df_pedidos.empty:
                print("\n=== PEDIDOS DO CLIENTE ===")
                print(df_pedidos.to_string(index=False))
            else:
                print("Nenhum pedido do cliente encontrado.")
            print("******************************")
            voltar = 1

        elif opcoes == 6:
            df_eventos = _normalizar_eventos_schema(load_cliente_eventos())
            if df_eventos is not None and not df_eventos.empty:
                print("\n=== EVENTOS DE PEDIDOS (TRACKING) ===")
                df_eventos = df_eventos.sort_values('Timestamp', ascending=True)
                for _, evento in df_eventos.iterrows():
                    pid_full = str(evento.get('PedidoID', 'N/A'))
                    est = str(evento.get('Estado', 'N/A'))
                    ts = str(evento.get('Timestamp', 'N/A'))
                    desc = str(evento.get('Descricao', ''))[:40]
                    track = str(evento.get('Tracking', ''))
                    print(f"  {pid_full} | {est:20s} | {ts} | TRACK: {track} | {desc}")
            else:
                print("✗ Nenhum evento de pedido encontrado.")
            print("******************************")
            voltar = 1

        elif opcoes == 7:
            df_mensagens = load_cliente_mensagens()
            if df_mensagens is not None and not df_mensagens.empty:
                print("\n=== MENSAGENS (CONFIRMAÇÕES/AVISOS) ===")
                print(df_mensagens.to_string(index=False))
            else:
                print("Nenhuma mensagem encontrada.")
            print("******************************")
            voltar = 1

        elif opcoes == 8:
            print("\n=== ALTERAR ESTADO DE PEDIDO ===")

            pedido_id_input = input("Insira o ID do pedido: ").strip()
            pedido_id = resolver_pedido_id(pedido_id_input)
            if pedido_id != pedido_id_input:
                print(f"✓ PedidoID resolvido automaticamente: {pedido_id}")

            print("Estados disponíveis:")
            for i, estado in enumerate(ESTADOS_PEDIDO, 1):
                print(f"{i} - {estado}")

            opcao_estado = int(input("Escolha o novo estado: ")) - 1

            if 0 <= opcao_estado < len(ESTADOS_PEDIDO):
                novo_estado = ESTADOS_PEDIDO[opcao_estado]
                descricao = input("Descrição da alteração (opcional): ").strip()

                cliente_id = "gestor"
                try:
                    df_eventos = _normalizar_eventos_schema(load_eventos())
                    if df_eventos is not None and not df_eventos.empty:
                        evs = df_eventos[df_eventos['PedidoID'] == pedido_id]
                        if not evs.empty:
                            cliente_id = str(evs.iloc[0].get('ClienteID', cliente_id)).strip() or cliente_id
                except Exception:
                    cliente_id = "gestor"

                sucesso = alterar_estado_pedido(pedido_id, novo_estado, cliente_id, descricao)
                if sucesso:
                    print(f"✓ Estado do pedido {pedido_id} alterado para '{novo_estado}'")
                else:
                    print(f"✗ Erro ao alterar estado do pedido")
            else:
                print("Opção inválida.")
            print("******************************")
            voltar = 1

        elif opcoes == 9:
            print("\n=== HISTÓRICO DE Tracking ===")

            pedido_id_input = input("Insira o ID do pedido: ").strip()
            pedido_id = resolver_pedido_id(pedido_id_input)
            if pedido_id != pedido_id_input:
                print(f"✓ PedidoID resolvido automaticamente: {pedido_id}")

            df_historico = obter_historico_pedido(pedido_id)

            if not df_historico.empty:
                print(f"\nPedido: {pedido_id}")
                print("-" * 70)
                for _, evento in df_historico.iterrows():
                    ts = str(evento.get('Timestamp', ''))
                    est = str(evento.get('Estado', ''))
                    desc = str(evento.get('Descricao', ''))
                    track = str(evento.get('Tracking', ''))
                    print(f"{ts} | {est:20s} | TRACK: {track} | {desc}")
                print("-" * 70)

                estado_atual = obter_estado_atual_pedido(pedido_id)
                print(f"\n➤ Estado Atual: {estado_atual}")
            else:
                print(f"✗ Nenhum evento encontrado para o pedido {pedido_id}")
            print("******************************")
            voltar = 1

        elif opcoes == 10:
            listar_pedidos_filtrados_estado_zona()
            print("******************************")
            voltar = 1

        elif opcoes == 11:
            voltar = 0

        else:
            print("Insira um número entre 1-11")
            voltar = 1

        if voltar != 1:
            break

    print("Sistema finalizado com sucesso")


# ------------------ Estafeta functions ------------------
def aceitarRecusar(tarefas, anomalia, timestamps, estado, estadoAtual, contadorSucesso, contadorTarefas):
    var_return = 0
    print("Existem as seguintes encomendas atribuídas com os IDs no ínicio e contacto no final:")
    for i in range(0, len(tarefas)):
        print(str(1 + i) + ") " + tarefas[i])
    while True:
        print("Qual o ID da encomenda que pretende aceitar ou trocar de estado?(No caso de querer recusar digite outro número qualquer)")
        idTarefa = int(input())
        if 1 <= idTarefa <= len(tarefas):
            print("Qual operação pretende executar:\n1-Aceitar atribuição;\n2- Trocar estado operacional da encomenda;")
            x = int(input())
            if x == 1:
                print("O estado da sua tarefa está em recolha.")
                estadoAtual[idTarefa - 1] = estado[0]
                contadorTarefas[idTarefa - 1] = 1
            else:
                if x == 2:
                    print("Digite para que estado pretende alterar a tarefa escolhida:")
                    for i in range(0, len(estado)):
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
            for i in range(0, len(anomalia)):
                print(str(i + 1) + ")" + anomalia[i])
            motivo = int(input())
            print("Introduza a data e hora no formato DD/MM/AAAA HH:MM.")
            timestamp = input()
            print("O motivo pela qual a encomenda não vai ser entregue é o seguinte: " + anomalia[motivo - 1] +
                  " E a data e hora que o estafeta relatou a anomalia foi: " + timestamp)
            timestamps[idTarefa - 1] = timestamp
        print("Se pretender aceitar/ recusar/ trocar de estado alguma outra encomenda, digite 1.")
        var_return = int(input())
        if var_return != 1:
            break


def tarefasAtribuidas(tarefas):
    print("---Lista de tarefas atribuídas---")
    for i in range(0, len(tarefas)):
        print(str(i + 1) + ") " + tarefas[i])


def estafeta_menu():
    print("----MENU ESTAFETA----")
    print("1) Lista de tarefas atribuídas;")
    print("2) Aceitar e recusar atribuição e trocar estado operacional de encomenda;")
    print("3) Registar localização;")
    print("4) Reportar anomalias;")
    print("5) Consultar dados pessoais;")
    print("6) Sair;")
    opcao = int(input())
    return opcao


def estafeta_main():
    contadorTarefas = [0] * 4
    contadorSucesso = [0] * 4
    timestamps = [""] * 4
    anomalia = [""] * 5
    estadoAtual = [""] * 4
    localizacao = [""] * 4
    tarefas = [""] * 4
    estado = [""] * 4

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
    print("Seja bem vindo ao portal do estafeta, qual o seu nome?")
    nome = input()
    print("O que o/a " + nome + " deseja fazer?")
    for i in range(0, len(contadorTarefas)):
        contadorTarefas[i] = 0
    for i in range(0, len(contadorSucesso)):
        contadorSucesso[i] = 0

    while True:
        opcao = estafeta_menu()
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
        if menuCall != 1:
            break
    print("Obrigado por trabalhar connosco!")


# ------------------ Portal Gestão de Produtos ------------------
def calcfinal_prod(pedidoprodutoQtd, materialsPrice):
    endcalc = 0
    for i in range(0, len(pedidoprodutoQtd)):
        endcalc = endcalc + pedidoprodutoQtd[i] * materialsPrice[i]
    return endcalc


def materialconsultation_prod(materialsName, materialsPrice, materialsQtd):
    for i in range(0, len(materialsName)):
        print(materialsName[i] + ": " + str(materialsPrice[i]) + "€ || stock : " + str(materialsQtd[i]))


def gestao_produtos_menu():
    print("Menu Gestão de Produtos:")
    print("1 - Consultar materiais")
    print("2 - Colocar materiais no carrinho")
    print("3 - Finalização do pedido")
    print("4 - Sair")
    option = int(input())
    return option


def stockupdate_prod(materialsQtd, pedidoprodutoQtd):
    for i in range(0, len(pedidoprodutoQtd)):
        materialsQtd[i] = materialsQtd[i] - pedidoprodutoQtd[i]


def validstock_prod(materialsQtd, pedidoprodutoQtd, materialsName):
    for i in range(0, len(pedidoprodutoQtd)):
        if pedidoprodutoQtd[i] > 0:
            if pedidoprodutoQtd[i] > materialsQtd[i]:
                print("A sua encomenda ultrapassa o nosso limite de stock de " + materialsName[i])
            else:
                print("A sua encomenda de " + materialsName[i] + " foi validada com sucesso")


def gestao_produtos_main():
    materialsName = [""] * 10
    materialsQtd = [0] * 10
    materialsPrice = [0] * 10
    pedidoprodutoQtd = [0] * 10

    for i in range(0, len(pedidoprodutoQtd)):
        pedidoprodutoQtd[i] = 0

    materialsName[0] = "Tintas"
    materialsName[1] = "Martelo"
    materialsName[2] = "Parafusos"
    materialsName[3] = "Pincéis"
    materialsName[4] = "Verniz"
    materialsName[5] = "Nivelador"
    materialsName[6] = "Lixa"
    materialsName[7] = "Aparafusador"
    materialsName[8] = "Fita métrica"
    materialsName[9] = "Serra"

    materialsQtd[0] = 10
    materialsQtd[1] = 100
    materialsQtd[2] = 6
    materialsQtd[3] = 6
    materialsQtd[4] = 10
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
    menuCall = 0

    while True:
        option = gestao_produtos_menu()
        if option == 1:
            materialconsultation_prod(materialsName, materialsPrice, materialsQtd)
            menuCall = 1
        elif option == 2:
            while True:
                print("Indique o material desejado (número):")
                for i in range(0, len(materialsName)):
                    print(str(i) + " - " + materialsName[i])
                i = int(input())
                print("Que quantidade de " + materialsName[i] + " deseja?")
                pedidoprodutoQtd[i] = float(input())
                validstock_prod(materialsQtd, pedidoprodutoQtd, materialsName)
                stockupdate_prod(materialsQtd, pedidoprodutoQtd)
                print("Deseja adicionar mais artigos ao carrinho? Digite 1 para sim")
                repeat = int(input())
                if repeat != 1:
                    break
            endcalc = calcfinal_prod(pedidoprodutoQtd, materialsPrice)
            menuCall = 1
        elif option == 3:
            endcalc = calcfinal_prod(pedidoprodutoQtd, materialsPrice)
            print("O preço do seu carrinho é de " + str(endcalc) + "€")
            print("O seu pedido encontra-se finalizado, obrigado pelo seu voto de confiança.")
            menuCall = 0
        elif option == 4:
            menuCall = 0
        else:
            print("Opção inválida")
            menuCall = 1

        if menuCall != 1:
            break


def main():
    produtosNome, produtosQtd, produtosPreco = init_inventario()
    while True:
        print("Escolha o portal:")
        print("1 - Portal Gestor")
        print("2 - Portal Cliente")
        print("3 - Portal Estafeta")
        print("4 - Portal Gestão Produtos")
        print("5 - Sair")
        escolha = int(input())
        if escolha == 1:
            gestor_main(produtosNome, produtosQtd, produtosPreco)
        elif escolha == 2:
            cliente_main(produtosNome, produtosQtd, produtosPreco)
        elif escolha == 3:
            estafeta_main()
        elif escolha == 4:
            gestao_produtos_main()
        elif escolha == 5:
            break
        else:
            print("Escolha inválida")
    print("Aplicação terminada")


if __name__ == '__main__':
    main()
