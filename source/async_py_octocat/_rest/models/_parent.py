from pydantic import BaseModel


__all__ = ["Parent"]


class Parent(BaseModel):
    url: str
    sha: str
