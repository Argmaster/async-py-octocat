from aiohttp import ClientSession

from .._constants import BASE_URL
from .._models import Repository
from ..exceptions import Forbidden403, MovedPermanently301, NotFound404

__all__ = ["RepoAccessMixin"]


class RepoAccessMixin:

    session: ClientSession

    async def get_repo(self, owner: str, repo: str) -> Repository:
        async with self.session.get(
            f"{BASE_URL}/repos/{owner}/{repo}"
        ) as response:
            content = await response.text()
            if response.status == 301:
                raise MovedPermanently301(content)
            if response.status == 403:
                raise Forbidden403(content)
            if response.status == 404:
                raise NotFound404(content)
            assert response.status == 200, response
        repository = Repository.parse_raw(content, content_type="json")
        repository._session = self  # type: ignore
        return repository
