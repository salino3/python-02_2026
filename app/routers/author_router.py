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