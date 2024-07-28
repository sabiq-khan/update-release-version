#!/usr/bin/env python3
from subprocess import CompletedProcess
import subprocess
from requests import Response
import json
import os
import sys
from logging import Logger
WORKSPACE_ROOT: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(WORKSPACE_ROOT)
from src.release_version_updater.types import CommitType, MESSAGE_PREFIX_TO_COMMIT_TYPE
from src.clients.github.github_client import GitHubClient


class ReleaseVersionUpdater:
    """
    Increments the semantic release version of a specified GitHub repository.

    Requires that the release version is being stored in a repository variable.
    Also requires that the release version has the format f"v{major_version}.{minor_version}.{patch_version}".

    Tries to determine which digit to increment based on the prefix of the latest commit, see https://www.conventionalcommits.org/en/v1.0.0/

    Commits that break backwards compatibility result in a major version increment.
    Commits that add non-breaking features result in a minor version increment.
    Commits for bug fixes, refactoring, or performance improvements result in patch version increments.
    All other commits do not result in any release version increment.
    """
    def __init__(self, logger: Logger, repo_owner: str, repo_name: str, repo_variable: str, github_client: GitHubClient):
        """
        Arguments:

        logger (Logger) - An instance of logging.Logger
        
        repo_variable (str) - GitHub repository variable storing current release version
        
        repo_name (str) - GitHub repo where release version must be incremented
        
        repo_owner (str) - GitHub username of the account that owns the repo
        
        github_client (GitHubClient) - An instance of src.clients.github.github_client.GitHubClient
        """
        self.logger: Logger = logger
        self.repo_owner: str = repo_owner
        self.repo_name: str = repo_name
        self.repo_variable: str = repo_variable
        self.github_client: GitHubClient = github_client

    def _get_latest_commit_msg(self) -> str:
        git_log: CompletedProcess = subprocess.run(
            [
                "git",
                "log",
                "-1",
                "--pretty=%B"
            ],
            shell=False,
            capture_output=True
        )

        commit_msg: str = bytes(git_log.stdout).decode("utf-8")

        return commit_msg

    def _get_commit_type(self, commit_msg: str) -> CommitType:
        msg_prefix: str = commit_msg.split(":")[0]
        commit_type: CommitType = MESSAGE_PREFIX_TO_COMMIT_TYPE.get(
            msg_prefix, CommitType.OTHER)

        return commit_type

    def _get_current_release_version(self) -> str:
        response: Response = self.github_client.get_repository_actions_variable(
            repo_owner=self.repo_owner,
            repo_name=self.repo_name,
            variable=self.repo_variable
        )

        release_version: str = json.loads(response.content)["value"]

        return release_version

    def _increment_release_version(self, curr_release_version: str, latest_commit_type: CommitType) -> str:
        major_version, minor_version, patch_version = map(
            int, curr_release_version.lstrip("v").split("."))

        if latest_commit_type == CommitType.MAJOR:
            major_version += 1
        elif latest_commit_type == CommitType.MINOR:
            minor_version += 1
        elif latest_commit_type == CommitType.PATCH:
            patch_version += 1

        new_release_version: str = f"v{major_version}.{minor_version}.{patch_version}"

        return new_release_version

    def update_release_version(self):
        try:
            self.logger.info(f"Checking latest commit for {self.repo_owner}/{self.repo_name}...")
            latest_commit_msg: str = self._get_latest_commit_msg()
            self.logger.info(f"Latest commit message: {latest_commit_msg}")
            latest_commit_type: CommitType = self._get_commit_type(latest_commit_msg)
            self.logger.info(f"Latest commit type: {latest_commit_type}")

            self.logger.info(
                f"Calling GitHub API to get current release version for {self.repo_owner}/{self.repo_name}...")
            curr_release_version: str = self._get_current_release_version()
            self.logger.info(f"Latest release version: {curr_release_version}")

            incremented_version: str = self._increment_release_version(curr_release_version, latest_commit_type)
            # Ensures version was successfully incremented
            if incremented_version != curr_release_version:
                self.logger.info(
                    f"Calling GitHub API to update release version for {self.repo_owner}/{self.repo_name} to {incremented_version}...")
                response: Response = self.github_client.update_repository_actions_variable(
                    repo_owner=self.repo_owner,
                    repo_name=self.repo_name,
                    variable=self.repo_variable,
                    new_value=incremented_version
                )
                self.logger.info(
                    f"Received the following response from GitHub: {response.status_code}")
                self.logger.info(f"Successfully incremented release version from {curr_release_version} to {incremented_version}!")
            else:
                self.logger.info(f"No increment applied to version number {curr_release_version}. Exiting.")
        except Exception as e:
            self.logger.error(e)
            raise e
