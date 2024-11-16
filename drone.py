import math
from datetime import datetime, timedelta

def ajusta_para_horario_comercial(horario_atual, inicio=6, fim=19):
    if horario_atual.hour < inicio:
        return horario_atual.replace(hour=inicio, minute=0, second=0, microsecond=0)
    elif horario_atual.hour >= fim:
        proximo_dia = horario_atual + timedelta(days=1)
        return proximo_dia.replace(hour=inicio, minute=0, second=0, microsecond=0)
    return horario_atual

def verifica_e_paused_horario_comercial(horario_atual, inicio=6, fim=19):
    if horario_atual.hour < inicio or horario_atual.hour >= fim:
        horario_ajustado = ajusta_para_horario_comercial(horario_atual, inicio, fim)
        print(f"Operação fora do horário comercial. Pausando até {horario_ajustado}.")
        return horario_ajustado
    return None

# Exemplo de integração na lógica existente do drone
horario_atual = datetime.now()
novo_horario = verifica_e_paused_horario_comercial(horario_atual)
if novo_horario:
    exit()  # Sai do script se estiver fora do horário comercial

class Drone:
    def __init__(self, coordenadas, autonomia, custo_parada):
        self.coordenadas = coordenadas
        self.autonomia = autonomia
        self.custo_parada = custo_parada

    def calcular_distancia(self, coord1, coord2):
        """Calcula a distância entre duas coordenadas geográficas."""
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        R = 6371  # Raio da Terra em km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def calcular_consumo_bateria(self, distancia, velocidade):
        """Calcula o consumo de bateria com base na distância e velocidade."""
        autonomia_base = 1800  # segundos
        velocidade_base = 30  # km/h
        consumo_base = velocidade_base / autonomia_base

        if velocidade > velocidade_base:
            consumo = consumo_base * (1 + (velocidade - velocidade_base) * 0.05)
        else:
            consumo = consumo_base

        return consumo * distancia

    def custo_total(self, rota):
        """Calcula o custo total de uma rota, incluindo tempo e paradas."""
        custo_total = 0
        bateria_restante = self.autonomia
        tempo_total = 0

        for i in range(len(rota) - 1):
            ponto_a = rota[i]
            ponto_b = rota[i + 1]

            distancia = self.calcular_distancia(
                (ponto_a['latitude'], ponto_a['longitude']),
                (ponto_b['latitude'], ponto_b['longitude'])
            )
            consumo = self.calcular_consumo_bateria(distancia, 30)

            if bateria_restante < consumo:
                custo_total += self.custo_parada
                bateria_restante = self.autonomia

            bateria_restante -= consumo
            tempo_total += distancia / 30 * 3600

        return custo_total + tempo_total
