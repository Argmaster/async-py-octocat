from datetime import datetime
from pydantic import BaseModel


class Committer(BaseModel):
    name: str
    email: str
    date: datetime
