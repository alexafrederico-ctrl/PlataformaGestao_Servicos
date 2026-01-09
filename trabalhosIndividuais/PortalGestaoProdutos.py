import csv
import os
from datetime import datetime, timedelta

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

def menu():
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

# Main program execution
catalog = load_catalog()
service_slots = load_turnos()
cart_quantities = [0] * len(catalog)

add_more_items = 0
unused_price = 0  # Not used
continue_menu = 0
selected_option = 0
total_cart_value = 0
while True:    # Main menu loop
    selected_option = menu()
    if selected_option == 1:
        materialconsultation(catalog)
        continue_menu = 1
    elif selected_option == 2:
        while True:    # Cart addition loop
            item_index = 0
            print("indique o material desejado")
            for item_index in range(len(catalog)):
                print(str(item_index) + " se desejar " + catalog[item_index]['nome'])
            item_index = int(input())
            print("Quanta quantidade de " + catalog[item_index]['nome'] + " que deseja?")
            cart_quantities[item_index] = float(input())
            validstock(catalog, cart_quantities)
            stockupdate(catalog, cart_quantities)
            save_catalog(catalog)
            print("Deseja adicionar mais artigos ao carinho? Digite 1 ")
            add_more_items = int(input())
            if add_more_items != 1: break
        total_cart_value = calcfinal(cart_quantities, catalog)
        continue_menu = 1
    elif selected_option == 4:
        add_new_material(catalog)
        cart_quantities.append(0)  # Add to cart list
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
        cart_quantities = [0] * len(catalog)  # Reset cart due to index changes
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
    else:
        continue_menu = 0
    if continue_menu != 1: break
total_cart_value = calcfinal(cart_quantities, catalog)
save_catalog(catalog)
print(" o  preço do seu carinho é de " + str(total_cart_value) + "€")
print("O seu pedido encontra-se finalizados, obrigado pelo seu voto de confiança. ")
