#!/usr/bin/env python3
import os
from typing import Dict
import requests
from requests import Response
import subprocess
from subprocess import CompletedProcess

REPO_NAME: str = os.environ["REPO_NAME"]
REPO_OWNER: str = os.environ["REPO_OWNER"]
GITHUB_TOKEN: str = os.environ["GITHUB_TOKEN"]
MESSAGE_PREFIX_TO_COMMIT_TYPE: Dict[str, str] = {
    "breaking": "breaking",
    "feat": "feature",
    "fix": "fix"
}


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

    commit_msg: str = git_log.stdout

    return commit_msg


def get_commit_type(commit_msg: str) -> str:
    msg_prefix: str = commit_msg.split(":")[0]
    commit_type: str = MESSAGE_PREFIX_TO_COMMIT_TYPE.get(msg_prefix, "other")

    return commit_type


def get_current_version() -> Response:
    response: Response = requests.get(
        url=f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/variables/VERSION",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
    )

    return response


def update_current_version(new_version: str) -> Response:
    response: Response = requests.patch(
        url=f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/variables/VERSION",
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        },
        data={
            "name": "VERSION",
            "value": new_version
        }
    )

    return response


def main():
    commit_msg: str = get_latest_commit_msg()
    commit_type: str = get_commit_type(commit_msg)
    response: Response = get_current_version()


if __name__ == "__main__":
    main()
