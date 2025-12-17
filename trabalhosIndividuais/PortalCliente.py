"""
Portal Cliente - Refatorizado para trabalho de grupo
Exporta dados em CSV: pedidos.csv, eventos_pedido.csv, mensagens.csv
"""
import os
import pandas as pd
from datetime import datetime

# Diretório base para CSVs
DATA_DIR = os.path.dirname(__file__)

# Try to reuse PortalServicos constants/functions when available (same repo)
import sys
import importlib
ps = None
try:
    ps_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'trabalhoFinal'))
    if ps_path not in sys.path:
        sys.path.insert(0, ps_path)
    ps = importlib.import_module('PortalServicos')
except Exception:
    ps = None

if ps is not None:
    CLIENT_DIR = ps.CLIENT_DIR
    PEDIDOS_CSV = ps.PEDIDOS_CSV
    EVENTOS_CSV = ps.EVENTOS_CSV
    MENSAGENS_CSV = ps.MENSAGENS_CSV
else:
    CLIENT_DIR = DATA_DIR
    PEDIDOS_CSV = os.path.join(DATA_DIR, 'pedidos.csv')
    EVENTOS_CSV = os.path.join(DATA_DIR, 'eventos_pedido.csv')
    MENSAGENS_CSV = os.path.join(DATA_DIR, 'mensagens.csv')

# Global application state (kept at top for clarity)
avaliacoes = [0] * 3
destinosOpcao = [""] * 3
destinos = [""] * 3
produtosNome = [""] * 3
produtosQtd = [0] * 3
produtosPreco = [0] * 3
encomendas = [0] * 3

chamadaMenu = 0
td = 0
t = 0
CLIENT_ID = None

def apresentacaoProd(produtosNome, produtosPreco):
    print("Lista de Produtos")
    for i in range(0, len(produtosNome) - 1 + 1, 1):
        print(str(i + 1) + "- " + produtosNome[i] + "(" + str(produtosPreco[i]) + " eur/uni)")

def avaliacao():
    print("1- Experiência Boa")
    print("2- Experiência intermédia")
    print("3- Experiência Má")
    ava = int(input())
    
    return ava

def calcTotal(encomendas, produtoPreco):
    total = 0
    for i in range(0, len(encomendas) - 1 + 1, 1):
        total = total + encomendas[i] * produtoPreco[i]
    
    return total

def consultaPed(produtosNome, encomendas, produtosPreco, avaliacoes, t, td, destinos):
    for i in range(0, len(encomendas) - 1 + 1, 1):
        print(produtosNome[i] + " com a quantidade de " + str(encomendas[i]) + " e com o preço de " + str(encomendas[i] * produtosPreco[i]))
    print("---Avalições---")
    for a in range(0, t - 1 + 1, 1):
        print("Avalição " + str(a + 1) + "--> " + str(avaliacoes[a]))
    print("---Destino da Encomenda---")
    for d in range(0, td - 1 + 1, 1):
        print("Destino " + str(d + 1) + ": " + destinos[d])

def consultaStock(produtosNome, produtosQtd, produtosPreco):
    for r in range(0, len(produtosNome) - 1 + 1, 1):
        print(produtosNome[r] + " - " + str(produtosQtd[r]) + " unidades | " + str(produtosPreco[r]) + "eur/uni")

def criacaoPedido(produtosNome, encomendas, produtosPreco):
    repeat = 0
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
        if repeat != 1: break

def escolherDestino(destinosOpcao):
    print("Escolha o destino: ")
    print("1 - " + destinosOpcao[0])
    print("2 - " + destinosOpcao[1])
    print("3 - " + destinosOpcao[2])
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

def validacaoStock(produtosNome, produtosQtd, encomendas, produtosPreco, chamadaMenu):
    for i in range(0, len(encomendas) - 1 + 1, 1):
        if encomendas[i] > 0:
            if encomendas[i] > produtosQtd[i]:
                print("Encomendas-te " + produtosNome[i] + "(" + str(encomendas[i]) + "). A quantidade encomendada é superior à quantidade máxima do stock " + str(produtosQtd[i]))
                print("A sua encomenda poderá demorar mais tempo até obter o stock necessário!")
            else:
                produtosQtd[i] = produtosQtd[i] - encomendas[i]
                print(" - " + produtosNome[i] + " com a quantidade de " + str(encomendas[i]) + " e o preço de " + str(encomendas[i] * produtosPreco[i]))

