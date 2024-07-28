from typing import Callable, Dict
import requests
from requests import HTTPError, RequestException, Response
from src.clients.github.constants import BASE_URI


class GitHubClient:
    def __init__(self, github_token: str):
        self.github_token: str = github_token
        self.base_uri: str = BASE_URI
        self.headers: Dict[str, str] = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {self.github_token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    def _handle_api_request(self, api_request_method: Callable) -> Response:
        response: Response = api_request_method()

        if response.status_code >= 400:
            raise HTTPError(f"{response.status_code} {response.reason}: {response.text}")
        elif response.status_code >= 300:
            raise RequestException(f"{response.status_code} {response.reason}: {response.text}")

        return response
    
    def get_repository_actions_variable(self, repo_owner: str, repo_name: str, variable: str) -> Response:
        def _get_repository_actions_variable() -> Response:
            response: Response = requests.get(
                url=f"{self.base_uri}/repos/{repo_owner}/{repo_name}/actions/variables/{variable}",
                headers=self.headers
            )

            return response
        
        response: Response = self._handle_api_request(_get_repository_actions_variable)

        return response
    
    def update_repository_actions_variable(self, repo_owner: str, repo_name: str, variable: str, new_value: str) -> Response:
        def _update_repository_actions_variable():
            response: Response = requests.patch(
                url=f"{self.base_uri}/repos/{repo_owner}/{repo_name}/actions/variables/{variable}",
                headers=self.headers,
                json={
                    "name": variable,
                    "value": new_value
                }
            )

            return response

        response: Response = self._handle_api_request(_update_repository_actions_variable)

        return response
