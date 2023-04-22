from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import HttpUrl

from . import _user as user
from ._interactive import Interactive
from ._license import License
from ._organization import Organization
from ._perms import Permissions
from ._commit import Commit

from backports.cached_property import cached_property


class Visibility(Enum):
    PRIVATE = "private"
    PUBLIC = "public"


class ListProxy(Interactive):
    def commits(self) -> Commit:
        ...


class Repository(Interactive):
    id: int  # noqa: A003
    node_id: str
    name: str
    full_name: str
    owner: user.User
    private: bool
    html_url: HttpUrl
    description: str
    fork: bool
    url: HttpUrl
    archive_url: HttpUrl
    assignees_url: HttpUrl
    blobs_url: HttpUrl
    branches_url: HttpUrl
    collaborators_url: HttpUrl
    comments_url: HttpUrl
    commits_url: HttpUrl
    compare_url: HttpUrl
    contents_url: HttpUrl
    contributors_url: HttpUrl
    deployments_url: HttpUrl
    downloads_url: HttpUrl
    events_url: HttpUrl
    forks_url: HttpUrl
    git_commits_url: HttpUrl
    git_refs_url: HttpUrl
    git_tags_url: HttpUrl
    git_url: str
    issue_comment_url: HttpUrl
    issue_events_url: HttpUrl
    issues_url: HttpUrl
    keys_url: HttpUrl
    labels_url: HttpUrl
    languages_url: HttpUrl
    merges_url: HttpUrl
    milestones_url: HttpUrl
    notifications_url: HttpUrl
    pulls_url: HttpUrl
    releases_url: HttpUrl
    ssh_url: str
    stargazers_url: HttpUrl
    statuses_url: HttpUrl
    subscribers_url: HttpUrl
    subscription_url: HttpUrl
    tags_url: HttpUrl
    teams_url: HttpUrl
    trees_url: HttpUrl
    clone_url: HttpUrl
    mirror_url: Optional[str]
    hooks_url: HttpUrl
    svn_url: HttpUrl
    homepage: str
    language: Optional[str]
    forks_count: int
    forks: int
    stargazers_count: int
    watchers_count: int
    watchers: int
    size: int
    default_branch: str
    open_issues_count: int
    open_issues: int
    is_template: bool
    topics: List[str]
    has_issues: bool
    has_projects: bool
    has_wiki: bool
    has_pages: bool
    has_downloads: bool
    archived: bool
    disabled: bool
    visibility: Visibility
    pushed_at: datetime
    created_at: datetime
    updated_at: datetime
    permissions: Permissions
    allow_rebase_merge: Optional[bool]
    template_repository: Optional[Repository]
    temp_clone_token: str
    allow_squash_merge: Optional[bool]
    allow_auto_merge: Optional[bool]
    delete_branch_on_merge: Optional[bool]
    allow_merge_commit: Optional[bool]
    subscribers_count: int
    network_count: int
    license: Optional[License]  # noqa: A003
    organization: Optional[Organization]
    parent: Optional[Repository]
    source: Optional[Repository]

    @cached_property
    def list(self) -> ListProxy:  # noqa: FNE002, A003
        return ListProxy(gh_session_object=self.gh_session_object)

    def commit(self, sha_or_tag: str) -> Commit:
        ...
