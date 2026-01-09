import os
import csv
import pandas as pd
from typing import Optional
from datetime import datetime, timedelta

#--------------------------------------------------------------------------------- Portal Cliente (Alexandra)-------------------------------------------------------------------------------------------------
# Caminhos para os CSV do cliente
CLIENT_DIR = os.path.join(os.path.dirname(__file__), '..', 'trabalhoFinal')
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

# DataFrames globais (em memoria para acesso rapido)
DF_PEDIDOS = pd.DataFrame()
DF_EVENTOS = pd.DataFrame()
DF_MENSAGENS = pd.DataFrame()
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


def resolver_pedido_id_cliente(input_id: str) -> str:
    """
    Resolve apenas com pedidos existentes em pedidos.csv (portal cliente).
    Se indicar apenas ClienteID, escolhe o pedido mais recente que não esteja cancelado.
    """
    input_id = str(input_id).strip()
    if not input_id:
        return input_id
    if "_" in input_id:
        return input_id
    df_pedidos = _normalizar_pedidos_schema(load_pedidos())
    if df_pedidos.empty or 'ClienteID' not in df_pedidos.columns or 'PedidoID' not in df_pedidos.columns:
        return input_id
    df_cli = df_pedidos[df_pedidos['ClienteID'].astype(str).str.strip() == input_id].copy()
    if df_cli.empty:
        return input_id
    if 'Estado' in df_cli.columns:
        df_nao_cancel = df_cli[df_cli['Estado'].astype(str).str.lower() != 'cancelado']
        if not df_nao_cancel.empty:
            df_cli = df_nao_cancel
    if 'Data' in df_cli.columns:
        data_series = pd.to_datetime(df_cli['Data'], errors='coerce')
        if data_series.notna().any():
            df_cli = df_cli.assign(_data_ord=data_series).sort_values('_data_ord', ascending=True)
            return str(df_cli.iloc[-1]['PedidoID']).strip()
    return str(df_cli.iloc[-1]['PedidoID']).strip()

def _obter_produtos_do_catalogo():
    try:
        catalogo = load_catalog()
    except Exception:
        return None
    produtos = [m for m in catalogo if m.get('ativo') and m.get('tipo') == 'produto']
    if not produtos:
        return None
    nomes = [str(m.get('nome', '')).strip() for m in produtos]
    qtds = []
    precos = []
    for m in produtos:
        try:
            qtds.append(int(float(m.get('stock', 0) or 0)))
        except Exception:
            qtds.append(0)
        try:
            precos.append(float(m.get('preco', 0) or 0))
        except Exception:
            precos.append(0.0)
    return nomes, qtds, precos

def _obter_destinos_de_estafetas():
    try:
        estafetas = ler_csv("estafetas.csv")
    except Exception:
        return []
    zonas = []
    for e in estafetas:
        zona = str(e.get("zona", "")).strip()
        if zona and zona not in zonas:
            zonas.append(zona)
    return zonas

def _pedido_existe_em_pedidos_csv(pedido_id: str) -> bool:
    df_pedidos = _normalizar_pedidos_schema(load_pedidos())
    if df_pedidos.empty or 'PedidoID' not in df_pedidos.columns:
        return False
    pid = str(pedido_id).strip()
    return (df_pedidos['PedidoID'].astype(str).str.strip() == pid).any()

def _pedido_existe_em_encomendas_csv(pedido_id: str) -> bool:
    encomendas = ler_csv("encomendas.csv")
    if not encomendas:
        return False
    pid = str(pedido_id).strip()
    return any(str(e.get("id", "")).strip() == pid or str(e.get("idOriginal", "")).strip() == pid for e in encomendas)


# Funcoes do Cliente
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
    pedido_id = resolver_pedido_id_cliente(pedido_id_input)
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
        while True:
            try:
                produtoSelecionado = int(input())
                break
            except Exception:
                print("Valor invalido. Insira um numero inteiro.")
        if produtoSelecionado > len(produtosNome) or produtoSelecionado == 0:
            print("Escolha inválida")
        else:
            print("Indique a quantidade")
            while True:
                try:
                    qtd = float(input())
                    break
                except Exception:
                    print("Valor invalido. Insira um numero.")
            encomendas[produtoSelecionado - 1] = encomendas[produtoSelecionado - 1] + qtd
        print("Quer adicionar mais produtos? Se sim, insere 1")
        while True:
            try:
                repeat = int(input())
                break
            except Exception:
                print("Valor invalido. Insira um numero inteiro.")
        if repeat != 1:
            print("Boa escolha!")
            break
