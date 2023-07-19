#Use this file to lounch the app as subprocess
import os
import subprocess

def execute_docker_compose():
    directory = os.path.expanduser("~/Documents/code/python_projects/kazna_mysql")
    compose_file = os.path.join(directory, "docker-compose.yml")

    try:
        subprocess.run(["docker-compose", "-f", compose_file, "up", "-d"], check=True)
        print("Docker Compose executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error executing Docker Compose: {e}")

execute_docker_compose()