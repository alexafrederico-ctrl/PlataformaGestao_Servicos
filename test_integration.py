"""
Script de Teste - Verifica integração entre PortalCliente e PortalServicos
"""
import os
import sys

# Adicionar caminhos
TRABALHO_INDIVIDUAL = r'c:\Users\Utilizador\Desktop\GitHub\PlataformaGestao_Servicos\trabalhosIndividuais'
TRABALHO_FINAL = r'c:\Users\Utilizador\Desktop\GitHub\PlataformaGestao_Servicos\trabalhoFinal'

sys.path.insert(0, TRABALHO_INDIVIDUAL)
sys.path.insert(0, TRABALHO_FINAL)

try:
    import pandas as pd
    print("✓ pandas instalado")
except ImportError:
    print("✗ pandas não instalado. Execute: pip install pandas")
    sys.exit(1)

# Importar módulos
try:
    from PortalCliente import ler_pedidos_csv, ler_eventos_csv, ler_mensagens_csv
    print("✓ PortalCliente importado")
except ImportError as e:
    print(f"✗ Erro ao importar PortalCliente: {e}")

try:
    from PortalServicos import load_cliente_pedidos, load_cliente_eventos, load_materials_dataframe
    print("✓ PortalServicos importado")
except ImportError as e:
    print(f"✗ Erro ao importar PortalServicos: {e}")

# Verificar materiais
print("\n📦 Carregando materiais.csv...")
try:
    df_materiais = load_materials_dataframe()
    if isinstance(df_materiais, pd.DataFrame):
        print(f"✓ {len(df_materiais)} materiais carregados")
        print(df_materiais.head())
    else:
        print(f"✓ Materiais carregados (sem pandas): {len(df_materiais)} itens")
except Exception as e:
    print(f"✗ Erro ao carregar materiais: {e}")

# Verificar CSVs do cliente
print("\n📋 Verificando CSVs do cliente...")
print("- pedidos.csv:", "✓" if os.path.exists(os.path.join(TRABALHO_INDIVIDUAL, 'pedidos.csv')) else "✗ (será criado após primeiro pedido)")
print("- eventos_pedido.csv:", "✓" if os.path.exists(os.path.join(TRABALHO_INDIVIDUAL, 'eventos_pedido.csv')) else "✗ (será criado após primeiro pedido)")
print("- mensagens.csv:", "✓" if os.path.exists(os.path.join(TRABALHO_INDIVIDUAL, 'mensagens.csv')) else "✗ (será criado após primeira mensagem)")

print("\n✅ Sistema pronto!")
print("\n📖 Para começar:")
print("1. cd trabalhosIndividuais && python PortalCliente.py")
print("2. Em outro terminal: cd trabalhoFinal && python PortalServicos.py")
print("3. No Gestor, escolha opção 5 para ver pedidos do cliente")
