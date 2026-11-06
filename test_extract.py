import pymupdf

pdf_path = r"uploads\invoices.pdf"

document = pymupdf.open(pdf_path)

text = ""

for page in document:
    text += page.get_text()

document.close()

print("=" * 60)
print("EXTRACTED PDF TEXT")
print("=" * 60)
print(repr(text))
print("=" * 60)

print("\nReadable text:")
print(text)