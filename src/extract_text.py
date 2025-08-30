import os

def extract_text_from_pdf(pdf_path):
    import pdfplumber

    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = "./data/outputs"
    os.makedirs(output_folder, exist_ok=True)

    text_output_path = os.path.join(output_folder, f"{filename}.txt")
    all_text = []

    print(f"\n📄 Extracting text from: {pdf_path}")

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    all_text.append(f"\n--- Page {page_num} ---\n{text}")
        with open(text_output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(all_text))
        print(f"✅ Saved full text → {text_output_path}")
    except Exception as e:
        print(f"❌ Error while extracting text: {e}")
