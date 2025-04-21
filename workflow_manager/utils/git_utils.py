from airflow.providers.github.hooks.github import GithubHook
from github import GithubException

def push_dag_to_github(conn_id, repo_name, file_path, content, commit_message="Auto-generated DAG file"):
    print("Step 1: Getting GitHub repo object")
    try:
        hook = GithubHook(github_conn_id=conn_id)
        resource = hook.client
        print("GitHub resource object acquired")
        print("🔐 GitHub username:", resource.get_user().login)
        github_method_args = {"full_name_or_id": "saitejaanagani/StructuredDataComparator"}
        github_repo = getattr(resource, 'get_repo')(**github_method_args)
        print("Step 1 success: GitHub repo object acquired")
    except Exception as e:
        print(f"Step 1 failed: Cannot get GitHub repo object - {e}")
        return f"Failed to get GitHub repo object: {e}"

    print(f"Step 3: Checking if file exists at {file_path}")
    try:
        existing_file = github_repo.get_contents(file_path)
        print(f"File exists. Updating...")
        github_repo.update_file(
            path=file_path,
            message=commit_message,
            content=content,
            sha=existing_file.sha
        )
        print("File updated successfully")
        return f"Updated file at {file_path}"
    except GithubException as e:
        if e.status == 404:
            print("File does not exist. Creating...")
            try:
                github_repo.create_file(file_path, commit_message, content)
                print("File created successfully")
                return f"Created new file at {file_path}"
            except Exception as e:
                print(f"Step 4 failed: Failed to create file - {e}")
                return f"Failed to create file: {e}"
        else:
            print(f"Step 3 failed: GitHub API error - {e}")
            return f"GitHub API error: {e.data}"
    except Exception as e:
        print(f"Unknown error in Step 3 - {e}")
        return f"Unexpected error during file push: {e}"
