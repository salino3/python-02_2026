from sqlalchemy.orm import Session
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
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

    if not author.id:
        raise HTTPException(status_code=400, detail="ID in the body query is required")
    elif not isinstance(author.id, int):
        raise HTTPException(status_code=400, detail="ID must be an integer")
    
    if not author.name.strip() and not author.bio.strip():
        raise HTTPException(status_code=400, detail="In the body query there is not 'name' nor 'bio' for updating the author")

    try:
        numeric_url_id = int(author_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID must be a valid integer")
    
    if author.id != numeric_url_id:
        raise HTTPException(
            status_code=400, 
            detail=(
                f"Mismatched IDs. The URL specifies ID {numeric_url_id}, "
                f"but the request body specifies ID {author.id}. "
                f"These must match."
            )
        )

    update_data = author.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No update data provided")
    # removing "id" prevents unnecessary database constraint checks.
    update_data.pop("id")
    
    try:
        # 1. Build the UPDATE statement with RETURNING
        stmt = (
            update(models.Author)
            .where(models.Author.id == numeric_url_id)
            .values(**update_data)
            .returning(models.Author)  # <-- Postgres will return the updated row
        )
        
        # 2. Execute and grab the returned row directly
        result = db.execute(stmt)
        updated_author = result.scalars().first()   
        
        # If nothing was returned, the author didn't exist
        if not updated_author:
            raise HTTPException(
                status_code=404, 
                detail=f"Author update failed. ID {numeric_url_id} does not exist."
            )
        
        db.commit()
        return updated_author  # Return the object Postgres gave us

    except HTTPException:
        raise
    except SQLAlchemyError as db_err:
        db.rollback()
        error_detail = str(db_err.orig) if hasattr(db_err, "orig") else str(db_err)
        raise HTTPException(
            status_code=400, 
            detail=f"Database rejected the update. Reason: {error_detail}"
        )
    

    #
def delete_author(db: Session, author_id: str):
    # 1. Validate that the URL ID can be converted to an integer
    try:
        numeric_id = int(author_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID must be a valid number")
    
    # 2. Fetch the author from the database
    author = db.query(models.Author).filter(models.Author.id == numeric_id).first()
    
    # 3. If author does not exist, raise 404
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    # 4. Delete the author record (Cascade will handle the books)
    db.delete(author)
    db.commit()
    
    return {"message": f"Author with ID {numeric_id} and all their books have been successfully deleted"} 