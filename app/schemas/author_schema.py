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

class AuthorSearchRequest(BaseModel):
    name: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=10) # Max 10 rows
    offset: int = Field(default=0, ge=0)

class AuthorWithoutBooks(BaseModel):
    id: int
    name: str
    bio: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Response Schema Wrapper
class AuthorSearchResponse(BaseModel):
    total: int
    results: List[AuthorWithoutBooks]