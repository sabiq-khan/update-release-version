#!/usr/bin/env python3
import sys
import json
from constants import WORKSPACE_ROOT
sys.path.append(WORKSPACE_ROOT)
import requests
from requests import Response, HTTPError, RequestException
import subprocess
from subprocess import CompletedProcess
from src.modules.constants import LOGGER, REPO_OWNER, REPO_NAME, GITHUB_TOKEN
from src.modules.types import CommitType, MESSAGE_PREFIX_TO_COMMIT_TYPE


def get_latest_commit_msg() -> str:
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


def get_commit_type(commit_msg: str) -> str:
    msg_prefix: str = commit_msg.split(":")[0]
    commit_type: str = MESSAGE_PREFIX_TO_COMMIT_TYPE.get(msg_prefix, CommitType.OTHER)

    return commit_type


def get_current_version() -> str:
    response: Response = requests.get(
        url=f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/variables/VERSION",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    )

    version: str = json.loads(response.content)["value"]

    return version


def increment_version(curr_version: str, latest_commit_type: CommitType) -> str:
    major_version, minor_version, patch_version = map(int, curr_version.lstrip("v").split("."))

    if latest_commit_type == CommitType.BREAKING:
        major_version += 1
    elif latest_commit_type == CommitType.FEATURE:
        minor_version += 1
    elif latest_commit_type == CommitType.FIX:
        patch_version += 1
    
    new_version: str = f"v{major_version}.{minor_version}.{patch_version}"

    return new_version

def update_current_version(new_version: str) -> Response:
    response: Response = requests.patch(
        url=f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/variables/VERSION",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        },
        json={
            "name": "VERSION",
            "value": new_version
        }
    )

    if response.status_code >= 400:
        raise HTTPError(f"{response.status_code} {response.reason}: {response.text}")
    elif response.status_code >= 300:
        raise RequestException(f"{response.status_code} {response.reason}: {response.text}")

    return response


def main():
    LOGGER.info(f"Checking latest commit for {REPO_OWNER}/{REPO_NAME}...")
    latest_commit_msg: str = get_latest_commit_msg()
    LOGGER.info(f"Latest commit message: {latest_commit_msg}")
    latest_commit_type: str = get_commit_type(latest_commit_msg)
    LOGGER.info(f"Latest commit type: {latest_commit_type}")

    LOGGER.info(f"Calling GitHub API to get current release version for {REPO_OWNER}/{REPO_NAME}")
    curr_version: str = get_current_version()
    LOGGER.info(f"Latest release version: {curr_version}")

    new_version: str = increment_version(curr_version, latest_commit_type)
    LOGGER.info(f"Calling GitHub API to update release version for {REPO_OWNER}/{REPO_NAME} to {new_version}...")
    update_version_response: Response = update_current_version(new_version)
    LOGGER.info(f"Received the following response from GitHub: {update_version_response.status_code}")
    LOGGER.info(f"Successfully incremented release version to {new_version}!")


if __name__ == "__main__":
    main()
