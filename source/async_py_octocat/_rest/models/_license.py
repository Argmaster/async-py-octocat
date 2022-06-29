from __future__ import annotations

from typing import Optional

from pydantic import HttpUrl

from ._response import RestResponse

__all__ = ["License"]


class License(RestResponse):
    key: str
    name: str
    url: HttpUrl
    spdx_id: str
    node_id: str
    html_url: Optional[HttpUrl]
