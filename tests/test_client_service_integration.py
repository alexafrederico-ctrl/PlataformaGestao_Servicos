import sys
import os
import importlib

import pytest


def setup_import_paths():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    trabalho_final = os.path.join(repo_root, 'trabalhoFinal')
    trabalhos_individuais = os.path.join(repo_root, 'trabalhosIndividuais')
    # Ensure the modules can be imported by name
    if trabalhos_individuais not in sys.path:
        sys.path.insert(0, trabalhos_individuais)
    if trabalho_final not in sys.path:
        sys.path.insert(0, trabalho_final)


def test_persist_and_load_csvs(tmp_path):
    """Integration test: PortalCliente saves CSVs and PortalServicos loads them."""
    setup_import_paths()

    import PortalCliente as pc
    import PortalServicos as ps

    # Point PortalCliente to write into the temporary directory
    temp_dir = str(tmp_path)
    pc.DATA_DIR = temp_dir

    # Prepare sample data
    produtosNome = ['ProdutoA', 'ProdutoB']
    produtosPreco = [10.0, 5.0]
    encomendas = [2, 0]
    destinos = ['Braga']
    avaliacoes = [5, 0, 0]
    t = 1
    td = 1

    # Ensure no pre-existing files
    for fname in ('pedidos.csv', 'eventos_pedido.csv', 'mensagens.csv'):
        p = os.path.join(temp_dir, fname)
        if os.path.exists(p):
            os.remove(p)

    # Call the client save functions
    pc.salvar_pedidos_csv(produtosNome, encomendas, produtosPreco, destinos, avaliacoes, t, td)
    pc.salvar_eventos_pedido_csv(produtosNome, encomendas, destinos, td)
    pc.salvar_mensagens_csv('Confirmação', 'Pedido confirmado teste')

    # Now point PortalServicos to read from the same temp dir
    ps.CLIENT_DIR = temp_dir
    ps.PEDIDOS_CSV = os.path.join(ps.CLIENT_DIR, 'pedidos.csv')
    ps.EVENTOS_CSV = os.path.join(ps.CLIENT_DIR, 'eventos_pedido.csv')
    ps.MENSAGENS_CSV = os.path.join(ps.CLIENT_DIR, 'mensagens.csv')

    # Load CSVs into PS global DataFrames
    ps.load_all_client_csvs()

    # Assertions: each DF should have at least one row
    assert not ps.DF_PEDIDOS.empty, 'DF_PEDIDOS should not be empty after saving pedidos.csv'
    assert ps.DF_PEDIDOS.iloc[0]['Produto'] == 'ProdutoA'
    assert not ps.DF_EVENTOS.empty, 'DF_EVENTOS should not be empty after saving eventos_pedido.csv'
    assert not ps.DF_MENSAGENS.empty, 'DF_MENSAGENS should not be empty after saving mensagens.csv'

    # Verify message text
    assert 'Pedido confirmado teste' in ps.DF_MENSAGENS.iloc[0]['Mensagem']
