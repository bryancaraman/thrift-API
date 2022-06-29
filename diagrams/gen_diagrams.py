from diagrams import Diagram, Cluster, Edge
from diagrams.aws.general import Disk
from diagrams.generic.network import Subnet
from diagrams.onprem.client import User
from diagrams.onprem.container import Docker
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.framework import React
from diagrams.programming.language import Python

with Diagram("Docker-Compose Resources", filename="/diagrams/docker_compose_resources", direction="LR"):
    user = User("API User")

    with Cluster("docker host resources"):
        disk = Disk("Disk Storage")

    with Cluster("docker-compose resources"):
        docker_network = Subnet("docker_bootcamp_network")

        with Cluster("services"):
            db = PostgreSQL("Postgres Database")
            api = Python("API Backend")
            db_volume = Docker("Docker Volume")

        web = React("UI Frontend")

        docker_network - db
        docker_network - api
        docker_network - web

        user >> Edge(label="User hits web frontend") >> web
        web >> Edge(label="Internal API Call") >> api
        api >> Edge(label="API stores state in db") >> db
        db >> Edge(label="Database stores state in a docker volume") >> db_volume
        db_volume >> Edge(label="Docker volume lives on disk") >> disk
