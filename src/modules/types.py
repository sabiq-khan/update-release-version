from enum import Enum
from typing import Dict


class CommitMessagePrefix(str, Enum):
    BREAKING = "breaking"
    FEAT = "feat"
    FIX = "fix"


class CommitType(str, Enum):
    BREAKING = "breaking"
    FEATURE = "feature"
    FIX = "fix"
    OTHER = "other"


MESSAGE_PREFIX_TO_COMMIT_TYPE: Dict[CommitMessagePrefix, CommitType] = {
    CommitMessagePrefix.BREAKING: CommitType.BREAKING,
    CommitMessagePrefix.FEAT: CommitType.FEATURE,
    CommitMessagePrefix.FIX: CommitType.FIX
}
