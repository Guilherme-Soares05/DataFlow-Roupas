import psycopg2
import time
from datetime import datetime
from typing import Optional, Tuple

# Constantes para retentativa de conexão
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

def obter_conexao_banco(database_url: str) -> Optional[psycopg2.connection]:
    """
    Obtém uma conexão com o banco de dados PostgreSQL com retentativa.

    Args:
        database_url (str): A URL de conexão com o banco de dados.

    Retorna:
        Optional[psycopg2.connection]: Uma conexão com o banco de dados em caso de sucesso,
                                        None em caso de falha após várias tentativas.
    """
    for tentativa in range(MAX_RETRIES):
        try:
            # Tenta estabelecer a conexão
            conexao = psycopg2.connect(database_url)
            conexao.autocommit = False  # Define autocommit para False para controle de transação explícito
            return conexao  # Retorna a conexão se bem-sucedida
        except psycopg2.OperationalError as erro:
            # Captura erros de conexão (por exemplo, banco de dados não disponível)
            print(f"Erro de conexão com o banco de dados (tentativa {tentativa + 1}/{MAX_RETRIES}): {erro}")
            if tentativa < MAX_RETRIES - 1:
                # Espera antes de tentar novamente, a não ser que seja a última tentativa
                print(f"Retentando em {RETRY_DELAY_SECONDS} segundos...")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                # Se todas as tentativas falharem, imprime um erro e retorna None
                print(f"Falha ao conectar ao banco de dados após {MAX_RETRIES} tentativas.")
                return None
        except Exception as erro:
            # Captura erros inesperados
            print(f"Erro inesperado ao conectar ao banco de dados: {erro}")
            return None

def executar_query(conexao: psycopg2.connection, query: str, params: Tuple = ()) -> Optional[psycopg2.cursor]:
    """
    Executa uma consulta SQL com tratamento de erro e retentativa.

    Args:
        conexao (psycopg2.connection): A conexão com o banco de dados.
        query (str): A consulta SQL a ser executada.
        params (Tuple, opcional): Os parâmetros a serem passados para a consulta. Padrão: ().

    Retorna:
        Optional[psycopg2.cursor]: Um cursor em caso de sucesso, None em caso de falha.
    """
    for tentativa in range(MAX_RETRIES):
        try:
            # Tenta executar a consulta
            cursor = conexao.cursor()
            cursor.execute(query, params)
            return cursor  # Retorna o cursor se bem-sucedida
        except psycopg2.OperationalError as erro:
            # Captura erros de operação do banco de dados
            print(f"Erro de operação do banco de dados (tentativa {tentativa + 1}/{MAX_RETRIES}): {erro}")
            if tentativa < MAX_RETRIES - 1:
                # Espera e tenta novamente
                print(f"Retentando a consulta em {RETRY_DELAY_SECONDS} segundos...")
                time.sleep(RETRY_DELAY_SECONDS)
            else:
                # Se falhar após várias tentativas, faz rollback e retorna None
                print(f"Falha ao executar a consulta após {MAX_RETRIES} tentativas. Rollback da transação.")
                conexao.rollback()
                return None
        except Exception as erro:
            # Captura erros inesperados e faz rollback
            print(f"Erro inesperado ao executar a consulta: {erro}. Rollback da transação.")
            conexao.rollback()
            return None

def inserir_venda(database_url: str, produto: str, quantidade: int, preco: float) -> bool:
    """
    Insere uma nova venda no banco de dados.

    Args:
        database_url (str): A URL de conexão com o banco de dados.
        produto (str): O nome do produto vendido.
        quantidade (int): A quantidade vendida.
        preco (float): O preço do produto.

    Retorna:
        bool: True se a venda for inserida com sucesso, False caso contrário.
    """
    conexao = obter_conexao_banco(database_url)
    if conexao is None:
        return False  # Retorna False se não conseguir conectar ao banco

    query = """
        INSERT INTO vendas (produto, quantidade, preco, data_venda)
        VALUES (%s, %s, %s, %s)
    """
    params = (produto, quantidade, preco, datetime.now())
    cursor = executar_query(conexao, query, params)
    if cursor is None:
        conexao.close()
        return False  # Retorna False se a consulta falhar

    try:
        # Tenta commitar a transação
        conexao.commit()
        print(f"Venda de '{produto}' adicionada com sucesso!")
        cursor.close()
        conexao.close()
        return True  # Retorna True se o commit for bem-sucedido
    except Exception as erro:
        # Captura erros ao commitar
        print(f"Erro ao commitar a transação: {erro}. Rollback da transação.")
        conexao.rollback()  # Faz rollback em caso de erro
        cursor.close()
        conexao.close()
        return False  # Retorna False se o commit falhar

def main():
    """
    Função principal para inserir dados de vendas de teste.
    """
    # Configurações do Banco de Dados (use as variáveis já definidas)
    database_url = "postgresql://dataflow:password@db:5432/dataflow_db"
    vendas = [
        ('Camiseta Azul', 2, 25.99),
        ('Calça Jeans', 1, 79.50),
        ('Vestido Floral', 3, 45.00),
        ('Tênis Esportivo', 1, 120.00),
        ('Meias (par)', 5, 9.90),
    ]

    for produto, quantidade, preco in vendas:
        # Chama a função inserir_venda e verifica o resultado
        if not inserir_venda(database_url, produto, quantidade, preco):
            print(f"Falha ao inserir venda de '{produto}'.")

    print("\nDados de vendas de teste inseridos.")

if __name__ == '__main__':
    main()