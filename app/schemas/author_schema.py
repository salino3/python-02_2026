from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from .book_schema import Book

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    id: int = Field(strict=True)
    name: Optional[str] = None
    bio: Optional[str] = None

class Author(AuthorBase):
    id: int
    books: List[Book] = [] 

    model_config = ConfigDict(from_attributes=True)