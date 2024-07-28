import sys
import os
from logging import Logger, StreamHandler, Formatter, INFO

WORKSPACE_ROOT: str = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

LOGGER: Logger = Logger("update_release_version")
LOGGER.setLevel(INFO)
HANDLER = StreamHandler(sys.stdout)
HANDLER.setLevel(INFO)
FORMATTER = Formatter(
    "[%(asctime)s][%(name)s][%(filename)s:%(lineno)d][%(funcName)s][%(levelname)s]: %(message)s")
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

REPO_NAME: str = os.environ["REPO_NAME"]
REPO_OWNER: str = os.environ["REPO_OWNER"]
GITHUB_TOKEN: str = os.environ["GITHUB_TOKEN"]