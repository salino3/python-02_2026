from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())

    if not book.title:
        raise HTTPException(status_code=404, detail="Title not found")
    
    # Convert SQLAlchemy object to something JSON-friendly
    data = jsonable_encoder(db_book)
         
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return  JSONResponse(
            status_code = 201, 
            content = data
        )
 
# 
def get_books(db: Session):
    return db.query(models.Book).all()