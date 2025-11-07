from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from typing import List 

class User(BaseModel):
    name:str
    email: EmailStr
    password: str = Field(...,min_length=8)
    username:str

class Login(BaseModel):
    email: EmailStr
    password: str = Field(...,min_length=8)
    

class NoteBase(BaseModel):
    title: str
    content: Optional[str] = None


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class NoteDictResponse(NoteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    # owner_id: int
class NoteResponse():
    data: List[NoteDictResponse]