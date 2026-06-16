from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, controllers

router = APIRouter(
    prefix="/save-data",
    tags=["save-data"]
)

@router.post("/new-author/book", response_model=dict)
def create_author_and_book_atomic(
    author_data: schemas.AuthorCreate, 
    book_data: schemas.BookCreate,
    db: Session = Depends(get_db)
):
    return controllers.create_author_and_book_atomic(
        db=db, 
        author_data=author_data, 
        book_data=book_data
    )