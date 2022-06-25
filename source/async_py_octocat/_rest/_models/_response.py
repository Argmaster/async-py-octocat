from __future__ import annotations

from typing import Any, Tuple

from backports.cached_property import cached_property
from pydantic import BaseModel, Extra

__all__ = ["RestResponse"]


class RestResponse(BaseModel):
    class Config:
        anystr_strip_whitespace: bool = True
        validate_all: bool = True
        extra: Extra = Extra.ignore
        allow_mutation: bool = False
        arbitrary_types_allowed: bool = True
        keep_untouched: Tuple[Any, ...] = (cached_property,)
        underscore_attrs_are_private: bool = True
        copy_on_model_validation: bool = True
