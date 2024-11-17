import random
import numpy as np
from haversine import haversine
from datetime import datetime, timedelta

def calculate_distance(route, coordinates):
    total_distance = 0
    total_time = 0
    battery_time = 1800  # 30 minutos em segundos
    route_status = []    # Lista para armazenar informações da rota
    velocidade_km_h = 54
    
    route_coords = [coordinates[i] for i in route]
    
    # Hora inicial do drone
    current_time = datetime.strptime("06:00", "%H:%M")
    
    for i in range(len(route_coords)):
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
                'distancia_ate_proximo': 0,
                'tempo_ate_proximo': 0,
                'horario': current_time.strftime("%H:%M")
            })
            battery_time = 1800  # Recarrega bateria
        
        # Desconta tempo de voo
        battery_time -= time_to_next
        
        # Atualiza o tempo atual
        current_time += timedelta(seconds=time_to_next)
        
        # Verifica se o drone precisa pousar ao atingir 19h
        if current_time.hour >= 19:
            route_status.append({
                'ponto': route[i],
                'acao': 'POUSO NOTURNO',
                'bateria_restante': battery_time,
                'distancia_ate_proximo': 0,
                'tempo_ate_proximo': 0,
                'horario': current_time.strftime("%H:%M")
            })
            current_time = current_time.replace(hour=6, minute=0) + timedelta(days=1)
        
        route_status.append({
            'ponto': route[i],
            'distancia_ate_proximo': distance,
            'tempo_ate_proximo': time_to_next,
            'bateria_restante': battery_time,
            'acao': 'FOTO',
            'horario': current_time.strftime("%H:%M")
        })
        
        total_distance += distance
        total_time += (time_to_next + 60) / 3600
    
    return total_distance, total_time, route_status

def calculate_fitness(route, coordinates):
    distance, time, route_status = calculate_distance(route, coordinates)
    return 1.0 / (1.0 + distance + time * 60)

def select_parents(population, fitness_scores):
    tournament_size = 5
    population_with_fitness = list(zip(fitness_scores, population))
    tournament = random.sample(population_with_fitness, tournament_size)
    return max(tournament, key=lambda x: x[0])[1] 