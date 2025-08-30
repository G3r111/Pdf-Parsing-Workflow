import os
import json
import re
from datetime import datetime
import pdfplumber

def esg_parser(pdf_path):
    esg_codes = {
        "305-1": "Direct (Scope 1) GHG emissions",
        "305-2": "Energy indirect (Scope 2) GHG emissions",
        "305-3": "Other indirect (Scope 3) GHG emissions",
        "306-4": "Waste diverted from disposal",
        "303-4": "Water discharge",
        "303-5": "Water consumption",
        "401-3": "Parental leave",
        "405-1": "Diversity of governance bodies and employees",
        "408-1": "Child labor violations",
        "409-1": "Forced labor violations"
    }

    results = {
        "filename": os.path.basename(pdf_path),
        "timestamp": datetime.now().isoformat(),
        "metrics": {},
        "log": []
    }

    print(f"\n📄 Starting ESG parsing for: {pdf_path}")

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    results["log"].append(f"Page {page_num}: Text extracted.")
                    for code, label in esg_codes.items():
                        pattern = rf"{code}.*?([\d,.]+)\s*([a-zA-Z%/()]+)?"
                        match = re.search(pattern, text)
                        if match:
                            try:
                                value = float(match.group(1).replace(",", ""))
                            except ValueError:
                                value = match.group(1)
                            unit = match.group(2) if match.group(2) else "unknown"
                            results["metrics"][code] = {
                                "label": label,
                                "value": value,
                                "unit": unit,
                                "page": page_num
                            }
                            results["log"].append(f"✅ Found {code} in text on page {page_num}: {value} {unit}")
                        else:
                            results["log"].append(f"🔍 {code} not found in text on page {page_num}")
                else:
                    results["log"].append(f"Page {page_num}: No text extracted.")

                # Try table extraction
                tables = page.extract_tables()
                if tables:
                    for table in tables:
                        for row in table:
                            if not row:
                                continue
                            for code, label in esg_codes.items():
                                if any(code in str(cell) for cell in row):
                                    for cell in row:
                                        match = re.search(r"([\d,.]+)\s*([a-zA-Z%/()]+)?", str(cell))
                                        if match:
                                            try:
                                                value = float(match.group(1).replace(",", ""))
                                            except ValueError:
                                                value = match.group(1)
                                            unit = match.group(2) if match.group(2) else "unknown"
                                            results["metrics"][code] = {
                                                "label": label,
                                                "value": value,
                                                "unit": unit,
                                                "page": page_num
                                            }
                                            results["log"].append(f"✅ Found {code} in table on page {page_num}: {value} {unit}")
                                            break

    except Exception as e:
        error_msg = f"❌ Error while parsing {pdf_path}: {str(e)}"
        print(error_msg)
        results["error"] = error_msg
        results["log"].append(error_msg)

    print(f"✅ Finished parsing: {pdf_path}")
    return results

# Optional: Run directly on one file
if __name__ == "__main__":
    test_pdf = "./data/input_pdfs/CLP_Sustainability_Report_2023_en-1.pdf"  # Replace with your actual file name
    result = esg_parser(test_pdf)

    # Save output
    output_path = "./data/outputs/CLP_Sustainability_Report_2023_en-1.json"
    with open(output_path, "w") as f:
        json.dump(result, f, indent=2)

    # Print summary
    print("\n📊 Extracted Metrics:")
    for code, metric in result["metrics"].items():
        print(f"{code}: {metric['value']} {metric['unit']} (Page {metric['page']})")

    if "error" in result:
        print("\n⚠️ Error:", result["error"])
