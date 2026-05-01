from pydantic import BaseModel, ConfigDict
from typing import List, Optional

# --- Book Schemas ---
class BookBase(BaseModel):
    title: str
    price: int
    author_id: int

class BookCreate(BookBase):
    pass 

class Book(BookBase):
    id: int
    
    # Modern Pydantic V2 way
    model_config = ConfigDict(from_attributes=True)

# --- Author Schemas ---
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List[Book] = [] 

    model_config = ConfigDict(from_attributes=True)