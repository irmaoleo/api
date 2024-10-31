from typing import Optional, List
from pydantic import BaseModel


class Users(BaseModel):
    _id: Optional[str] = None
    fullName: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    postalCode: Optional[str] = None
    gender: Optional[str] = None
    birthDate: Optional[str] = None