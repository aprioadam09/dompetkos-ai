from datetime import date
from src.categories import CATEGORIES, TRANSACTION_TYPES


def build_extraction_prompt(user_input: str) -> str:
    today = date.today().isoformat()
    categories_text = ", ".join(CATEGORIES)
    transaction_types_text = ", ".join(TRANSACTION_TYPES)

    return f"""
Kamu adalah financial transaction extraction system untuk aplikasi DompetKos AI.

Tugasmu adalah mengekstrak transaksi keuangan dari input Bahasa Indonesia natural menjadi JSON valid.

Tanggal hari ini adalah: {today}

Kategori yang valid:
{categories_text}

Tipe transaksi yang valid:
{transaction_types_text}

Aturan penting:
1. Output harus berupa JSON valid saja.
2. Jangan berikan penjelasan di luar JSON.
3. Jika user menyebut "hari ini", gunakan tanggal hari ini.
4. Jika user menyebut "kemarin", gunakan tanggal satu hari sebelum hari ini.
5. Jika user menyebut "besok", gunakan tanggal satu hari setelah hari ini.
6. Amount harus berupa integer dalam Rupiah.
7. "18 ribu" berarti 18000.
8. "12k" berarti 12000.
9. "1 juta" berarti 1000000.
10. Jangan mengarang nominal jika user tidak menyebut nominal.
11. Jika ada item tanpa nominal, masukkan ke ambiguous_items.
12. Jika input tidak mengandung transaksi, status harus "no_transaction".
13. Gunakan kategori paling sesuai dari daftar kategori valid.
14. Jika kategori tidak jelas, gunakan "Lainnya".
15. Default tipe transaksi adalah "expense", kecuali jelas merupakan pemasukan, gaji, transfer masuk, hadiah uang, atau uang saku.

Format JSON wajib:
{{
  "status": "success | needs_clarification | no_transaction",
  "transactions": [
    {{
      "date": "YYYY-MM-DD",
      "description": "string",
      "amount": 0,
      "category": "string",
      "type": "expense | income"
    }}
  ],
  "ambiguous_items": [
    {{
      "description": "string",
      "reason": "string"
    }}
  ],
  "clarification_question": "string or null"
}}

Input user:
\"\"\"{user_input}\"\"\"
"""