import os
import subprocess
"""
In this part we setup the environment for kazna_bot_mysql app. 
We launch the docker-compose.yml file to create and setup MYSQL database.
To setup mysql database docker-compose.yaml file wil use init.sql file 
"""

#client = docker.from_env()
#current_dir = os.path.dirname(os.path.abspath(__file__))
#compose_file = os.path.join(current_dir, 'docker-compose.yml')

#docker_compose = docker.types.services.parse_yaml(compose_file)
#services = docker_compose.get('services', {})

#for service_name, service_config in services.items():
#    client.services.create(**service_config, name=service_name)

def execute_docker_compose():
    directory = os.path.expanduser("~/Documents/code/python_projects/kazna_mysql")
    compose_file = os.path.join(directory, "docker-compose.yml")

    try:
        subprocess.run(["docker-compose", "-f", compose_file, "up", "-d"], check=True)
        print("Docker Compose executed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error executing Docker Compose: {e}")

execute_docker_compose()