from os import getenv

from dotenv import load_dotenv
from pandas import DataFrame
from sqlalchemy import Engine

from data import base


def get_engine() -> Engine:
    """
    Função que cria a base de conexão com o banco SQL.

    Returns
    -------
    Engine
        Base SQLalchemy.
    """
    load_dotenv()

    dialect: str = getenv('DATABASE_DIALECT', '')
    driver: str = getenv('DATABASE_DRIVER', '')
    host: str = getenv('DATABASE_HOST', '')
    port: str | None = getenv('DATABASE_PORT', None)
    user: str = getenv('DATABASE_USERNAME', '')
    password: str = getenv('DATABASE_PASSWORD', '')
    database: str = getenv('DATABASE_NAME', '')

    return base.engine(
        dialect=dialect,
        driver=driver,
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
    )


def execute(sql_code: str, **kwargs) -> None:
    """
    Rotina que executa um comando em SQL

    Parameters
    ----------
    sql_code : str
        O comando de projeção em SQL que irá ser executado
    kwargs : dict, optional
        Parâmetros adicionais passados a função `database_execute()`.

    Raises
    ------
    ConnectionError
        Erro ao conectaro com o servidor.
    """
    try:
        base.execute(get_engine(), sql_code, **kwargs)
    except Exception as e:
        raise ConnectionError(f'Falha ao conectar com o servidor.\nErro: {e}')


def read(sql_code: str, **kwargs) -> DataFrame:
    """
    Função que lê uma tabela no banco SQL e transforma em um dataframe em pandas.

    Parameters
    ----------
    sql_code : str
        O comando de leitura da tabela no banco
    kwargs : dict, optional
        Parâmetros adicionais passados a função `to_pandas()`.

    Returns
    -------
    DataFrame
        Tabela formatada em pandas.

    Raises
    ------
    ConnectionError
        Erro ao conectaro com o servidor.
    """
    try:
        return base.to_pandas(get_engine(), sql_code, **kwargs)
    except Exception as e:
        raise ConnectionError(f'Falha ao conectar com o servidor.\nErro: {e}')


def write(table_name: str, dataframe: DataFrame, **kwargs) -> None:
    """
    Rotina que insere novas linhas em uma tabela.

    Parameters
    ----------
    table_name : str
        Nome da tabela no banco SQL.
    dataframe : DataFrame
        Dataframe em pandas com os dados a serem inseridos.
    kwargs : dict, optional
        Parâmetros adicionais passados a função `insert_from_pandas()`.

    Raises
    ------
    ConnectionError
        Erro ao conectaro com o servidor.
    """
    try:
        base.insert_from_pandas(get_engine(), table_name, dataframe, **kwargs)
    except Exception as e:
        raise ConnectionError(f'Falha ao conectar com o servidor.\nErro: {e}')


def ping_server() -> bool:
    """
    Rotina que tenta se conectar com o banco de dados e retorna.

    Returns
    -------
    bool
        `True`, se a conexão for bem-sucedida ou `False`, caso contrário.
    """
    try:
        execute('SELECT 1;')
        return True
    except Exception as e:
        print(f'Não foi possível conectar ao banco de dados: {e}')
        return False
