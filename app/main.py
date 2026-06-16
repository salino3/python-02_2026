from fastapi import FastAPI
from app.database import engine
from fastapi.middleware.cors import CORSMiddleware
import os
from app import models
from app.routers import author_router, book_router, atomic_services_router

# .\venv\Scripts\Activate.ps1
# uvicorn app.main:app --reload  
# Example   
# python -m sqlacodegen  postgresql://USER_NAME:PASSWORD_VALUE@localhost:PORT_VALUE/DATABASE_NAME > temp_models.py

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System")

FRONT_PORT = os.getenv("FRONT_PORT")

origins = [
    FRONT_PORT,
 ]

#  Add the middleware to your FastAPI application instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allows requests from your specific frontend URL
    allow_credentials=True,           # Allows cookies/authentication headers if needed later
    allow_methods=["*"],              # Allows all standard HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],              # Allows all custom/standard HTTP headers
)

# Include routers
app.include_router(author_router.router)
app.include_router(book_router.router)
app.include_router(atomic_services_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System API"}