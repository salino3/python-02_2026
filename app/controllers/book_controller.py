from sqlalchemy import func
from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())

    if not book.title:
        raise HTTPException(status_code=404, detail="Title is mandatory")
    
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


# 
def get_book_by_id(db: Session, book_id: str):

    try:
        numeric_id = int(book_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID must be a valid number")

    book = db.query(models.Book).filter(models.Book.id == numeric_id).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book

#
def update_book(db: Session, book_id: str, book_update: schemas.BookUpdate):
    try:
        numeric_id = int(book_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Book ID must be a valid number")

    db_book = db.query(models.Book).filter(models.Book.id == numeric_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_update.model_dump(exclude_unset=True)

    # CRITICAL CHECK: Verify the book belongs to the author provided in the request body
    if "author_id" in update_data and update_data["author_id"] is not None:
        if db_book.author_id != update_data["author_id"]:
            raise HTTPException(
                status_code=403,  # 403 Forbidden is ideal for relationship mismatches
                detail=f"Unauthorized: Book {numeric_id} does not belong to Author {update_data['author_id']}"
            )

    # Validation: If updating the title, prevent blank strings
    if "title" in update_data:
        if not update_data["title"] or not update_data["title"].strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        update_data["title"] = update_data["title"].strip()

    # Apply updates dynamically
    for key, value in update_data.items():
        setattr(db_book, key, value)

    db.commit()
    db.refresh(db_book)
    return db_book

#
def get_author_by_book_id(db: Session, book_id: str):
    # 1. Validate URL ID format
    try:
        numeric_id = int(book_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Book ID must be a valid number")

    # 2. Find the book and verify it exists
    db_book = db.query(models.Book).filter(models.Book.id == numeric_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")

    # 3. Find the author associated with this book
    author = db.query(models.Author).filter(models.Author.id == db_book.author_id).first()
    
    # Safety check: in case a book somehow has an invalid author_id or null
    if not author:
        raise HTTPException(status_code=404, detail="Author not found for this book")

    return author

#
def search_books(db: Session, filters: schemas.BookSearchRequest):
    # 1. Start a base query pointing to the Books table
    query = db.query(models.Book)

    # 2. Apply filtering
    if filters.title:
        clean_title = filters.title.strip().lower()
        if clean_title:
            query = query.filter(func.lower(models.Book.title).like(f"%{clean_title}%"))

    # 3. CRITICAL: Get total match count BEFORE applying offset/limit
    total_matches = query.count()

    # 4. Apply pagination limits to retrieve records slice
    paginated_results = query.offset(filters.offset).limit(filters.limit).all()
    
    # 5. Return the expected dictionary structure
    return {
        "total": total_matches,
        "results": paginated_results
    }
    