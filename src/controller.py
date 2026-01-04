from dash import Dash, Input, Output
from src.model import CSVTelemetryLoader
from src.view import GraphFactory, DashboardLayout

class AppController:
    def __init__(self, data_path):
        self.app = Dash(__name__)
        
        # Carrega todos os dados
        self.loader = CSVTelemetryLoader(data_path)
        self.full_data = self.loader.get_data()
        
        # Descobre quais veículos existem para colocar no menu
        unique_vehicles = self.full_data['Veiculo'].unique()
        self.vehicle_options = [{'label': v, 'value': v} for v in unique_vehicles]
        
        self.layout_manager = DashboardLayout()
        self._setup_layout()
        self._setup_callbacks()

    def _setup_layout(self):
        self.app.layout = self.layout_manager.get_layout(self.vehicle_options)

    def _setup_callbacks(self):
        @self.app.callback(
            [Output('graph-evolution', 'figure'),
             Output('graph-infractions', 'figure'),
             Output('graph-scatter', 'figure'),
             Output('graph-gauge', 'figure')],
            [Input('vehicle-selector', 'value')]
        )
        def update_dashboard(selected_vehicle):
            print(f"Usuário selecionou: {selected_vehicle}")
            
            # filtra os dados apenas para o veículo escolhido
            filtered_df = self.full_data[self.full_data['Veiculo'] == selected_vehicle].copy()
            
            # Recria os gráficos com os dados filtrados
            fig1 = GraphFactory.create_score_evolution(filtered_df)
            fig2 = GraphFactory.create_infractions_breakdown(filtered_df)
            fig3 = GraphFactory.create_scatter_distance_score(filtered_df)
            fig4 = GraphFactory.create_gauge_current_month(filtered_df)
            
            return fig1, fig2, fig3, fig4

    def run(self):
        self.app.run(debug=True)