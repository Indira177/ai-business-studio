from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.invoice import Invoice
from app.services.invoice_service import process_invoice


router = APIRouter(
    prefix="/api/invoices",
    tags=["Invoices"]
)


@router.post("/upload")
async def upload_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is missing"
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported"
        )

    try:
        file_content = await file.read()

        result = process_invoice(
            file_name=file.filename,
            file_content=file_content,
            db=db
        )

        return {
            "status": "success",
            "message": "Invoice uploaded successfully",
            "data": result
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Invoice processing failed: {str(e)}"
        )
@router.get("")
def get_all_invoices(
    db: Session = Depends(get_db)
):
    invoices = (
        db.query(Invoice)
        .order_by(Invoice.id.desc())
        .all()
    )

    return {
        "status": "success",
        "count": len(invoices),
        "data": [
            {
                "invoice_id": invoice.id,
                "invoice_number": invoice.invoice_number,
                "vendor_name": invoice.vendor_name,
                "customer_name": invoice.customer_name,
                "invoice_date": (
                    str(invoice.invoice_date)
                    if invoice.invoice_date
                    else None
                ),
                "due_date": (
                    str(invoice.due_date)
                    if invoice.due_date
                    else None
                ),
                "gst_number": invoice.gst_number,
                "subtotal": (
                    float(invoice.subtotal)
                    if invoice.subtotal is not None
                    else None
                ),
                "tax_amount": (
                    float(invoice.tax_amount)
                    if invoice.tax_amount is not None
                    else None
                ),
                "total_amount": (
                    float(invoice.total_amount)
                    if invoice.total_amount is not None
                    else None
                ),
                "file_name": invoice.file_name,
                "created_at": (
                    str(invoice.created_at)
                    if invoice.created_at
                    else None
                )
            }
            for invoice in invoices
        ]
    }

@router.get("/{invoice_id}")
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db)
):
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id)
        .first()
    )

    if not invoice:
        raise HTTPException(
            status_code=404,
            detail="Invoice not found"
        )

    return {
        "status": "success",
        "data": {
            "invoice_id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "vendor_name": invoice.vendor_name,
            "customer_name": invoice.customer_name,

            "invoice_date": (
                str(invoice.invoice_date)
                if invoice.invoice_date
                else None
            ),

            "due_date": (
                str(invoice.due_date)
                if invoice.due_date
                else None
            ),

            "gst_number": invoice.gst_number,

            "subtotal": (
                float(invoice.subtotal)
                if invoice.subtotal is not None
                else None
            ),

            "tax_amount": (
                float(invoice.tax_amount)
                if invoice.tax_amount is not None
                else None
            ),

            "total_amount": (
                float(invoice.total_amount)
                if invoice.total_amount is not None
                else None
            ),

            "file_name": invoice.file_name,
            "file_path": invoice.file_path,

            "created_at": (
                str(invoice.created_at)
                if invoice.created_at
                else None
            )
        }
    }