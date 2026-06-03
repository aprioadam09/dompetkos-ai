import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))

from src.database.db import init_db
from src.database.queries import (
    insert_transactions,
    get_all_transactions,
    set_monthly_budget,
    get_monthly_budget,
)


def main():
    init_db()

    sample_transactions = [
        {
            "date": "2026-06-02",
            "description": "ayam geprek",
            "amount": 18000,
            "category": "Makanan",
            "type": "expense",
        },
        {
            "date": "2026-06-02",
            "description": "kopi",
            "amount": 12000,
            "category": "Minuman",
            "type": "expense",
        },
    ]

    inserted_ids = insert_transactions(sample_transactions)

    set_monthly_budget("2026-06", 1500000)
    budget = get_monthly_budget("2026-06")
    transactions = get_all_transactions()

    print("Inserted transaction IDs:")
    print(inserted_ids)

    print("\nMonthly budget:")
    print(json.dumps(budget, indent=2, ensure_ascii=False))

    print("\nAll transactions:")
    print(json.dumps(transactions, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()