from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.hooks.sql import DbApiHook
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

connection_id = 'postgres_conn_id'

def get_db_session(conn_id: str = "postgres_conn_id"):
    """
    Get SQLAlchemy session using Airflow Connection.
    """
    connection = PostgresHook.get_connection(conn_id)
    hook:DbApiHook = connection.get_hook()
    engine = hook.get_sqlalchemy_engine()
    Session = sessionmaker(bind=engine)
    return Session()

Session = get_db_session(connection_id)
