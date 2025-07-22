from utils.pdf_utils import extract_text_from_pdf

# Test all three PDFs
pdf_files = {
    'English': 'sample_docs/english solar.pdf',
    'Malayalam': 'sample_docs/malayalam solar.pdf',
    'French': 'sample_docs/french solar.pdf'
}

print("Testing PDF extraction:")
print("=" * 50)

for lang, file_path in pdf_files.items():
    print(f"\n{lang} PDF:")
    text = extract_text_from_pdf(file_path)
    print(f"  Length: {len(text)} characters")
    print(f"  Preview: {text[:150]}...")
    print("-" * 30)
