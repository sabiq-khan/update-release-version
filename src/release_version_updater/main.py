import os
import sys
WORKSPACE_ROOT: str = os.path.abspath(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.path.append(WORKSPACE_ROOT)
from src.clients.github.github_client import GitHubClient
from src.release_version_updater.release_version_updater import ReleaseVersionUpdater
from src.release_version_updater.constants import LOGGER, REPO_OWNER, REPO_NAME, REPO_VARIABLE, GITHUB_TOKEN, GITHUB_OUTPUT


def main():
    try:
        github_client: GitHubClient = GitHubClient(github_token=GITHUB_TOKEN)
        release_version_updater: ReleaseVersionUpdater = ReleaseVersionUpdater(
            logger=LOGGER,
            repo_owner=REPO_OWNER,
            repo_name=REPO_NAME,
            repo_variable=REPO_VARIABLE,
            github_client=github_client,
            github_output=GITHUB_OUTPUT
        )

        release_version_updater.update_release_version()
    except Exception as e:
        LOGGER.info(e)
        raise e


if __name__ == "__main__":
    main()
