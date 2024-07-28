import sys
import os
from logging import Logger, StreamHandler, Formatter, INFO

LOGGER: Logger = Logger("release_version_updater")
LOGGER.setLevel(INFO)
HANDLER = StreamHandler(sys.stdout)
HANDLER.setLevel(INFO)
FORMATTER = Formatter(
    "[%(asctime)s][%(name)s][%(filename)s:%(lineno)d][%(funcName)s][%(levelname)s]: %(message)s")
HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(HANDLER)

REPO_NAME: str = os.environ["REPO_NAME"]
REPO_OWNER: str = os.environ["REPO_OWNER"]
REPO_VARIABLE: str = os.environ["REPO_VARIABLE"]
GITHUB_TOKEN: str = os.environ["GITHUB_TOKEN"]
GITHUB_OUTPUT: str = os.environ["GITHUB_OUTPUT"]
