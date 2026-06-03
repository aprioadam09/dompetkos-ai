import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.llm.extractor import extract_transactions
from src.validation.validator import validate_extraction_result


TEST_INPUTS = [
    "Hari ini makan ayam geprek 18 ribu, kopi 12 ribu, dan laundry 25 ribu.",
    "Hari ini dapat uang saku 500 ribu dari orang tua.",
    "Bayar kos bulan ini 1 juta 30 ribu.",
    "Beli paket data Telkomsel 35 ribu.",
    "Beli Netflix 25 ribu.",
    "Kemarin beli kopi dan makan ayam geprek.",
]


def run_single_test(user_input: str):
    print("=" * 80)
    print("Input:")
    print(user_input)

    try:
        result = extract_transactions(user_input)
        validation = validate_extraction_result(result)

        print("\nExtraction result:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        print("\nValidation result:")
        print(json.dumps(validation, indent=2, ensure_ascii=False))

    except Exception as error:
        print("\nTest failed:")
        print(type(error).__name__)
        print(error)


def main():
    print("Pilih test input:")
    for index, test_input in enumerate(TEST_INPUTS, start=1):
        print(f"{index}. {test_input}")

    selected = input("\nMasukkan nomor test: ").strip()

    if not selected.isdigit():
        print("Input harus berupa angka.")
        return

    selected_index = int(selected)

    if selected_index < 1 or selected_index > len(TEST_INPUTS):
        print("Nomor test tidak valid.")
        return

    user_input = TEST_INPUTS[selected_index - 1]
    run_single_test(user_input)


if __name__ == "__main__":
    main()