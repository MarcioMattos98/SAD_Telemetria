import os
import sys

# Tenta importar o controller
try:
    from src.controller import AppController
except ImportError as e:
    print(f"ERRO DE IMPORTAÇÃO: {e}")
    sys.exit(1)

if __name__ == "__main__":
    print("--- Passo 1: Iniciando sistema ---")
    
    # 1. DEFINIÇÃO DO CAMINHO DO ARQUIVO (Esta linha estava faltando ou com erro)
    # Certifique-se que o nome do arquivo aqui é IGUAL ao que está na pasta data
    nome_arquivo = 'Relatorio06-a-11-2025.csv'
    csv_path = os.path.join('data', nome_arquivo)
    
    print(f"--- Passo 2: Buscando arquivo em: {csv_path} ---")
    
    # 2. VERIFICAÇÃO DE EXISTÊNCIA
    if not os.path.exists(csv_path):
        print(f"ERRO CRÍTICO: O arquivo '{nome_arquivo}' não foi encontrado na pasta 'data'.")
        print("Verifique se o nome está correto e se a extensão é .csv mesmo.")
    else:
        print("--- Passo 3: Arquivo encontrado. Iniciando processamento... ---")
        
        try:
            # 3. EXECUÇÃO DO SISTEMA
            controller = AppController(csv_path)
            print("--- Passo 4: Servidor Dash rodando! Acesse o link abaixo ---")
            controller.run()
        except Exception as e:
            print(f"ERRO FATAL DURANTE A EXECUÇÃO: {e}")
            import traceback
            traceback.print_exc()