def escolherDestino(destinosOpcao):
    print("Escolha o destino: ")
    for i in range(0, len(destinosOpcao)):
        print(str(i + 1) + " - " + destinosOpcao[i])
    while True:
        try:
            escolha = int(input())
            break
        except Exception:
            print("Valor invalido. Insira um numero inteiro.")
    return escolha
def cliente_menu():
    print("##### Menu Cliente #####")
    print("1 - Lista de produtos")
    print("2 - Fazer pedido de produto")
    print("3 - Consultar lista de produtos encomendados")
    print("4 - Cancelar pedido")
    print("5 - Avaliar serviço")
    print("6 - Sair")
    while True:
        try:
            option = int(input())
            break
        except Exception:
            print("Valor invalido. Insira um numero inteiro.")
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
# Portal Cliente (principal)
def cliente_main(produtosNome, produtosQtd, produtosPreco):
    catalogo_produtos = _obter_produtos_do_catalogo()
    if catalogo_produtos:
        produtosNome, produtosQtd, produtosPreco = catalogo_produtos
    destinosOpcao = _obter_destinos_de_estafetas()
    if not destinosOpcao:
        destinosOpcao = ["Braga", "Fafe", "Guimarães"]
    destinos = [""] * max(3, len(destinosOpcao))
    encomendas = [0] * len(produtosNome)
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
            print("Indique o destino da encomenda:")
            escolha = escolherDestino(destinosOpcao)
            destinos[td] = destinosOpcao[escolha - 1]
            td = td + 1
            total = calcTotal(encomendas, produtosPreco)
            print("Obrigado pela encomenda. O total da encomenda é " + str(total) + " eur")
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
                                print("\n  Sem eventos de tracking ainda.")
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
            print("Pode inserir o ID.")
            pid_in = input("ID do pedido (ENTER para cancelar o mais recente): ").strip()
            if not pid_in:
                pid_in = str(CLIENT_ID).strip() if CLIENT_ID else ""
            pedido_id = resolver_pedido_id_cliente(pid_in)
            if pedido_id != pid_in:
                print(f"✓ PedidoID resolvido automaticamente: {pedido_id}")
            if not _pedido_existe_em_pedidos_csv(pedido_id) or not _pedido_existe_em_encomendas_csv(pedido_id):
                print("Não foi possível cancelar: a encomenda não existe nos registos.")
                chamadaMenu = 1
                continue
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
#--------------------------------------------------------------------------------- Gestor de encomendas (SARA)-------------------------------------------------------------------------------------------------

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

# ================= CSV(Mecanismos) =================

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
 
#================= FUNCIONALIDADES =================
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

def gestor_main():
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

# ------------------ ------------------ ------------------ ------------------ Estafeta functions (JOÂO)---------------------------- ------------------ ------------------ ------------------ ------------------ --------

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
    print("6) Mostrar métricas pessoais;")
    print("7) Sair;")

    opcao = input().strip()
    return opcao
def estafeta_main():
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
            salvar = input("Deseja gravar métricas em 'metricas_estafeta.csv'? (s/n): ").strip().lower().startswith('s')
            mostrar_metricas(idEstafeta, gravar=salvar)
        
        elif opc == "7":
            print("Obrigado por trabalhar connosco!")
            break
        else:
            print("Opção inválida. Tente novamente.")

# ------------------------------------------------------------------------------------------ Portal Gestão de Produtos (MARIA)------------------------------------------------------------------------------------------
 
def calcfinal(pedidoprodutoQtd, materials):
    # Calculate the total price of items in the cart
    endcalc = 0
    for i in range(len(pedidoprodutoQtd)):
        endcalc += pedidoprodutoQtd[i] * materials[i]['preco']
    return endcalc

def materialconsultation(materials):
    # Display all active items with their details
    for material in materials:
        if material['ativo']:
            tipo_str = "Produto" if material['tipo'] == 'produto' else "Serviço"
            stock_str = str(material['stock']) if material['stock'] is not None else 'N/A'
            print(f"{material['nome']} ({tipo_str}): {material['preco']}€ || stock: {stock_str}")

def gestao_produtos_main():
    # Display the main menu and get user choice
    print("Menu:")
    print("1 - consultar materiais ")
    print("2 - Colocar materias no carrinho ")
    print("3 - Finalização do pedido")
    print("4 - Adicionar novo material")
    print("5 - Filtrar materiais")
    print("6 - Registrar entrada de stock")
    print("7 - Gerir serviços")
    print("8 - Ver indicadores")
    print("9 - Editar item do catálogo")
    print("10 - Remover item do catálogo")
    print("11 - Listar por categoria")
    print("12 - Listar por faixa de preço")
    print("13 - Listar itens ativos")
    print("14 - Listar produtos sem stock")
    option = int(input())
    return option

