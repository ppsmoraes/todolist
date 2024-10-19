from sqlalchemy import Engine, create_engine, text
from dotenv import load_dotenv
from os import getenv
from pandas import DataFrame, read_sql

def _engine() -> Engine:
    load_dotenv()

    user: str = getenv('user')
    password: str = getenv('password')
    host: str = 'localhost'
    port: str = '5432'
    database: str = 'personal_projects'
    url : str = f'postgresql://{user}:{password}@{host}:{port}/{database}'

    return create_engine(url)

def execute(sql_comand: str) -> None:
    with _engine().begin() as conn:
        conn.execute(text(sql_comand))

def read(sql_comand: str) -> DataFrame:
    with _engine().begin() as conn:
        return read_sql(text(sql_comand), conn)