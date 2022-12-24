from time import sleep
import docker
from docker.errors import NotFound

from core.EsConnection import EsConnection
from core.common import env_is_ci


def ensure_db_running():
    """
    Ensure the Elasticsearch docker container is running using the docker library
    """
    if env_is_ci():
        return

    client = docker.from_env()
    es_container_name = "elasticsearch"
    es_version = "8.5.3"

    volume = get_es_volume()

    try:
        es_container = client.containers.get(es_container_name)
    except NotFound:
        es_container = client.containers.run(
            image=f"docker.elastic.co/elasticsearch/elasticsearch:{es_version}",
            name=es_container_name,
            ports={"9200/tcp": "9200"},
            detach=True,
            healthcheck={
                "test": ["CMD", "curl", "-f", "http://localhost:9200"],
                "interval": 5000000000,
                "timeout": 5000000000,
                "retries": 10,
            },
            environment=[
                "discovery.type=single-node",
                "xpack.security.enabled=false",
                "ELASTIC_PASSWORD=elastic",
                "LICENSE=basic"
            ],
            volumes={
                volume: {'bind': '/usr/share/elasticsearch/data', 'mode': 'rw'}
            }
        )

    while True:
        if es_container.status != 'running' or es_container.status != 'starting':
            es_container.start()

        try:
            if es_container.attrs['State']['Health']['Status'] == 'healthy':
                break
        except KeyError:
            pass

        sleep(1)
        es_container.reload()


def get_es_volume(es_container_name="esticsearch"):
    client = docker.from_env()
    es_volume_name = f"{es_container_name}-vol-1"

    volume = client.volumes.create(
        name=es_volume_name,
        driver='local'
    )

    return volume.name


def ensure_index_exists():
    es = EsConnection()

    if es.connection.indices.exists(index=es.index_name):
        return

    es.connection.indices.create(
        index=es.index_name,
        mappings={
            "dynamic": False,
            "properties": {
                "dataset": {
                    "type": "keyword"
                },
                "file_name": {
                    "type": "keyword"
                },
                "width": {
                    "type": "integer"
                },
                "height": {
                    "type": "integer"
                },
                "top_left": {
                    "type": "point"
                },
                "bottom_right": {
                    "type": "point"
                },
                "face_embedding": {
                    "type": "dense_vector",
                    "dims": 128,
                    "index": True,
                    "similarity": "l2_norm"
                }
            }
        }
    )
