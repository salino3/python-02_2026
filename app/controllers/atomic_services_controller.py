from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app import models, schemas   

 


def create_author_and_book_atomic(db: Session, author_data: schemas.AuthorCreate, book_data: schemas.BookCreate):
    # 1️⃣ Core Payload Validation
    if not author_data.name:
        raise HTTPException(status_code=400, detail="Author name is required")
    if not book_data.title:
        raise HTTPException(status_code=400, detail="Book title is required")

    try:
        # 2️⃣ Execute everything inside a shared, atomic transaction block
        with db.begin():
            
            # Formulate the PostgreSQL-specific native UPSERT statement
            author_upsert_stmt = (
                insert(models.Author)
                .values(name=author_data.name, bio=author_data.bio)
                .on_conflict_do_update(
                    constraint="unique_author_name",   # Matches the constraint you ran directly in your DB!
                    set_={"bio": insert(models.Author).excluded.bio}  # Overwrites the old bio with the fresh search bio
                )
                .returning(models.Author.id)  # Forces PostgreSQL to yield the ID back to Python
            )
            
            # Execute the query and extract the single primary key ID scalar value
            result = db.execute(author_upsert_stmt)
            author_id = result.scalar_one()

            # 3️⃣ Build the new book using the captured author_id (whether it was created or updated)
            db_book = models.Book(
                title=book_data.title,
                price=book_data.price,
                pages=book_data.pages,
                author_id=author_id  # Relational foreign key link
            )
            db.add(db_book)
            
            # 🌟 FIX: Return INSIDE the block so everything resolves while the transaction is open and secure!
            return {
                "success": True, 
                "message": f"Successfully mapped book '{book_data.title}' to author ID {author_id}."
            }

    except Exception as e:
        # 🛡️ If the book insertion fails, the entire block—including a new author or updated bio—is completely undone.
        raise HTTPException(status_code=500, detail=f"Database atomic write aborted: {str(e)}")