def stockupdate(materials, pedidoprodutoQtd):
    for i in range(len(pedidoprodutoQtd)):
        if pedidoprodutoQtd[i] > 0:
            if materials[i]['stock'] is not None:
                if materials[i]['stock'] - pedidoprodutoQtd[i] < 0:
                    print(f"Erro: Operação resultaria em stock negativo para {materials[i]['nome']}. Operação bloqueada.")
                    pedidoprodutoQtd[i] = 0  # reset to prevent
                    continue
                materials[i]['stock'] -= pedidoprodutoQtd[i]
                log_stock_movement(materials[i]['id'], 'saida', pedidoprodutoQtd[i], 'venda')

def validstock(materials, pedidoprodutoQtd):
    for i in range(len(pedidoprodutoQtd)):
        if pedidoprodutoQtd[i] > 0:
            if materials[i]['stock'] is not None and pedidoprodutoQtd[i] > materials[i]['stock']:
                print(f" A sua encomenda ultrapassa o nosso limite de stock de {materials[i]['nome']}")
            else:
                print(f"A sua encomenda de {materials[i]['nome']} foi validada com sucesso")

def add_new_material(materials):
    tipo = input("Tipo (produto/servico): ").lower().strip()
    if tipo not in ['produto', 'servico']:
        print("Tipo deve ser produto ou servico")
        return
    nome = input("Nome do material/serviço: ")
    descricao = input("Descrição: ")
    categoria = input("Categoria: ")
    preco = float(input("Preço: "))
    if preco < 0:
        print("Preço deve ser >= 0")
        return
    if tipo == 'servico':
        duracao_str = input("Duração padrão em minutos: ")
        try:
            duracaoPadraoMin = int(duracao_str)
            if duracaoPadraoMin <= 0:
                print("Duração deve ser positiva.")
                return
        except ValueError:
            print("Duração inválida.")
            return
        stock = None
    else:
        duracao_str = input("Duração padrão em minutos (opcional, pressione Enter para pular): ")
        duracaoPadraoMin = int(duracao_str) if duracao_str else None
        stock_str = input("Stock (opcional, pressione Enter para pular): ")
        stock = int(stock_str) if stock_str else None
        if stock is not None and stock < 0:
            print("Stock deve ser >= 0")
            return
    ativo_str = input("Ativo (true/false): ").lower()
    if ativo_str not in ['true', 'false']:
        print("Ativo deve ser true ou false")
        return
    ativo = ativo_str == 'true'
    
    # Auto ID
    if materials:
        new_id = max(m['id'] for m in materials) + 1
    else:
        new_id = 0
    
    new_material = {
        'id': new_id,
        'tipo': tipo,
        'nome': nome,
        'descricao': descricao,
        'categoria': categoria,
        'preco': preco,
        'duracaoPadraoMin': duracaoPadraoMin,
        'stock': stock,
        'ativo': ativo
    }
    materials.append(new_material)
    save_catalog(materials)
    print("Material/Serviço adicionado com sucesso!")

def edit_item(materials):
    try:
        id_to_edit = int(input("Digite o ID do item a editar: "))
    except ValueError:
        print("ID inválido.")
        return
    
    item = None
    for m in materials:
        if m['id'] == id_to_edit:
            item = m
            break
    
    if item is None:
        print(f"Item com ID {id_to_edit} não encontrado.")
        return
    
    print("Item atual:")
    print(f"Nome: {item['nome']}")
    print(f"Tipo: {item['tipo']}")
    print(f"Preço: {item['preco']}")
    print(f"Descrição: {item['descricao']}")
    print(f"Ativo: {item['ativo']}")
    
    while True:
        print("O que deseja alterar?")
        print("1 - Preço")
        print("2 - Descrição")
        print("3 - Ativar/Desativar")
        print("4 - Sair")
        try:
            choice = int(input("Opção: "))
        except ValueError:
            print("Opção inválida.")
            continue
        
        if choice == 1:
            try:
                new_price = float(input("Novo preço: "))
                if new_price < 0:
                    print("Preço não pode ser negativo.")
                    continue
                item['preco'] = new_price
                print("Preço alterado com sucesso.")
            except ValueError:
                print("Preço inválido.")
        
        elif choice == 2:
            new_desc = input("Nova descrição: ")
            item['descricao'] = new_desc
            print("Descrição alterada com sucesso.")
        
        elif choice == 3:
            ativo_str = input("Ativo (true/false): ").lower().strip()
            if ativo_str not in ['true', 'false']:
                print("Valor deve ser true ou false.")
                continue
            item['ativo'] = ativo_str == 'true'
            print("Status ativo alterado com sucesso.")
        
        elif choice == 4:
            break
        
        else:
            print("Opção inválida.")
    
    save_catalog(materials)
    print("Alterações salvas.")

