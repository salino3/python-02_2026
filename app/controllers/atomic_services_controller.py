from fastapi import HTTPException
import os
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app import models, schemas   
from app.utils import send_whatsapp_book_notification, send_email_book_notification

 
client_phone_number: str = os.getenv("PHONE_NUMBER_CLIENT")

def create_author_and_book_atomic(db: Session, author_data: schemas.AuthorCreate, book_data: schemas.BookCreate   ):
                                  
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
                    constraint="unique_author_name",   # Matches the constraint ran directly in DB
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

            # 🌟 Forces SQLAlchemy to fetch the generated Book ID 
            # from PostgreSQL immediately without breaking the transaction state
            db.flush() 

            new_book_id = db_book.id
            # 1️⃣ Pull ALL contact rows from your database table
            active_contacts = db.query(models.Contact).all()
            print(f"📊 Total rows found in database: {len(active_contacts)}")

            # 2️⃣ Start processing the rows one by one
            for contact in active_contacts:

                # Safely convert the database preference value to a lowercase string
                preference = contact.preferred_contact.value if hasattr(contact.preferred_contact, 'value') else contact.preferred_contact
                preference = str(preference).lower()

                print(f"👤 Processing row -> Name: {contact.name} | Preference: {preference} | Phone: {contact.tel}")

                # 📱 UTILITY 1: WHATSAPP EXECUTION GUARD
                # Fires if preference is "whatsapp" OR "both"
                if preference in ["whatsapp", "both"] and contact.tel:
                    try:
                        print(f"   ➔ 📱 Executing WhatsApp utility function for {contact.name}")
                        send_whatsapp_book_notification(
                            to_phone=contact.tel, 
                            book_id=new_book_id,
                            book_title=book_data.title, 
                            author_name=author_data.name
                        )
                    except Exception as whatsapp_error:
                        print(f"   ⚠️ WhatsApp utility crashed for {contact.name}: {whatsapp_error}")

                # 📧 UTILITY 2: EMAIL EXECUTION GUARD
                # Fires if preference is "email" OR "both"
                if preference in ["email", "both"] and contact.email:
                    try:
                        print(f"   ➔ 📧 Executing Email utility function for {contact.name}")
                        send_email_book_notification(
                            destination_email=contact.email,
                            recipient_name=contact.name,
                            book_id=new_book_id,
                            book_title=book_data.title,
                            author_name=author_data.name
                        )
                    except Exception as email_error:
                        print(f"   ⚠️ Email utility crashed for {contact.name}: {email_error}")

                print(f"✨ Finished processing all applicable utilities for {contact.name}.\n")
 

 
            return {
                "success": True, 
                "message": f"Successfully processed notifications across all {len(active_contacts)} database contact rows!"
            }

    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Database atomic write aborted: {str(error)}")