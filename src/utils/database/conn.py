import os
import psycopg2
from psycopg2.pool import SimpleConnectionPool


def _load_config_from_env():
    """
    Load DB connection settings from environment variables,
    falling back to sensible defaults for local development.
    """
    return {
        "host": os.getenv("DB_HOST", "192.168.100.250"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "database": os.getenv("DB_NAME", "geon_pr_cornelio"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", os.getenv("DB_PASS", "postgres")),
    }


# Criação lazy de um pool de conexões (evita falhar no import)
_POOL = None


def get_pool():
    """Get or create the connection pool lazily (singleton)."""
    global _POOL
    if _POOL is None:
        cfg = _load_config_from_env()
        try:
            _POOL = SimpleConnectionPool(1, 5, **cfg)
        except psycopg2.OperationalError as e:
            print("Erro ao conectar ao banco de dados:", e)
            # Mantém como None para evitar uso posterior
            _POOL = None
            raise
    return _POOL


def exec_select(sql, silent=False):
    """
    Executa um select e retorna os resultados.
    
    Args:
        sql: Query SQL a ser executada
        silent: Se True, suprime mensagens de erro (útil para queries opcionais)
    
    Returns:
        Lista de tuplas com os resultados ou None em caso de erro
    """
    
    conn = None
    cursor = None

    try:
        
        # Obtém uma conexão do pool (criado sob demanda)
        conn = get_pool().getconn()
        
        # Define a codificação para UTF-8
        conn.set_client_encoding('UTF8')
        
        # cria um cursor
        cursor = conn.cursor()
        # executa sql com o cursor
        cursor.execute(sql)
        # guarda todo o resultado do select
        resultados = cursor.fetchall()
        
        return resultados
    
    except psycopg2.Error as e:
        if not silent:
            print("Erro durante a execução da consulta:", e)
        return None
    finally:
        # fecha o cursor
        if cursor:
            cursor.close()
            if not silent:
                print('cursor fechado com sucesso!')
        # fecha a conexao
        if conn:
            get_pool().putconn(conn)
            if not silent:
                print('conexao fechada com sucesso!')
