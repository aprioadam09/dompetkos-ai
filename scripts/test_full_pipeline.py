import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.database.db import init_db
from src.database.queries import insert_transactions, get_all_transactions
from src.llm.extractor import extract_transactions
from src.validation.validator import validate_extraction_result


def main():
    init_db()

    user_input = "Hari ini makan ayam geprek 18 ribu, kopi 12 ribu, dan laundry 25 ribu."

    extraction_result = extract_transactions(user_input)
    validation_result = validate_extraction_result(extraction_result)

    print("Input:")
    print(user_input)

    print("\nExtraction result:")
    print(json.dumps(extraction_result, indent=2, ensure_ascii=False))

    print("\nValidation result:")
    print(json.dumps(validation_result, indent=2, ensure_ascii=False))

    if not validation_result["is_valid"]:
        print("\nStatus:")
        print("Data tidak valid. Transaksi tidak disimpan.")
        return

    if validation_result["needs_clarification"]:
        print("\nStatus:")
        print("Butuh klarifikasi. Transaksi tidak disimpan.")
        print(extraction_result.get("clarification_question"))
        return

    transactions = extraction_result["transactions"]
    inserted_ids = insert_transactions(transactions)

    print("\nStatus:")
    print("Transaksi berhasil disimpan.")

    print("\nInserted IDs:")
    print(inserted_ids)

    print("\nTransaction history:")
    all_transactions = get_all_transactions()
    print(json.dumps(all_transactions, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()