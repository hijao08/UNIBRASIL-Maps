import numpy as np
import random
from fitness import calculate_fitness, calculate_distance, select_parents
from crossover_mutation import crossover, mutate
from population import generate_population
from io_operations import load_coordinates, export_results_to_csv
from plotting import plot_route

def run_single_population():
    # Configurações iniciais
    pop_size = 50
    coordinates, ceps = load_coordinates('csv/coordenadas.csv')
    points = list(coordinates.keys())
    start_point = points[0]
    population = generate_population(pop_size, points, start_point)
    
    best_overall_distance = float('inf')
    best_overall_route = None
    best_overall_time = float('inf')
    best_route_status = None
    
    generations_without_improvement = 0
    max_generations_without_improvement = 1000
    
    for generation in range(1000):
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
            
            if random.random() < 0.5:
                mutate(child1)
            if random.random() < 0.5:
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
    
    # Exporta os resultados usando os CEPs
    export_results_to_csv(best_overall_route, best_overall_distance, best_overall_time, 
                         coordinates, best_route_status, ceps)  # Adicionado ceps aqui
    
    # Plota a melhor rota encontrada
    plot_route(coordinates, best_overall_route, "Melhor Resultado")

# Executar o algoritmo
if __name__ == "__main__":
    run_single_population() 