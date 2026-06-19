import tkinter as tk
from tkinter import messagebox, ttk
from controllers.controller_absensi import ControllerAbsensi
from controllers.controller_report import ControllerReport

class MahasiswaDashboard:
    def __init__(self, parent, user_data, logout_callback):
        self.parent = parent
        self.user = user_data
        self.logout_callback = logout_callback
        
        self.parent.title(f"Dashboard Mahasiswa - {self.user['username']}")
        self.parent.geometry("700x680") 
        self.parent.configure(bg="#F1F5F9") # Background Slate 100 (Warna dasar abu-abu bersih)
        
        # --- Mengatur Global Modern Style untuk TTK ---
        style = ttk.Style()
        style.theme_use("clam")
        
        # Konfigurasi Input Modern
        style.configure("TCombobox", fieldbackground="white", background="#CBD5E1")
        
        # Konfigurasi Tabel Modern (Treeview) - Menggunakan tema Navy/Slate
        style.configure("Treeview", 
                        background="white", 
                        foreground="#1E293B", 
                        rowheight=32, # Lebih tinggi sedikit agar lega
                        fieldbackground="white",
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading", 
                        background="#1E293B", # Header Tabel Navy Gelap
                        foreground="white", 
                        relief="flat",
                        font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", "#E2E8F0")], foreground=[("selected", "#0F172A")])

        # --- 1. HEADER FRAME (Top Bar - Slate Sangat Gelap) ---
        self.header_frame = tk.Frame(self.parent, bg="#0F172A", padx=25, pady=18)
        self.header_frame.pack(fill="x")
        
        self.label_welcome = tk.Label(
            self.header_frame, 
            text=f"🎓  {self.user['username'].upper()}", 
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
        
        # --- 2. CARD STATISTIK (Warna teks utama diubah ke Biru Link Modern, bukan hijau) ---
        self.card_stats = tk.Frame(self.parent, bg="white", padx=20, pady=18)
        self.card_stats.pack(fill="x", padx=25, pady=(20, 10))
        
        tk.Label(self.card_stats, text="📊 RINGKASAN PERSENTASE KEHADIRAN", 
                 font=("Segoe UI", 9, "bold"), bg="white", fg="#64748B").pack(anchor="w", pady=(0, 5))
                 
        self.label_persen = tk.Label(
            self.card_stats, text="Memuat data statistik...", 
            font=("Segoe UI", 12, "bold"), fg="#2563EB", bg="white" # Diubah ke Royal Blue modern
        )
        self.label_persen.pack(anchor="w")
        
        # --- 3. CARD FORM ABSENSI (Menggunakan tema Blue Accent) ---
        self.card_absen = tk.Frame(self.parent, bg="white", padx=20, pady=20)
        self.card_absen.pack(fill="x", padx=25, pady=10)
        
        tk.Label(self.card_absen, text="📝 FORMULIR PRESENSI", 
                 font=("Segoe UI", 10, "bold"), bg="white", fg="#0F172A").pack(anchor="w", pady=(0, 15))
        
        # Grid layout horizontal
        form_grid = tk.Frame(self.card_absen, bg="white")
        form_grid.pack(fill="x")
        
        # Dropdown Status
        status_frame = tk.Frame(form_grid, bg="white")
        status_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(status_frame, text="Status", font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w", pady=(0, 5))
        self.combo_status = ttk.Combobox(status_frame, values=["Hadir", "Izin", "Sakit"], state="readonly", font=("Segoe UI", 10))
        self.combo_status.set("Hadir")
        self.combo_status.pack(fill="x", ipady=2)
        
        # Kolom Keterangan
        ket_frame = tk.Frame(form_grid, bg="white")
        ket_frame.pack(side="left", fill="x", expand=True, padx=(10, 0))
        tk.Label(ket_frame, text="Keterangan (Wajib jika S/I)", font=("Segoe UI", 9, "bold"), bg="white", fg="#475569").pack(anchor="w", pady=(0, 5))
        self.entry_ket = ttk.Entry(ket_frame, font=("Segoe UI", 10))
        self.entry_ket.pack(fill="x", ipady=4)
        
        # Tombol Kirim Kehadiran (Warna Navy Blue Modern)
        self.btn_submit = tk.Button(
            self.card_absen, text="Kirim Kehadiran", font=("Segoe UI", 10, "bold"),
            bg="#1E40AF", fg="white", relief="flat", activebackground="#1E3A8A", activeforeground="white",
            cursor="hand2", command=self.proses_absen
        )
        self.btn_submit.pack(fill="x", pady=(20, 0), ipady=5)
        
        # --- 4. CARD TABEL RIWAYAT ---
        self.card_riwayat = tk.Frame(self.parent, bg="white", padx=20, pady=20)
        self.card_riwayat.pack(fill="both", expand=True, padx=25, pady=(10, 25))
        
        tk.Label(self.card_riwayat, text="🕒 RIWAYAT KEHADIRAN", 
                 font=("Segoe UI", 10, "bold"), bg="white", fg="#0F172A").pack(anchor="w", pady=(0, 10))
        
        # Kontainer Tabel
        self.table_frame = tk.Frame(self.card_riwayat, bg="white")
        self.table_frame.pack(fill="both", expand=True)

        columns = ("tanggal", "waktu", "status", "keterangan")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        
        scrollbar = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.heading("tanggal", text="Tanggal")
        self.tree.heading("waktu", text="Jam Presensi")
        self.tree.heading("status", text="Status")
        self.tree.heading("keterangan", text="Keterangan")
        
        self.tree.column("tanggal", width=120, anchor="center")
        self.tree.column("waktu", width=100, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        self.tree.column("keterangan", width=250, anchor="w")
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        self.refresh_data()

    def proses_absen(self):
        status = self.combo_status.get()
        keterangan = self.entry_ket.get().strip()
        
        if status in ["Izin", "Sakit"] and not keterangan:
            messagebox.showwarning("Peringatan", "Keterangan wajib diisi jika Anda memilih Izin atau Sakit!")
            return
            
        hasil = ControllerAbsensi.lakukan_absen(self.user['id'], status, keterangan)
        
        if hasil["status"]:
            messagebox.showinfo("Sukses", hasil["message"])
            self.entry_ket.delete(0, tk.END) 
            self.refresh_data() 
        else:
            messagebox.showerror("Error", hasil["message"])

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        riwayat = ControllerAbsensi.ambil_riwayat_mahasiswa(self.user['id'])
        for data in riwayat:
            self.tree.insert("", tk.END, values=(data['tanggal'], data['waktu'], data['status'], data['keterangan']))
            
        stats = ControllerReport.hitung_persentase_kehadiran(self.user['id'])
        self.label_persen.config(
            text=f"{stats['Persentase']}  │  (Hadir: {stats['Hadir']}  •  Sakit: {stats['Sakit']}  •  Izin: {stats['Izin']})"
        )

    def proses_logout(self):
        if messagebox.askyesno("Logout", "Apakah Anda yakin ingin keluar?"):
            self.logout_callback()