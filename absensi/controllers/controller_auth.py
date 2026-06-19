from models.model_users import User

class ControllerAuth:
    @staticmethod
    def login(username, password):
        """Memvalidasi login dari input user"""
        if not username or not password:
            return {"status": False, "message": "Username dan password tidak boleh kosong!"}
        
        # Memanggil fungsi login static dari model User
        user_data = User.login(username, password)
        
        if user_data:
            return {"status": True, "message": "Login berhasil!", "user": user_data}
        else:
            return {"status": False, "message": "Username atau password salah!"}

    @staticmethod
    def register(username, password, nama, role):
        """Validasi data pendaftaran dari view"""
        if not username or not password or not nama or not role:
            return {"status": False, "message": "Semua kolom wajib diisi!"}
        
        if len(password) < 3:
            return {"status": False, "message": "Password minimal harus 3 karakter!"}
            
        # Panggil fungsi register di model User
        return User.register(username, password, nama, role)