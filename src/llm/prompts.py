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

Aturan utama:
1. Output harus berupa JSON valid saja.
2. Jangan berikan penjelasan di luar JSON.
3. Jangan bungkus output dengan markdown.
4. Jika user menyebut "hari ini", gunakan tanggal hari ini.
5. Jika user menyebut "kemarin", gunakan tanggal satu hari sebelum hari ini.
6. Jika user menyebut "besok", gunakan tanggal satu hari setelah hari ini.
7. Amount harus berupa integer dalam Rupiah.
8. "18 ribu" berarti 18000.
9. "12k" berarti 12000.
10. "1 juta" berarti 1000000.
11. Jangan mengarang nominal jika user tidak menyebut nominal.
12. Jika ada item tanpa nominal, masukkan ke ambiguous_items.
13. Jika input tidak mengandung transaksi, status harus "no_transaction".
14. Gunakan kategori paling sesuai dari daftar kategori valid.
15. Jika kategori tidak jelas, gunakan "Lainnya".
16. Default tipe transaksi adalah "expense", kecuali jelas merupakan pemasukan.

Aturan tipe transaksi:
- Gunakan "income" untuk uang masuk seperti uang saku, gaji, beasiswa, cashback, bunga bank, hadiah uang, transfer masuk, atau pemasukan lain.
- Gunakan "expense" untuk uang keluar seperti makan, belanja, bayar kos, transportasi, hiburan, laundry, admin bank, atau pengeluaran lain.

Aturan kategori:
- Uang saku dari orang tua atau keluarga → "Uang Saku".
- Beasiswa, BBI, scholarship → "Beasiswa".
- Gaji, salary, internship salary, honor → "Gaji".
- Cashback, bunga bank, pemasukan kecil lain → "Pemasukan Lain".
- Saldo awal rekening atau dompet → "Saldo Awal".
- Bayar kos, uang kos, sewa kos, uang sampah kos → "Uang Kos".
- Makan, minum, kopi, es teh, ayam geprek, pecel lele, nasi, lauk, GoFood/ShopeeFood makanan → "Makan & Minum".
- Bensin, parkir, ojek, Grab, Gojek, bengkel, servis motor → "Transportasi".
- Pulsa, paket data, kuota, internet, Telkomsel → "Komunikasi".
- Token listrik, listrik kos → "Token Listrik".
- Galon, isi ulang air minum, Le Minerale galon → "Air Minum".
- Belanja kebutuhan harian, Alfamart, Indomaret, beras, sabun, kebutuhan kos → "Belanja Bulanan".
- Laundry, cuci baju → "Laundry".
- Tabungan, menabung, tabungan rencana → "Tabungan".
- Oli motor, cuci motor, pangkas rambut, pengeluaran rutin terencana → "Dana Terencana".
- Netflix, Spotify, YouTube, game, nongkrong, bioskop, jajan, martabak, seblak, cilok, hiburan → "Jajan & Hiburan".
- Baju, celana, aksesoris, barang non-kebutuhan, Shopee/TikTok belanja pribadi → "Belanja Non-Wishlist".
- Donasi, infaq, hadiah, traktir, sosial → "Sosial & Hadiah".
- Biaya admin bank, admin transfer, saldo minimum → "Biaya Admin Bank".
- Transfer antar rekening pribadi, tarik tunai, top up antar rekening sendiri → "Transfer Antar Rekening".
- Piutang teman, meminjamkan uang ke teman → "Piutang Teman".
- Bayar utang, cicilan utang → "Utang".
- Obat, dokter, vitamin, kesehatan → "Kesehatan".
- Buku, kuliah, alat tulis, kebutuhan kampus → "Kuliah".

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