# workflow_manager/configs/settings.py
from airflow.configuration import conf

class PluginSettings:
    enabled = conf.getboolean("workflow_manager", "enabled", fallback=True)
    git_enabled = conf.getboolean("workflow_manager", "git_enabled", fallback=False)
    git_conn_id = conf.get("workflow_manager", "git_conn_id", fallback=None)
    rds_conn_id = conf.get("workflow_manager", "rds_conn_id", fallback=None)
    template_path = conf.get("workflow_manager", "template_path", fallback="/opt/airflow/plugins/jinja_templates")
    config_path = conf.get("workflow_manager", "config_path", fallback="/opt/airflow/plugins/config/templates_field.json")
    log_level = conf.get("workflow_manager", "log_level", fallback="INFO")
