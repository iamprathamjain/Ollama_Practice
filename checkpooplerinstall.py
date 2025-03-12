import pdf2image
doc_path = r"./data/notice_eng_je_01102020.pdf"
try:
    pdf2image.pdfinfo_from_path(doc_path)
    print("✅ Poppler is installed!")
except pdf2image.exceptions.PDFInfoNotInstalledError:
    print("❌ Poppler is NOT installed or not in PATH!")
