import secrets
import string
import requests
from nicegui import app, ui, run

def generate_random_string(length=32):
    """Generate a random string of specified length."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

app.storage.secret = generate_random_string()

# --- 1. ESTRUTURA DE DADOS DAS CAPITAIS  ---
CAPITAIS = {
    'Aracaju': {'lat': -10.9472, 'lon': -37.0731}, 'Belém': {'lat': -1.4558, 'lon': -48.4902},
    'Belo Horizonte': {'lat': -19.9167, 'lon': -43.9345}, 'Boa Vista': {'lat': 2.8238, 'lon': -60.6753},
    'Brasília': {'lat': -15.7939, 'lon': -47.8828}, 'Campo Grande': {'lat': -20.4697, 'lon': -54.6201},
    'Cuiabá': {'lat': -15.6014, 'lon': -56.0979}, 'Curitiba': {'lat': -25.4284, 'lon': -49.2733},
    'Florianópolis': {'lat': -27.5954, 'lon': -48.5480}, 'Fortaleza': {'lat': -3.7172, 'lon': -38.5433},
    'Goiânia': {'lat': -16.6869, 'lon': -49.2648}, 'João Pessoa': {'lat': -7.1195, 'lon': -34.8450},
    'Macapá': {'lat': 0.0349, 'lon': -51.0694}, 'Maceió': {'lat': -9.6658, 'lon': -35.7350},
    'Manaus': {'lat': -3.1190, 'lon': -60.0217}, 'Natal': {'lat': -5.7945, 'lon': -35.2110},
    'Palmas': {'lat': -10.2491, 'lon': -48.3243}, 'Porto Alegre': {'lat': -30.0346, 'lon': -51.2177},
    'Porto Velho': {'lat': -8.7608, 'lon': -63.8999}, 'Recife': {'lat': -8.0476, 'lon': -34.8770},
    'Rio Branco': {'lat': -9.9754, 'lon': -67.8243}, 'Rio de Janeiro': {'lat': -22.9068, 'lon': -43.1729},
    'Salvador': {'lat': -12.9714, 'lon': -38.5014}, 'São Luís': {'lat': -2.5307, 'lon': -44.3068},
    'São Paulo': {'lat': -23.5505, 'lon': -46.6333}, 'Teresina': {'lat': -5.0892, 'lon': -42.8016},
    'Vitória': {'lat': -20.3155, 'lon': -40.3128},
}

# --- 2. FUNÇÃO DA API ---
def get_weather_data(lat, lon):
    """Busca os dados da API para uma latitude e longitude específicas."""
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation,rain,wind_direction_10m&hourly=temperature_2m,precipitation_probability&forecast_days=1"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Erro ao buscar dados da API: {e}")
        return None

# --- 3. PÁGINA HOME ---
@ui.page('/')
def home_page():
    """Página inicial que explica a aplicação."""
    with ui.column().classes('w-full h-screen items-center justify-center gap-4'):
        with ui.card().classes('w-full max-w-lg items-center'):
            ui.label('Bem-vindo à Previsão do Tempo!').classes('text-2xl font-bold')
            ui.markdown('''
                Este painel interativo permite que você consulte os dados meteorológicos
                atuais e a previsão para as próximas 24 horas para todas as capitais do Brasil.

                **Funcionalidades:** </br>
                - **Seleção de Capital:** Escolha uma capital no menu suspenso. </br>
                - **Dados Atuais:** Veja temperatura, umidade e informações do vento. </br>
                - **Previsão Gráfica:** Acompanhe a variação da temperatura e a probabilidade de chuva. </br>
                - **Atualização Automática:** Os dados da capital selecionada são atualizados a cada 10 minutos. </br>

                Clique no botão abaixo para começar!
            ''').classes('text-base')
            ui.button('Acessar o Dashboard', on_click=lambda: ui.navigate.to('/dashboard'))

# --- 4. DASHBOARD DE PREVISÃO DO TEMPO ---
@ui.page('/dashboard')
def weather_dashboard():
    
    with ui.header(elevated=True).classes('items-center justify-between p-2'):
        ui.label('Previsão do Tempo no Brasil').classes('text-lg font-bold')
        
        capital_inicial = app.storage.user.get('capital_selecionada', 'São Paulo')

        seletor_capital = ui.select(
            options=list(CAPITAIS.keys()),
            label='Selecione uma Capital',
            value=capital_inicial,
            on_change=lambda e: update_weather_display(e.value)
        ).classes('w-72').props('dark dense standout="bg-blue-grey-2"')
        
    with ui.column().classes('w-full items-center'):
        
        with ui.row(align_items='center').classes('text-sm text-gray-500 mt-2'):
            ui.icon('info').classes('mr-1')
            ui.label('Os dados da capital selecionada são atualizados automaticamente a cada 10 minutos.')

        weather_display_area = ui.column().classes('w-full items-center mt-4')

    def mostrar_skeleton():
        with weather_display_area:
            ui.skeleton().classes('w-64 h-8 mx-auto my-4')
            ui.skeleton().classes('w-full h-60 mx-auto')
            with ui.row().classes('w-full gap-4 p-4 justify-center'):
                ui.skeleton().classes('w-full max-w-lg h-96')
                ui.skeleton().classes('w-full max-w-lg h-96')

    def display_data(weather_data, capital_nome, capital_lat, capital_lon):
        ui.label(f'Dados Meteorológicos para {capital_nome}').classes('text-2xl font-bold mt-4 mb-2 text-center')
        options = {'zoomControl': False, 'scrollWheelZoom': False, 'doubleClickZoom': False, 'boxZoom': False, 'keyboard': False, 'dragging': False, 'touchZoom': False}
        map2 = ui.leaflet(center=(capital_lat, capital_lon), zoom=7, options=options)
        map2.clear_layers()
        map2.wms_layer(url_template='http://ows.mundialis.de/services/service?', options={'layers': 'TOPO-WMS,OSM-Overlay-WMS'})

        with ui.row().classes('w-full gap-4 p-4 justify-center'):
            current = weather_data['current']
            with ui.card().classes('w-full max-w-lg h-96 mx-auto items-center'):
                ui.label('Dados Atuais').classes('text-lg font-bold')
                with ui.grid(columns=2).classes('w-full gap-4 p-4'):
                    with ui.element('div').classes('text-center'):
                        ui.label('Temperatura').classes('text-sm font-semibold text-gray-500')
                        ui.label(f"{current['temperature_2m']} °C").classes('text-4xl font-bold')
                    with ui.element('div').classes('text-center'):
                        ui.label('Umidade').classes('text-sm font-semibold text-gray-500')
                        ui.label(f"{current['relative_humidity_2m']} %").classes('text-4xl font-bold')
                    with ui.element('div').classes('text-center border-t pt-2'):
                        ui.label('Vento').classes('text-sm font-semibold text-gray-500')
                        ui.label(f"{current['wind_speed_10m']} km/h").classes('text-xl')
                    with ui.element('div').classes('text-center border-t pt-2'):
                        ui.label('Direção do Vento').classes('text-sm font-semibold text-gray-500')
                        ui.label(f"{current['wind_direction_10m']} °").classes('text-xl')
            with ui.card().classes('w-full max-w-lg h-96 mx-auto items-center'):
                ui.label('Previsão do Tempo').classes('text-lg font-bold')
                hourly_data = weather_data['hourly']
                horas_formatadas = [t[11:16] for t in hourly_data['time']]
                temperaturas = hourly_data['temperature_2m']
                prob_chuva = hourly_data['precipitation_probability']

                figure = {
                    'data': [
                        {
                            'type': 'scatter', 'mode': 'lines+markers', 'name': 'Temperatura',
                            'x': horas_formatadas,
                            'y': temperaturas,  
                            'yaxis': 'y1', 'line': {'color': '#d62728'}
                        },
                        {
                            'type': 'bar', 'name': 'Prob. de Chuva',
                            'x': horas_formatadas,
                            'y': prob_chuva,  
                            'yaxis': 'y2', 'marker': {'color': '#1f77b4'}
                        }
                    ],
                    'layout': {
                        'title': {'text': 'Temperatura e Probabilidade de Chuva'},
                        'xaxis': {'title': 'Hora'},
                        'yaxis': {'title': 'Temperatura (°C)', 'titlefont': {'color': '#d62728'}, 'tickfont': {'color': '#d62728'}},
                        'yaxis2': {'title': 'Prob. de Chuva (%)', 'titlefont': {'color': '#1f77b4'}, 'tickfont': {'color': '#1f77b4'}, 'overlaying': 'y', 'side': 'right', 'range': [0, 100]},
                        'legend': {'orientation': 'h', 'y': 1.15, 'x': 0.5, 'xanchor': 'center'}
                    }
                }
                ui.plotly(figure).classes('w-full max-w-4xl h-full')

    async def update_weather_display(capital_selecionada: str):
        if not capital_selecionada:
            return

        app.storage.user['capital_selecionada'] = capital_selecionada
        
        weather_display_area.clear()
        mostrar_skeleton()
        coords = CAPITAIS[capital_selecionada]
        weather_data = await run.io_bound(get_weather_data, coords['lat'], coords['lon'])

        weather_display_area.clear()
        with weather_display_area:
            if weather_data:
                display_data(weather_data, capital_selecionada, coords['lat'], coords['lon'])
            else:
                ui.label(f'Não foi possível carregar os dados para {capital_selecionada}.').classes('text-red-500 text-center')

    ui.timer(0.1, lambda: update_weather_display(seletor_capital.value), once=True)
    ui.timer(600, lambda: update_weather_display(seletor_capital.value) if seletor_capital.value else None)

  
# --- PARA RODAR LOCAL ---
# ui.run(
#     storage_secret='CHAVE_SECRETA_PODE_SER_QUALQUER_COISA_123',
#     uvicorn_reload_dirs='.',
#     uvicorn_reload_includes='*.py',
#     title='Previsão do Tempo',
#     favicon='☀️',
#     dark=True
# )