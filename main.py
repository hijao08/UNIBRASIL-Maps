from algoritmo_genetico import algoritmo_genetico
from utils import salvar_rota_completa

# Configurações
ARQUIVO_COORDENADAS = "coordenadas.csv"
ARQUIVO_SAIDA = "rota_completa.csv"
AUTONOMIA = 1800  # segundos
VELOCIDADE_BASE = 30  # km/h
VENTOS = -4.22  # km/h
MAX_HORAS_VOO_DIARIO = 13 * 3600  # 06:00 às 19:00

def carregar_coordenadas(arquivo):
    """
    Carrega as coordenadas a partir do arquivo CSV.
    """
    import csv
    coordenadas = []
    with open(arquivo, 'r') as f:
        leitor = csv.DictReader(f)
        print(f"Colunas detectadas no CSV: {leitor.fieldnames}")
        for linha in leitor:
            coordenadas.append({
                "cep": linha["cep"],
                "latitude": float(linha["latitude"]),
                "longitude": float(linha["longitude"])
            })
    return coordenadas

# Carregar coordenadas
coordenadas = carregar_coordenadas(ARQUIVO_COORDENADAS)

# Configuração do algoritmo genético
parametros_algoritmo = {
    "tamanho_populacao": 100,
    "num_geracoes": 50,
    "taxa_mutacao": 0.1,
    "tamanho_elite": 5
}

# Executar algoritmo genético
melhor_rota_indices = algoritmo_genetico(coordenadas, parametros_algoritmo)

# Construir rota completa
rota_completa = [coordenadas[i] for i in melhor_rota_indices]

# Criar lista de dias para o voo (exemplo simples, pode ser ajustado)
dia_do_voo = [1] * len(rota_completa)  # Ajustar para calcular dias reais se necessário

# Salvar rota completa
salvar_rota_completa(rota_completa, ARQUIVO_SAIDA, dia_do_voo)

print(f"Rota completa salva em {ARQUIVO_SAIDA}")
