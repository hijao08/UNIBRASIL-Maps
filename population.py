import random

def generate_population(size, points, start_point):
    available_points = [p for p in points if p != start_point]
    population = []
    
    for _ in range(size):
        route = [start_point]
        route.extend(random.sample(available_points, len(available_points)))
        route.append(start_point)
        population.append(route)
    
    return population 