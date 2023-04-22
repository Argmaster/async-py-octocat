from pydantic import BaseModel
from typing import Optional


__all__ = ["Verification"]


class Verification(BaseModel):
    verified: bool
    reason: Optional[str]
    signature: Optional[str]
    payload: Optional[str]
