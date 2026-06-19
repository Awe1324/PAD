import sqlite3
from database import get_connection

class User:
    """Model untuk User"""
    
    @staticmethod
    def login(username, password):
        """Login pengguna"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM users 
            WHERE username = ? AND password = ?
        ''', (username, password))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    @staticmethod
    def get_by_id(user_id):
        """Get user by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    @staticmethod
    def get_all_mahasiswa():
        """Get all mahasiswa"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE role = "mahasiswa" ORDER BY nama')
        users = cursor.fetchall()
        conn.close()
        return [dict(user) for user in users]
    
    @staticmethod
    def get_all_users():
        """Get all users"""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY nama')
        users = cursor.fetchall()
        conn.close()
        return [dict(user) for user in users]
    
    @staticmethod
    def register(username, password, nama, role="mahasiswa"):
        """Mendaftarkan pengguna baru ke database"""
        conn = get_connection()
        cursor = conn.cursor()
        try:
            # Pengecekan apakah username sudah terdaftar atau belum
            cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
            if cursor.fetchone():
                return {"status": False, "message": "Username sudah digunakan!"}
            
            # Insert data user baru (kolom 'nama' disesuaikan dengan ORDER BY namamu kemarin)
            cursor.execute('''
                INSERT INTO users (username, password, nama, role)
                VALUES (?, ?, ?, ?)
            ''', (username, password, nama, role))
            conn.commit()
            return {"status": True, "message": "Pendaftaran berhasil! Silakan login."}
        except sqlite3.Error as e:
            return {"status": False, "message": f"Gagal mendaftar: {e}"}
        finally:
            conn.close()