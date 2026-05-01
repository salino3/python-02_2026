from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas, controllers

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

@router.post("/", response_model=schemas.Book)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    return controllers.create_book(db=db, book=book)

@router.get("/", response_model=List[schemas.Book])
def list_books(db: Session = Depends(get_db)):
    return controllers.get_books(db=db)