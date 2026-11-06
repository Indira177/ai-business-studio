import os
import re
import uuid
from datetime import datetime
from pathlib import Path

import pymupdf
from sqlalchemy.orm import Session

from app.models.invoice import Invoice

UPLOAD_DIR = "uploads"


def find_value(patterns, text):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            value = match.group(1).strip()
            if value:
                return value
    return None


def extract_invoice_number(text):
    return find_value([
        r"\bInvoice\s*(?:Number|No\.?|#)\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-\/]*)",
        r"\bInv\.?\s*(?:No\.?|#)\s*[:\-]?\s*([A-Z0-9][A-Z0-9\-\/]*)",
    ], text)


def extract_date(patterns, text):
    value = find_value(patterns, text)
    if not value:
        return None

    for fmt in (
        "%m/%d/%Y", "%d/%m/%Y", "%Y-%m-%d",
        "%d-%m-%Y", "%m-%d-%Y", "%d %b %Y",
        "%d %B %Y", "%b %d, %Y", "%B %d, %Y",
    ):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            pass

    return None


def extract_invoice_date(text):
    return extract_date([
        r"\bInvoice\s+Date\s*[:\-]?\s*(\d{1,4}[/-]\d{1,2}[/-]\d{1,4})",
        r"\bDate\s*[:\-]?\s*(\d{1,4}[/-]\d{1,2}[/-]\d{1,4})",
        r"\bDate\s*[:\-]?\s*(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"\bDate\s*[:\-]?\s*([A-Za-z]{3,9}\s+\d{1,2},?\s+\d{4})",
    ], text)


def extract_due_date(text):
    return extract_date([
        r"\bDue\s+Date\s*[:\-]?\s*(\d{1,4}[/-]\d{1,2}[/-]\d{1,4})",
        r"\bDue\s+Date\s*[:\-]?\s*(\d{1,2}\s+[A-Za-z]{3,9}\s+\d{4})",
        r"\bDue\s+Date\s*[:\-]?\s*([A-Za-z]{3,9}\s+\d{1,2},?\s+\d{4})",
    ], text)


def extract_vendor_name(text):
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    for line in lines[:8]:
        if re.search(
            r"invoice|bill\s+to|ship\s+to|invoiced\s+to|"
            r"date|tax\s+invoice|gst|www\.|@",
            line,
            re.IGNORECASE,
        ):
            continue
        if len(line) >= 2:
            return line[:255]

    return None


def extract_customer_name(text):
    return find_value([
        r"\bInvoiced\s+To\s*[:\-]?\s*\n?\s*([^\n]+)",
        r"\bBill\s+To\s*[:\-]?\s*\n?\s*([^\n]+)",
        r"\bBilled\s+To\s*[:\-]?\s*\n?\s*([^\n]+)",
        r"\bCustomer\s+Name\s*[:\-]?\s*([^\n]+)",
    ], text)


def extract_gst_number(text):
    match = re.search(
        r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z\d]Z[A-Z\d]\b",
        text.upper(),
    )
    return match.group(0) if match else None


def extract_amount_for_labels(text, labels):
    for label in labels:
        pattern = (
            rf"(?im)^\s*{label}\s*[:\-]?\s*"
            rf"(?:USD|INR|Rs\.?|â‚¹|\$)?\s*"
            rf"(-?\d[\d,]*(?:\.\d{{1,2}})?)\s*$"
        )
        match = re.search(pattern, text)
        if match:
            try:
                return float(match.group(1).replace(",", ""))
            except ValueError:
                pass
    return None