def remove_item(materials, turnos):
    try:
        id_to_remove = int(input("Digite o ID do item a remover: "))
    except ValueError:
        print("ID inválido.")
        return
    
    item = None
    for m in materials:
        if m['id'] == id_to_remove:
            item = m
            break
    
    if item is None:
        print(f"Item com ID {id_to_remove} não encontrado.")
        return
    
    print("Item a remover:")
    print(f"Nome: {item['nome']}")
    print(f"Tipo: {item['tipo']}")
    print(f"Preço: {item['preco']}")
    print(f"Descrição: {item['descricao']}")
    print(f"Ativo: {item['ativo']}")
    
    confirm = input("Tem certeza que deseja remover este item? (s/n): ").lower().strip()
    if confirm != 's':
        print("Remoção cancelada.")
        return
    
    materials.remove(item)
    # Remove associated turnos
    turnos[:] = [t for t in turnos if t['id'] != id_to_remove]
    
    save_catalog(materials)
    save_turnos(turnos)
    print("Item removido com sucesso.")

def list_by_category(materials):
    category = input("Categoria: ").strip()
    filtered = []
    for m in materials:
        if m['categoria'].lower() == category.lower():
            filtered.append(m)
    if not filtered:
        print(f"Nenhum item encontrado na categoria '{category}'.")
        return
    print(f"Itens na categoria '{category}':")
    for m in filtered:
        tipo_str = "Produto" if m['tipo'] == 'produto' else "Serviço"
        stock_str = str(m['stock']) if m['stock'] is not None else 'N/A'
        print(f"{m['nome']} ({tipo_str}): {m['preco']}€ || stock: {stock_str}")

def list_by_price_range(materials):
    try:
        min_price = float(input("Preço mínimo: "))
        max_price = float(input("Preço máximo: "))
        if min_price < 0 or max_price < 0 or min_price > max_price:
            print("Valores inválidos.")
            return
    except ValueError:
        print("Preços inválidos.")
        return
    filtered = []
    for m in materials:
        if min_price <= m['preco'] <= max_price:
            filtered.append(m)
    if not filtered:
        print(f"Nenhum item encontrado na faixa de preço {min_price}€ - {max_price}€.")
        return
    print(f"Itens na faixa de preço {min_price}€ - {max_price}€:")
    for m in filtered:
        tipo_str = "Produto" if m['tipo'] == 'produto' else "Serviço"
        stock_str = str(m['stock']) if m['stock'] is not None else 'N/A'
        print(f"{m['nome']} ({tipo_str}): {m['preco']}€ || stock: {stock_str}")

def list_active_items(materials):
    filtered = []
    for m in materials:
        if m['ativo']:
            filtered.append(m)
    if not filtered:
        print("Nenhum item ativo encontrado.")
        return
    print("Itens ativos:")
    for m in filtered:
        tipo_str = "Produto" if m['tipo'] == 'produto' else "Serviço"
        stock_str = str(m['stock']) if m['stock'] is not None else 'N/A'
        print(f"{m['nome']} ({tipo_str}): {m['preco']}€ || stock: {stock_str}")

def list_out_of_stock_products(materials):
    filtered = []
    for m in materials:
        if m['tipo'] == 'produto' and m['stock'] == 0:
            filtered.append(m)
    if not filtered:
        print("Nenhum produto sem stock encontrado.")
        return
    print("Produtos sem stock:")
    for m in filtered:
        print(f"{m['nome']}: {m['preco']}€")

