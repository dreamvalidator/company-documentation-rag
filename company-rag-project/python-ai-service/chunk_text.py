
from pypdf import PdfReader

pdf_path = "documents/hr-policy.pdf"

reader = PdfReader(pdf_path)

# Extract text from all pages
full_text = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        full_text += text + "\n"

# Split text into chunks
chunk_size = 500
overlap = 50

chunks = []

start = 0

while start < len(full_text):
    end = start + chunk_size

    chunk = full_text[start:end]

    chunks.append(chunk)

    start += chunk_size - overlap

# Display results
print("Total Characters:", len(full_text))
print("Total Chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"\n--- Chunk {i} ---")
    print(chunk)

print("\n========== FIRST 2 CHUNKS ==========")

for i, chunk in enumerate(chunks[:2], start=1):
    print(f"\n--- Chunk {i} ---")
    print(chunk)