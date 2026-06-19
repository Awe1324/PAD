from models.model_absensi import Absensi

class ControllerReport:
    @staticmethod
    def hitung_persentase_kehadiran(user_id):
        """
        Menghitung total status absen (Hadir, Sakit, Izin, Alpa) 
        dan persentase kehadiran untuk satu mahasiswa tertentu.
        """
        riwayat = Absensi.get_riwayat_by_user_id(user_id)
        total_hari = len(riwayat)
        
        if total_hari == 0:
            return {
                "Hadir": 0, "Sakit": 0, "Izin": 0, "Alpa": 0,
                "Persentase": "0%"
            }
            
        # Hitung kemunculan masing-masing status
        rekap = {"Hadir": 0, "Sakit": 0, "Izin": 0, "Alpa": 0}
        for absen in riwayat:
            status = absen['status']
            if status in rekap:
                rekap[status] += 1
                
        # Menghitung persentase kehadiran (Hadir / Total Hari) * 100
        persentase = (rekap["Hadir"] / total_hari) * 100
        rekap["Persentase"] = f"{int(persentase)}%"
        
        return rekap

    @staticmethod
    def generate_rekap_bulanan():
        """
        Mengambil semua data absensi untuk kebutuhan cetak/tampilan laporan dosen.
        Di sini data bisa difilter atau langsung diambil dari semua riwayat.
        """
        # Mengambil data mentah dari database lewat model absensi
        semua_data = Absensi.get_semua_absen_untuk_dosen()
        
        # Di sini kamu bisa menambahkan logika tambahan jika ingin memfilter 
        # berdasarkan bulan tertentu sebelum dilempar ke View (Tampilan).
        return semua_data