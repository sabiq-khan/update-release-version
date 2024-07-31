import os
import sys
import unittest
from docker import DockerClient
from docker.models.images import Image
from docker.types import Mount
from typing import List
WORKSPACE_ROOT: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(WORKSPACE_ROOT)

IMAGE_NAME: str ="update-release-version"
DOCKERFILE: str = "Dockerfile"
WORKDIR: str = "/app"
ENTRYPOINT: List[str] = ["/usr/bin/env", "python3", "src/release_version_updater/main.py"]

GITHUB_OUTPUT: str = os.environ["GITHUB_OUTPUT"]
SUB_DIR: str = "src/release_version_updater"
HOST_OUTPUT_PATH: str = f"{os.path.abspath(WORKSPACE_ROOT)}/{SUB_DIR}/{GITHUB_OUTPUT}"
CONTAINER_OUTPUT_PATH: str = f"/app/{SUB_DIR}/{GITHUB_OUTPUT}"


class TestDocker(unittest.TestCase):
    def setUp(self):
        self.docker_client: DockerClient = DockerClient()

    def test_image_build(self):
        image: Image = self.docker_client.images.build(path=WORKSPACE_ROOT, dockerfile=DOCKERFILE, tag=IMAGE_NAME)[0]
        assert image.tags[0] == f"{IMAGE_NAME}:latest"
        assert image.attrs["ContainerConfig"]["WorkingDir"] == WORKDIR
        assert image.attrs["ContainerConfig"]["Entrypoint"] == ENTRYPOINT
        assert image.attrs["Size"] < 100000000
    
    def _get_environ(self) -> List[str]:
        environ: List[str] = []
        with open(file=".env.local.docker", mode="r") as env_file:
            lines: List[str] = env_file.readlines()
            for line in lines:
                if not line.startswith("#"):
                    environ.append(line.rstrip("\n"))

        return environ

    def test_container_run(self):
        environ: List[str] = self._get_environ()
        container_logs: str = bytes(self.docker_client.containers.run(image=IMAGE_NAME, environment=environ, mounts=[Mount(source=HOST_OUTPUT_PATH, target=CONTAINER_OUTPUT_PATH, type="bind")], stdout=True, stderr=True)).decode("utf-8")
        print(container_logs)


if __name__ == "__main__":
    unittest.main()
