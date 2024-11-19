import matplotlib.pyplot as plt

def plot_route(coordinates, route, generation):
    """Plota a rota do drone em um gráfico."""
    if not route:  # Verifica se a rota está vazia
        raise ValueError("A rota não pode estar vazia.")
    
    lats = [coordinates[point][0] for point in route]
    lons = [coordinates[point][1] for point in route]
    
    plt.figure(figsize=(10, 6))
    plt.plot(lons, lats, 'o-', label=f'Geração {generation}')
    
    for i, (lon, lat) in enumerate(zip(lons, lats)):
        if i == 0 or i == len(route) - 1:
            plt.plot(lon, lat, 'ro', markersize=10)
            plt.annotate(f'Início/Fim', (lon, lat), 
                        xytext=(5, 5), textcoords='offset points',
                        color='red', fontweight='bold')
        else:
            plt.annotate(f'{i}', (lon, lat), 
                        xytext=(5, 5), textcoords='offset points',
                        fontsize=9, fontweight='bold')
    
    plt.title(f'Caminho na Geração {generation}')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.legend()
    plt.show() 