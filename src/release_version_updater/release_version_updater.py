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
    def __init__(self, logger: Logger, repo_owner: str, repo_name: str, repo_variable: str, github_token: str):
        self.logger: Logger = logger
        self.repo_owner: str = repo_owner
        self.repo_name: str = repo_name
        self.repo_variable: str = repo_variable
        self.github_client: GitHubClient = GitHubClient(github_token)

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

    def _get_commit_type(self, commit_msg: str) -> str:
        msg_prefix: str = commit_msg.split(":")[0]
        commit_type: str = MESSAGE_PREFIX_TO_COMMIT_TYPE.get(
            msg_prefix, CommitType.OTHER)

        return commit_type

    def _get_current_version(self) -> str:
        response: Response = self.github_client.get_repository_actions_variable(
            repo_owner=self.repo_owner,
            repo_name=self.repo_name,
            variable=self.repo_variable
        )

        version: str = json.loads(response.content)["value"]

        return version

    def _increment_version(self, curr_version: str, latest_commit_type: CommitType) -> str:
        major_version, minor_version, patch_version = map(
            int, curr_version.lstrip("v").split("."))

        if latest_commit_type == CommitType.BREAKING:
            major_version += 1
        elif latest_commit_type == CommitType.FEATURE:
            minor_version += 1
        elif latest_commit_type == CommitType.FIX:
            patch_version += 1

        new_version: str = f"v{major_version}.{minor_version}.{patch_version}"

        return new_version

    def update_release_version(self):
        self.logger.info(f"Checking latest commit for {self.repo_owner}/{self.repo_name}...")
        latest_commit_msg: str = self._get_latest_commit_msg()
        self.logger.info(f"Latest commit message: {latest_commit_msg}")
        latest_commit_type: str = self._get_commit_type(latest_commit_msg)
        self.logger.info(f"Latest commit type: {latest_commit_type}")

        self.logger.info(
            f"Calling GitHub API to get current release version for {self.repo_owner}/{self.repo_name}...")
        curr_version: str = self._get_current_version()
        self.logger.info(f"Latest release version: {curr_version}")

        new_version: str = self._increment_version(curr_version, latest_commit_type)
        self.logger.info(
            f"Calling GitHub API to update release version for {self.repo_owner}/{self.repo_name} to {new_version}...")
        response: Response = self.github_client.update_repository_actions_variable(
            repo_owner=self.repo_owner,
            repo_name=self.repo_name,
            variable=self.repo_variable,
            new_value=new_version
        )
        self.logger.info(
            f"Received the following response from GitHub: {response.status_code}")
        self.logger.info(f"Successfully incremented release version to {new_version}!")
