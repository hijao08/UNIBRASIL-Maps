import unittest
from io_operations import load_coordinates, export_results_to_csv
import os
import glob

class TestIOOperations(unittest.TestCase):

    def test_load_coordinates(self):
        coordinates, ceps = load_coordinates('csv/coordenadas.csv')  # Certifique-se de que este arquivo existe
        self.assertIsInstance(coordinates, dict)  # Deve retornar um dicionário
        self.assertIsInstance(ceps, dict)          # Deve retornar um dicionário

    def test_export_results_to_csv(self):
        best_route = ['A', 'B', 'C']
        best_distance = 10.0
        best_time = 1.0
        coordinates = {'A': (0, 0), 'B': (1, 1), 'C': (2, 2)}
        route_status = [{'ponto': 'A', 'acao': 'FOTO', 'dia': 1, 'horario': '06:00'},
                        {'ponto': 'B', 'acao': 'FOTO', 'dia': 1, 'horario': '06:10'}]
        ceps = {'A': 12345, 'B': 67890, 'C': 54321}

        export_results_to_csv(best_route, best_distance, best_time, coordinates, route_status, ceps)

        # Verifica se o arquivo foi criado
        files = glob.glob('resultados_rota_*.csv')
        self.assertTrue(len(files) > 0)  # Verifica se pelo menos um arquivo foi criado

    def test_export_results_to_csv_with_empty_route(self):
        best_route = []
        best_distance = 0.0
        best_time = 0.0
        coordinates = {}
        route_status = []
        ceps = {}

        with self.assertRaises(ValueError):  # Espera-se que ocorra um erro ao tentar exportar uma rota vazia
            export_results_to_csv(best_route, best_distance, best_time, coordinates, route_status, ceps)

    def test_export_results_to_csv_with_single_point(self):
        best_route = ['A']
        best_distance = 10.0
        best_time = 1.0
        coordinates = {'A': (0, 0)}
        route_status = [{'ponto': 'A', 'acao': 'FOTO', 'dia': 1, 'horario': '06:00'}]
        ceps = {'A': 12345}

        export_results_to_csv(best_route, best_distance, best_time, coordinates, route_status, ceps)

        # Verifica se o arquivo foi criado
        files = glob.glob('resultados_rota_*.csv')
        self.assertTrue(len(files) > 0)  # Verifica se pelo menos um arquivo foi criado

if __name__ == '__main__':
    unittest.main() 