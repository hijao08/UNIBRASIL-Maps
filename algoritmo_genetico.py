import random
import math

def algoritmo_genetico(coordenadas, parametros):
    tamanho_populacao = parametros["tamanho_populacao"]
    num_geracoes = parametros["num_geracoes"]
    taxa_mutacao = parametros["taxa_mutacao"]

    populacao = inicializar_populacao(len(coordenadas), tamanho_populacao)
    for _ in range(num_geracoes):
        aptidoes = [avaliar_individuo(individuo, coordenadas) for individuo in populacao]
        nova_populacao = []
        for _ in range(len(populacao) // 2):
            pai1, pai2 = selecao(populacao, aptidoes)
            filho1, filho2 = crossover(pai1, pai2)
            nova_populacao.extend([mutacao(filho1, taxa_mutacao), mutacao(filho2, taxa_mutacao)])
        populacao = nova_populacao
    melhor_individuo = min(populacao, key=lambda ind: avaliar_individuo(ind, coordenadas))
    return melhor_individuo

def inicializar_populacao(num_pontos, tamanho_populacao):
    return [random.sample(range(num_pontos), num_pontos) for _ in range(tamanho_populacao)]

def avaliar_individuo(individuo, coordenadas):
    distancia_total = 0
    for i in range(len(individuo) - 1):
        coord1 = coordenadas[individuo[i]]
        coord2 = coordenadas[individuo[i + 1]]
        distancia_total += calcular_distancia(coord1, coord2)
    return distancia_total

def calcular_distancia(coord1, coord2):
    lat1, lon1 = map(math.radians, [coord1["latitude"], coord1["longitude"]])
    lat2, lon2 = map(math.radians, [coord2["latitude"], coord2["longitude"]])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    return 6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def selecao(populacao, aptidoes):
    total_aptidao = sum(aptidoes)
    selecionados = random.choices(populacao, weights=[1 / apt for apt in aptidoes], k=2)
    return selecionados

def crossover(pai1, pai2):
    corte = random.randint(0, len(pai1) - 1)
    filho1 = pai1[:corte] + [gene for gene in pai2 if gene not in pai1[:corte]]
    filho2 = pai2[:corte] + [gene for gene in pai1 if gene not in pai2[:corte]]
    return filho1, filho2

def mutacao(individuo, taxa_mutacao):
    if random.random() < taxa_mutacao:
        idx1, idx2 = random.sample(range(len(individuo)), 2)
        individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]
    return individuo
