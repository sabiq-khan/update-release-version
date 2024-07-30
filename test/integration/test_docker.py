import os
import sys
import unittest
from docker import DockerClient
from docker.models.images import Image
from typing import Dict, List
import pytest
WORKSPACE_ROOT: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(WORKSPACE_ROOT)

IMAGE_NAME: str ="update-release-version"
DOCKERFILE: str = "Dockerfile"
WORKDIR: str = "/app"
ENTRYPOINT: List[str] = ["/usr/bin/env", "python3", "src/release_version_updater/main.py"]

class TestDocker(unittest.TestCase):
    def setUp(self):
        self.docker_client: DockerClient = DockerClient()
    
    pytest.fixture(scope="module")
    def image(self) -> Image:
        image: Image = self.docker_client.images.build(path=WORKSPACE_ROOT, dockerfile=DOCKERFILE, tag=IMAGE_NAME)[0]
        assert image.tags[0] == f"{IMAGE_NAME}:latest"
        assert image.attrs["ContainerConfig"]["WorkingDir"] == WORKDIR
        assert image.attrs["ContainerConfig"]["Entrypoint"] == ENTRYPOINT
        assert image.attrs["Size"] < 100000000

        return image
    
    def _get_environ(self) -> List[str]:
        environ: List[str] = []
        with open(file=".env.local.docker", mode="r") as env_file:
            lines: List[str] = env_file.readlines()
            for line in lines:
                if not line.startswith("#"):
                    environ.append(line)
        
        return environ

    def test_container(self, image):
        environ: List[str] = self._get_environ()
        self.docker_client.containers.run(image=image, env=environ)

if __name__ == "__main__":
    unittest.main()
