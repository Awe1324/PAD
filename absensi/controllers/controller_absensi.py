from models.model_absensi import Absensi

class ControllerAbsensi:
    """Controller untuk mengatur logika bisnis terkait Absensi dan Mata Kuliah"""

    @staticmethod
    def lakukan_absen(user_id, status, keterangan=""):
        """Validasi data absen mahasiswa sebelum dikirim ke model"""
        if not status:
            return {"status": False, "message": "Status kehadiran harus dipilih!"}
            
        # Aturan bisnis: Jika Izin atau Sakit, wajib mengisi kolom keterangan
        if status in ["Izin", "Sakit"] and not keterangan.strip():
            return {"status": False, "message": f"Keterangan wajib diisi jika status {status}!"}
            
        # Mengirim data valid ke Model Absensi
        return Absensi.catat_absen(user_id, status, keterangan.strip())

    @staticmethod
    def ambil_riwayat_mahasiswa(user_id):
        """Mengambil riwayat absensi khusus untuk mahasiswa yang sedang login"""
        return Absensi.get_riwayat_by_user_id(user_id)

    @staticmethod
    def ambil_rekap_dosen():
        """Mengambil seluruh data absensi mahasiswa untuk keperluan panel dosen"""
        return Absensi.get_semua_absen_untuk_dosen()

    @staticmethod
    def tambah_matakuliah(nama_matkul, dosen_id):
        """Validasi data mata kuliah baru dari dosen sebelum disimpan ke database"""
        if not nama_matkul.strip():
            return {"status": False, "message": "Nama mata kuliah tidak boleh kosong!"}
            
        if len(nama_matkul.strip()) < 3:
            return {"status": False, "message": "Nama mata kuliah minimal harus 3 karakter!"}
        
        # Import lokal di dalam fungsi untuk menghindari masalah circular import di Python
        from models.model_absensi import MataKuliah
        return MataKuliah.tambah_matkul(nama_matkul.strip(), dosen_id)
    