from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import schemas, controllers

router = APIRouter(
    prefix="/authors",
    tags=["authors"]
)

@router.post("/", response_model=schemas.Author)
def create_author(author: schemas.AuthorCreate, db: Session = Depends(get_db)):
    return controllers.create_author(db=db, author=author)

@router.get("/", response_model=List[schemas.Author])
def list_authors(db: Session = Depends(get_db)):
    return controllers.get_authors(db=db)

@router.get("/{author_id}", response_model=schemas.Author, status_code=200)
def get_author_by_id(author_id: str, db: Session = Depends(get_db)):
    return controllers.get_author_by_id(db=db, author_id=author_id)

@router.put("/{author_id}", response_model=schemas.Author, status_code=200 )
def update_author( author_id: str, author: schemas.AuthorUpdate,  db: Session = Depends(get_db)):
    return controllers.update_author(db=db,  author_id=author_id, author=author )

@router.delete("/{author_id}", status_code=200)
def delete_author(author_id: str, db: Session = Depends(get_db)):
    return controllers.author_controller.delete_author(db=db, author_id=author_id)

@router.delete("/{author_id}/books/{book_id}", status_code=200)
def delete_author_book(author_id: str, book_id: str, db: Session = Depends(get_db)):
    return controllers.author_controller.delete_author_book(
        db=db, 
        author_id=author_id, 
        book_id=book_id
    )