from datetime import datetime
from src.categories import CATEGORIES, TRANSACTION_TYPES


VALID_STATUSES = [
    "success",
    "needs_clarification",
    "no_transaction",
]


REQUIRED_TRANSACTION_FIELDS = [
    "date",
    "description",
    "amount",
    "category",
    "type",
]


def is_valid_date(date_text: str) -> bool:
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_transaction(transaction: dict, index: int) -> list[str]:
    errors = []

    for field in REQUIRED_TRANSACTION_FIELDS:
        if field not in transaction:
            errors.append(f"Transaction {index}: missing field '{field}'.")

    if errors:
        return errors

    date_value = transaction["date"]
    description = transaction["description"]
    amount = transaction["amount"]
    category = transaction["category"]
    transaction_type = transaction["type"]

    if not isinstance(date_value, str) or not is_valid_date(date_value):
        errors.append(f"Transaction {index}: invalid date '{date_value}'.")

    if not isinstance(description, str) or not description.strip():
        errors.append(f"Transaction {index}: description must be a non-empty string.")

    if not isinstance(amount, int) or amount <= 0:
        errors.append(f"Transaction {index}: amount must be a positive integer.")

    if category not in CATEGORIES:
        errors.append(f"Transaction {index}: invalid category '{category}'.")

    if transaction_type not in TRANSACTION_TYPES:
        errors.append(f"Transaction {index}: invalid type '{transaction_type}'.")

    return errors


def validate_extraction_result(result: dict) -> dict:
    errors = []

    if not isinstance(result, dict):
        return {
            "is_valid": False,
            "needs_clarification": False,
            "errors": ["Extraction result must be a dictionary."],
        }

    status = result.get("status")
    transactions = result.get("transactions")
    ambiguous_items = result.get("ambiguous_items", [])
    clarification_question = result.get("clarification_question")

    if status not in VALID_STATUSES:
        errors.append(f"Invalid status '{status}'.")

    if not isinstance(transactions, list):
        errors.append("Transactions must be a list.")
        transactions = []

    if not isinstance(ambiguous_items, list):
        errors.append("Ambiguous items must be a list.")

    for index, transaction in enumerate(transactions, start=1):
        if not isinstance(transaction, dict):
            errors.append(f"Transaction {index}: must be a dictionary.")
            continue

        errors.extend(validate_transaction(transaction, index))

    needs_clarification = status == "needs_clarification" or len(ambiguous_items) > 0

    if needs_clarification and not clarification_question:
        errors.append("Clarification question is required when clarification is needed.")

    if status == "success" and len(transactions) == 0:
        errors.append("Successful extraction must contain at least one transaction.")

    return {
        "is_valid": len(errors) == 0,
        "needs_clarification": needs_clarification,
        "errors": errors,
    }