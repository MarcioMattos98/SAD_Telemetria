import pandas as pd
from abc import ABC, abstractmethod

class IDataSource(ABC):
    @abstractmethod
    def get_data(self):
        pass

class CSVTelemetryLoader(IDataSource):
    def __init__(self, file_path):
        self.file_path = file_path

    def get_data(self):
        # 1. LEITURA EXATA BASEADA NO SEU ARQUIVO
        # O encoding 'latin-1' ou 'cp1252' é o padrão do Excel no Brasil
        try:
            df = pd.read_csv(self.file_path, sep=';', encoding='cp1252')
        except:
            df = pd.read_csv(self.file_path, sep=';', encoding='utf-8-sig')

        # 2. LIMPEZA DE LINHAS INÚTEIS
        # Remove a linha que contém "Pontos adicionados/removidos"
        # Remove as linhas de "Total" e "Média"
        # Removemos qualquer linha onde a coluna 'Descrição do ativo' esteja vazia
        df = df[df['Descrição do ativo'].notna()]
        
        # Filtra para manter apenas linhas onde 'Descrição do ativo' contém "M.B." (Modelo do onibus)
        # Isso elimina automaticamente as linhas de cabeçalho extra, Total e Média
        df = df[df['Descrição do ativo'].astype(str).str.contains('M.B.', na=False)]

        # 3. RENOMEAÇÃO DAS COLUNAS
        # Mapeamos as colunas do CSV para os nomes internos do sistema
        col_map = {
            'Descrição do ativo': 'Veiculo',  # AQUI ESTAVA O ERRO ANTES
            'distância (km)': 'Distancia',
            'Pontuação avançada': 'Score',
            '(Tr) Aceleração Brusca': 'Aceleracao_Brusca',
            '(Tr) Freada Brusca': 'Freada_Brusca',
            '(Tr) Curva Brusca': 'Curva_Brusca',
            '(Tr) Excesso de Velocidade 85 Km': 'Exc_Velocidade'
        }
        df.rename(columns=col_map, inplace=True)

        # 4. TRATAMENTO DE NÚMEROS (FORMATO BRASILEIRO)
        # Transforma "1.580,30" em 1580.30
        cols_to_fix = ['Distancia', 'Score', 'Aceleracao_Brusca', 'Freada_Brusca', 'Curva_Brusca', 'Exc_Velocidade']
        
        for col in cols_to_fix:
            if col in df.columns:
                # Remove o ponto de milhar (1.000 -> 1000)
                # Troca a vírgula decimal por ponto (1000,50 -> 1000.50)
                if df[col].dtype == object:
                    df[col] = df[col].astype(str).str.replace('.', '', regex=False)
                    df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
                
                # Converte para número
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # 5. CRIAÇÃO DOS MESES
        # Como o nome do mês está na primeira coluna misturado com texto (Ex: "Bureal Veritas - Junho 2025")
        # Vamos tentar extrair o mês dali. Se falhar, usa a lista fixa.
        
        try:
            # Tenta pegar o texto após o hífen. Ex: "Bureal Veritas - Junho 2025" -> "Junho 2025"
            # O split(' - ') vai dividir o texto. Pegamos a parte 1.
            # Ajuste: A coluna original era 'Ativo Nome da garagem'
            if 'Ativo Nome da garagem' in df.columns:
                df['Mes'] = df['Ativo Nome da garagem'].astype(str).apply(lambda x: x.split('-')[1].strip() if '-' in x else x)
            else:
                raise Exception("Coluna original não encontrada")
        except:
            # Fallback: Se der erro na extração, usa a lista manual sequencial
            meses_fixos = ['Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro']
            # Garante que a lista tem o tamanho dos dados
            if len(df) > len(meses_fixos):
                # Repete a lista se tiver mais dados
                meses_fixos = (meses_fixos * ((len(df) // len(meses_fixos)) + 1))
            df['Mes'] = meses_fixos[:len(df)]

        return df