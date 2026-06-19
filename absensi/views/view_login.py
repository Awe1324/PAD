import tkinter as tk
from tkinter import messagebox, ttk
# Pastikan jalur import controller Anda sudah benar sesuai struktur folder Anda
from controllers.controller_auth import ControllerAuth

class LoginView:
    def __init__(self, parent, on_login_success):
        self.parent = parent
        self.on_login_success = on_login_success
        
        # Konfigurasi dasar Window Utama
        self.parent.title("Sistem Absensi")
        self.parent.geometry("460x550")
        self.parent.configure(bg="#F8FAFC") # Background modern abu-abu sangat muda (Slate 50)
        
        # Mengatur tema TTK agar Combobox dan Entry terlihat modern
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TCombobox", fieldbackground="white", background="#E2E8F0")
        
        # Inisialisasi placeholder container untuk login dan register
        self.login_frame = None
        self.reg_frame = None
        
        # Tampilkan halaman login pertama kali saat aplikasi dibuka
        self.tampilkan_halaman_login()

    # =========================================================================
    # 1. HALAMAN LOGIN
    # =========================================================================
    def tampilkan_halaman_login(self):
        # Set judul window khusus login
        self.parent.title("Sistem Absensi - Login")
        
        # Jika frame register masih ada, sembunyikan terlebih dahulu
        if self.reg_frame:
            self.reg_frame.pack_forget()
            
        # Buat Card Container untuk Form Login (Efek melayang/Clean Card)
        self.login_frame = tk.Frame(self.parent, padx=35, pady=35, bg="white")
        self.login_frame.pack(expand=True, padx=30, pady=30)
        
        # Header text
        self.label_title = tk.Label(self.login_frame, text="Selamat Datang", font=("Segoe UI", 18, "bold"), bg="white", fg="#0F172A")
        self.label_title.pack(pady=(0, 5))
        
        self.label_subtitle = tk.Label(self.login_frame, text="Silakan masuk ke akun Anda", font=("Segoe UI", 10), bg="white", fg="#64748B")
        self.label_subtitle.pack(pady=(0, 25))
        
        # Input Username
        tk.Label(self.login_frame, text="Username", font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w", pady=(0, 5))
        self.entry_user = ttk.Entry(self.login_frame, width=32, font=("Segoe UI", 10))
        self.entry_user.pack(pady=(0, 15), ipady=5)
        
        # Input Password
        tk.Label(self.login_frame, text="Password", font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w", pady=(0, 5))
        self.entry_pass = ttk.Entry(self.login_frame, width=32, show="*", font=("Segoe UI", 10))
        self.entry_pass.pack(pady=(0, 25), ipady=5)
        
        # Tombol Login Modern (Indigo Blue)
        self.btn_login = tk.Button(self.login_frame, text="Masuk", width=28, bg="#2563EB", fg="white", 
                                   font=("Segoe UI", 10, "bold"), relief="flat", activebackground="#1D4ED8", activeforeground="white", cursor="hand2", command=self.proses_login)
        self.btn_login.pack(pady=(0, 15), ipady=4)
        
        # Tombol untuk pindah ke halaman Register
        self.btn_ke_register = tk.Button(self.login_frame, text="Belum punya akun? Daftar di sini", bg="white", fg="#2563EB",
                                         font=("Segoe UI", 9), relief="flat", activebackground="white", activeforeground="#1D4ED8", cursor="hand2", command=self.tampilkan_halaman_register)
        self.btn_ke_register.pack()

    def proses_login(self):
        username = self.entry_user.get()
        password = self.entry_pass.get()
        
        # Validasi dasar agar input tidak kosong
        if not username or not password:
            messagebox.showwarning("Peringatan", "Username dan Password tidak boleh kosong!")
            return
            
        hasil = ControllerAuth.login(username, password)
        
        if hasil["status"]:
            messagebox.showinfo("Sukses", hasil["message"])
            self.on_login_success(hasil["user"])
        else:
            messagebox.showerror("Error", hasil["message"])

    # =========================================================================
    # 2. HALAMAN REGISTRASI
    # =========================================================================
    def tampilkan_halaman_register(self):
        # Set judul window khusus registrasi
        self.parent.title("Sistem Absensi - Daftar Akun Baru")
        
        # Sembunyikan frame login
        if self.login_frame:
            self.login_frame.pack_forget()
            
        # Buat Card Container untuk Form Register
        self.reg_frame = tk.Frame(self.parent, padx=35, pady=35, bg="white")
        self.reg_frame.pack(expand=True, padx=30, pady=30)
        
        # Header text
        tk.Label(self.reg_frame, text="Daftar Akun", font=("Segoe UI", 18, "bold"), bg="white", fg="#0F172A").pack(pady=(0, 5))
        tk.Label(self.reg_frame, text="Lengkapi data di bawah ini", font=("Segoe UI", 9), bg="white", fg="#64748B").pack(pady=(0, 20))
        
        # Input Nama Lengkap
        tk.Label(self.reg_frame, text="Nama Lengkap", font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w", pady=(0, 5))
        self.entry_reg_nama = ttk.Entry(self.reg_frame, width=32, font=("Segoe UI", 10))
        self.entry_reg_nama.pack(pady=(0, 12), ipady=5)
        
        # Input Username Baru
        tk.Label(self.reg_frame, text="Username Baru", font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w", pady=(0, 5))
        self.entry_reg_user = ttk.Entry(self.reg_frame, width=32, font=("Segoe UI", 10))
        self.entry_reg_user.pack(pady=(0, 12), ipady=5)
        
        # Input Password
        tk.Label(self.reg_frame, text="Password", font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w", pady=(0, 5))
        self.entry_reg_pass = ttk.Entry(self.reg_frame, width=32, show="*", font=("Segoe UI", 10))
        self.entry_reg_pass.pack(pady=(0, 12), ipady=5)
        
        # Dropdown / Combobox Role
        tk.Label(self.reg_frame, text="Daftar Sebagai (Role)", font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w", pady=(0, 5))
        self.combo_reg_role = ttk.Combobox(self.reg_frame, values=["mahasiswa", "dosen"], state="readonly", font=("Segoe UI", 10), width=30)
        self.combo_reg_role.set("mahasiswa")
        self.combo_reg_role.pack(pady=(0, 25), ipady=2)
        
        # Tombol Submit Register (Emerald Green Modern)
        btn_submit_reg = tk.Button(self.reg_frame, text="Register Sekarang", width=28, bg="#0099FF", fg="white",
                                   font=("Segoe UI", 10, "bold"), relief="flat", activebackground="#06D4F8", activeforeground="white", cursor="hand2", command=self.proses_register)
        btn_submit_reg.pack(pady=(0, 15), ipady=4)
        
        # Tombol Kembali ke Login jika user membatalkan registrasi
        btn_kembali = tk.Button(self.reg_frame, text="Sudah punya akun? Login di sini", bg="white", fg="#64748B",
                                font=("Segoe UI", 9), relief="flat", activebackground="white", activeforeground="#475569", cursor="hand2", command=self.tampilkan_halaman_login)
        btn_kembali.pack()

    def proses_register(self):
        nama = self.entry_reg_nama.get()
        username = self.entry_reg_user.get()
        password = self.entry_reg_pass.get()
        role = self.combo_reg_role.get()
        
        # Validasi dasar agar form terisi semua
        if not nama or not username or not password or not role:
            messagebox.showwarning("Peringatan", "Semua kolom registrasi wajib diisi!")
            return
            
        hasil = ControllerAuth.register(username, password, nama, role)
        
        if hasil["status"]:
            messagebox.showinfo("Sukses", hasil["message"])
            # Setelah sukses mendaftar, otomatis dialihkan kembali ke halaman login
            self.tampilkan_halaman_login()
        else:
            messagebox.showerror("Error", hasil["message"])