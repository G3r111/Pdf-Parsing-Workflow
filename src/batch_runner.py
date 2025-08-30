import os
import json
import pandas as pd

GROUND_TRUTH_PATH = "./data/ground_truth/ground_truth.csv"
OUTPUT_FOLDER = "./data/outputs"

def load_ground_truth():
    return pd.read_csv(GROUND_TRUTH_PATH)

def load_parser_output(filename):
    json_path = os.path.join(OUTPUT_FOLDER, filename.replace(".pdf", ".json"))
    if os.path.exists(json_path):
        with open(json_path) as f:
            return json.load(f)
    return None

def compare_fields(truth_row, parsed_data):
    mismatches = {}
    for field in ["total", "date"]:
        truth_value = str(truth_row[field])
        parsed_value = str(parsed_data.get(field, ""))
        if truth_value != parsed_value:
            mismatches[field] = {"truth": truth_value, "parsed": parsed_value}
    return mismatches

def run_accuracy_check():
    truth_df = load_ground_truth()
    total_files = len(truth_df)
    correct = 0
    mismatch_log = []

    for _, row in truth_df.iterrows():
        filename = row["filename"]
        parsed = load_parser_output(filename)
        if parsed:
            mismatches = compare_fields(row, parsed)
            if not mismatches:
                correct += 1
            else:
                mismatch_log.append({"filename": filename, "errors": mismatches})
        else:
            mismatch_log.append({"filename": filename, "errors": "No parser output found"})

    accuracy = correct / total_files * 100
    print(f"Accuracy: {accuracy:.2f}%")
    print("Mismatches:")
    for entry in mismatch_log:
        print(entry)

if __name__ == "__main__":
    run_accuracy_check()
