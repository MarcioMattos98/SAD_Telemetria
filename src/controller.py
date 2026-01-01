from dash import Dash, Input, Output
from src.model import CSVTelemetryLoader
from src.view import GraphFactory, DashboardLayout

class AppController:
    def __init__(self, data_path):
        self.app = Dash(__name__)
        # Instanciação do Model
        self.loader = CSVTelemetryLoader(data_path)
        self.data = self.loader.get_data()
        
        # Instanciação da View
        self.layout_manager = DashboardLayout()
        
        # Configuração inicial
        self._setup_layout()
        self._setup_callbacks()

    def _setup_layout(self):
        # Gera os gráficos iniciais
        graphs = {
            'evolution': GraphFactory.create_score_evolution(self.data),
            'infractions': GraphFactory.create_infractions_breakdown(self.data),
            'scatter': GraphFactory.create_scatter_distance_score(self.data),
            'gauge': GraphFactory.create_gauge_current_month(self.data)
        }
        self.app.layout = self.layout_manager.get_layout(graphs)

    def _setup_callbacks(self):
        # Exemplo de interatividade (Callback do Dash)
        @self.app.callback(
            Output('filter-dropdown', 'style'), # Apenas um dummy output para exemplo
            Input('filter-dropdown', 'value')
        )
        def update_dashboard(value):
            # Aqui você implementaria a lógica de filtragem real
            # Para o trabalho, isso mostra que você sabe capturar eventos
            print(f"Usuário selecionou filtro: {value}")
            return {'display': 'block'}

    def run(self):
        # CORREÇÃO AQUI: Mudou de run_server para run
        self.app.run(debug=True)