def filter_materials(materials):
    print("Filtros (pressione Enter para ignorar):")
    tipo = input("Tipo (produto/servico/ambos): ").lower().strip()
    categoria = input("Categoria: ").strip()
    preco_min_str = input("Preço mínimo: ").strip()
    preco_max_str = input("Preço máximo: ").strip()
    ativo_str = input("Ativo (true/false/ambos): ").lower().strip()
    stock_min_str = input("Stock mínimo: ").strip()
    
    tipo_filter = None
    if tipo == 'produto':
        tipo_filter = 'produto'
    elif tipo == 'servico':
        tipo_filter = 'servico'
    
    preco_min = float(preco_min_str) if preco_min_str else None
    preco_max = float(preco_max_str) if preco_max_str else None
    stock_min = int(stock_min_str) if stock_min_str else None
    ativo_filter = None
    if ativo_str == 'true':
        ativo_filter = True
    elif ativo_str == 'false':
        ativo_filter = False
    
    filtered = []
    for m in materials:
        if tipo_filter and m['tipo'] != tipo_filter:
            continue
        if categoria and m['categoria'].lower() != categoria.lower():
            continue
        if preco_min is not None and m['preco'] < preco_min:
            continue
        if preco_max is not None and m['preco'] > preco_max:
            continue
        if ativo_filter is not None and m['ativo'] != ativo_filter:
            continue
        if stock_min is not None and (m['stock'] is None or m['stock'] < stock_min):
            continue
        filtered.append(m)
    
    # Print table
    if not filtered:
        print("Nenhum material encontrado com os filtros aplicados.")
        return
    
    print(f"{'ID':<5} {'Tipo':<10} {'Nome':<20} {'Categoria':<15} {'Preço':<10} {'Stock':<10} {'Ativo':<6}")
    print("-" * 80)
    for m in filtered:
        tipo_str = "Produto" if m['tipo'] == 'produto' else "Serviço"
        stock_str = str(m['stock']) if m['stock'] is not None else 'N/A'
        ativo_str = 'Sim' if m['ativo'] else 'Não'
        print(f"{m['id']:<5} {tipo_str:<10} {m['nome']:<20} {m['categoria']:<15} {m['preco']:<10.2f} {stock_str:<10} {ativo_str:<6}")

def log_stock_movement(id, tipo, quantidade, motivo):
    filename = 'stock_movements.csv'
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'tipo', 'quantidade', 'data_hora', 'motivo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'id': id,
            'tipo': tipo,
            'quantidade': quantidade,
            'data_hora': datetime.now().isoformat(),
            'motivo': motivo
        })

def register_stock_entry(materials):
    print("Materiais disponíveis:")
    for i, m in enumerate(materials):
        if m['tipo'] == 'produto':
            print(f"{i}: {m['nome']} (Stock atual: {m['stock']})")
    try:
        idx = int(input("Índice do material: "))
        if idx < 0 or idx >= len(materials) or materials[idx]['tipo'] != 'produto':
            print("Índice inválido ou não é produto.")
            return
        quantidade = int(input("Quantidade a adicionar: "))
        if quantidade <= 0:
            print("Quantidade deve ser positiva.")
            return
        motivo = input("Motivo da entrada: ").strip()
        materials[idx]['stock'] = (materials[idx]['stock'] or 0) + quantidade
        log_stock_movement(materials[idx]['id'], 'entrada', quantidade, motivo)
        save_catalog(materials)
        print("Entrada de stock registrada com sucesso.")
    except ValueError:
        print("Entrada inválida.")

def load_turnos(filename='turnos.csv'):
    turnos = []
    if os.path.exists(filename):
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                turno = {
                    'id': int(row.get('id', row.get('idItem', 0))),
                    'data': row['data'],
                    'hora_inicio': row['hora_inicio'],
                    'hora_fim': row['hora_fim'],
                    'disponivel': row['disponivel'].lower() == 'true'
                }
                turnos.append(turno)
    return turnos

