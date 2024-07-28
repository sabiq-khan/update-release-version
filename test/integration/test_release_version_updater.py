import os
import sys
import unittest
WORKSPACE_ROOT: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(WORKSPACE_ROOT)
from src.release_version_updater.release_version_updater import ReleaseVersionUpdater
from src.release_version_updater.types import CommitType
from src.release_version_updater.constants import LOGGER, REPO_OWNER, REPO_NAME, REPO_VARIABLE, GITHUB_TOKEN


class TestReleaseVersionUpdater(unittest.TestCase):
    def setUp(self):
        self.release_version_updater: ReleaseVersionUpdater = ReleaseVersionUpdater(
            logger=LOGGER,
            repo_owner=REPO_OWNER,
            repo_name=REPO_NAME,
            repo_variable=REPO_VARIABLE,
            github_token=GITHUB_TOKEN
        )
    
    def test_get_commit_type_feature(self):
        commit_msg: str = "feat: Implemented new API endpoint"
        commit_type: CommitType = self.release_version_updater._get_commit_type(commit_msg)

        assert commit_type == CommitType.FEATURE

    def test_get_commit_type_fix(self):
        commit_msg: str = "fix: Fixed bug"
        commit_type: CommitType = self.release_version_updater._get_commit_type(commit_msg)

        assert commit_type == CommitType.FIX

    def test_get_commit_type_breaking(self):
        commit_msg: str = "breaking: Deprecated legacy API endpoint"
        commit_type: CommitType = self.release_version_updater._get_commit_type(commit_msg)

        assert commit_type == CommitType.BREAKING
    
    def test_get_commit_type_other(self):
        commit_msg: str = "Created files"
        commit_type: CommitType = self.release_version_updater._get_commit_type(commit_msg)

        assert commit_type == CommitType.OTHER


if __name__ == "__main__":
    unittest.main()
