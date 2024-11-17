import pandas as pd
import csv
from datetime import datetime

def load_coordinates(filename):
    df = pd.read_csv(filename)
    print("Colunas disponíveis:", list(df.columns))
    coordinates = {i: (row['latitude'], row['longitude']) for i, row in df.iterrows()}
    return coordinates

def export_results_to_csv(best_route, best_distance, best_time, coordinates, route_status):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'resultados_rota_{timestamp}.csv'
    
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerow(['=== RESUMO GERAL ==='])
        writer.writerow(['Distância Total (km)', 'Tempo Total (h)', 'Tempo Total (min)'])
        writer.writerow([round(best_distance, 2), round(best_time, 2), round(best_time * 60, 2)])
        writer.writerow([])
        
        writer.writerow(['=== DETALHES DA ROTA ==='])
        writer.writerow(['Ordem', 'Ponto', 'Latitude', 'Longitude', 'Distância até próximo (km)', 
                        'Tempo até próximo (s)', 'Bateria Restante (s)', 'Ação', 'Horário'])
        
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
                status['horario']
            ])
    
    print(f"\nResultados exportados para: {filename}")