def save_turnos(turnos, filename='turnos.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'data', 'hora_inicio', 'hora_fim', 'disponivel']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for turno in turnos:
            writer.writerow({
                'id': turno['id'],
                'data': turno['data'],
                'hora_inicio': turno['hora_inicio'],
                'hora_fim': turno['hora_fim'],
                'disponivel': str(turno['disponivel'])
            })

def generate_slots(materials, turnos):
    print("Serviços disponíveis:")
    services = [m for m in materials if m['tipo'] == 'servico' and m['ativo']]
    for i, s in enumerate(services):
        print(f"{i}: {s['nome']} (Duração: {s['duracaoPadraoMin']} min)")
    try:
        idx = int(input("Índice do serviço: "))
        if idx < 0 or idx >= len(services):
            print("Índice inválido.")
            return
        service = services[idx]
        data = input("Data (YYYY-MM-DD): ").strip()
        # Assume 9:00 to 18:00, slots of duration
        start = datetime.strptime(f"{data} 09:00", "%Y-%m-%d %H:%M")
        end = datetime.strptime(f"{data} 18:00", "%Y-%m-%d %H:%M")
        duration = timedelta(minutes=service['duracaoPadraoMin'])
        current = start
        while current + duration <= end:
            hora_inicio = current.strftime("%H:%M")
            hora_fim = (current + duration).strftime("%H:%M")
            # Check if already exists
            exists = any(t['id'] == service['id'] and t['data'] == data and t['hora_inicio'] == hora_inicio for t in turnos)
            if not exists:
                turnos.append({
                    'id': service['id'],
                    'data': data,
                    'hora_inicio': hora_inicio,
                    'hora_fim': hora_fim,
                    'disponivel': True
                })
            current += duration
        save_turnos(turnos)
        print("Slots gerados com sucesso.")
    except ValueError:
        print("Entrada inválida.")

def book_slot(materials, turnos):
    print("Serviços disponíveis:")
    services = [m for m in materials if m['tipo'] == 'servico' and m['ativo']]
    for i, s in enumerate(services):
        print(f"{i}: {s['nome']}")
    try:
        idx = int(input("Índice do serviço: "))
        if idx < 0 or idx >= len(services):
            print("Índice inválido.")
            return
        service = services[idx]
        data = input("Data (YYYY-MM-DD): ").strip()
        available_slots = [t for t in turnos if t['id'] == service['id'] and t['data'] == data and t['disponivel']]
        if not available_slots:
            print("Nenhum slot disponível para essa data.")
            return
        print("Slots disponíveis:")
        for i, slot in enumerate(available_slots):
            print(f"{i}: {slot['hora_inicio']} - {slot['hora_fim']}")
        slot_idx = int(input("Índice do slot: "))
        if slot_idx < 0 or slot_idx >= len(available_slots):
            print("Índice inválido.")
            return
        slot = available_slots[slot_idx]
        slot['disponivel'] = False
        save_turnos(turnos)
        print("Slot reservado com sucesso.")
    except ValueError:
        print("Entrada inválida.")

def manage_services(materials, turnos):
    while True:
        print("Gestão de Serviços:")
        print("1 - Gerar slots para um serviço")
        print("2 - Reservar slot")
        print("3 - Adicionar turno manualmente")
        print("4 - Voltar")
        try:
            option = int(input("Opção: "))
            if option == 1:
                generate_slots(materials, turnos)
            elif option == 2:
                book_slot(materials, turnos)
            elif option == 3:
                add_manual_slot(materials, turnos)
            elif option == 4:
                break
            else:
                print("Opção inválida.")
        except ValueError:
            print("Entrada inválida.")

def add_manual_slot(materials, turnos):
    print("Serviços disponíveis:")
    services = [m for m in materials if m['tipo'] == 'servico' and m['ativo']]
    for i, s in enumerate(services):
        print(f"{i}: {s['nome']} (Duração: {s['duracaoPadraoMin']} min)")
    try:
        idx = int(input("Índice do serviço: "))
        if idx < 0 or idx >= len(services):
            print("Índice inválido.")
            return
        service = services[idx]
        data = input("Data (YYYY-MM-DD): ").strip()
        hora_inicio_str = input("Hora de início (HH:MM): ").strip()
        start = datetime.strptime(f"{data} {hora_inicio_str}", "%Y-%m-%d %H:%M")
        duration = timedelta(minutes=service['duracaoPadraoMin'])
        end = start + duration
        hora_fim = end.strftime("%H:%M")
        
        # Check for overlaps
        existing_turnos = [t for t in turnos if t['id'] == service['id'] and t['data'] == data]
        overlap = False
        for t in existing_turnos:
            t_start = datetime.strptime(f"{data} {t['hora_inicio']}", "%Y-%m-%d %H:%M")
            t_end = datetime.strptime(f"{data} {t['hora_fim']}", "%Y-%m-%d %H:%M")
            if not (end <= t_start or start >= t_end):
                overlap = True
                break
        if overlap:
            print("Sobreposição de horário com turno existente.")
            return
        
        turnos.append({
            'id': service['id'],
            'data': data,
            'hora_inicio': hora_inicio_str,
            'hora_fim': hora_fim,
            'disponivel': True
        })
        save_turnos(turnos)
        print("Turno adicionado com sucesso.")
    except ValueError:
        print("Entrada inválida.")

def show_indicators(materials):
    # Display various indicators about the catalog
    print("Indicadores:")
    
    # Count active items
    total_active = 0
    active_products = 0
    active_services = 0
    for item in materials:
        if item['ativo']:
            total_active += 1
            if item['tipo'] == 'produto':
                active_products += 1
            elif item['tipo'] == 'servico':
                active_services += 1
    print(f"Número total de itens ativos: {total_active}")
    print(f"Número de produtos ativos: {active_products}")
    print(f"Número de serviços ativos: {active_services}")
    
    # Find products with low stock
    low_stock_items = []
    for item in materials:
        if item['tipo'] == 'produto' and item['ativo'] and item['stock'] is not None and item['stock'] <= 5:
            low_stock_items.append(item)
    if low_stock_items:
        print("Produtos com stock baixo (≤ 5):")
        for item in low_stock_items:
            print(f"  - {item['nome']}: {item['stock']}")
    else:
        print("Nenhum produto com stock baixo.")
    
    # Calculate average price per category
    from collections import defaultdict
    price_sums = defaultdict(float)
    price_counts = defaultdict(int)
    for item in materials:
        if item['ativo']:
            price_sums[item['categoria']] += item['preco']
            price_counts[item['categoria']] += 1
    print("Preço médio por categoria:")
    for category in sorted(price_sums.keys()):
        average_price = price_sums[category] / price_counts[category]
        print(f"  - {category}: {average_price:.2f}€")
    
    # Calculate average duration per category for services
    duration_sums = defaultdict(float)
    duration_counts = defaultdict(int)
    for item in materials:
        if item['ativo'] and item['tipo'] == 'servico' and item['duracaoPadraoMin'] is not None:
            duration_sums[item['categoria']] += item['duracaoPadraoMin']
            duration_counts[item['categoria']] += 1
    if duration_counts:
        print("Duração média por categoria (serviços):")
        for category in sorted(duration_sums.keys()):
            average_duration = duration_sums[category] / duration_counts[category]
            print(f"  - {category}: {average_duration:.1f} min")
    else:
        print("Duração média por categoria (serviços):")
        print("  - Nenhum serviço com duração definida.")

def load_catalog(filename='catalogo.csv'):
    # Load catalog from CSV file, with validations
    materials = []
    if not os.path.exists(filename):
        # Create default catalog if file doesn't exist
        default_data = [
            {'id': 0, 'tipo': 'produto', 'nome': 'tintas', 'descricao': '', 'categoria': 'ferramentas', 'preco': 11.0, 'duracaoPadraoMin': None, 'stock': 10, 'ativo': True},
            {'id': 1, 'tipo': 'produto', 'nome': 'martelo', 'descricao': '', 'categoria': 'ferramentas', 'preco': 1.6, 'duracaoPadraoMin': None, 'stock': 100, 'ativo': True},
            {'id': 2, 'tipo': 'produto', 'nome': 'parafusos', 'descricao': '', 'categoria': 'ferramentas', 'preco': 5.0, 'duracaoPadraoMin': None, 'stock': 6, 'ativo': True},
            {'id': 3, 'tipo': 'produto', 'nome': 'pincéis', 'descricao': '', 'categoria': 'ferramentas', 'preco': 9.0, 'duracaoPadraoMin': None, 'stock': 6, 'ativo': True},
            {'id': 4, 'tipo': 'produto', 'nome': 'vernizes', 'descricao': '', 'categoria': 'ferramentas', 'preco': 14.0, 'duracaoPadraoMin': None, 'stock': 10, 'ativo': True},
            {'id': 5, 'tipo': 'produto', 'nome': 'nivelador', 'descricao': '', 'categoria': 'ferramentas', 'preco': 23.0, 'duracaoPadraoMin': None, 'stock': 15, 'ativo': True},
            {'id': 6, 'tipo': 'produto', 'nome': 'lixa', 'descricao': '', 'categoria': 'ferramentas', 'preco': 1.0, 'duracaoPadraoMin': None, 'stock': 150, 'ativo': True},
            {'id': 7, 'tipo': 'produto', 'nome': 'aparafusador', 'descricao': '', 'categoria': 'ferramentas', 'preco': 55.0, 'duracaoPadraoMin': None, 'stock': 3, 'ativo': True},
            {'id': 8, 'tipo': 'produto', 'nome': 'fita métrica', 'descricao': '', 'categoria': 'ferramentas', 'preco': 3.0, 'duracaoPadraoMin': None, 'stock': 57, 'ativo': True},
            {'id': 9, 'tipo': 'produto', 'nome': 'serra', 'descricao': '', 'categoria': 'ferramentas', 'preco': 7.0, 'duracaoPadraoMin': None, 'stock': 5, 'ativo': True},
        ]
        materials = default_data
        save_catalog(materials, filename)
    else:
        # Load from file with error handling
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                preco = float(row['preco'])
                if preco < 0:
                    print(f"Aviso: Preço negativo para {row['nome']}, definindo como 0")
                    preco = 0.0
                stock = int(float(row['stock'])) if row['stock'] else None
                if stock is not None and stock < 0:
                    print(f"Aviso: Stock negativo para {row['nome']}, definindo como 0")
                    stock = 0
                ativo_str = row['ativo'].lower()
                if ativo_str not in ['true', 'false']:
                    print(f"Aviso: Ativo inválido para {row['nome']}, definindo como false")
                    ativo = False
                else:
                    ativo = ativo_str == 'true'
                material = {
                    'id': int(row.get('id', row.get('idItem', 0))),
                    'tipo': row['tipo'],
                    'nome': row['nome'],
                    'descricao': row['descricao'],
                    'categoria': row['categoria'],
                    'preco': preco,
                    'duracaoPadraoMin': int(row['duracaoPadraoMin']) if row['duracaoPadraoMin'] else None,
                    'stock': stock,
                    'ativo': ativo
                }
                materials.append(material)
    return materials

def save_catalog(materials, filename='catalogo.csv'):
    # Save catalog to CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'tipo', 'nome', 'descricao', 'categoria', 'preco', 'duracaoPadraoMin', 'stock', 'ativo']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for material in materials:
            row = {
                'id': material['id'],
                'tipo': material['tipo'],
                'nome': material['nome'],
                'descricao': material['descricao'],
                'categoria': material['categoria'],
                'preco': material['preco'],
                'duracaoPadraoMin': material['duracaoPadraoMin'] if material['duracaoPadraoMin'] is not None else '',
                'stock': material['stock'] if material['stock'] is not None else '',
                'ativo': str(material['ativo'])
            }
            writer.writerow(row)

def gestao_produtos_main():
    catalog = load_catalog()
    service_slots = load_turnos()
    cart_quantities = [0] * len(catalog)

    add_more_items = 0
    continue_menu = 0
    selected_option = 0
    total_cart_value = 0

    while True:  # Main menu loop
        # Apresentação do Menu para evitar a recursão infinita
        print("\n" + "="*30)
        print("      GESTÃO DE PRODUTOS")
        print("="*30)
        print("1  - Consultar Materiais")
        print("2  - Adicionar ao Carrinho")
        print("4  - Novo Material")
        print("5  - Filtrar Materiais")
        print("6  - Registar Entrada de Stock")
        print("7  - Gerir Serviços")
        print("8  - Mostrar Indicadores")
        print("9  - Editar Item")
        print("10 - Remover Item")
        print("11 - Listar por Categoria")
        print("12 - Listar por Faixa de Preço")
        print("13 - Listar Itens Ativos")
        print("14 - Listar Produtos sem Stock")
        print("0  - Finalizar / Sair")
        print("-" * 30)

        try:
            selected_option = int(input("Escolha uma opção: "))
        except ValueError:
            print("Erro: Insira um número válido!")
            continue

        if selected_option == 1:
            materialconsultation(catalog)
            continue_menu = 1
        elif selected_option == 2:
            while True:    # Cart addition loop
                print("\nIndique o material desejado:")
                for item_index in range(len(catalog)):
                    print(f"{item_index} - {catalog[item_index]['nome']}")
                
                try:
                    chosen_idx = int(input("ID do produto: "))
                    print(f"Quanta quantidade de {catalog[chosen_idx]['nome']} deseja?")
                    cart_quantities[chosen_idx] = float(input())
                    
                    validstock(catalog, cart_quantities)
                    stockupdate(catalog, cart_quantities)
                    save_catalog(catalog)
                except (ValueError, IndexError):
                    print("Produto inválido ou quantidade errada.")

                print("Deseja adicionar mais artigos ao carinho? Digite 1")
                add_more_items = int(input())
                if add_more_items != 1: break
            continue_menu = 1

        elif selected_option == 4:
            add_new_material(catalog)
            cart_quantities.append(0)
            continue_menu = 1
        elif selected_option == 5:
            filter_materials(catalog)
            continue_menu = 1
        elif selected_option == 6:
            register_stock_entry(catalog)
            continue_menu = 1
        elif selected_option == 7:
            manage_services(catalog, service_slots)
            continue_menu = 1
        elif selected_option == 8:
            show_indicators(catalog)
            continue_menu = 1
        elif selected_option == 9:
            edit_item(catalog)
            continue_menu = 1
        elif selected_option == 10:
            remove_item(catalog, service_slots)
            cart_quantities = [0] * len(catalog)
            continue_menu = 1
        elif selected_option == 11:
            list_by_category(catalog)
            continue_menu = 1
        elif selected_option == 12:
            list_by_price_range(catalog)
            continue_menu = 1
        elif selected_option == 13:
            list_active_items(catalog)
            continue_menu = 1
        elif selected_option == 14:
            list_out_of_stock_products(catalog)
            continue_menu = 1
        elif selected_option == 0:
            continue_menu = 0 # Sai do loop
        else:
            print("Opção inválida!")
            continue_menu = 1
        
        if continue_menu != 1: break

    # Finalização
    total_cart_value = calcfinal(cart_quantities, catalog)
    save_catalog(catalog)
    print(f"\nO preço do seu carrinho é de: {total_cart_value}€")
    print("O seu pedido encontra-se finalizado. Obrigado pela confiança!")
#------------------------------------------------------------------ A TÃO ILUMINADAA MAIN (PRINCIPAL) ------------------------------------------------------------------
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
            gestor_main()
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
