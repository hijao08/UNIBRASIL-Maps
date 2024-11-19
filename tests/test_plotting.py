import unittest
from unittest.mock import patch
from plotting import plot_route

class TestPlotting(unittest.TestCase):

    @patch('matplotlib.pyplot.show')
    def test_plot_route(self, mock_show):
        coordinates = {'A': (0, 0), 'B': (1, 1), 'C': (2, 2)}
        route = ['A', 'B', 'C']
        generation = 1
        
        plot_route(coordinates, route, generation)
        
        # Verifica se a função show foi chamada
        mock_show.assert_called_once()

    def test_plot_route_empty(self):
        coordinates = {}
        route = []
        generation = 1
        
        with self.assertRaises(ValueError):  # Espera-se que ocorra um erro ao tentar plotar uma rota vazia
            plot_route(coordinates, route, generation)

    def test_plot_route_with_invalid_coordinates(self):
        coordinates = {'A': (0, 0)}
        route = ['A', 'B']  # 'B' não está nas coordenadas
        generation = 1
        
        with self.assertRaises(KeyError):  # Espera-se que ocorra um erro ao tentar plotar uma rota com coordenadas inválidas
            plot_route(coordinates, route, generation)

    def test_plot_route_with_empty_route(self):
        coordinates = {'A': (0, 0)}
        route = []  # Rota vazia
        generation = 1
        
        with self.assertRaises(ValueError):  # Espera-se que ocorra um erro ao tentar plotar uma rota vazia
            plot_route(coordinates, route, generation)

if __name__ == '__main__':
    unittest.main() 