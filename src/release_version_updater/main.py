import os
import sys
WORKSPACE_ROOT: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(WORKSPACE_ROOT)
from release_version_updater.release_version_updater import ReleaseVersionUpdater
from src.release_version_updater.constants import LOGGER, REPO_OWNER, REPO_NAME, REPO_VARIABLE, GITHUB_TOKEN

def main():
    release_version_updater: ReleaseVersionUpdater = ReleaseVersionUpdater(
        logger=LOGGER,
        repo_owner=REPO_OWNER,
        repo_name=REPO_NAME,
        repo_variable=REPO_VARIABLE,
        github_token=GITHUB_TOKEN
    )

    release_version_updater.update_release_version()


if __name__ == "__main__":
    main()
