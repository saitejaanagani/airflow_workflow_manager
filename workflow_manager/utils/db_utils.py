# db_utils.py

from workflow_manager.models.models import DagMetadata, DagTemplate
from workflow_manager.utils.db import Session

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
