import sqlite3
from database import get_connection
from datetime import datetime

class Absensi:
    """Model untuk menangani data Absensi Mahasiswa"""
    
    @staticmethod
    def catat_absen(user_id, status, keterangan=""):
        """Mencatat kehadiran mahasiswa ke dalam database"""
        conn = get_connection()
        cursor = conn.cursor()
        
        # Menggabungkan Tanggal dan Jam menjadi satu format standar
        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            # Menginput data ke kolom tanggal, status, dan keterangan
            cursor.execute('''
                INSERT INTO absensi (user_id, tanggal, status, keterangan)
                VALUES (?, ?, ?, ?)
            ''', (user_id, waktu_sekarang, status, keterangan))
            conn.commit()
            return {"status": True, "message": "Absensi berhasil dicatat!"}
        except sqlite3.Error as e:
            # Jalur alternatif jika skema database kamu membutuhkan kolom 'waktu' terpisah
            try:
                cursor.execute('''
                    INSERT INTO absensi (user_id, tanggal, waktu, status, keterangan)
                    VALUES (?, ?, ?, ?, ?)
                ''', (user_id, datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S"), status, keterangan))
                conn.commit()
                return {"status": True, "message": "Absensi berhasil dicatat!"}
            except sqlite3.Error:
                return {"status": False, "message": f"Gagal mencatat absen: {e}"}
        finally:
            conn.close()
            
    @staticmethod
    def get_riwayat_by_user_id(user_id):
        """Mengambil semua riwayat absen milik satu mahasiswa tertentu"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Mengambil data dengan asumsi kolom tanggal dan waktu terpisah
            cursor.execute('''
                SELECT tanggal, waktu, status, keterangan 
                FROM absensi 
                WHERE user_id = ? 
                ORDER BY id DESC
            ''', (user_id,))
            rows = cursor.fetchall()
        except sqlite3.OperationalError:
            # Alternatif aman jika kolom 'waktu' tidak ada di database
            cursor.execute('''
                SELECT tanggal, tanggal AS waktu, status, keterangan 
                FROM absensi 
                WHERE user_id = ? 
                ORDER BY id DESC
            ''', (user_id,))
            rows = cursor.fetchall()
            
        conn.close()
        return [dict(row) for row in rows]
        
    @staticmethod
    def get_semua_absen_untuk_dosen():
        """Mengambil semua data absensi mahasiswa untuk tampilan dashboard dosen"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                SELECT a.id, u.username, a.tanggal, a.waktu, a.status, a.keterangan
                FROM absensi a
                JOIN users u ON a.user_id = u.id
                ORDER BY a.id DESC
            ''')
            rows = cursor.fetchall()
        except sqlite3.OperationalError:
            # Alternatif aman jika kolom 'waktu' tidak terdeteksi di database
            cursor.execute('''
                SELECT a.id, u.username, a.tanggal, a.tanggal AS waktu, a.status, a.keterangan
                FROM absensi a
                JOIN users u ON a.user_id = u.id
                ORDER BY a.id DESC
            ''')
            rows = cursor.fetchall()
            
        conn.close()
        return [dict(row) for row in rows]


class MataKuliah:
    """Model baru untuk menangani data Mata Kuliah oleh Dosen"""

    @staticmethod
    def tambah_matkul(nama_matkul, dosen_id):
        """Menambahkan mata kuliah baru ke database"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Proteksi otomatis untuk membuat tabel matakuliah jika belum terbentuk
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS matakuliah (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama_matkul TEXT NOT NULL UNIQUE,
                    dosen_id INTEGER,
                    FOREIGN KEY (dosen_id) REFERENCES users (id)
                )
            ''')
            
            # Memasukkan data mata kuliah baru
            cursor.execute('''
                INSERT INTO matakuliah (nama_matkul, dosen_id)
                VALUES (?, ?)
            ''', (nama_matkul, dosen_id))
            conn.commit()
            return {"status": True, "message": f"Mata kuliah '{nama_matkul}' berhasil ditambahkan!"}
        except sqlite3.IntegrityError:
            return {"status": False, "message": "Mata kuliah tersebut sudah ada!"}
        except sqlite3.Error as e:
            return {"status": False, "message": f"Gagal menambahkan mata kuliah: {e}"}
        finally:
            conn.close()

    @staticmethod
    def get_matkul_by_dosen(dosen_id):
        """Mengambil daftar seluruh mata kuliah yang diajar oleh dosen tertentu"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('SELECT nama_matkul FROM matakuliah WHERE dosen_id = ?', (dosen_id,))
            rows = cursor.fetchall()
            return [row['nama_matkul'] for row in rows]
        except sqlite3.Error:
            return []
        finally:
            conn.close()