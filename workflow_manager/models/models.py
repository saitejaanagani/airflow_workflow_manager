from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DagMetadata(Base):
    __tablename__ = 'dag_metadata'

    dag_id = Column(String, primary_key=True)
    template_name = Column(String)
    owner = Column(String)
    schedule_interval = Column(String)
    start_date = Column(String)

class DagTemplate(Base):
    __tablename__ = 'dag_templates'

    template_name = Column(String, primary_key=True)
    description = Column(String)
