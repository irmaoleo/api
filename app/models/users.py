from typing import Optional, List
from pydantic import BaseModel


class Users(BaseModel):
    _id: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    