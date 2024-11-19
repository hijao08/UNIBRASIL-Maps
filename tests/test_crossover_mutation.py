import unittest
from crossover_mutation import crossover, mutate
import random

class TestCrossoverMutation(unittest.TestCase):

    def test_crossover(self):
        parent1 = ['A', 'B', 'C', 'D', 'E']
        parent2 = ['A', 'F', 'G', 'H', 'I']
        child1, child2 = crossover(parent1, parent2)
        
        # Verifica se o ponto inicial e final são os mesmos
        self.assertEqual(child1[0], 'A')
        self.assertEqual(child1[-1], 'A')
        self.assertEqual(child2[0], 'A')
        self.assertEqual(child2[-1], 'A')
        
        # Verifica se os filhos contêm elementos dos pais
        self.assertTrue(set(child1[1:-1]).issubset(set(parent1[1:] + parent2[1:])))
        self.assertTrue(set(child2[1:-1]).issubset(set(parent1[1:] + parent2[1:])))
    
    def test_mutate(self):
        route = ['A', 'B', 'C', 'D', 'E']
        original_route = route.copy()
        mutate(route)
        
        # Verifica se a rota foi alterada
        self.assertNotEqual(route, original_route)
        # Verifica se o tamanho da rota permanece o mesmo
        self.assertEqual(len(route), len(original_route))
    
    def test_crossover_edge_case(self):
        parent1 = ['A', 'B', 'C', 'D', 'E']
        parent2 = ['A', 'B', 'C', 'D', 'E']  # Caso onde os pais são iguais
        child1, child2 = crossover(parent1, parent2)
        
        # Verifica se os filhos são iguais aos pais
        self.assertEqual(child1, parent1)
        self.assertEqual(child2, parent2)
    
    def test_crossover_with_identical_parents(self):
        parent1 = ['A', 'B', 'C', 'D', 'E']
        parent2 = ['A', 'B', 'C', 'D', 'E']  # Caso onde os pais são iguais
        child1, child2 = crossover(parent1, parent2)
        
        # Verifica se os filhos são iguais aos pais
        self.assertEqual(child1, parent1)
        self.assertEqual(child2, parent2)
    
    def test_crossover_with_different_parents(self):
        parent1 = ['A', 'B', 'C', 'D', 'E']
        parent2 = ['A', 'F', 'G', 'H', 'I']
        child1, child2 = crossover(parent1, parent2)
        
        # Verifica se o ponto inicial e final são os mesmos
        self.assertEqual(child1[0], 'A')
        self.assertEqual(child1[-1], 'A')
        self.assertEqual(child2[0], 'A')
        self.assertEqual(child2[-1], 'A')
        
        # Verifica se os filhos contêm elementos dos pais
        self.assertTrue(set(child1[1:-1]).issubset(set(parent1[1:] + parent2[1:])))
        self.assertTrue(set(child2[1:-1]).issubset(set(parent1[1:] + parent2[1:])))
    
    def test_mutate_edge_case(self):
        route = ['A', 'B', 'C', 'D', 'E']
        original_route = route.copy()
        mutate(route)
        
        # Verifica se a rota foi alterada
        self.assertNotEqual(route, original_route)
        # Verifica se o tamanho da rota permanece o mesmo
        self.assertEqual(len(route), len(original_route))
        
        # Verifica se a mutação não altera o primeiro e o último elemento
        self.assertEqual(route[0], 'A')
        self.assertEqual(route[-1], 'E')

        # Adiciona uma verificação para garantir que a mutação não remove elementos
        self.assertTrue(set(route).issubset(set(original_route)))

    def test_crossover_with_edge_case(self):
        parent1 = ['A', 'B', 'C', 'D', 'E']
        parent2 = ['A', 'B', 'C', 'D', 'E']  # Caso onde os pais são iguais
        child1, child2 = crossover(parent1, parent2)
        
        # Verifica se os filhos são iguais aos pais
        self.assertEqual(child1, parent1)
        self.assertEqual(child2, parent2)

        # Adiciona uma verificação para garantir que a mutação não remove elementos
        self.assertTrue(set(child1).issubset(set(parent1)))
        self.assertTrue(set(child2).issubset(set(parent2)))

    def test_crossover_with_empty_parents(self):
        parent1 = []
        parent2 = []
        with self.assertRaises(ValueError):  # Espera-se que ocorra um erro ao tentar cruzar pais vazios
            crossover(parent1, parent2)

    def test_crossover_with_single_element_parents(self):
        parent1 = ['A']
        parent2 = ['B']
        with self.assertRaises(ValueError):  # Espera-se que ocorra um erro ao tentar cruzar pais com um único elemento
            crossover(parent1, parent2)

    def test_crossover_with_identical_parents(self):
        parent1 = ['A', 'B', 'C']
        parent2 = ['A', 'B', 'C']
        child1, child2 = crossover(parent1, parent2)
        
        # Verifica se os filhos são iguais aos pais
        self.assertEqual(child1, parent1)
        self.assertEqual(child2, parent2)

    def test_crossover_with_repeated_elements(self):
        parent1 = ['A', 'B', 'C', 'A', 'D']
        parent2 = ['A', 'E', 'F', 'A', 'G']
        child1, child2 = crossover(parent1, parent2)

        # Verifica se o ponto inicial e final são os mesmos
        self.assertEqual(child1[0], 'A')
        self.assertEqual(child1[-1], 'A')
        self.assertEqual(child2[0], 'A')
        self.assertEqual(child2[-1], 'A')

        # Verifica se os filhos contêm elementos dos pais
        self.assertTrue(set(child1[1:-1]).issubset(set(parent1[1:] + parent2[1:])))
        self.assertTrue(set(child2[1:-1]).issubset(set(parent1[1:] + parent2[1:])))

if __name__ == '__main__':
    unittest.main() 