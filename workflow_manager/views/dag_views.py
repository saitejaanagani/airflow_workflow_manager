
from flask import request
from flask_appbuilder import BaseView, expose
from airflow.www.app import csrf
import os

from ingestion.repo.plugins.dag_manager_plugin.db_utils import (
    get_dag_metadata,
    get_all_templates,
)
from ingestion.repo.plugins.dag_manager_plugin.db import Session
from ingestion.repo.plugins.dag_manager_plugin.models.models import DagMetadata
from flask import make_response, flash
from ingestion.repo.plugins.dag_manager_plugin.git_utils import push_dag_to_github


def render_and_save_dag_file(dag):
    from jinja2 import Environment, FileSystemLoader
    import os

    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    jinja_env = Environment(loader=FileSystemLoader(template_dir))
    template_file = f"{dag.template_name}_dag.py.j2"

    if not os.path.exists(os.path.join(template_dir, template_file)):
        raise FileNotFoundError(f"Template {template_file} not found")

    template = jinja_env.get_template(template_file)

    rendered = template.render(
        dag_id=dag.dag_id,
        owner=dag.owner,
        schedule_interval=dag.schedule_interval,
        start_date=dag.start_date
    )

    # output_path = f"/opt/airflow/dags/{dag.dag_id}.py"
    # with open(output_path, "w") as f:
    #     f.write(rendered)

    output_path = f"dags/anagast/{dag.dag_id}.py"
    response = push_dag_to_github(
        conn_id="git_conn_id",
        repo_name="saitejaanagani/StructuredDataComparator",
        file_path=output_path,
        content=rendered,
        commit_message=f"Created DAG {dag.dag_id} via UI"
    )
    # flash(response, "success")
    return response



class DagManager2View(BaseView):
    route_base = "/dagmanager2view"
    template_folder = os.path.join(os.path.dirname(__file__), "templates")
    base_template = "appbuilder/base.html"

    @expose('/')
    def list(self):
        from sqlalchemy import or_
        session = Session

        # Search + Pagination params
        search = request.args.get("search", "").strip()
        page = int(request.args.get("page", 1))
        per_page = 10
        try:
            # Base query
            query = session.query(DagMetadata)

            if search:
                query = query.filter(
                    or_(
                        DagMetadata.dag_id.ilike(f"%{search}%"),
                        DagMetadata.owner.ilike(f"%{search}%"),
                        DagMetadata.template_name.ilike(f"%{search}%")
                    )
                )
        
            total = query.count()
            dags = query.offset((page - 1) * per_page).limit(per_page).all()

            template_name = "dagmanager/list_table.html" if request.headers.get("HX-Request") else "dagmanager/list.html"

            return self.render_template(
                template_name,
                dags=dags,
                load_error_msg = None,
                search_term=search,
                current_page=page,
                total_pages=(total // per_page) + (1 if total % per_page else 0),
                success_dag_id=request.args.get("success"),
                error=request.args.get("error"),
                error_dag_id=request.args.get("dag_id"),
                error_msg=request.args.get("msg"),
                update_success=request.args.get("update_success"),
                update_error=request.args.get("update_error"),
                update_error_msg=request.args.get("msg")
            )
        except Exception as e:
            return self.render_template(
            "dagmanager/list.html",
            dags=[],
            load_error_msg=f"❌ Unable to connect to database. Please try again later. {str(e)}",
            search_term=search,
            current_page=page,
            total_pages=1,
        )

    @expose('/create_dag', methods=["POST"])
    def create_dag(self):
        dag_id = request.form.get("dag_id")
        template_name = request.form.get("template_name")
        owner = request.form.get("owner")
        schedule_interval = request.form.get("schedule_interval")
        start_date = request.form.get("start_date")

        session = Session
        try:
            existing = session.query(DagMetadata).filter_by(dag_id=dag_id).first()
            if existing:
                response = make_response('', 204)
                response.headers['HX-Redirect'] = f"/dagmanager2view/?error=exists&msg={dag_id}"
                return response
            new_dag = DagMetadata(
                dag_id=dag_id,
                template_name=template_name,
                owner=owner,
                schedule_interval=schedule_interval,
                start_date=start_date
            )
            session.add(new_dag)
            session.commit()
            render_and_save_dag_file(new_dag)

            response = make_response('', 204)
            response.headers['HX-Redirect'] = f"/dagmanager2view/?success={dag_id}"
            return response

        except Exception as e:
            session.rollback()
            response = make_response('', 204)
            response.headers['HX-Redirect'] = f"/dagmanager2view/?error=exception&msg={str(e)}"
            return response

        finally:
            session.close()


    @expose('/select_template')
    def select_template(self):
        templates = get_all_templates()
        return self.render_template('dagmanager/select_template.html', templates=templates)

    @expose('/create_form')
    def create_form(self):
        template = request.args.get("template")
        if not template:
            return "<p class='text-red-600'> No template selected.</p>"
        return self.render_template("dagmanager/create_form.html", template_name=template)

    @expose('/edit')
    def edit(self):
        dag_id = request.args.get("dag_id")
        dag = get_dag_metadata(dag_id)
        return self.render_template("dagmanager/edit_form.html", dag=dag)

    @expose('/update_dag', methods=["POST"])
    def update_dag(self):
        dag_id = request.form.get("dag_id")
        session = Session
        try:
            dag = session.query(DagMetadata).filter_by(dag_id=dag_id).first()
            if dag:
                dag.template_name = request.form.get("template_name")
                dag.owner = request.form.get("owner")
                dag.schedule_interval = request.form.get("schedule_interval")
                dag.start_date = request.form.get("start_date")
                session.commit()
                render_and_save_dag_file(dag)
                response = make_response('', 204)
                response.headers['HX-Redirect'] = f"/dagmanager2view/?update_success={dag_id}"
                return response
            else:
                message = f'{dag_id} not found'
                response = make_response('', 204)
                response.headers['HX-Redirect'] = f"/dagmanager2view/?update_error=1&msg={message}"
                return response
        except Exception as e:
            session.rollback()
            response = make_response('', 204)
            response.headers['HX-Redirect'] = f"/dagmanager2view/?update_error=1&msg={str(e)}"
            return response

        finally:
            session.close()


# Register plugin
dag_manager_view = DagManager2View()

dag_appbuilder_view = {
    "name": "Manage DAGs 2",
    "category": "Manager",
    "view": dag_manager_view
}

from airflow.plugins_manager import AirflowPlugin

class DagManager2Plugin(AirflowPlugin):
    name = "dagmanager2"
    appbuilder_views = [dag_appbuilder_view]
