import os
from extract_text import extract_text_from_pdf
from extract_tables import camelot_table_extractor as extract_tables_from_pdf

INPUT_FOLDER = "./data/input_pdfs"

def list_pdfs():
    files = [f for f in os.listdir(INPUT_FOLDER) if f.endswith(".pdf")]
    print("\nAvailable PDFs:")
    for i, f in enumerate(files, start=1):
        print(f"{i}. {f}")
    return files

def main():
    files = list_pdfs()
    choice = input("\nEnter the number of the file to process: ")
    try:
        index = int(choice) - 1
        filename = files[index]
        pdf_path = os.path.join(INPUT_FOLDER, filename)

        mode = input("Run (T)ext extraction, (C)SV table extraction, or (B)oth? ").lower()
        if mode == "t":
            extract_text_from_pdf(pdf_path)
        elif mode == "c":
            extract_tables_from_pdf(pdf_path)
        elif mode == "b":
            extract_text_from_pdf(pdf_path)
            extract_tables_from_pdf(pdf_path)
        else:
            print("Invalid mode selected.")

    except (IndexError, ValueError):
        print("Invalid selection. Please try again.")

if __name__ == "__main__":
    main()
