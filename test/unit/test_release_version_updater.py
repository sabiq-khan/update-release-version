import json
import os
import sys
import time
from typing import List
import unittest
from unittest.mock import MagicMock
from logging import Logger, StreamHandler, Formatter, INFO
from requests import Response
WORKSPACE_ROOT: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(WORKSPACE_ROOT)
from src.release_version_updater.release_version_updater import ReleaseVersionUpdater
from src.release_version_updater._types import CommitType

LOGGER: Logger = Logger("test_release_version_updater")
LOGGER.setLevel(INFO)
HANDLER = StreamHandler(sys.stdout)
HANDLER.setLevel(INFO)
FORMATTER = Formatter(
    "[%(asctime)s][%(name)s][%(filename)s:%(lineno)d][%(funcName)s][%(levelname)s]: %(message)s")
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

MOCK_REPO_OWNER: str = "test-user"
MOCK_REPO_NAME: str = "test-repo"
MOCK_REPO_VARIABLE: str = "VERSION_NUMBER"
MOCK_GITHUB_TOKEN: str = "abcdefghij-1234567890"
MOCK_GITHUB_OUTPUT: str = "test-github-output.txt"


class TestReleaseVersionUpdater(unittest.TestCase):
    def setUp(self):
        mock_github_client = MagicMock()
        with open(file=MOCK_GITHUB_OUTPUT, mode="w"):
            pass
        self.release_version_updater: ReleaseVersionUpdater = ReleaseVersionUpdater(
            logger=LOGGER,
            repo_owner=MOCK_REPO_OWNER,
            repo_name=MOCK_REPO_NAME,
            repo_variable=MOCK_REPO_VARIABLE,
            github_client=mock_github_client,
            github_output=MOCK_GITHUB_OUTPUT
        )
    
    def tearDown(self):
        with open(file=MOCK_GITHUB_OUTPUT, mode="w"):
            pass

    def test_get_commit_type_breaking(self):
        commit_msg: str = "BREAKING CHANGE: Deprecated legacy API endpoint"
        commit_type: CommitType = self.release_version_updater._get_commit_type(commit_msg)

        assert commit_type == CommitType.MAJOR
    
    def test_get_commit_type_feature(self):
        commit_msg: str = "feat: Implemented new API endpoint"
        commit_type: CommitType = self.release_version_updater._get_commit_type(commit_msg)

        assert commit_type == CommitType.MINOR

    def test_get_commit_type_fix(self):
        commit_msg: str = "fix: Fixed bug"
        commit_type: CommitType = self.release_version_updater._get_commit_type(commit_msg)

        assert commit_type == CommitType.PATCH

    def test_get_commit_type_refactor(self):
        commit_msg: str = "refactor: Removed redundant code"
        commit_type: CommitType = self.release_version_updater._get_commit_type(commit_msg)

        assert commit_type == CommitType.PATCH

    def test_get_commit_type_performance(self):
        commit_msg: str = "perf: Removed redundant code"
        commit_type: CommitType = self.release_version_updater._get_commit_type(commit_msg)

        assert commit_type == CommitType.PATCH
    
    def test_get_commit_type_other(self):
        commit_msg: str = "Created files"
        commit_type: CommitType = self.release_version_updater._get_commit_type(commit_msg)

        assert commit_type == CommitType.OTHER

    def test_get_current_release_version(self):
        mock_response: Response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(
            {
                "name": MOCK_REPO_VARIABLE,
                "value": "1.0.0",
                "created_at": "2021-08-10T14:59:22Z",
                "updated_at": "2022-01-10T14:59:22Z"
            }
        )
        self.release_version_updater.github_client.get_repository_variable.return_value = mock_response
        
        version: str = self.release_version_updater._get_current_release_version()
        self.release_version_updater.github_client.get_repository_variable.assert_called_once_with(
            repo_owner=MOCK_REPO_OWNER,
            repo_name=MOCK_REPO_NAME,
            variable=MOCK_REPO_VARIABLE
        )
        assert version == "1.0.0"

    def test_increment_release_version_major(self):
        curr_release_version: str = "1.0.0"
        latest_commit_type: str = CommitType.MAJOR
        new_release_version: str = self.release_version_updater._increment_release_version(curr_release_version, latest_commit_type)

        assert new_release_version == "2.0.0"

    def test_increment_release_version_minor(self):
        curr_release_version: str = "1.0.0"
        latest_commit_type: str = CommitType.MINOR
        new_release_version: str = self.release_version_updater._increment_release_version(curr_release_version, latest_commit_type)

        assert new_release_version == "1.1.0"

    def test_increment_release_version_patch(self):
        curr_release_version: str = "1.0.0"
        latest_commit_type: str = CommitType.PATCH
        new_release_version: str = self.release_version_updater._increment_release_version(curr_release_version, latest_commit_type)

        assert new_release_version == "1.0.1"

    def test_increment_release_version_other(self):
        curr_release_version: str = "1.0.0"
        latest_commit_type: str = CommitType.OTHER
        new_release_version: str = self.release_version_updater._increment_release_version(curr_release_version, latest_commit_type)

        assert new_release_version == "1.0.0"

    def test_write_to_github_output(self):
        curr_unix_time: int = int(time.time())
        self.release_version_updater._write_to_github_output(f"test_key_{curr_unix_time}", f"TEST_VALUE_{curr_unix_time}")

        with open(file=self.release_version_updater.github_output, mode="r") as github_output:
            lines: List[str] = github_output.readlines()
        
        assert lines[-1] == f"test_key_{curr_unix_time}=TEST_VALUE_{curr_unix_time}"

    def test_update_release_version(self):
        latest_commit_msg: str = self.release_version_updater._get_latest_commit_msg()
        latest_commit_type: str = self.release_version_updater._get_commit_type(latest_commit_msg)

        mock_response: Response = Response()
        mock_response.status_code = 200
        mock_response._content = json.dumps(
            {
                "name": MOCK_REPO_VARIABLE,
                "value": "1.0.0",
                "created_at": "2021-08-10T14:59:22Z",
                "updated_at": "2022-01-10T14:59:22Z"
            }
        )
        self.release_version_updater.github_client.get_repository_variable.return_value = mock_response

        self.release_version_updater.update_release_version()

        with open(file=MOCK_GITHUB_OUTPUT, mode="r") as github_output:
            lines: List[str] = github_output.readlines()
            if latest_commit_type == CommitType.MAJOR:
                self.release_version_updater.github_client.update_repository_variable.assert_called_once_with(
                    repo_owner=MOCK_REPO_OWNER,
                    repo_name=MOCK_REPO_NAME,
                    variable=MOCK_REPO_VARIABLE,
                    new_value="2.0.0"
                )
                assert lines[-1] == "release_version=2.0.0"
            elif latest_commit_type == CommitType.MINOR:
                self.release_version_updater.github_client.update_repository_variable.assert_called_once_with(
                    repo_owner=MOCK_REPO_OWNER,
                    repo_name=MOCK_REPO_NAME,
                    variable=MOCK_REPO_VARIABLE,
                    new_value="1.1.0"
                )
                assert lines[-1] == "release_version=1.1.0"
            elif latest_commit_type == CommitType.PATCH:
                self.release_version_updater.github_client.update_repository_variable.assert_called_once_with(
                    repo_owner=MOCK_REPO_OWNER,
                    repo_name=MOCK_REPO_NAME,
                    variable=MOCK_REPO_VARIABLE,
                    new_value="1.0.1"
                )
                assert lines[-1] == "release_version=1.0.1"
            elif latest_commit_type == CommitType.OTHER:
                self.release_version_updater.github_client.update_repository_variable.assert_not_called()
                assert lines[-1] == "release_version=1.0.0"


if __name__ == "__main__":
    unittest.main()
