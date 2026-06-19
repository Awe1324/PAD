import tkinter as tk
from tkinter import messagebox, ttk
from controllers.controller_absensi import ControllerAbsensi
from controllers.controller_report import ControllerReport

class DosenDashboard:
    def __init__(self, parent, user_data, logout_callback):
        self.parent = parent
        self.user = user_data
        self.logout_callback = logout_callback
        
        self.parent.title(f"Dashboard Dosen - {self.user['username']}")
        self.parent.geometry("950x680") 
        self.parent.configure(bg="#F1F5F9") # Background dasar Slate 100 yang bersih
        
        # --- Mengatur Global Modern Style untuk TTK ---
        style = ttk.Style()
        style.theme_use("clam")
        
        # Konfigurasi Tabel Modern (Treeview)
        style.configure("Treeview", 
                        background="white", 
                        foreground="#1E293B", 
                        rowheight=32, # Jarak baris tabel lebih lega dan tidak menumpuk
                        fieldbackground="white",
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading", 
                        background="#1E293B", # Header Tabel Navy Gelap Professional
                        foreground="white", 
                        relief="flat",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#E2E8F0")], foreground=[("selected", "#0F172A")])

        # --- 1. HEADER FRAME (Top Bar - Dark Slate) ---
        self.header_frame = tk.Frame(self.parent, bg="#0F172A", padx=25, pady=18)
        self.header_frame.pack(fill="x")
        
        self.label_welcome = tk.Label(
            self.header_frame, 
            text=f"👨‍🏫  PANEL DOSEN : {self.user['username'].upper()}", 
            font=("Segoe UI", 13, "bold"), fg="#F8FAFC", bg="#0F172A"
        )
        self.label_welcome.pack(side="left")
        
        self.btn_logout = tk.Button(
            self.header_frame, text="Keluar Akun", font=("Segoe UI", 9, "bold"),
            bg="#334155", fg="#F8FAFC", relief="flat", padx=18, pady=6,
            activebackground="#475569", activeforeground="white",
            cursor="hand2", command=self.proses_logout
        )
        self.btn_logout.pack(side="right")
        
        # --- 2. KONTEN UTAMA (Menggunakan Split Grid Frame) ---
        self.content_frame = tk.Frame(self.parent, bg="#F1F5F9")
        self.content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # --- FRAME KIRI: Kelola Mata Kuliah (Modern Card Layout) ---
        self.left_card = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        self.left_card.pack(side="left", fill="y", padx=(0, 15))
        
        tk.Label(self.left_card, text="📚 KELOLA MATAKULIAH", 
                 font=("Segoe UI", 10, "bold"), bg="white", fg="#0F172A").pack(anchor="w", pady=(0, 15))
        
        tk.Label(self.left_card, text="Nama Mata Kuliah", font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w", pady=(0, 5))
        self.entry_matkul = ttk.Entry(self.left_card, font=("Segoe UI", 10), width=25)
        self.entry_matkul.pack(pady=(0, 15), ipady=4)
        
        self.btn_simpan_matkul = tk.Button(
            self.left_card, text="Tambah Matkul", font=("Segoe UI", 10, "bold"),
            bg="#2563EB", fg="white", relief="flat", activebackground="#1D4ED8",
            cursor="hand2", command=self.proses_tambah_matkul
        )
        self.btn_simpan_matkul.pack(fill="x", ipady=4)
        
        # --- FRAME KANAN: Tabel & Aksi Rekapitulasi (Modern Card Layout) ---
        self.main_card = tk.Frame(self.content_frame, bg="white", padx=20, pady=20)
        self.main_card.pack(side="right", fill="both", expand=True)
        
        tk.Label(self.main_card, text="📋 REKAPITULASI ABSENSI MAHASISWA", 
                 font=("Segoe UI", 10, "bold"), bg="white", fg="#0F172A").pack(anchor="w", pady=(0, 15))
        
        # Top Bar Aksi (Hanya berisi Refresh & Cetak Laporan saja)
        self.action_frame = tk.Frame(self.main_card, bg="white")
        self.action_frame.pack(fill="x", pady=(0, 15))
        
        self.btn_refresh = tk.Button(
            self.action_frame, text="🔄 Refresh Data", font=("Segoe UI", 9, "bold"),
            bg="#475569", fg="white", relief="flat", padx=15, pady=6,
            activebackground="#334155", cursor="hand2", command=self.refresh_tabel
        )
        self.btn_refresh.pack(side="left", padx=(0, 8))
        
        self.btn_report = tk.Button(
            self.action_frame, text="📄 Cetak Laporan", font=("Segoe UI", 9, "bold"),
            bg="#EA580C", fg="white", relief="flat", padx=15, pady=6,
            activebackground="#C2410C", cursor="hand2", command=self.cetak_laporan
        )
        self.btn_report.pack(side="left")
        
        # Kontainer Tabel Riwayat Absen dengan Scrollbar
        self.table_frame = tk.Frame(self.main_card, bg="white")
        self.table_frame.pack(fill="both", expand=True)

        columns = ("id", "nama", "tanggal", "waktu", "status", "keterangan")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.heading("id", text="ID Absen")
        self.tree.heading("nama", text="Nama Mahasiswa")
        self.tree.heading("tanggal", text="Tanggal")
        self.tree.heading("waktu", text="Jam")
        self.tree.heading("status", text="Status")
        self.tree.heading("keterangan", text="Keterangan")
        
        self.tree.column("id", width=70, anchor="center")
        self.tree.column("nama", width=140, anchor="w")
        self.tree.column("tanggal", width=100, anchor="center")
        self.tree.column("waktu", width=90, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        self.tree.column("keterangan", width=160, anchor="w")
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Muat data pertama kali saat dashboard dibuka
        self.refresh_tabel()

    def proses_tambah_matkul(self):
        nama_matkul = self.entry_matkul.get().strip()
        if not nama_matkul:
            messagebox.showwarning("Peringatan", "Nama mata kuliah tidak boleh kosong!")
            return
            
        hasil = ControllerAbsensi.tambah_matakuliah(nama_matkul, self.user['id'])
        
        if hasil["status"]:
            messagebox.showinfo("Sukses", hasil["message"])
            self.entry_matkul.delete(0, tk.END)
        else:
            messagebox.showerror("Error", hasil["message"])

    def refresh_tabel(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        semua_absen = ControllerAbsensi.ambil_rekap_dosen()
        
        for data in semua_absen:
            self.tree.insert("", tk.END, values=(
                data['id'], 
                data['username'],  
                data['tanggal'], 
                data['waktu'], 
                data['status'], 
                data['keterangan']
            ))

    def cetak_laporan(self):
        data_laporan = ControllerReport.generate_rekap_bulanan()
        total_data = len(data_laporan)
        messagebox.showinfo("Cetak Laporan", f"Berhasil menarik {total_data} data absensi untuk dicetak!")

    def proses_logout(self):
        if messagebox.askyesno("Logout", "Apakah Anda yakin ingin keluar?"):
            self.logout_callback()