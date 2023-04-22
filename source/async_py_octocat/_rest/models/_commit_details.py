from pydantic import BaseModel
from ._parent import Parent
from ._committer import Committer
from ._verification import Verification


__all__ = ["CommitDetails"]


class CommitDetails(BaseModel):
    url: str
    author: Committer
    committer: Committer
    message: str
    tree: Parent
    comment_count: int
    verification: Verification
