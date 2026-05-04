from typing import Optional
from sqlalchemy import ForeignKeyConstraint, Integer, PrimaryKeyConstraint, Column, Integer, String, ForeignKey
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from app.database import Base

class Book(Base):
    __tablename__ = "books"
    __table_args__ = (
    ForeignKeyConstraint(['author_id'], ['authors.id'], ondelete='CASCADE', name='fk_author'),
    PrimaryKeyConstraint('id', name='books_pkey')
    )
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Integer)
    author_id = Column(Integer, ForeignKey("authors.id"))
    pages: Mapped[Optional[int]] = mapped_column(Integer)
    owner = relationship("Author", back_populates="books")