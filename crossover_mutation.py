import random

def crossover(parent1, parent2):
    start_point = parent1[0]
    cut = random.randint(1, len(parent1) - 2)
    
    child1 = [start_point] + parent1[1:cut] + [x for x in parent2[1:-1] if x not in parent1[1:cut]]
    child2 = [start_point] + parent2[1:cut] + [x for x in parent1[1:-1] if x not in parent2[1:cut]]
    
    child1.append(start_point)
    child2.append(start_point)
    
    return child1, child2

def mutate(route):
    i, j = random.sample(range(1, len(route) - 1), 2)
    route[i], route[j] = route[j], route[i] 