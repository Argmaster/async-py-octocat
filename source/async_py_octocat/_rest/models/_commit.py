from typing import List
from ._interactive import Interactive
from ._parent import Parent
from ._user import User
from ._commit_details import CommitDetails


__all__ = ["Commit"]


class Commit(Interactive):
    url: str
    sha: str
    node_id: str
    html_url: str
    comments_url: str
    commit: CommitDetails
    author: User
    committer: User
    parents: List[Parent]
