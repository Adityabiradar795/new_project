from pydantic import BaseModel
from typing import Optional
class UserCreate(BaseModel):
    username: str
    password: str
    adminkey:Optional[str]=None


class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True