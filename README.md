# UNIBRASIL-Maps

## Descrição

O **UNIBRASIL-Maps** é um projeto desenvolvido para otimizar rotas utilizando algoritmos de crossover e mutação, com foco em aplicações de mapeamento e logística. O projeto utiliza técnicas de programação em Python, incluindo manipulação de dados, cálculos de distância e visualização de rotas.

## Funcionalidades

- Cálculo de distâncias entre pontos utilizando a fórmula de Haversine.
- Algoritmos de crossover e mutação para otimização de rotas.
- Exportação de resultados para arquivos CSV.
- Visualização de rotas em gráficos.

## Tecnologias Utilizadas

- Python 3.x
- NumPy
- Pandas
- Haversine
- Matplotlib

## Instalação

Para instalar as dependências necessárias, siga os passos abaixo:

1. Clone o repositório:

   ```bash
   git clone https://github.com/seu_usuario/UNIBRASIL-Maps.git
   cd UNIBRASIL-Maps
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Linux/Mac
   venv\Scripts\activate     # Para Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

Para executar o projeto, você pode usar o seguinte comando:
   ```bash
   python main.py
   ```

Certifique-se de que os arquivos de entrada necessários (como `coordenadas.csv`) estejam disponíveis no diretório correto.

## Testes

O projeto inclui testes automatizados. Para executá-los, use:
   ```bash
   python -m unittest discover -s tests
   ```
