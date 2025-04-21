from airflow.plugins_manager import AirflowPlugin
from .views import dag_views

class WorkflowManagerPlugin(AirflowPlugin):
    name = 'workflow_manager'
    flask_blueprints = [dag_views.dag_manager_bp]
