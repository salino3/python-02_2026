from typing import Optional
from pydantic import BaseModel, ConfigDict

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

# Inheritance from BookBase
class Book(BookBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)