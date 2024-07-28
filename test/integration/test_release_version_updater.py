import os
import sys
from typing import List
import unittest
WORKSPACE_ROOT: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(WORKSPACE_ROOT)
from src.clients.github.github_client import GitHubClient
from src.release_version_updater.release_version_updater import ReleaseVersionUpdater
from src.release_version_updater._types import CommitType
from src.release_version_updater.constants import LOGGER, REPO_OWNER, REPO_NAME, REPO_VARIABLE, GITHUB_TOKEN, GITHUB_OUTPUT

EXPECTED_INITIAL_VALUE: str = "v1.0.0"


class TestReleaseVersionUpdater(unittest.TestCase):
    def setUp(self):
        self.github_client: GitHubClient = GitHubClient(github_token=GITHUB_TOKEN)
        with open(file=GITHUB_OUTPUT, mode="w"):
            pass
        self.release_version_updater: ReleaseVersionUpdater = ReleaseVersionUpdater(
            logger=LOGGER,
            repo_owner=REPO_OWNER,
            repo_name=REPO_NAME,
            repo_variable=REPO_VARIABLE,
            github_client=self.github_client,
            github_output=GITHUB_OUTPUT
        )

    def tearDown(self):
        self.github_client.update_repository_variable(
            repo_owner=REPO_OWNER,
            repo_name=REPO_NAME,
            variable=REPO_VARIABLE,
            new_value=EXPECTED_INITIAL_VALUE
        )
        with open(file=GITHUB_OUTPUT, mode="w"):
            pass

    def test_update_release_version(self):
        curr_release_version: str = self.release_version_updater._get_current_release_version()

        assert curr_release_version == EXPECTED_INITIAL_VALUE

        self.release_version_updater.update_release_version()

        latest_commit_msg: str = self.release_version_updater._get_latest_commit_msg()
        latest_commit_type: CommitType = self.release_version_updater._get_commit_type(latest_commit_msg)
        updated_release_version: str = self.release_version_updater._get_current_release_version()

        with open(file=GITHUB_OUTPUT, mode="r") as github_output:
            lines: List[str] = github_output.readlines()
            if latest_commit_type == CommitType.MAJOR:
                assert updated_release_version == "v2.0.0"
                assert lines[-1] == "v2.0.0"
            elif latest_commit_type == CommitType.MINOR:
                assert updated_release_version == "v1.1.0"
                assert lines[-1] == "v1.1.0"
            elif latest_commit_type == CommitType.PATCH:
                assert updated_release_version == "v1.0.1"
                assert lines[-1] == "v1.0.1"
            elif latest_commit_type == CommitType.OTHER:
                assert updated_release_version == EXPECTED_INITIAL_VALUE
                assert lines[-1] == "v1.0.0"


if __name__ == "__main__":
    unittest.main()
