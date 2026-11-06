from datetime import datetime

from sqlalchemy import Column, Integer, String, Date, Numeric, DateTime

from app.database.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    invoice_number = Column(String(100), nullable=True)
    vendor_name = Column(String(255), nullable=True)
    customer_name = Column(String(255), nullable=True)

    invoice_date = Column(Date, nullable=True)
    due_date = Column(Date, nullable=True)

    gst_number = Column(String(100), nullable=True)

    subtotal = Column(Numeric(12, 2), nullable=True)
    tax_amount = Column(Numeric(12, 2), nullable=True)
    total_amount = Column(Numeric(12, 2), nullable=True)

    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )