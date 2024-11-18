import pandas as pd
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import csv
from datetime import datetime, timedelta

# Função para calcular a distância entre dois pontos usando a fórmula de Haversine
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Raio da Terra em Km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# Função para calcular a aptidão de um indivíduo (rota)
def calculate_distance(route, coordinates):
    total_distance = 0
    total_time = 0
    battery_time = 1800  # 30 minutos em segundos
    route_status = []    # Lista para armazenar informações da rota
    velocidade_km_h = 54
    
    route_coords = [coordinates[i] for i in route]
    
    # Hora inicial do drone
    current_time = datetime.strptime("06:00", "%H:%M")
    current_day = current_time.date()  # Armazena o dia atual
    
    i = 0  # Índice do ponto atual
    while i < len(route_coords):
        point1 = route_coords[i]
        point2 = route_coords[(i + 1) % len(route_coords)]
        
        # Calcula distância e tempo até próximo ponto
        distance = haversine(point1[0], point1[1], point2[0], point2[1])
        time_to_next = (distance / velocidade_km_h) * 3600  # Converte para segundos
        
        # Desconta tempo de pouso/decolagem em cada ponto (60 segundos)
        battery_time -= 60
        
        # Verifica se precisa recarregar
        if time_to_next > battery_time:
            route_status.append({
                'ponto': route[i],
                'acao': 'POUSO PARA RECARGA',
                'bateria_restante': battery_time,
                'distancia_ate_proximo': 0,  # Não há distância até o próximo ponto se pousar
                'tempo_ate_proximo': 0,  # Não há tempo até o próximo ponto se pousar
                'horario': current_time.strftime("%H:%M"),  # Adiciona horário
                'dia': current_day.day  # Armazena apenas o número do dia
            })
            battery_time = 1800  # Recarrega bateria
        
        # Desconta tempo de voo
        battery_time -= time_to_next
        
        # Atualiza o tempo atual
        new_time = current_time + timedelta(seconds=time_to_next)
        
        # Verifica se o novo tempo ultrapassa 19h
        if new_time.hour >= 19:
            # Pousa e espera até as 6h do dia seguinte
            route_status.append({
                'ponto': route[i],
                'acao': 'POUSO NOTURNO',
                'bateria_restante': battery_time,
                'distancia_ate_proximo': 0,
                'tempo_ate_proximo': 0,
                'horario': current_time.strftime("%H:%M"),  # Adiciona horário
                'dia': current_day.day  # Armazena apenas o número do dia
            })
            # Recarrega a bateria ao pousar à noite
            battery_time = 1800  # Recarrega bateria
            # Espera até as 6h do dia seguinte
            current_time = current_time.replace(hour=6, minute=0) + timedelta(days=1)
            current_day = current_time.date()  # Atualiza o dia
            continue  # Retorna ao início do loop para continuar a partir do último ponto
        
        # Atualiza o tempo atual
        current_time = new_time
        
        route_status.append({
            'ponto': route[i],
            'distancia_ate_proximo': distance,
            'tempo_ate_proximo': time_to_next,
            'bateria_restante': battery_time,
            'acao': 'FOTO',
            'horario': current_time.strftime("%H:%M"),  # Adiciona horário
            'dia': current_day.day  # Armazena apenas o número do dia
        })
        
        total_distance += distance
        total_time += (time_to_next + 60) / 3600  # Converte para horas
        
        # Avança para o próximo ponto
        i += 1
    
    return total_distance, total_time, route_status

def calculate_fitness(route, coordinates):
    distance, time, route_status = calculate_distance(route, coordinates)
    # Penaliza rotas mais longas e que levam mais tempo
    return 1.0 / (1.0 + distance + time * 60)  # time * 60 converte para minutos

# Função para selecionar dois pais com base na aptidão (roleta)
def select_parents(population, fitness_scores):
    tournament_size = 5
    # Convertendo para lista de tuplas para melhor performance
    population_with_fitness = list(zip(fitness_scores, population))
    tournament = random.sample(population_with_fitness, tournament_size)
    return max(tournament, key=lambda x: x[0])[1]

# Função para cruzar dois pais e gerar filhos (crossover)
def crossover(parent1, parent2):
    # Preserva o primeiro e último ponto (que são iguais)
    start_point = parent1[0]
    cut = random.randint(1, len(parent1) - 2)
    
    # Faz o crossover apenas na parte intermediária da rota
    child1 = [start_point] + parent1[1:cut] + [x for x in parent2[1:-1] if x not in parent1[1:cut]]
    child2 = [start_point] + parent2[1:cut] + [x for x in parent1[1:-1] if x not in parent2[1:cut]]
    
    # Adiciona o ponto inicial novamente como ponto final
    child1.append(start_point)
    child2.append(start_point)
    
    return child1, child2

# Função para mutação (troca aleatória de dois pontos)
def mutate(route):
    # Seleciona dois pontos aleatórios, excluindo o primeiro e último ponto
    i, j = random.sample(range(1, len(route) - 1), 2)
    route[i], route[j] = route[j], route[i]

# Função para gerar a população inicial (rotas aleatórias)
def generate_population(size, points, start_point):
    # Remove o ponto inicial da lista de pontos disponíveis
    available_points = [p for p in points if p != start_point]
    population = []
    
    for _ in range(size):
        # Cria uma rota começando com o ponto inicial
        route = [start_point]
        # Adiciona os pontos restantes aleatoriamente
        route.extend(random.sample(available_points, len(available_points)))
        # Adiciona o ponto inicial novamente como ponto final
        route.append(start_point)
        population.append(route)
    
    return population

# Leitura do arquivo CSV e carregamento das coordenadas
def load_coordinates(filename):
    df = pd.read_csv(filename)
    print("Colunas disponíveis:", list(df.columns))
    coordinates = {i: (row['latitude'], row['longitude']) for i, row in df.iterrows()}
    return coordinates

# Função para desenhar o gráfico da rota
def plot_route(coordinates, route, generation):
    lats = [coordinates[point][0] for point in route]
    lons = [coordinates[point][1] for point in route]
    
    plt.figure(figsize=(10, 6))
    plt.plot(lons, lats, 'o-', label=f'Geração {generation}')
    
    # Adicionar números para cada ponto da rota
    for i, (lon, lat) in enumerate(zip(lons, lats)):
        # Destaca o ponto inicial/final de forma diferente
        if i == 0 or i == len(route) - 1:
            plt.plot(lon, lat, 'ro', markersize=10)
            plt.annotate(f'Início/Fim', (lon, lat), 
                        xytext=(5, 5), textcoords='offset points',
                        color='red', fontweight='bold')
        else:
            plt.annotate(f'{i}', (lon, lat), 
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=9, fontweight='bold')
    
    plt.title(f'Caminho na Geração {generation}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.legend()
    plt.show()

def export_results_to_csv(best_route, best_distance, best_time, coordinates, route_status):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'resultados_rota_{timestamp}.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Resumo geral
        writer.writerow(['=== RESUMO GERAL ==='])
        writer.writerow(['Distância Total (km)', 'Tempo Total (h)', 'Tempo Total (min)'])
        writer.writerow([round(best_distance, 2), round(best_time, 2), round(best_time * 60, 2)])
        writer.writerow([])
        
        # Detalhes da rota
        writer.writerow(['=== DETALHES DA ROTA ==='])
        writer.writerow(['Ordem', 'Ponto', 'Latitude', 'Longitude', 'Distância até próximo (km)', 
                        'Tempo até próximo (s)', 'Bateria Restante (s)', 'Ação', 'Horário', 'Dia'])
        
        for i, status in enumerate(route_status):
            lat, lon = coordinates[status['ponto']]
            writer.writerow([
                i + 1,
                status['ponto'],
                lat,
                lon,
                round(status['distancia_ate_proximo'], 2),
                round(status['tempo_ate_proximo'], 2),
                round(status['bateria_restante'], 2),
                status['acao'],
                status['horario'],
                status['dia']
            ])
    
    print(f"\nResultados exportados para: {filename}")

def run_single_population():
    # Configurações iniciais
    pop_size = 50
    coordinates = load_coordinates('coordenadas.csv')
    points = list(coordinates.keys())
    start_point = points[0]
    population = generate_population(pop_size, points, start_point)
    
    best_overall_distance = float('inf')
    best_overall_route = None
    best_overall_time = float('inf')
    best_route_status = None
    
    generations_without_improvement = 0
    max_generations_without_improvement = 100
    
    for generation in range(100):
        fitnesses = [calculate_fitness(route, coordinates) for route in population]
        best_idx = np.argmax(fitnesses)
        best_route = population[best_idx]
        best_distance, best_time, route_status = calculate_distance(best_route, coordinates)
        
        if best_distance < best_overall_distance:
            best_overall_distance = best_distance
            best_overall_route = best_route.copy()
            best_overall_time = best_time
            best_route_status = route_status
            generations_without_improvement = 0
        else:
            generations_without_improvement += 1
        
        print(f"\rGeração {generation + 1}: Distância = {best_distance:.2f} km, Tempo = {best_time:.2f} h", end="")
        
        if generations_without_improvement >= max_generations_without_improvement:
            print(f"\nParando após {generation} gerações sem melhoria.")
            break
        
        # Elitismo - mantém os melhores 10%
        elite_size = int(pop_size * 0.1)
        elite = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)[:elite_size]
        elite = [x[0] for x in elite]
        
        new_population = elite.copy()
        
        # Gera nova população
        while len(new_population) < pop_size:
            parent1 = select_parents(population, fitnesses)
            parent2 = select_parents(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            
            if random.random() < 0.10:
                mutate(child1)
            if random.random() < 0.10:
                mutate(child2)
                
            new_population.extend([child1, child2])
        
        population = new_population[:pop_size]
    
    # Calcula o número de dias de operação com base nos eventos registrados
    dias_de_operacao = max(status['dia'] for status in best_route_status)
    
    # Mostra resultados finais
    print("\n\nResultados Finais:")
    print(f"Melhor distância encontrada: {best_overall_distance:.2f} km")
    print(f"Tempo total estimado: {best_overall_time:.2f} horas ({best_overall_time*60:.1f} minutos)")
    
    # Ajuste para mostrar o número de dias de operação
    print(f"Total de dias de operação: {dias_de_operacao}")
    
    # Exporta os resultados
    export_results_to_csv(best_overall_route, best_distance, best_time, coordinates, best_route_status)
    
    # Plota a melhor rota encontrada
    plot_route(coordinates, best_overall_route, "Melhor Resultado")

# Executar o algoritmo
run_single_population()