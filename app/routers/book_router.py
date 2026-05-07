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

 
 