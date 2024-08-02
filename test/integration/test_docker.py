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
from src.clients.github.github_client import GitHubClient

IMAGE_NAME: str ="update-release-version"
DOCKERFILE: str = "Dockerfile"
CONTAINER_APP_ROOT: str = f"/app"
ENTRYPOINT: List[str] = ["/usr/bin/env", "python3", "src/release_version_updater/main.py"]

GITHUB_OUTPUT: str = os.environ["GITHUB_OUTPUT"]

EXPECTED_INITIAL_VALUE: str = "1.0.0"
GITHUB_TOKEN: str = os.environ["GITHUB_TOKEN"]
REPO_OWNER: str = os.environ["REPO_OWNER"]
REPO_NAME: str = os.environ["REPO_NAME"]
REPO_VARIABLE: str = os.environ["REPO_VARIABLE"]


class TestDocker(unittest.TestCase):
    def setUp(self):
        self.docker_client: DockerClient = DockerClient()
        with open(file=f"{WORKSPACE_ROOT}/{GITHUB_OUTPUT}", mode="w"):
            pass

    def tearDown(self):
        github_client: GitHubClient = GitHubClient(github_token=GITHUB_TOKEN)
        github_client.update_repository_variable(
            repo_owner=REPO_OWNER,
            repo_name=REPO_NAME,
            variable=REPO_VARIABLE,
            new_value=EXPECTED_INITIAL_VALUE
        )
        with open(file=f"{WORKSPACE_ROOT}/{GITHUB_OUTPUT}", mode="w"):
            pass

    def test_image_build(self):
        image: Image = self.docker_client.images.build(path=WORKSPACE_ROOT, dockerfile=DOCKERFILE, tag=IMAGE_NAME)[0]
        assert image.tags[0] == f"{IMAGE_NAME}:latest"
        assert image.attrs["ContainerConfig"]["WorkingDir"] == CONTAINER_APP_ROOT
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
        bind_mount: Mount = Mount(source=WORKSPACE_ROOT, target=CONTAINER_APP_ROOT, type="bind")
        container_logs: str = bytes(self.docker_client.containers.run(image=IMAGE_NAME, environment=environ, mounts=[bind_mount], stdout=True, stderr=True)).decode("utf-8")
        print(container_logs)


if __name__ == "__main__":
    unittest.main()
