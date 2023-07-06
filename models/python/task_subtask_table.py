import requests
import pandas as pd


def model(dbt, session):
    dbt.config(
        materialized = "table",
        packages = ["requests","pandas"])
    # Set up the API endpoint URL for projects
    projects_url = 'https://app.asana.com/api/1.0/projects'

    # Set up the request headers with your API key
    headers = {
        'Authorization': 'Bearer 1/1204064105829073:13464d199ef9c21424e503a8bf56a146',
    }

    # Send the GET request to retrieve projects
    response = requests.get(projects_url, headers=headers)
    projects_data = response.json()

    # Process the projects data
    project_info = []

    for project in projects_data['data']:
        project_id = project['gid']
        project_name = project['name']
        project_info.append((project_id, project_name))

    # Select the project ID automatically
    selected_project_id = project_info[0][0]  # Example: Select the first project ID

    # Set up the API endpoint URL with the selected project ID
    tasks_url = f'https://app.asana.com/api/1.0/tasks?project=1203064799050708&opt_fields=assignee.name,completed,name,start_on,due_on,subtasks.name,subtasks.start_on,subtasks.due_on,subtasks.assignee.name'

    # Send the GET request to retrieve tasks
    response = requests.get(tasks_url, headers=headers)
    tasks_data = response.json()

    # Process the tasks data
    table_data = []

    for task in tasks_data['data']:
        project_id = selected_project_id
        project_name = project_info[0][1]  # Assuming project name corresponds to the first project in the list
        task_id = task['gid']
        subtask_ids = []

        if 'subtasks' in task:
            subtasks = task['subtasks']
            subtask_ids = [subtask['gid'] for subtask in subtasks]

        table_data.append((project_id, project_name, task_id, subtask_ids))

    # Create a DataFrame from the table data
    headers = ['Project ID', 'Project Name', 'Task ID', 'Subtask IDs']
    df = pd.DataFrame(table_data, columns=headers)

    # Perform additional transformations or calculations if needed
    final_df = df  # No additional transformations, return the DataFrame as is
    session.use_database(dbt.this.database)
    session.use_schema(dbt.this.schema)
    return final_df