from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, bio=author.bio)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

# 
def get_authors(db: Session):
    return db.query(models.Author).all()

# 
def get_author_by_id(db: Session, author_id: str):

    try:
      numeric_id = int(author_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID must be a valid number")
    
    author = db.query(models.Author).filter(models.Author.id == numeric_id).first()
    
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    return author

# 
def update_author(db: Session, author_id: str, author: schemas.AuthorUpdate):
   
    try:
        numeric_id = int(author_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID must be a valid number")
    
    
    db_author = db.query(models.Author).filter(models.Author.id == numeric_id).first()
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    # Extract the update data (exclude fields that weren't provided)
    update_data = author.model_dump(exclude_unset=True)
    
    # 4. Apply the updates dynamically to the database model
    for key, value in update_data.items():
        setattr(db_author, key, value)
    
    try:
        db.commit()
        db.refresh(db_author)  # Refresh to get updated fields and relationships (like books)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database update failed")
        
    return db_author

