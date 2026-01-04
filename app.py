import os
import sys

try:
    from src.controller import AppController
except ImportError as e:
    print(f"ERRO DE IMPORTAÇÃO: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("--- Passo 1: Iniciando sistema ---")
    
    # 1. Definição do caminho do arquivo CSV
    nome_arquivo = 'Relatorio06-a-11-2025.csv'
    csv_path = os.path.join('data', nome_arquivo)
    
    print(f"--- Passo 2: Buscando arquivo em: {csv_path} ---")
    
    # Verifica se o arquivo existe
    if not os.path.exists(csv_path):
        print(f"ERRO CRÍTICO: O arquivo '{nome_arquivo}' não foi encontrado na pasta 'data'.")
        print("Verifique se o nome está correto e se a extensão é .csv mesmo.")
    else:
        print("--- Passo 3: Arquivo encontrado. Iniciando processamento... ---")
        
        try:
            # 3. Execução do Controller
            controller = AppController(csv_path)
            print("--- Passo 4: Servidor Dash rodando! Acesse o link abaixo ---")
            controller.run()
        except Exception as e:
            print(f"ERRO FATAL DURANTE A EXECUÇÃO: {e}")
            import traceback
            traceback.print_exc()