import csv
from datetime import datetime

DATA_FILE = "crypto_data.csv"
FIELDNAMES = ["Tanggal", "Crypto", "Open", "Buy Fee", "Sell Fee", "Close", "Volume"]

data_list = []              
index_data = {}             

# ==========================
# FUNGSI: Load & Simpan CSV
# ==========================

def load_data():
    try:
        with open(DATA_FILE, 'r') as file:
            reader = csv.DictReader(file)
            for i, row in enumerate(reader):
                for key in ["Open", "Buy Fee", "Sell Fee", "Close", "Volume"]:
                    row[key] = float(row[key])
                data_list.append(row)
                index_data[(row["Tanggal"], row["Crypto"])] = i
    except FileNotFoundError:
        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()

def simpan_data():
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(data_list)
    print("✅ Data berhasil disimpan.")

# =============================
# FUNGSI: Tambah, Ubah, Hapus
# =============================

def tambah_data():
    print("\n--- Tambah Data ---")
    tanggal_input = input("Tanggal (DD-MM-YYYY): ")
    try:
        tanggal = datetime.strptime(tanggal_input, "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("❌ Format tanggal salah.")
        return

    crypto = input("Crypto (misal: BTC): ").upper()
    key = (tanggal, crypto)

    if key in index_data:
        print("❌ Data sudah ada.")
        return

    try:
        open_ = float(input("Open: "))
        buy_fee = float(input("Buy Fee (%): ")) / 100
        sell_fee = float(input("Sell Fee (%): ")) / 100
        close = float(input("Close: "))
        volume = float(input("Volume (USD): "))
    except ValueError:
        print("❌ Masukkan angka yang valid.")
        return

    data = {
        "Tanggal": tanggal,
        "Crypto": crypto,
        "Open": open_,
        "Buy Fee": buy_fee,
        "Sell Fee": sell_fee,
        "Close": close,
        "Volume": volume
    }

    data_list.append(data)
    index_data[key] = len(data_list) - 1
    print("✅ Data berhasil ditambahkan.")

def ubah_data():
    print("\n--- Ubah Data ---")
    tanggal_input = input("Tanggal (DD-MM-YYYY): ")
    try:
        tanggal = datetime.strptime(tanggal_input, "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("❌ Format tanggal salah.")
        return

    crypto = input("Crypto: ").upper()
    key = (tanggal, crypto)

    if key not in index_data:
        print("❌ Data tidak ditemukan.")
        return

    kolom = input("Data yang ingin diubah (Open/Buy Fee/Sell Fee/Close/Volume): ").title()
    if kolom not in FIELDNAMES or kolom in ["Tanggal", "Crypto"]:
        print("❌ Data tidak valid atau tidak bisa diubah.")
        return

    try:
        nilai = float(input("Nilai baru: "))
        if kolom in ["Buy Fee", "Sell Fee"]:
            nilai = nilai / 100
        data_list[index_data[key]][kolom] = nilai
        print("✅ Data berhasil diubah.")
    except ValueError:
        print("❌ Nilai tidak valid.")

def hapus_data():
    print("\n--- Hapus Data ---")
    tanggal_input = input("Tanggal (DD-MM-YYYY): ")
    try:
        tanggal = datetime.strptime(tanggal_input, "%d-%m-%Y").strftime("%Y-%m-%d")
    except ValueError:
        print("❌ Format tanggal salah.")
        return

    crypto = input("Crypto: ").upper()
    key = (tanggal, crypto)

    if key in index_data:
        index = index_data[key]
        data_list.pop(index)
        index_data.clear()
        for i, row in enumerate(data_list):
            index_data[(row["Tanggal"], row["Crypto"])] = i
        print("✅ Data berhasil dihapus.")
    else:
        print("❌ Data tidak ditemukan.")
# =============================
# FUNGSI: Analisis & Ringkasan
# =============================

def lihat_ringkasan():
    print("\n--- Ringkasan Data ---")
    if not data_list:
        print("⚠️  Data kosong.")
        return

    ringkasan = {}
    total_pnl = 0
    total_roi = 0
    valid_roi_count = 0

    for row in data_list:
        crypto = row["Crypto"]
        ringkasan.setdefault(crypto, {"close": [], "volume": 0})
        ringkasan[crypto]["close"].append(row["Close"])
        ringkasan[crypto]["volume"] += row["Volume"]

        open_ = row["Open"]
        volume = row["Volume"]
        buy_fee = row["Buy Fee"]
        sell_fee = row["Sell Fee"]
        close = row["Close"]

        if open_ > 0:
            unit = (volume / open_) * (1 - buy_fee)
            hasil_kotor = close * unit
            hasil_bersih = hasil_kotor * (1 - sell_fee)
            pnl = hasil_bersih - volume
            roi = (pnl / volume) * 100
            total_pnl += pnl
            total_roi += roi
            valid_roi_count += 1

    for crypto, val in ringkasan.items():
        print(f"\n{crypto}")
        print(f"- Rata-rata Close : {sum(val['close']) / len(val['close']):.2f}")
        print(f"- Tertinggi       : {max(val['close']):.2f}")
        print(f"- Terendah        : {min(val['close']):.2f}")
        print(f"- Total Volume    : {val['volume']:.0f}")

    print("\n=== Ringkasan PNL & ROI Keseluruhan ===")
    print(f"Total Keuntungan Bersih : {total_pnl:.2f} USD")
    if valid_roi_count:
        print(f"Rata-rata ROI           : {total_roi / valid_roi_count:.2f}%")
    else:
        print("Tidak ada transaksi valid untuk menghitung ROI.")

def hitung_untung_rugi():
    print("\n--- Analisis PNL, ROI, dan Keuntungan ---")
    for row in data_list:
        open_ = row["Open"]
        close = row["Close"]
        volume = row["Volume"]
        buy_fee = row["Buy Fee"]
        sell_fee = row["Sell Fee"]

        if open_ == 0:
            print(f"{row['Tanggal']} | {row['Crypto']} : ❌ Open 0.")
            continue

        unit = (volume / open_) * (1 - buy_fee)
        hasil_kotor = close * unit
        hasil_bersih = hasil_kotor * (1 - sell_fee)

        pnl = hasil_bersih - volume
        roi = (pnl / volume) * 100

        status = "Untung" if pnl > 0 else "Rugi" if pnl < 0 else "Imbang"
        print(f"{row['Tanggal']} | {row['Crypto']} => PNL: {pnl:.2f} USD | ROI: {roi:.2f}% ({status})")

# =============================
# FUNGSI: Filter Data
# =============================

def filter_data():
    print("\n--- Cari Data ---")
    mode = input("Filter berdasarkan (bulan/tahun): ").lower()
    nilai = input("Nilai (contoh: 2024 atau 2024-06): ")
    hasil = []

    for row in data_list:
        try:
            tgl = datetime.strptime(row["Tanggal"], "%Y-%m-%d")
            if (mode == "bulan" and tgl.strftime("%Y-%m") == nilai) or \
               (mode == "tahun" and tgl.strftime("%Y") == nilai):
                hasil.append((tgl, row))
        except:
            continue

    if not hasil:
        print("❌ Data tidak ditemukan.")
    else:
        print(f"\nDitemukan {len(hasil)} data:")
        for _, row in sorted(hasil):
            print(f"Tanggal: {row['Tanggal']}, Crypto: {row['Crypto']}, Open: {row['Open']:.2f}, Close: {row['Close']:.2f}, Volume: {row['Volume']:.2f}")

# =============================
# MENU UTAMA
# =============================

def menu():
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Tambah Data")
        print("2. Lihat Ringkasan")
        print("3. Ubah Data")
        print("4. Hapus Data")
        print("5. Hitung PNL & ROI")
        print("6. Filter Data Bulan/Tahun")
        print("7. Simpan dan Keluar")
        pilihan = input("Pilih (1-7): ")

        if pilihan == '1': tambah_data()
        elif pilihan == '2': lihat_ringkasan()
        elif pilihan == '3': ubah_data()
        elif pilihan == '4': hapus_data()
        elif pilihan == '5': hitung_untung_rugi()
        elif pilihan == '6': filter_data()
        elif pilihan == '7': simpan_data(); break
        else: print("❌ Pilihan tidak valid.")

load_data()
menu()
