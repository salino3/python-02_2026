from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import author_router, book_router
# uvicorn app.main:app --reload  
# Example   
# python -m sqlacodegen  postgresql://USER_NAME:PASSWORD_VALUE@localhost:PORT_VALUE/DATABASE_NAME > temp_models.py

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")

# Include routers
app.include_router(author_router.router)
app.include_router(book_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System API"}