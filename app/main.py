from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import author_router, book_router

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")

# Include routers
app.include_router(author_router.router)
app.include_router(book_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System API"}