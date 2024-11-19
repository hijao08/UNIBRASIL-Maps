import pandas as pd
import csv
from datetime import datetime

def load_coordinates(filename):
    df = pd.read_csv(filename)
    print("Colunas disponíveis:", list(df.columns))
    coordinates = {i: (row['latitude'], row['longitude']) for i, row in df.iterrows()}
    ceps = {i: int(row['cep']) for i, row in df.iterrows()}
    return coordinates, ceps

def export_results_to_csv(best_route, best_distance, best_time, coordinates, route_status, ceps):
    if not best_route:  # Verifica se a rota está vazia
        raise ValueError("A rota não pode estar vazia.")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'resultados_rota_{timestamp}.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Cabeçalho
        writer.writerow(['CEP inicial', 'Latitude inicial', 'Longitude inicial', 
                        'Dia do vôo', 'Hora inicial', 'Velocidade', 
                        'CEP final', 'Latitude final', 'Longitude final',
                        'Pouso', 'Hora final'])
        
        # Para cada ponto na rota (exceto o último)
        for i in range(len(route_status) - 1):
            current_point = route_status[i]
            next_point = route_status[i + 1]
            
            # Obtém coordenadas do ponto atual
            lat_inicial, lon_inicial = coordinates[current_point['ponto']]
            # Obtém coordenadas do próximo ponto
            lat_final, lon_final = coordinates[next_point['ponto']]
            
            # Determina se houve pouso
            pouso = "SIM" if current_point['acao'] in ['POUSO PARA RECARGA', 'POUSO NOTURNO'] else "NÃO"
            
            # Usa os CEPs reais em vez dos índices
            cep_inicial = ceps[current_point['ponto']]
            cep_final = ceps[next_point['ponto']]
            
            writer.writerow([
                cep_inicial,  # CEP inicial real
                lat_inicial,
                lon_inicial,
                current_point['dia'],
                current_point['horario'],
                54,  # Velocidade fixa em 54 km/h
                cep_final,  # CEP final real
                lat_final,
                lon_final,
                pouso,
                next_point['horario']
            ])
    
    print(f"\nResultados exportados para: {filename}")