import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html

class GraphFactory:
    """
    Fábrica de gráficos. Segue OCP: se quiser um novo gráfico, 
    crie um novo método sem quebrar os outros.
    """
    
    @staticmethod
    def create_score_evolution(df):
        # Gráfico 1: Linha - Evolução da Pontuação
        fig = px.line(df, x='Mes', y='Score', markers=True, 
                      title='Evolução da Pontuação de Segurança (Últimos 6 Meses)',
                      color_discrete_sequence=['#2ecc71'])
        fig.update_yaxes(range=[0, 100]) # Score vai até 100
        return fig

    @staticmethod
    def create_infractions_breakdown(df):
        # Gráfico 2: Barras Empilhadas - Tipos de Infração
        # Precisamos derreter (melt) o dataframe para formato longo
        df_melted = df.melt(id_vars=['Mes'], 
                            value_vars=['Aceleracao_Brusca', 'Freada_Brusca', 'Curva_Brusca', 'Exc_Velocidade'],
                            var_name='Tipo_Infracao', value_name='Qtd')
        
        fig = px.bar(df_melted, x='Mes', y='Qtd', color='Tipo_Infracao',
                     title='Detalhamento de Infrações por Mês',
                     barmode='group')
        return fig

    @staticmethod
    def create_scatter_distance_score(df):
        # Gráfico 3: Dispersão - Distância vs Score
        fig = px.scatter(df, x='Distancia', y='Score', 
                         size='Freada_Brusca', # Tamanho da bolha = qtd de freadas
                         hover_data=['Mes'],
                         title='Correlação: Distância Percorrida vs Pontuação',
                         color='Score', color_continuous_scale='RdYlGn')
        return fig

    @staticmethod
    def create_gauge_current_month(df):
        # Gráfico 4: Gauge - Score Médio do último mês
        last_month_score = df.iloc[-1]['Score']
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = last_month_score,
            title = {'text': "Pontuação Atual (Novembro)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "red"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}],
            }
        ))
        return fig

class DashboardLayout:
    """
    Define a estrutura HTML do Dashboard.
    """
    def __init__(self):
        pass
    
    def get_layout(self, graphs):
        return html.Div([
            html.H1("SAD - Sistema de Apoio à Decisão: Frota Romestur", 
                    style={'textAlign': 'center', 'fontFamily': 'Arial'}),
            
            html.Div([
                html.H3("Análise de Telemetria (Jun - Nov 2025)", style={'textAlign': 'center'}),
                html.P("Este painel apoia a decisão sobre quais motoristas precisam de retreinamento.", 
                       style={'textAlign': 'center'})
            ]),

            html.Hr(),

            # Grid de Gráficos
            html.Div([
                html.Div([dcc.Graph(figure=graphs['evolution'])], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(figure=graphs['infractions'])], style={'width': '48%', 'display': 'inline-block'}),
            ]),

            html.Div([
                html.Div([dcc.Graph(figure=graphs['scatter'])], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(figure=graphs['gauge'])], style={'width': '48%', 'display': 'inline-block'}),
            ]),
            
            # Área de Controle Interativo (Simulado para o requisito)
            html.Div([
                html.Label("Filtrar por Gravidade (Interatividade):"),
                dcc.Dropdown(
                    options=[
                        {'label': 'Todos os Veículos', 'value': 'ALL'},
                        {'label': 'Apenas Críticos (Score < 70)', 'value': 'CRITIC'}
                    ],
                    value='ALL',
                    id='filter-dropdown'
                )
            ], style={'padding': '20px'})
        ])