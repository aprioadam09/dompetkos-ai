from src.database.db import get_connection


def insert_transaction(transaction: dict) -> int:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (
            date,
            description,
            amount,
            category,
            type
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            transaction["date"],
            transaction["description"],
            transaction["amount"],
            transaction["category"],
            transaction["type"],
        ),
    )

    connection.commit()
    transaction_id = cursor.lastrowid
    connection.close()

    return transaction_id


def insert_transactions(transactions: list[dict]) -> list[int]:
    inserted_ids = []

    for transaction in transactions:
        transaction_id = insert_transaction(transaction)
        inserted_ids.append(transaction_id)

    return inserted_ids


def get_all_transactions() -> list[dict]:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            date,
            description,
            amount,
            category,
            type,
            created_at
        FROM transactions
        ORDER BY date DESC, id DESC
        """
    )

    rows = cursor.fetchall()
    connection.close()

    return [dict(row) for row in rows]


def set_monthly_budget(month: str, amount: int) -> None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO budgets (
            month,
            amount
        )
        VALUES (?, ?)
        ON CONFLICT(month)
        DO UPDATE SET
            amount = excluded.amount,
            updated_at = CURRENT_TIMESTAMP
        """,
        (month, amount),
    )

    connection.commit()
    connection.close()


def get_monthly_budget(month: str) -> dict | None:
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            month,
            amount,
            created_at,
            updated_at
        FROM budgets
        WHERE month = ?
        """,
        (month,),
    )

    row = cursor.fetchone()
    connection.close()

    if row is None:
        return None

    return dict(row)