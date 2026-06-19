import sqlite3

def hapus_data_absen(id_yang_mau_dihapus):
    try:
        # Menghubungkan langsung ke file database proyekmu
        conn = sqlite3.connect("absensi.db")
        cursor = conn.cursor()
        
        # Eksekusi perintah hapus
        cursor.execute("DELETE FROM absensi WHERE ID = ?", (id_yang_mau_dihapus,))
        
        # MENYIMPAN PERUBAHAN SECARA PERMANEN (COMMIT)
        conn.commit()
        
        if cursor.rowcount > 0:
            print(f" BERHASIL: Data absensi dengan ID {id_yang_mau_dihapus} telah dihapus permanen!")
        else:
            print(f" GAGAL: Data dengan ID {id_yang_mau_dihapus} tidak ditemukan di database.")
            
        conn.close()
    except Exception as e:
        print(f" ERROR: Terjadi kesalahan: {e}")

if __name__ == "__main__":
    # GANTI ANGKA DI BAWAH INI SESUAI ID YANG INGIN KAMU HAPUS
    # Contoh: Mau hapus data ID nomor 1
    id_target = 4
    
    hapus_data_absen(id_target)