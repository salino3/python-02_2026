from fastapi import FastAPI
from app.database import engine
from app import models
from app.routers import authors, books

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")

# Include routers
app.include_router(authors.router)
app.include_router(books.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System API"}