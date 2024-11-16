import csv
import math
from datetime import datetime, timedelta

def calcular_tempo(distancia, velocidade):
    """Calcula o tempo de viagem em segundos com base na distância e velocidade."""
    return math.ceil((distancia / velocidade) * 3600)  # Converte horas em segundos

def calcular_distancia(lat1, lon1, lat2, lon2):
    """Calcula a distância em km entre dois pontos geográficos usando a fórmula de Haversine."""
    R = 6371  # Raio da Terra em km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) ** 2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def salvar_rota_completa(rota, arquivo_saida, dia_do_voo, autonomia=1800, velocidade_base=30):
    """
    Salva a rota completa em um arquivo CSV com os campos especificados nos requisitos.
    """
    with open(arquivo_saida, 'w', newline='') as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow([
            "CEP inicial", "Latitude inicial", "Longitude inicial",
            "Dia do voo", "Hora inicial", "Velocidade",
            "CEP final", "Latitude final", "Longitude final",
            "Pouso", "Hora final"
        ])
        
        bateria_restante = autonomia
        hora_atual = datetime.strptime("06:00:00", "%H:%M:%S")
        
        for i in range(len(rota) - 1):
            ponto_atual = rota[i]
            proximo_ponto = rota[i + 1]
            dia = dia_do_voo[i]
            
            # Calcula distância e tempo de voo
            distancia = calcular_distancia(
                ponto_atual['latitude'], ponto_atual['longitude'],
                proximo_ponto['latitude'], proximo_ponto['longitude']
            )
            tempo_voo = calcular_tempo(distancia, velocidade_base)
            
            # Atualiza a bateria restante e verifica necessidade de pouso
            pouso = "NÃO"
            if tempo_voo > bateria_restante:
                pouso = "SIM"
                bateria_restante = autonomia - 60  # Consome 1 minuto para recarga
                hora_atual += timedelta(seconds=60)  # Atualiza horário
            
            bateria_restante -= tempo_voo
            hora_final = hora_atual + timedelta(seconds=tempo_voo)
            
            escritor.writerow([
                ponto_atual['cep'], ponto_atual['latitude'], ponto_atual['longitude'],
                dia, hora_atual.strftime("%H:%M:%S"), velocidade_base,
                proximo_ponto['cep'], proximo_ponto['latitude'], proximo_ponto['longitude'],
                pouso, hora_final.strftime("%H:%M:%S")
            ])
            
            # Atualiza hora atual
            hora_atual = hora_final
