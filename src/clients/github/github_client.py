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
            raise HTTPError(
                f"{response.status_code} {response.reason}: {response.text}")
        elif response.status_code >= 300:
            raise RequestException(
                f"{response.status_code} {response.reason}: {response.text}")

        return response

    def get_repository_variable(self, repo_owner: str, repo_name: str, variable: str) -> Response:
        """
        Retrieves the value of a specified GitHub Actions repository variable for a specified repository. See https://docs.github.com/en/rest/actions/variables?apiVersion=2022-11-28#get-a-repository-variable

        Arguments:
        variable (str) - GitHub repository variable whose value will be retrieved
        
        repo_name (str) - GitHub repo to which the variable belongs
        
        repo_owner (str) - GitHub username of the account that owns the repo

        Returns:
        
        response (Response) - A requests.Response object containing JSON body in Response.content byte string
        """
        def _get_repository_variable() -> Response:
            response: Response = requests.get(
                url=f"{self.base_uri}/repos/{repo_owner}/{repo_name}/actions/variables/{variable}",
                headers=self.headers
            )

            return response

        response: Response = self._handle_api_request(
            _get_repository_variable)

        return response

    def update_repository_variable(self, repo_owner: str, repo_name: str, variable: str, new_value: str) -> Response:
        """
        Changes the value of a specified GitHub Actions repository variable for a specified repository. See https://docs.github.com/en/rest/actions/variables?apiVersion=2022-11-28#update-a-repository-variable

        Arguments:

        variable (str) - GitHub repository variable whose value will be changed

        new_value (str) - The new value of the repository variable
        
        repo_name (str) - GitHub repo to which the variable belongs
        
        repo_owner (str) - GitHub username of the account that owns the repo

        Returns:
        
        response (Response) - A requests.Response object. This call does not return data in response body.
        """
        def _update_repository_variable() -> Response:
            response: Response = requests.patch(
                url=f"{self.base_uri}/repos/{repo_owner}/{repo_name}/actions/variables/{variable}",
                headers=self.headers,
                json={
                    "name": variable,
                    "value": new_value
                }
            )

            return response

        response: Response = self._handle_api_request(
            _update_repository_variable)

        return response
