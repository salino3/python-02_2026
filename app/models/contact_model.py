import enum
from sqlalchemy import Column, Integer, String, Enum, CheckConstraint
from app.database import Base

class ContactPreference(str, enum.Enum):
    EMAIL = "email"
    WHATSAPP = "whatsapp"
    BOTH = "both"

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=False)  
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    tel = Column(String, nullable=True)
    preferred_contact = Column(
        Enum(ContactPreference, name="contact_preference_enum"),  
        default=ContactPreference.EMAIL, 
        nullable=False
    )

    # 🛡️ Update Python constraints to match the smart database security guard perfectly!
    __table_args__ = (
        CheckConstraint(
            "(preferred_contact = 'email' AND email IS NOT NULL) OR "
            "(preferred_contact = 'whatsapp' AND tel IS NOT NULL) OR "
            "(preferred_contact = 'both' AND email IS NOT NULL AND tel IS NOT NULL)",
            name="validate_preferred_contact_data"
        ),
    )