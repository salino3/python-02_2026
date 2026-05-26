from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field

class BookBase(BaseModel):
    title: str
    price: Optional[int] = None
    pages: Optional[int] = None  
    author_id: Optional[int] = None

# Inheritance from BookBase
class BookCreate(BookBase):
    pass 

class BookUpdate(BaseModel):
    title: Optional[str] = None
    price: Optional[int] = None
    pages: Optional[int] = None
    author_id: Optional[int] = None

class BookSearchRequest(BaseModel):
    title: Optional[str] = None
    limit: int = Field(default=10, ge=1, le=10)  # Min 1, Max 10 books per request
    offset: int = Field(default=0, ge=0) # Cannot be negative


# Inheritance from BookBase
class Book(BookBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class BookSearchResponse(BaseModel):
    total: int               
    results: List[Book]