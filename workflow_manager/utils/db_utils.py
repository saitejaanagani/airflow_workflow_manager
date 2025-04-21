# db_utils.py

from ingestion.repo.plugins.dag_manager_plugin.models.models import DagMetadata, DagTemplate
from ingestion.repo.plugins.dag_manager_plugin.db import Session

def get_all_dag_metadata():
    session = Session
    try:
        return session.query(DagMetadata).all()
    finally:
        session.close()


def get_dag_metadata(dag_id):
    session = Session
    try:
        return session.query(DagMetadata).filter_by(dag_id=dag_id).first()
    finally:
        session.close()


def get_all_templates():
    session = Session
    try:
        return session.query(DagTemplate).all()
    finally:
        session.close()
