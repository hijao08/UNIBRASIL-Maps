# Gerenciamento de Rotas de Drone

Este projeto é uma solução para a otimização de rotas de coleta de dados utilizando drones. Ele considera restrições meteorológicas, de horário de operação e autonomia do drone, oferecendo um planejamento eficiente para garantir a conclusão das coletas dentro de 5 dias.

## Objetivos

- **Planejamento de Rota**: Determinar a rota mais eficiente para o drone realizar coletas em coordenadas específicas.
- **Respeito às Restrições**:
  - Operação permitida apenas das **06:00 às 19:00**.
  - Pouso obrigatório para recarga após 19:00.
  - Todas as coletas devem ser realizadas em até **5 dias**.
- **Adaptação Meteorológica**: Ajustar a autonomia do drone considerando a velocidade e direção do vento.

## Requisitos

- Python 3.8+
- Bibliotecas:
  - pandas
  - numpy
  - matplotlib
  - geopy
  - outras, listadas no `requirements.txt` (se aplicável)

## Estrutura do Projeto

- **`algoritmo_genetico.py`**: Implementação do algoritmo genético para otimização de rotas.
- **`drone.py`**: Definição das funcionalidades do drone, como autonomia e adaptação às condições meteorológicas.
- **`main.py`**: Ponto de entrada do programa. Integra as funcionalidades do projeto.
- **`utils.py`**: Funções auxiliares para cálculos e manipulação de dados.
- **`coordenadas.csv`**: Coordenadas das localidades de coleta.
- **`dados_meteorologicos.csv`**: Previsão de condições climáticas (velocidade e direção do vento).
- **`rota_completa.csv`**: Resultado final contendo a rota detalhada.

## Funcionalidades

- **Algoritmo Genético**: Otimiza a ordem das coletas para minimizar o tempo e respeitar as restrições.
- **Ajuste por Condições Climáticas**: Modifica a autonomia do drone com base em dados meteorológicos.
- **Planejamento de Dias**: Garante que as operações aconteçam somente durante o período permitido.

## Como Executar

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu_usuario/seu_repositorio.git
   cd seu_repositorio

2. Instale as dependências:

```bash
pip install -r requirements.txt
```
3. Execute o script principal:
```bash
python main.py
```
4. Os resultados serão salvos no arquivo rota_completa.csv.

Exemplo de Uso
Entrada:
Coordenadas das localidades (coordenadas.csv).
Previsão meteorológica (dados_meteorologicos.csv).
Saída:
Rota otimizada com dias e horários detalhados.
