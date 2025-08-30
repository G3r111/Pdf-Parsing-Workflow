import os
import camelot
import pandas as pd

def camelot_table_extractor(pdf_path):
    filename = os.path.splitext(os.path.basename(pdf_path))[0]
    output_folder = "./data/outputs"
    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, f"{filename}_camelot_tables.csv")

    print(f"\n📊 Extracting tables using Camelot from: {pdf_path}")

    try:
        # Extract tables using both stream and lattice modes
        tables_stream = camelot.read_pdf(pdf_path, pages="all", flavor="stream")
        tables_lattice = camelot.read_pdf(pdf_path, pages="all", flavor="lattice")

        # Merge both TableLists safely
        all_tables = list(tables_stream) + list(tables_lattice)
        print(f"🔍 Found {len(all_tables)} tables")

        combined_df = pd.DataFrame()

        for i, table in enumerate(all_tables):
            df = table.df
            df.insert(0, "Table_ID", f"Table_{i+1}")
            df.insert(1, "Page", table.page)
            combined_df = pd.concat([combined_df, df], ignore_index=True)

        combined_df.to_csv(output_path, index=False)
        print(f"✅ Saved merged tables → {output_path}")

    except Exception as e:
        print(f"❌ Error while extracting tables: {e}")
