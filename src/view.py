import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html

class GraphFactory:
    @staticmethod
    def create_score_evolution(df):
        # Gráfico de linha
        fig = px.line(df, x='Mes', y='Score', markers=True, 
                      title='Evolução da Pontuação de Segurança',
                      color_discrete_sequence=['#2ecc71'])
        fig.update_yaxes(range=[0, 105])
        return fig

    @staticmethod
    def create_infractions_breakdown(df):
        # Gráfico de barras
        df_melted = df.melt(id_vars=['Mes'], 
                            value_vars=['Aceleracao_Brusca', 'Freada_Brusca', 'Curva_Brusca', 'Exc_Velocidade'],
                            var_name='Tipo_Infracao', value_name='Qtd')
        
        fig = px.bar(df_melted, x='Mes', y='Qtd', color='Tipo_Infracao',
                     title='Detalhamento de Infrações',
                     barmode='group')
        return fig

    @staticmethod
    def create_scatter_distance_score(df):
        # Gráfico de dispersão
        fig = px.scatter(df, x='Distancia', y='Score', 
                         size='Freada_Brusca', 
                         hover_data=['Mes'],
                         title='Distância vs Pontuação (Tamanho = Freadas)',
                         color='Score', color_continuous_scale='RdYlGn')
        return fig

    @staticmethod
    def create_gauge_current_month(df):
        # Pega o último mês disponível deste veículo específico
        if len(df) > 0:
            last_month_score = df.iloc[-1]['Score']
            mes_nome = df.iloc[-1]['Mes']
        else:
            last_month_score = 0
            mes_nome = "--"
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = last_month_score,
            title = {'text': f"Pontuação Atual ({mes_nome})"},
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
    def get_layout(self, vehicle_options):
        return html.Div([
            html.H1("SAD - Sistema de Apoio à Decisão: Frota Romestur", 
                    style={'textAlign': 'center', 'fontFamily': 'Arial', 'color': '#333'}),
            
            # --- ÁREA DE SELEÇÃO (INTERATIVIDADE) ---
            html.Div([
                html.Label("Selecione o Veículo para Análise:", style={'fontWeight': 'bold', 'fontSize': '18px'}),
                dcc.Dropdown(
                    id='vehicle-selector',
                    options=vehicle_options, # Lista de veiculos que vem do banco de dados
                    value=vehicle_options[0]['value'] if vehicle_options else None, # Seleciona o primeiro por padrão
                    clearable=False,
                    style={'width': '50%', 'margin': 'auto'}
                ),
            ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#f9f9f9', 'borderRadius': '10px'}),

            html.Hr(),

            # --- ÁREA DOS GRÁFICOS (Ids necessários para o Callback) ---
            html.Div([
                html.Div([dcc.Graph(id='graph-evolution')], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(id='graph-infractions')], style={'width': '48%', 'display': 'inline-block'}),
            ]),

            html.Div([
                html.Div([dcc.Graph(id='graph-scatter')], style={'width': '48%', 'display': 'inline-block'}),
                html.Div([dcc.Graph(id='graph-gauge')], style={'width': '48%', 'display': 'inline-block'}),
            ]),
        ], style={'padding': '20px'})