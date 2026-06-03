import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.append(str(PROJECT_ROOT))

from src.database.db import init_db
from src.database.queries import get_all_transactions, insert_transactions
from src.llm.extractor import extract_transactions
from src.validation.validator import validate_extraction_result


st.set_page_config(
    page_title="DompetKos AI",
    page_icon="💰",
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

    st.subheader("Catat Transaksi")

    user_input = st.text_area(
        "Tulis transaksi kamu",
        placeholder="Contoh: Hari ini makan ayam geprek 18 ribu, kopi 12 ribu, dan laundry 25 ribu.",
        height=120,
    )

    extract_button = st.button("Extract & Save", type="primary")

    if extract_button:
        if not user_input.strip():
            st.warning("Input masih kosong.")
        else:
            with st.spinner("Mengekstrak transaksi dengan Gemini..."):
                try:
                    extraction_result = extract_transactions(user_input)
                    validation_result = validate_extraction_result(extraction_result)

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

                except Exception as error:
                    st.error("Terjadi error saat memproses input.")
                    st.exception(error)

    st.divider()

    st.subheader("Riwayat Transaksi")

    transactions = get_all_transactions()

    if not transactions:
        st.info("Belum ada transaksi tersimpan.")
    else:
        df = pd.DataFrame(transactions)
        df["amount_display"] = df["amount"].apply(format_rupiah)

        st.dataframe(
            df[
                [
                    "id",
                    "date",
                    "description",
                    "amount_display",
                    "category",
                    "type",
                    "created_at",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )


if __name__ == "__main__":
    main()