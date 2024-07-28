from enum import Enum
from typing import Dict


class CommitMessagePrefix(str, Enum):
    BREAKING = "breaking"
    FEAT = "feat"
    FEATURE = "feature"
    FIX = "fix"
    REFACTOR = "refactor"
    PERF = "perf"
    PERFORMANCE = "performance"


class CommitType(str, Enum):
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
