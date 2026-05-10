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