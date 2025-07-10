import fitz  # PyMuPDF

def check_pdf_content(pdf_path):
    print(f"\n=== Checking {pdf_path} ===")
    try:
        doc = fitz.open(pdf_path)
        print(f"Number of pages: {len(doc)}")
        
        total_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            print(f"Page {page_num + 1} text length: {len(page_text)} characters")
            if page_text.strip():
                print(f"Page {page_num + 1} first 200 chars: {repr(page_text[:200])}")
            else:
                print(f"Page {page_num + 1}: NO TEXT FOUND (likely image-based)")
            total_text += page_text
        
        doc.close()
        print(f"Total extracted text length: {len(total_text)} characters")
        
        if len(total_text.strip()) < 50:
            print("⚠️  PDF appears to be image-based or has very little extractable text")
            return False
        else:
            print("✅ PDF has extractable text content")
            return True
            
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return False

# Check all three PDFs
pdf_files = [
    'sample_docs/english solar.pdf',
    'sample_docs/malayalam solar.pdf', 
    'sample_docs/french solar.pdf'
]

for pdf_file in pdf_files:
    has_text = check_pdf_content(pdf_file)
