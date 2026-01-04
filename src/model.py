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
        
        try:
            df = pd.read_csv(self.file_path, sep=';', encoding='cp1252')
        except:
            df = pd.read_csv(self.file_path, sep=';', encoding='utf-8-sig')

        # Remoção de linhas com valores nulos na coluna 'Descrição do ativo'
        df = df[df['Descrição do ativo'].notna()]
        
        df = df[df['Descrição do ativo'].astype(str).str.contains('M.B.', na=False)]

        # Renomeia colunas para facilitar o uso
        col_map = {
            'Descrição do ativo': 'Veiculo', 
            'distância (km)': 'Distancia',
            'Pontuação avançada': 'Score',
            '(Tr) Aceleração Brusca': 'Aceleracao_Brusca',
            '(Tr) Freada Brusca': 'Freada_Brusca',
            '(Tr) Curva Brusca': 'Curva_Brusca',
            '(Tr) Excesso de Velocidade 85 Km': 'Exc_Velocidade'
        }
        df.rename(columns=col_map, inplace=True)
        # Convertendo colunas para tipos numéricos
        cols_to_fix = ['Distancia', 'Score', 'Aceleracao_Brusca', 'Freada_Brusca', 'Curva_Brusca', 'Exc_Velocidade']
        
        for col in cols_to_fix:
            if col in df.columns:
                if df[col].dtype == object:
                    df[col] = df[col].astype(str).str.replace('.', '', regex=False)
                    df[col] = df[col].astype(str).str.replace(',', '.', regex=False)
                
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Cria coluna 'Mes' a partir da coluna 'Ativo Nome da garagem' ou usa meses fixos     
        try:
            if 'Ativo Nome da garagem' in df.columns:
                df['Mes'] = df['Ativo Nome da garagem'].astype(str).apply(lambda x: x.split('-')[1].strip() if '-' in x else x)
            else:
                raise Exception("Coluna original não encontrada")
        except:
            meses_fixos = ['Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro']
            if len(df) > len(meses_fixos):
                meses_fixos = (meses_fixos * ((len(df) // len(meses_fixos)) + 1))
            df['Mes'] = meses_fixos[:len(df)]

        return df