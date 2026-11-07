import sqlite3

# --- 1. INISIALISASI DATABASE & TABEL ---
def inisialisasi_db():
    conn = sqlite3.connect("inventaris.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS barang (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_barang TEXT NOT NULL,
        jumlah INTEGER NOT NULL,
        harga INTEGER NOT NULL
    )
    """)
    conn.commit()
    conn.close()



# --- 2. FUNGSI CREATE  ---
def tambah_barang():
    print("\n--- TAMBAH BARANG BARU ---")
    nama = input("Masukkan nama barang: ")
    jumlah = int(input("Masukkan jumlah stok: "))
    harga = int(input("Masukkan harga per unit (Rp): "))

    conn = sqlite3.connect("inventaris.db")
    cursor = conn.cursor()
    sql = "INSERT INTO barang (nama_barang, jumlah, harga) VALUES (?, ?, ?)"
    cursor.execute(sql, (nama, jumlah, harga))
    conn.commit()
    conn.close()

    print(f" Barang '{nama}' berhasil ditambahkan!")


# --- 3. FUNGSI READ  ---
def lihat_barang():
    print("\n--- DAFTAR STOK BARANG ---")
    conn = sqlite3.connect("inventaris.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM barang")
    daftar_barang = cursor.fetchall()
    conn.close()

    if not daftar_barang:
        print(" Belum ada data barang.")
    else:
        print("-" * 45)
        for b in daftar_barang:
            print(f"ID: {b[0]} | Nama: {b[1]} | Stok: {b[2]} | Harga: Rp {b[3]}")
        print("-" * 45)



# --- 4. FUNGSI UPDATE  ---
def ubah_barang():
    print("\n--- UBAH DATA BARANG ---")
    lihat_barang()
    id_barang = int(input("\nMasukkan ID barang yang mau diubah: "))

    conn = sqlite3.connect("inventaris.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM barang WHERE id = ?", (id_barang,))
    barang = cursor.fetchone()

    if not barang:
        print(f" Barang dengan ID {id_barang} tidak ditemukan!")
        conn.close()
        return

    print(f"Data Lama: {barang[1]} | Stok: {barang[2]} | Harga: Rp {barang[3]}")
    print("-" * 40)
    nama_baru = input("Masukkan nama baru: ")
    jumlah_baru = int(input("Masukkan jumlah stok baru: "))
    harga_baru = int(input("Masukkan harga baru (Rp): "))

    sql = """
    UPDATE barang 
    SET nama_barang = ?, jumlah = ?, harga = ? 
    WHERE id = ?
    """
    cursor.execute(sql, (nama_baru, jumlah_baru, harga_baru, id_barang))
    conn.commit()
    conn.close()

    print(f" Data barang ID {id_barang} berhasil diperbarui!")


# --- 5. FUNGSI DELETE  ---
def hapus_barang():
    print("\n--- HAPUS DATA BARANG ---")
    lihat_barang()
    id_barang = int(input("\nMasukkan ID barang yang mau dihapus: "))

    conn = sqlite3.connect("inventaris.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM barang WHERE id = ?", (id_barang,))
    barang = cursor.fetchone()

    if not barang:
        print(f" Barang dengan ID {id_barang} tidak ditemukan!")
        conn.close()
        return

    yakin = input(f"Yakin mau menghapus '{barang[1]}'? (y/n): ")
    if yakin.lower() == 'y':
        cursor.execute("DELETE FROM barang WHERE id = ?", (id_barang,))
        conn.commit()
        print(f" Barang '{barang[1]}' berhasil dihapus!")
    else:
        print(" Penghapusan dibatalkan.")

    conn.close()


# --- 6. MENU UTAMA INTERAKTIF (CLI) ---
def menu_utama():
    inisialisasi_db()
    
    while True:
        print("\n=================================")
        print("   TOKO BIPBIP  ")
        print("=================================")
        print("1. Lihat Daftar Barang (Read)")
        print("2. Tambah Barang Baru (Create)")
        print("3. Ubah Data Barang (Update)")
        print("4. Hapus Barang (Delete)")
        print("5. Keluar")
        print("=================================")
        
        pilihan = input("Pilih menu (1-5): ")

        if pilihan == '1':
            lihat_barang()
        elif pilihan == '2':
            tambah_barang()
        elif pilihan == '3':
            ubah_barang()
        elif pilihan == '4':
            hapus_barang()
        elif pilihan == '5':
            print("\nTerima kasih! Data selesai.")
            break
        else:
            print(" Pilihan tidak valid. Silakan pilih angka 1-5.")


# --- EKSEKUSI PROGRAM ---
if __name__ == "__main__":
    menu_utama()