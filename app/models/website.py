from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from app.database.database import Base


class Website(Base):

    __tablename__ = "websites"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    business_name = Column(
        String(255),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    pages = Column(
        Text,
        nullable=True
    )

    style = Column(
        String(100),
        nullable=True
    )

    folder_path = Column(
        String(500),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )