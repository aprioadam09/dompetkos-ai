from collections import defaultdict


def filter_transactions_by_month(transactions: list[dict], month: str) -> list[dict]:
    return [
        transaction
        for transaction in transactions
        if transaction["date"].startswith(month)
    ]


def calculate_monthly_summary(transactions: list[dict], month: str) -> dict:
    monthly_transactions = filter_transactions_by_month(transactions, month)

    total_income = 0
    total_expense = 0

    for transaction in monthly_transactions:
        amount = transaction["amount"]

        if transaction["type"] == "income":
            total_income += amount
        elif transaction["type"] == "expense":
            total_expense += amount

    cash_flow = total_income - total_expense

    return {
        "month": month,
        "total_income": total_income,
        "total_expense": total_expense,
        "cash_flow": cash_flow,
        "transaction_count": len(monthly_transactions),
    }


def calculate_expense_by_category(transactions: list[dict], month: str) -> list[dict]:
    monthly_transactions = filter_transactions_by_month(transactions, month)

    category_totals = defaultdict(int)

    for transaction in monthly_transactions:
        if transaction["type"] == "expense":
            category = transaction["category"]
            category_totals[category] += transaction["amount"]

    result = [
        {
            "category": category,
            "total_expense": total,
        }
        for category, total in category_totals.items()
    ]

    return sorted(result, key=lambda item: item["total_expense"], reverse=True)


def get_top_spending_category(transactions: list[dict], month: str) -> dict | None:
    expense_by_category = calculate_expense_by_category(transactions, month)

    if not expense_by_category:
        return None

    return expense_by_category[0]