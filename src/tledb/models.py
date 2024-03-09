from typing import Optional

from sqlmodel import Field, SQLModel


class TLE(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    line1: str
    line2: str
