import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.llm.extractor import extract_transactions


def main():
    user_input = "Hari ini makan ayam geprek 18 ribu, kopi 12 ribu, dan laundry 25 ribu."

    result = extract_transactions(user_input)

    print("Input:")
    print(user_input)

    print("\nExtraction result:")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()