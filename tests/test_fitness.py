import unittest
from fitness import calculate_distance, calculate_fitness, select_parents
from haversine import haversine

class TestFitness(unittest.TestCase):

    def setUp(self):
        self.coordinates = {
            'A': (0, 0),
            'B': (1, 1),
            'C': (2, 2),
            'D': (3, 3),
            'E': (4, 4)
        }
        self.route = ['A', 'B', 'C', 'D', 'E']

    def test_calculate_distance(self):
        distance, time, route_status = calculate_distance(self.route, self.coordinates)
        self.assertGreaterEqual(distance, 0)  # A distância não pode ser negativa
        self.assertGreaterEqual(time, 0)      # O tempo não pode ser negativo

    def test_calculate_fitness(self):
        fitness = calculate_fitness(self.route, self.coordinates)
        self.assertGreaterEqual(fitness, 0)   # A fitness deve ser não negativa

    def test_select_parents(self):
        population = [['A', 'B', 'C'], ['A', 'C', 'B'], ['B', 'A', 'C']]
        fitness_scores = [0.5, 0.7, 0.6]
        parent = select_parents(population, fitness_scores)
        self.assertIn(parent, population)  # O pai selecionado deve estar na população

    def test_calculate_distance_with_battery_recharge(self):
        route = ['A', 'B', 'C', 'D']
        distance, time, route_status = calculate_distance(route, self.coordinates)
        self.assertIn('POUSO PARA RECARGA', [status['acao'] for status in route_status])  # Verifica se houve pouso para recarga

    def test_calculate_fitness_with_empty_route(self):
        empty_route = []
        fitness = calculate_fitness(empty_route, self.coordinates)
        self.assertEqual(fitness, 1.0)  # A fitness deve ser 1.0 para uma rota vazia

    def test_calculate_fitness_with_single_point(self):
        single_point_route = ['A']
        fitness = calculate_fitness(single_point_route, self.coordinates)
        self.assertGreaterEqual(fitness, 0)  # A fitness deve ser não negativa

if __name__ == '__main__':
    unittest.main() 