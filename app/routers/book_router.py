from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas, controllers

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.post("/", response_model=schemas.Book, status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return controllers.create_book(db=db, book=book)

@router.get("/", response_model=List[schemas.Book], status_code=200)
def list_books(db: Session = Depends(get_db)):
    return controllers.get_books(db=db)

@router.get("/{book_id}", response_model=schemas.Book, status_code=200)
def get_book_by_id(book_id: str, db: Session = Depends(get_db)):
    return controllers.get_book_by_id(db=db, book_id=book_id)

@router.put("/{book_id}", response_model=schemas.Book, status_code=200)
def update_book(book_id: str, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    return controllers.update_book(db=db, book_id=book_id, book_update=book)
 
# Use schemas.Author because it returns the full author data profile
@router.get("/{book_id}/author", response_model=schemas.Author, status_code=200)
def get_author_by_book_id(book_id: str, db: Session = Depends(get_db)):
    return controllers.get_author_by_book_id(db=db, book_id=book_id)