# ============= Persistência em CSV com Pandas =============
def salvar_pedidos_csv(produtosNome, encomendas, produtosPreco, destinos, avaliacoes, t, td):
    """
    Salva pedidos realizados em pedidos.csv
    Colunas: Produto, Quantidade, Preço_Unitário, Preço_Total, Destino, Avaliação, Data
    """

    # debug entry removed
    dados_pedidos = []
    cid = '' if CLIENT_ID is None else str(CLIENT_ID).strip()
    for i in range(len(encomendas)):
        if encomendas[i] > 0:
            dados_pedidos.append({
                'ClienteID': cid,
                'Produto': produtosNome[i],
                'Quantidade': encomendas[i],
                'Preço_Unitário': produtosPreco[i],
                'Preço_Total': encomendas[i] * produtosPreco[i],
                'Destino': destinos[min(td-1, len(destinos)-1)] if td > 0 else 'N/A',
                'Avaliação': avaliacoes[min(t-1, len(avaliacoes)-1)] if t > 0 else 'N/A',
                'Data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
    print(dados_pedidos)
    if dados_pedidos:
        # Create a DataFrame only for the new rows and then append to any existing
        df_new = pd.DataFrame(dados_pedidos)
        # Try to append to in-memory DF in PortalServicos (if available in same environment)
        try:
            if ps is not None and hasattr(ps, 'DF_PEDIDOS'):
                try:
                    existing = ps.DF_PEDIDOS if getattr(ps, 'DF_PEDIDOS') is not None else pd.DataFrame()
                    if not existing.empty:
                        ps.DF_PEDIDOS = pd.concat([existing, df_new], ignore_index=True)
                    else:
                        ps.DF_PEDIDOS = df_new
                except Exception:
                    # non-fatal: continue and write CSV
                    pass
        except Exception:
            pass

        csv_path = PEDIDOS_CSV
        # ensure target directory exists (use directory of csv_path)
        target_dir = os.path.dirname(csv_path) or DATA_DIR
        os.makedirs(target_dir, exist_ok=True)
        # If existing file, merge on-disk as well (to keep file consistent if PS wasn't imported)
        if os.path.exists(csv_path):
            try:
                df_existente = pd.read_csv(csv_path)
                df = pd.concat([df_existente, df_new], ignore_index=True)
            except Exception:
                # fallback: if reading fails, write only the new rows
                df = df_new
        else:
            df = df_new

        tmp_path = csv_path + '.tmp'
        df.to_csv(tmp_path, index=False, encoding='utf-8')
        try:
            os.replace(tmp_path, csv_path)
        except Exception:
            # fallback to non-atomic write
            df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"✓ Pedidos salvos em {csv_path}")

def salvar_eventos_pedido_csv(produtosNome, encomendas, destinos, td):
    """
    Salva eventos/tracking de pedidos em eventos_pedido.csv
    Colunas: Evento, Produto, Status, Destino, Timestamp
    """
    cid = '' if CLIENT_ID is None else str(CLIENT_ID).strip()
    dados_eventos = []
    for i in range(len(encomendas)):
        if encomendas[i] > 0:
            dados_eventos.append({
                'ClienteID': cid,
                'Evento': 'Pedido Criado',
                'Produto': produtosNome[i],
                'Status': 'Confirmado',
                'Destino': destinos[min(td-1, len(destinos)-1)] if td > 0 else 'N/A',
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
    
    if dados_eventos:
        df_new = pd.DataFrame(dados_eventos)
        # Update in-memory PortalServicos DF_EVENTOS if available
        try:
            if ps is not None and hasattr(ps, 'DF_EVENTOS'):
                try:
                    existing = ps.DF_EVENTOS if getattr(ps, 'DF_EVENTOS') is not None else pd.DataFrame()
                    if not existing.empty:
                        ps.DF_EVENTOS = pd.concat([existing, df_new], ignore_index=True)
                    else:
                        ps.DF_EVENTOS = df_new
                except Exception:
                    pass
        except Exception:
            pass

        csv_path = EVENTOS_CSV
        target_dir = os.path.dirname(csv_path) or DATA_DIR
        os.makedirs(target_dir, exist_ok=True)
        if os.path.exists(csv_path):
            try:
                df_existente = pd.read_csv(csv_path)
                df = pd.concat([df_existente, df_new], ignore_index=True)
            except Exception:
                df = df_new
        else:
            df = df_new
        tmp_path = csv_path + '.tmp'
        df.to_csv(tmp_path, index=False, encoding='utf-8')
        try:
            os.replace(tmp_path, csv_path)
        except Exception:
            df.to_csv(csv_path, index=False, encoding='utf-8')
        print(f"✓ Eventos salvos em {csv_path}")

def salvar_mensagens_csv(mensagem_tipo, mensagem_texto):
    """
    Salva mensagens de confirmação/avisos em mensagens.csv
    Colunas: Tipo, Mensagem, Timestamp
    """
    cid = '' if CLIENT_ID is None else str(CLIENT_ID).strip()
    dados_msg = [{
        'ClienteID': cid,
        'Tipo': mensagem_tipo,
        'Mensagem': mensagem_texto,
        'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }]

    df_new = pd.DataFrame(dados_msg)
    # Update in-memory PortalServicos DF_MENSAGENS if available
    try:
        if ps is not None and hasattr(ps, 'DF_MENSAGENS'):
            try:
                existing = ps.DF_MENSAGENS if getattr(ps, 'DF_MENSAGENS') is not None else pd.DataFrame()
                if not existing.empty:
                    ps.DF_MENSAGENS = pd.concat([existing, df_new], ignore_index=True)
                else:
                    ps.DF_MENSAGENS = df_new
            except Exception:
                pass
    except Exception:
        pass

    csv_path = MENSAGENS_CSV
    target_dir = os.path.dirname(csv_path) or DATA_DIR
    os.makedirs(target_dir, exist_ok=True)
    if os.path.exists(csv_path):
        try:
            df_existente = pd.read_csv(csv_path)
            df = pd.concat([df_existente, df_new], ignore_index=True)
        except Exception:
            df = df_new
    else:
        df = df_new
    tmp_path = csv_path + '.tmp'
    df.to_csv(tmp_path, index=False, encoding='utf-8')
    try:
        os.replace(tmp_path, csv_path)
    except Exception:
        df.to_csv(csv_path, index=False, encoding='utf-8')

def ler_pedidos_csv():
    """Lê todos os pedidos salvos"""
    csv_path = PEDIDOS_CSV
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        # normalize ClienteID column to string for consistent filtering
        if 'ClienteID' in df.columns:
            df['ClienteID'] = df['ClienteID'].fillna('').astype(str).str.strip()
        return df
    return pd.DataFrame()

def ler_eventos_csv():
    """Lê todos os eventos de tracking"""
    csv_path = EVENTOS_CSV
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        if 'ClienteID' in df.columns:
            df['ClienteID'] = df['ClienteID'].fillna('').astype(str).str.strip()
        return df
    return pd.DataFrame()

def ler_mensagens_csv():
    """Lê todas as mensagens"""
    csv_path = MENSAGENS_CSV
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        if 'ClienteID' in df.columns:
            df['ClienteID'] = df['ClienteID'].fillna('').astype(str).str.strip()
        return df
    return pd.DataFrame()

# Main (globals defined at module top; assign initial values)
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

# t = indice de Avaliação( 1, 2 ou 3)


def cliente_main():
    """Interactive client portal loop.

    Asks for CLIENT_ID at the start of the session and re-asks when the user
    chooses the exit option. This function does not run on import.
    """
    global CLIENT_ID, chamadaMenu, td, t, encomendas

    print("PORTAL DO CLIENTE")
    # Perguntar pelo ID do cliente e guardar para filtragem de pedidos
    try:
        CLIENT_ID = input("Insira o seu ID de cliente: ").strip()
    except Exception:
        CLIENT_ID = None

    for i in range(0, len(encomendas) - 1 + 1, 1):
        encomendas[i] = 0
    while True:    #This simulates a Do Loop
        opcao = menu()
        if opcao == 1:
            consultaStock(produtosNome, produtosQtd, produtosPreco)
            chamadaMenu = 1
        elif opcao == 2:
            print("Qual o produto que escolhe?")
            criacaoPedido(produtosNome, encomendas, produtosPreco)
            print("Lista de produtos encomendados:")
            validacaoStock(produtosNome, produtosQtd, encomendas, produtosPreco, chamadaMenu)
            print("Indique o destino da encomenda: ")
            escolha = escolherDestino(destinosOpcao)
            destinos[td] = destinosOpcao[escolha - 1]
            td = td + 1
            total = calcTotal(encomendas, produtosPreco)
            print("Obrigado pela a encomenda" + " O total da encomenda é " + str(total) + " eur")
            print("Avalie o seu pedido")
            ava = avaliacao()
            # guardamos avaliação apenas se houver espaço
            if t < len(avaliacoes):
                avaliacoes[t] = ava
            t = t + 1

            # Salvar dados em CSV
            salvar_pedidos_csv(produtosNome, encomendas, produtosPreco, destinos, avaliacoes, t, td)
            salvar_eventos_pedido_csv(produtosNome, encomendas, destinos, td)
            salvar_mensagens_csv("Confirmação", f"Pedido confirmado para {destinos[td-1]} - Total: {total}€")

            chamadaMenu = 1
        elif opcao == 3:
            # Mostrar apenas pedidos deste cliente usando DataFrame.loc
            try:
                df_pedidos = ler_pedidos_csv()
                if not df_pedidos.empty and CLIENT_ID is not None and 'ClienteID' in df_pedidos.columns:
                    df_my = df_pedidos.loc[df_pedidos['ClienteID'] == CLIENT_ID]
                    if not df_my.empty:
                        print("\n=== SUAS ENCOMENDAS ===")
                        print(df_my.to_string(index=False))
                    else:
                        print("Nenhuma encomenda encontrada para o seu ID.")
                else:
                    # fallback to session data view
                    consultaPed(produtosNome, encomendas, produtosPreco, avaliacoes, t, td, destinos)
            except Exception:
                consultaPed(produtosNome, encomendas, produtosPreco, avaliacoes, t, td, destinos)
            chamadaMenu = 1
        elif opcao == 4:
            chamadaMenu = 0
        else:
            print("Opção inválida")
            chamadaMenu = 1
        if chamadaMenu != 1:
            break
    print("Continuação de um ótimo dia")


if __name__ == '__main__':
    cliente_main()