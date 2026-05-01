from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from .book import Book

class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List[Book] = [] 

    model_config = ConfigDict(from_attributes=True)