import os
import fitz
import numpy as np

DATA_PATH = "data/Textbooks"
OUTPUT_FILE = "vector_store/chunks.npy"


def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text()

    return text


def get_all_pdfs(folder):
    pdf_files = []

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))

    return pdf_files


def chunk_text(text, chunk_size=500, overlap=100):

    chunks = []
    start = 0

    while start < len(text):

        chunk = text[start:start + chunk_size]
        chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def main():

    pdf_files = get_all_pdfs(DATA_PATH)

    print("Found PDFs:", len(pdf_files))

    all_chunks = []

    for pdf in pdf_files:

        text = extract_text(pdf)

        chunks = chunk_text(text)

        print(f"{pdf} → {len(chunks)} chunks")

        subject = pdf.lower()

        if "science" in subject:
            subject_name = "science"
        elif "math" in subject:
            subject_name = "math"
        elif "social" in subject:
            subject_name = "social science"
        else:
            subject_name = "general"

        for chunk in chunks:
            all_chunks.append({
               "text": chunk,
               "subject": subject_name
            })

    np.save(OUTPUT_FILE, np.array(all_chunks))

    print()
    print("Total chunks created:", len(all_chunks))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()