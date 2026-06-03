import sys
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

from src.analytics.insights import (
    calculate_expense_by_category,
    calculate_monthly_summary,
    get_top_spending_category,
)
from src.database.db import init_db
from src.database.queries import get_all_transactions, insert_transactions
from src.llm.extractor import extract_transactions
from src.validation.validator import validate_extraction_result


st.set_page_config(
    page_title="DompetKos AI",
    layout="wide",
)


def format_rupiah(amount: int) -> str:
    return f"Rp{amount:,.0f}".replace(",", ".")


def main():
    init_db()

    st.title("DompetKos AI")
    st.write(
        "Catat pengeluaran atau pemasukan dengan Bahasa Indonesia natural, "
        "lalu sistem akan mengekstraknya menjadi transaksi terstruktur."
    )

    current_month = date.today().strftime("%Y-%m")

    selected_month = st.text_input(
        "Pilih bulan laporan",
        value=current_month,
        help="Format: YYYY-MM, contoh: 2026-06",
    )

    transactions = get_all_transactions()

    st.subheader("Dashboard Bulanan")

    summary = calculate_monthly_summary(transactions, selected_month)
    top_category = get_top_spending_category(transactions, selected_month)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        label="Total Pemasukan",
        value=format_rupiah(summary["total_income"]),
    )

    col2.metric(
        label="Total Pengeluaran",
        value=format_rupiah(summary["total_expense"]),
    )

    col3.metric(
        label="Cash Flow",
        value=format_rupiah(summary["cash_flow"]),
    )

    if top_category:
        col4.metric(
            label="Kategori Paling Boros",
            value=top_category["category"],
            delta=format_rupiah(top_category["total_expense"]),
        )
    else:
        col4.metric(
            label="Kategori Paling Boros",
            value="-",
        )

    st.divider()

    st.subheader("Catat Transaksi")

    user_input = st.text_area(
        "Tulis transaksi kamu",
        placeholder="Contoh: Hari ini makan ayam geprek 18 ribu, kopi 12 ribu, dan laundry 25 ribu.",
        height=120,
    )

    extract_button = st.button("Catat Transaksi", type="primary")

    if extract_button:
        if not user_input.strip():
            st.warning("Input masih kosong.")
        else:
            with st.spinner("Mengekstrak transaksi dengan Gemini..."):
                try:
                    extraction_result = extract_transactions(user_input)
                    validation_result = validate_extraction_result(extraction_result)

                    with st.expander("Lihat detail ekstraksi"):
                        st.subheader("Hasil Ekstraksi")
                        st.json(extraction_result)

                        st.subheader("Hasil Validasi")
                        st.json(validation_result)

                    if not validation_result["is_valid"]:
                        st.error("Data hasil ekstraksi tidak valid. Transaksi tidak disimpan.")
                        for error in validation_result["errors"]:
                            st.write(f"- {error}")

                    elif validation_result["needs_clarification"]:
                        st.warning("Input masih membutuhkan klarifikasi. Transaksi belum disimpan.")
                        st.write(extraction_result.get("clarification_question"))

                    else:
                        inserted_ids = insert_transactions(extraction_result["transactions"])
                        st.success(f"{len(inserted_ids)} transaksi berhasil disimpan.")
                        st.rerun()

                except Exception as error:
                    st.error("Terjadi error saat memproses input.")
                    st.exception(error)

    st.divider()

    st.subheader("Pengeluaran per Kategori")

    expense_by_category = calculate_expense_by_category(transactions, selected_month)

    if not expense_by_category:
        st.info("Belum ada pengeluaran pada bulan ini.")
    else:
        category_df = pd.DataFrame(expense_by_category)
        category_df["total_expense_display"] = category_df["total_expense"].apply(format_rupiah)

        st.dataframe(
            category_df[
                [
                    "category",
                    "total_expense_display",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.bar_chart(
            data=category_df,
            x="category",
            y="total_expense",
        )

    st.divider()

    st.subheader("Riwayat Transaksi")

    if not transactions:
        st.info("Belum ada transaksi tersimpan.")
    else:
        df = pd.DataFrame(transactions)
        df = df[df["date"].str.startswith(selected_month)]

        if df.empty:
            st.info("Belum ada transaksi untuk bulan yang dipilih.")
        else:
            df["amount_display"] = df["amount"].apply(format_rupiah)

            df = df.rename(
                columns={
                    "id": "ID",
                    "date": "Tanggal",
                    "description": "Keterangan",
                    "amount_display": "Nominal",
                    "category": "Kategori",
                    "type": "Tipe",
                    "created_at": "Dibuat Pada",
                }
            )

            st.dataframe(
                df[
                    [
                        "ID",
                        "Tanggal",
                        "Keterangan",
                        "Nominal",
                        "Kategori",
                        "Tipe",
                        "Dibuat Pada",
                    ]
                ],
                use_container_width=True,
                hide_index=True,
            )


if __name__ == "__main__":
    main()