def extract_invoice_amounts(text):
    subtotal = extract_amount_for_labels(
        text, [r"Sub\s*total", r"Subtotal", r"Taxable\s+Amount"]
    )

    tax_amount = extract_amount_for_labels(
        text,
        [
            r"GST\s*\(\s*\d+(?:\.\d+)?%\s*\)",
            r"Total\s+Tax",
            r"Tax\s+Amount",
            r"GST",
            r"VAT",
        ],
    )

    total_amount = extract_amount_for_labels(
        text, [
            r"Grand\s+Total", r"Invoice\s+Total",
            r"Total\s+Due", r"Amount\s+Due", r"Total",
        ]
    )

    if subtotal is None or total_amount is None:
        amounts = re.findall(
            r"(?i)(?:USD|INR|Rs\.?|â‚¹|\$)\s*(-?\d[\d,]*(?:\.\d{1,2})?)"
            r"|(-?\d[\d,]*\.\d{2})\s*(?:USD|INR|Rs\.?|â‚¹|\$)",
            text,
        )
        numbers = []
        for first, second in amounts:
            value = first or second
            try:
                numbers.append(float(value.replace(",", "")))
            except ValueError:
                pass

        if total_amount is None and numbers:
            total_amount = max(numbers)

        if subtotal is None and numbers:
            subtotal = max(numbers)

    return subtotal, tax_amount, total_amount


def process_invoice(file_name: str, file_content: bytes, db: Session):
    if not file_content:
        raise ValueError("The selected PDF file is empty.")

    original_name = Path(file_name).name
    upload_dir = Path(UPLOAD_DIR)
    upload_dir.mkdir(parents=True, exist_ok=True)

    unique_name = f"{uuid.uuid4().hex}_{original_name}"
    file_path = str(upload_dir / unique_name)

    try:
        with pymupdf.open(stream=file_content, filetype="pdf") as document:
            if document.page_count == 0:
                raise ValueError("The PDF has no pages.")
            extracted_text = "\n".join(
                page.get_text() for page in document
            ).strip()
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError(
            "Unable to read this PDF. Please select a valid PDF file."
        ) from exc

    if not extracted_text:
        raise ValueError(
            "No readable text was found. This may be a scanned PDF."
        )

    invoice_number = extract_invoice_number(extracted_text)
    invoice_date = extract_invoice_date(extracted_text)
    due_date = extract_due_date(extracted_text)
    vendor_name = extract_vendor_name(extracted_text)
    customer_name = extract_customer_name(extracted_text)
    gst_number = extract_gst_number(extracted_text)
    subtotal, tax_amount, total_amount = extract_invoice_amounts(
        extracted_text
    )

    if not any([
        invoice_number, invoice_date, customer_name,
        gst_number, total_amount is not None,
    ]):
        raise ValueError(
            "Invoice details could not be recognized. "
            "No invoice was saved. The PDF may use an unsupported format."
        )

    with open(file_path, "wb") as saved_file:
        saved_file.write(file_content)

    try:
        invoice = Invoice(
            invoice_number=invoice_number,
            vendor_name=vendor_name,
            customer_name=customer_name,
            invoice_date=invoice_date,
            due_date=due_date,
            gst_number=gst_number,
            subtotal=subtotal,
            tax_amount=tax_amount,
            total_amount=total_amount,
            file_name=original_name,
            file_path=file_path,
        )
        db.add(invoice)
        db.commit()
        db.refresh(invoice)
    except Exception:
        db.rollback()
        if os.path.exists(file_path):
            os.remove(file_path)
        raise

    return {
        "invoice_id": invoice.id,
        "file_name": invoice.file_name,
        "file_path": invoice.file_path,
        "invoice_number": invoice.invoice_number,
        "vendor_name": invoice.vendor_name,
        "customer_name": invoice.customer_name,
        "invoice_date": str(invoice.invoice_date) if invoice.invoice_date else None,
        "due_date": str(invoice.due_date) if invoice.due_date else None,
        "gst_number": invoice.gst_number,
        "subtotal": float(invoice.subtotal) if invoice.subtotal is not None else None,
        "tax_amount": float(invoice.tax_amount) if invoice.tax_amount is not None else None,
        "total_amount": float(invoice.total_amount) if invoice.total_amount is not None else None,
        "extracted_text": extracted_text,
    }
