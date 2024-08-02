from enum import Enum
from typing import Dict


class CommitMessagePrefix(str, Enum):
    """
    Represents prefixes to commit messages, e.g. "feat: Added API endpoint".

    See https://www.conventionalcommits.org/en/v1.0.0/
    """
    BREAKING = "BREAKING CHANGE"
    FEAT = "feat"
    FEATURE = "feature"
    FIX = "fix"
    REFACTOR = "refactor"
    PERF = "perf"
    PERFORMANCE = "performance"


class CommitType(str, Enum):
    """
    Commits that break backwards compatibility are a major change.
    
    Commits that add non-breaking features are a minor change.
    
    Commits for bug fixes, refactoring, or performance improvements are a patch.
    
    All other commits do not result in externally noticeable changes.
    """
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"
    OTHER = "other"


MESSAGE_PREFIX_TO_COMMIT_TYPE: Dict[CommitMessagePrefix, CommitType] = {
    CommitMessagePrefix.BREAKING: CommitType.MAJOR,
    CommitMessagePrefix.FEATURE: CommitType.MINOR,
    CommitMessagePrefix.FEAT: CommitType.MINOR,
    CommitMessagePrefix.FIX: CommitType.PATCH,
    CommitMessagePrefix.REFACTOR: CommitType.PATCH,
    CommitMessagePrefix.PERFORMANCE: CommitType.PATCH,
    CommitMessagePrefix.PERF: CommitType.PATCH
}
