# Plataforma de Gestão de Serviços - Integração Cliente-Servidor

## 📋 Estrutura Atual

```
trabalhoFinal/
  ├─ PortalServicos.py (Portal central - gestor, cliente, estafeta, produtos)
  └─ materials.csv (Inventário de materiais)

trabalhosIndividuais/
  ├─ PortalCliente.py (Portal cliente - TRABALHO DE GRUPO)
  ├─ pedidos.csv (Gerado automaticamente)
  ├─ eventos_pedido.csv (Gerado automaticamente)
  └─ mensagens.csv (Gerado automaticamente)
```

## 🔄 Fluxo de Integração

1. **Editar apenas `PortalCliente.py`** - Qualquer alteração se reflete automaticamente
2. **Dados persistem em CSVs** via pandas:
   - `pedidos.csv` - Todos os pedidos realizados (Produto, Quantidade, Preço, Destino, Avaliação, Data)
   - `eventos_pedido.csv` - Rastreamento de eventos (Evento, Produto, Status, Destino, Timestamp)
   - `mensagens.csv` - Confirmações/avisos (Tipo, Mensagem, Timestamp)

3. **PortalServicos.py sincroniza** - Gestor pode ver pedidos do cliente em tempo real (opção 5 do menu)

## 📦 Instalação

```bash
pip install pandas
```

## ▶️ Como Usar

### Executar o Portal Cliente (com persistência)
```bash
cd trabalhosIndividuais
python PortalCliente.py
```

### Executar o Portal de Serviços (com sincronização)
```bash
cd trabalhoFinal
python PortalServicos.py
```

## ✨ Funcionalidades Implementadas

### Portal Cliente (`PortalCliente.py`)
- ✅ Visualizar produtos
- ✅ Criar pedidos
- ✅ Validar stock
- ✅ Escolher destino
- ✅ Avaliar pedido
- ✅ **Salvar em CSV** (pedidos, eventos, mensagens)

### Portal Gestor (`PortalServicos.py`)
- ✅ Consultar encomendas
- ✅ Consultar estafetas
- ✅ Consultar zonas
- ✅ Aprovar encomendas
- ✅ **Sincronizar com pedidos do cliente (CSV)**

## 📊 Exemplos de CSVs Gerados

### pedidos.csv
| Produto | Quantidade | Preço_Unitário | Preço_Total | Destino | Avaliação | Data |
|---------|-----------|-----------------|-------------|---------|-----------|------|
| Tintas | 2 | 11 | 22 | Braga | 1 | 2024-12-09 14:30:45 |
| Parafusos | 5 | 1.6 | 8 | Braga | 1 | 2024-12-09 14:30:45 |

### eventos_pedido.csv
| Evento | Produto | Status | Destino | Timestamp |
|--------|---------|--------|---------|-----------|
| Pedido Criado | Tintas | Confirmado | Braga | 2024-12-09 14:30:45 |

### mensagens.csv
| Tipo | Mensagem | Timestamp |
|------|----------|-----------|
| Confirmação | Pedido confirmado para Braga - Total: 30€ | 2024-12-09 14:30:45 |

## 🔧 Próximas Melhorias

- [ ] Conectar Estafeta com pedidos do cliente
- [ ] Dashboard em tempo real
- [ ] API REST para integração
- [ ] Backup automático de CSVs

