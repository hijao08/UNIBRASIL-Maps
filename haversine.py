import math

def haversine(lat1, lon1, lat2, lon2):
    """Calcula a distância entre dois pontos geográficos usando a fórmula de Haversine."""
    R = 6371.0  # Raio da Terra em Km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Retorna a distância em Km