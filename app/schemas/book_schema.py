from typing import Optional
from pydantic import BaseModel, ConfigDict

class BookBase(BaseModel):
    title: str
    price: Optional[int] = None
    pages: Optional[int] = None  
    author_id: Optional[int] = None

class BookCreate(BookBase):
    pass 

class Book(BookBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)