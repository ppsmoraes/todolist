from pandas import DataFrame, read_sql
from sqlalchemy import text
from sqlalchemy.engine import Engine, create_engine


def engine(
    *,
    dialect: str,
    driver: str,
    host: str,
    port: str | None = None,
    user: str,
    password: str,
    database: str,
    **kwargs,
) -> Engine:
    """
    Função que gera a instância de conexão ao banco SQL.

    Parameters
    ----------
    dialect : str
        Dialeto do banco. Exemplos: 'mysql' e 'postgresql'.
    driver : str
        Driver a ser usado na conexão. Exemplos: 'mysqlconnector', 'pymysql' ou 'pyodbc' para MySQL e 'psycopg2', 'pg8000' ou 'asyncpg' para PostgreSQL.
    host : str
        Servidor do banco. Utilize 'localhost' para conexões locais.
    port : str
        A porta do servidor.
    user : str
        Usuário de login no banco.
    password : str
        Senha do usuário a ser conectado.
    database : str
        Banco de dados a ser conectado.
    kwargs : dict, optional
        Parâmetros adicionais passados para a criação da instância.

    Returns
    -------
    Engine
        Instância de conexão SQLAlchemy.
    """
    kwargs['connect_args'] = kwargs.get('connect_args', {'connect_timeout': 10})
    kwargs['echo'] = kwargs.get('echo', False)

    if port is not None:
        host = f'{host}:{port}'

    string_connection: str = f"{dialect}+{driver}://{user}:{password}@{host}/{database}"
    return create_engine(string_connection, **kwargs)


def execute(engine: Engine, sql_code: str, **kwargs) -> None:
    """
    Rotina que executa um comando em SQL.

    Parameters
    ----------
    engine : Engine
        Instância de conexão SQLAlchemy.
    sql_code : str
        O comando de projeção em SQL que irá ser executado
    kwargs : dict, optional
        Parâmetros adicionais passados para execução.

    Returns
    -------
    None
    """
    with engine.connect() as conn:
        conn.execute(text(sql_code), **kwargs)
        conn.commit()


def to_pandas(engine: Engine, sql_code: str, **kwargs) -> DataFrame:
    """
    Função que ler e retorna um dateframe em pandas.

    Parameters
    ----------
    engine : Engine
        Instância de conexão SQLAlchemy.
    sql_code : str
        O comando de projeção em SQL que irá nos fornecer um dataframe
    kwargs : dict, optional
        Parâmetros adicionais passados para `pandas.read_sql()`.

    Returns
    -------
    DataFrame
        Tabela formatada em pandas.
    """
    with engine.connect() as conn:
        df: DataFrame = read_sql(text(sql_code), conn, **kwargs)
    return df


def insert_from_pandas(
    engine: Engine, table_name: str, dataframe: DataFrame, **kwargs
) -> None:
    """
    Rotina que insere novas linhas em uma tabela.

    Parameters
    ----------
    engine : Engine
        Instância de conexão SQLAlchemy.
    table_name : str
        Nome da tabela no banco SQL.
    dataframe : DataFrame
        Dataframe em pandas com os dados a serem inseridos.
    kwargs : dict, optional
        Parâmetros adicionais passados para `pandas.to_sql()`.

    Returns
    -------
    None
    """
    with engine.connect() as conn:
        dataframe.to_sql(table_name, conn, **kwargs)
        conn.commit()
