# app/models.py
import enum
from sqlalchemy import Column, Integer, String, Enum, CheckConstraint
from app.database import Base

class ContactPreference(str, enum.Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    BOTH = "both"

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    tel = Column(String, nullable=True)
    preferred_contact = Column(
        Enum(ContactPreference), 
        default=ContactPreference.EMAIL, 
        nullable=False
    )

    # 🌟 SQL Safety Guard: Ensures database rejects rows missing BOTH communication lines
    __table_args__ = (
        CheckConstraint(
            "(email IS NOT NULL) OR (tel IS NOT NULL)", 
            name="at_least_one_contact_method"
        ),
    )