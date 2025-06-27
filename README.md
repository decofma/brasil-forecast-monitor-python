# Dashboard de Previsão do Tempo para Capitais Brasileiras

!(https://placehold.co/800x400/1f77b4/ffffff?text=Dashboard+de+Previsão+do+Tempo)

Um painel de controle (dashboard) web interativo e elegante, construído com Python e NiceGUI, para visualizar dados meteorológicos atuais e a previsão para as próximas 24 horas das capitais do Brasil.

---

## 🚀 Funcionalidades

- **Página de Boas-vindas:** Uma página inicial que explica o propósito e as funcionalidades da aplicação.
- **Seleção de Capital Dinâmica:** Escolha qualquer capital brasileira a partir de um menu suspenso para carregar instantaneamente os seus dados.
- **Cache de Seleção:** A aplicação "lembra" a última capital que você selecionou, mesmo após fechar o navegador, usando o armazenamento local.
- **Atualização Automática:** Os dados da capital selecionada são atualizados automaticamente a cada 10 minutos, garantindo informações sempre recentes sem qualquer interação manual.
- **Dados em Tempo Real:** Veja a temperatura, umidade, velocidade e direção do vento atuais.
- **Previsão Gráfica 24h:** Um gráfico interativo da Plotly exibe a variação da temperatura e a probabilidade de chuva hora a hora.
- **Visualização Geográfica:** Um mapa da Leaflet mostra a localização da capital selecionada.
- **Interface Reativa:** A interface exibe um "esqueleto" (skeleton UI) enquanto os dados são carregados, garantindo que a aplicação nunca pareça travada.

---

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído utilizando as seguintes tecnologias:

- **[Python](https://www.python.org/)**: A linguagem de programação principal.
- **[NiceGUI](https://nicegui.io/)**: Um framework web baseado em Python para criar interfaces de usuário de forma rápida e fácil.
- **[Pandas](https://pandas.pydata.org/)**: Utilizado para a manipulação e estruturação dos dados horários recebidos da API.
- **[Requests](https://requests.readthedocs.io/en/latest/)**: Para realizar as chamadas HTTP à API de previsão do tempo.
- **[Open-Meteo API](https://open-meteo.com/)**: A fonte de dados meteorológicos, gratuita e de código aberto.

---

## ⚙️ Instalação e Execução

Para executar este projeto localmente, siga os passos abaixo.

### Pré-requisitos

- Python 3.8 ou superior.

### 1. Clonar o Repositório

```bash
git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
cd seu-repositorio
```

### 2. Criar e Ativar um Ambiente Virtual

É uma boa prática criar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar no Windows
.\.venv\Scripts\activate

# Ativar no macOS/Linux
source .venv/bin/activate
```

### 3. Instalar as Dependências

Crie um arquivo `requirements.txt` na raiz do projeto com o seguinte conteúdo:

**requirements.txt**
```
nicegui
pandas
requests
```

Em seguida, instale os pacotes:

```bash
pip install -r requirements.txt
```

### 4. Executar a Aplicação

Com as dependências instaladas, basta executar o script principal:

```bash
# Substitua main.py pelo nome do seu arquivo Python
python main.py
```

A aplicação estará disponível no seu navegador. Abra o link fornecido no terminal (geralmente `http://localhost:8080`).

---

## 📂 Estrutura do Código

O código-fonte está organizado da seguinte forma:

- **`CAPITAIS`**: Um dicionário Python que armazena as coordenadas de todas as capitais brasileiras.
- **`get_weather_data(lat, lon)`**: Função que faz a chamada à API da Open-Meteo, trata erros e devolve os dados em JSON.
- **`@ui.page('/')` (home_page)**: Rota da página inicial que apresenta a aplicação ao usuário.
- **`@ui.page('/dashboard')` (weather_dashboard)**: Rota principal do dashboard, onde toda a visualização de dados acontece.
- **`app.storage.user`**: Utilizado para salvar a última capital selecionada no cache do navegador, proporcionando persistência entre as sessões.
- **`ui.timer`**: Componente usado para disparar a atualização automática dos dados em intervalos definidos (neste caso, 10 minutos).
- **Funções de UI aninhadas:**
    - `mostrar_skeleton()`: Gera uma interface de carregamento para melhorar a experiência do usuário.
    - `display_data(...)`: Constrói dinamicamente os elementos visuais (mapa, cartões, gráfico) com os dados da API.
    - `update_weather_display(...)`: Função assíncrona que orquestra a atualização da UI.