CATEGORIES = [
    "Uang Saku",
    "Beasiswa",
    "Gaji",
    "Pemasukan Lain",
    "Saldo Awal",
    "Uang Kos",
    "Makan & Minum",
    "Transportasi",
    "Komunikasi",
    "Token Listrik",
    "Air Minum",
    "Belanja Bulanan",
    "Laundry",
    "Tabungan",
    "Dana Terencana",
    "Jajan & Hiburan",
    "Belanja Non-Wishlist",
    "Sosial & Hadiah",
    "Biaya Admin Bank",
    "Transfer Antar Rekening",
    "Piutang Teman",
    "Utang",
    "Kesehatan",
    "Kuliah",
    "Lainnya",
]


TRANSACTION_TYPES = [
    "expense",
    "income",
]


CATEGORY_GROUPS = {
    "Pemasukan": [
        "Uang Saku",
        "Beasiswa",
        "Gaji",
        "Pemasukan Lain",
        "Saldo Awal",
    ],
    "Kebutuhan Pokok": [
        "Uang Kos",
        "Makan & Minum",
        "Transportasi",
        "Komunikasi",
        "Token Listrik",
        "Air Minum",
        "Belanja Bulanan",
        "Laundry",
        "Kesehatan",
        "Kuliah",
    ],
    "Tabungan": [
        "Tabungan",
    ],
    "Dana Terencana": [
        "Dana Terencana",
    ],
    "Gaya Hidup": [
        "Jajan & Hiburan",
        "Belanja Non-Wishlist",
    ],
    "Lain-lain": [
        "Sosial & Hadiah",
        "Biaya Admin Bank",
        "Transfer Antar Rekening",
        "Piutang Teman",
        "Utang",
        "Lainnya",
    ],
}


def get_category_group(category: str) -> str:
    for group_name, categories in CATEGORY_GROUPS.items():
        if category in categories:
            return group_name

    return "Lain-lain"