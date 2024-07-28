import sys
import json
import os
from typing import Any, Dict
from constants import WORKSPACE_ROOT
sys.path.append(WORKSPACE_ROOT)
from src.clients.github.github_client import GitHubClient
import unittest
from requests import Response

GITHUB_TOKEN: str = os.environ["GITHUB_TOKEN"]

REPO_OWNER: str = os.environ["REPO_OWNER"]
REPO_NAME: str = os.environ["REPO_NAME"]
VARIABLE: str = os.environ["VARIABLE"]
EXPECTED_VALUE: str = os.environ["EXPECTED_VALUE"]
NEW_VALUE: str = "wazam"

class TestGitHubClient(unittest.TestCase):
    def setUp(self) -> GitHubClient:
        self.github_client: GitHubClient = GitHubClient(github_token=GITHUB_TOKEN)
    
    def tearDown(self) -> None:
        # Resets variable to original value
        self.github_client.update_repository_actions_variable(
            repo_owner=REPO_OWNER,
            repo_name=REPO_NAME,
            variable=VARIABLE,
            new_value=EXPECTED_VALUE
        )
    
    def test_get_repository_actions_variable(self):
        response: Response = self.github_client.get_repository_actions_variable(
            repo_owner=REPO_OWNER,
            repo_name=REPO_NAME,
            variable=VARIABLE
        )

        body: Dict[str, Any] = json.loads(response.content)

        assert 200 <= response.status_code < 300
        assert "value" in body
        assert "name" in body
        assert body["name"] == VARIABLE
        assert body["value"] == EXPECTED_VALUE
    
    def test_update_repository_actions_variable(self):
        update_variable_response: Response = self.github_client.update_repository_actions_variable(
            repo_owner=REPO_OWNER,
            repo_name=REPO_NAME,
            variable=VARIABLE,
            new_value=NEW_VALUE
        )

        assert 200 <= update_variable_response.status_code < 300
        
        get_variable_response: Response = self.github_client.get_repository_actions_variable(
            repo_owner=REPO_OWNER,
            repo_name=REPO_NAME,
            variable=VARIABLE
        )

        body: Dict[str, Any] = json.loads(get_variable_response.content)
        assert body["value"] == NEW_VALUE

if __name__ == "__main__":
    unittest.main()
