from datetime import datetime


class StasiunPengisian:
    """class untuk mengelola stasiun pengisian kendaraan listrik"""
    
    # ini atribut kelas
    total_stasiun = 0
    kota_operasional = "samarinda"
    versi_sistem = "1.0"
    
    def __init__(self, id_stasiun, nama, lokasi, jumlah_slot):
        # ini atribut publik
        self.id_stasiun = id_stasiun
        self.nama = nama
        self.lokasi = lokasi
        self.jumlah_slot = jumlah_slot
        self.slot_terisi = 0
        
        # ini atribut private
        self.__kode_rahasia = f"SP-{id_stasiun}-2026"
        self.__saldo_kas = 0
    
    # instance method
    def tambah_kendaraan(self, jumlah=1):
        """menambah jumlah kendaraan yang mengisi daya"""
        if self.slot_terisi + jumlah <= self.jumlah_slot:
            self.slot_terisi += jumlah
            print(f"[OK] {jumlah} kendaraan masuk ke {self.nama}")
            print(f"    slot terisi: {self.slot_terisi}/{self.jumlah_slot}")
            return True
        else:
            print(f"[ERROR] slot penuh! tersedia {self.jumlah_slot - self.slot_terisi} slot")
            return False
    
    def kurangi_kendaraan(self, jumlah=1):
        """mengurangi jumlah kendaraan setelah selesai charging"""
        if self.slot_terisi >= jumlah:
            self.slot_terisi -= jumlah
            print(f"[INFO] {jumlah} kendaraan keluar dari {self.nama}")
            return True
        return False
    
    def info_stasiun(self):
        """menampilkan informasi stasiun"""
        print(f"\n{'='*50}")
        print(f"Stasiun: {self.nama}")
        print(f"ID: {self.id_stasiun}")
        print(f"Lokasi: {self.lokasi}")
        print(f"Slot: {self.slot_terisi}/{self.jumlah_slot}")
        print(f"Kota: {StasiunPengisian.kota_operasional}")
        print(f"{'='*50}\n")
    
    # class method
    @classmethod
    def ubah_kota_operasional(cls, kota_baru):
        """mengubah kota operasional untuk semua stasiun"""
        cls.kota_operasional = kota_baru
        print(f"kota operasional diubah menjadi: {kota_baru}")
    
    @classmethod
    def dari_dict(cls, data):
        """factory method: membuat objek dari dictionary"""
        return cls(
            data["id_stasiun"],
            data["nama"],
            data["lokasi"],
            data["jumlah_slot"]
        )
    
    # static method
    @staticmethod
    def validasi_id_stasiun(id_stasiun):
        """validasi format ID stasiun (harus diawali SP-)"""
        return id_stasiun.startswith("SP-") and len(id_stasiun) >= 5
    
    @staticmethod
    def hitung_kapasitas_total(daftar_stasiun):
        """menghitung total kapasitas semua stasiun"""
        total = 0
        for stasiun in daftar_stasiun:
            total += stasiun.jumlah_slot
        return total
    
    # getter dan setter
    @property
    def kode_rahasia(self):
        """getter untuk kode_rahasia"""
        return self.__kode_rahasia
    
    @property
    def saldo_kas(self):
        """getter untuk saldo_kas"""
        return self.__saldo_kas
    
    @saldo_kas.setter
    def saldo_kas(self, jumlah):
        """setter untuk saldo_kas dengan validasi"""
        if jumlah < 0:
            raise ValueError("[ERROR] saldo kas tidak boleh negatif!")
        self.__saldo_kas = jumlah
        print(f"[INFO] saldo kas {self.nama} diperbarui: Rp{self.__saldo_kas:,.0f}")
    
    @saldo_kas.deleter
    def saldo_kas(self):
        """deleter untuk saldo_kas"""
        print(f"[WARNING] saldo kas {self.nama} akan dihapus")
        del self.__saldo_kas


class KendaraanListrik:
    """class untuk mengelola data kendaraan listrik"""
    
    # atribut kelas
    total_kendaraan = 0
    jenis_bahan_bakar = "listrik"
    emisi_karbon = 0
    
    def __init__(self, nomor_polisi, merek, model, kapasitas_baterai):
        # atribut instance
        self.nomor_polisi = nomor_polisi
        self.merek = merek
        self.model = model
        self.status = "tersedia"
        
        # atribut private
        self.__kapasitas_baterai = kapasitas_baterai
        self.__persentase_baterai = 0
        self.__riwayat_pengisian = []
    
    # instance method
    def mulai_pengisian(self, daya_kwh):
        """memulai proses pengisian baterai"""
        energi_maksimal = self.__kapasitas_baterai - (self.__persentase_baterai / 100 * self.__kapasitas_baterai)
        
        if daya_kwh <= 0:
            print("[ERROR] daya pengisian harus lebih dari 0!")
            return False
        
        if daya_kwh > energi_maksimal:
            print(f"[WARNING] daya {daya_kwh} kWh melebihi kapasitas tersisa ({energi_maksimal:.1f} kWh)")
            daya_kwh = energi_maksimal
        
        self.__persentase_baterai = ((self.__persentase_baterai / 100 * self.__kapasitas_baterai) + daya_kwh) / self.__kapasitas_baterai * 100
        
        self.__riwayat_pengisian.append({
            "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "daya": daya_kwh
        })
        
        print(f"[CHARGING] {self.merek} {self.model} terisi {daya_kwh:.1f} kWh")
        print(f"    BATERAI: {self.__persentase_baterai:.1f}%")
        return True
    
    def selesai_pengisian(self):
        """menandai pengisian selesai"""
        self.status = "tersedia"
        print(f"[OK] pengisian {self.nomor_polisi} selesai")
    
    def info_kendaraan(self):
        """menampilkan informasi kendaraan"""
        print(f"\nkendaraan: {self.merek} {self.model}")
        print(f"polisi: {self.nomor_polisi}")
        print(f"baterai: {self.__persentase_baterai:.1f}% / {self.__kapasitas_baterai} kWh")
        print(f"status: {self.status}")
        print(f"jenis: {KendaraanListrik.jenis_bahan_bakar}")
    
    # class method
    @classmethod
    def ubah_jenis_bahan_bakar(cls, jenis):
        """mengubah jenis bahan bakar"""
        cls.jenis_bahan_bakar = jenis
    
    @classmethod
    def reset_total_kendaraan(cls):
        """reset counter total kendaraan"""
        cls.total_kendaraan = 0
        print("[INFO] total kendaraan direset")
    
    # static method
    @staticmethod
    def validasi_nomor_polisi(nopol):
        """validasi format nomor polisi"""
        return len(nopol) >= 5 and nopol.replace(" ", "").isalnum()
    
    @staticmethod
    def hitung_jarak_tempuh(kapasitas_kwh, efisiensi_km_per_kwh=6):
        """mengestimasi jarak tempuh berdasarkan kapasitas baterai"""
        return kapasitas_kwh * efisiensi_km_per_kwh
    
    # getter dan setter
    @property
    def kapasitas_baterai(self):
        """getter untuk kapasitas_baterai"""
        return self.__kapasitas_baterai
    
    @property
    def persentase_baterai(self):
        """getter untuk persentase_baterai"""
        return self.__persentase_baterai
    
    @persentase_baterai.setter
    def persentase_baterai(self, persen):
        """setter untuk persentase_baterai dengan validasi"""
        if persen < 0 or persen > 100:
            raise ValueError("[ERROR] persentase baterai harus antara 0-100!")
        self.__persentase_baterai = persen
        print(f"[INFO] Baterai diperbarui: {persen}%")
    
    @property
    def riwayat_pengisian(self):
        """getter untuk riwayat_pengisian"""
        return self.__riwayat_pengisian.copy()


class Transaksi:
    """class untuk mengelola transaksi pengisian daya"""
    
    # atribut kelas
    total_transaksi = 0
    total_pendapatan = 0
    prefix_id = "TRX"
    
    def __init__(self, id_transaksi, stasiun, kendaraan, daya_kwh, tarif_per_kwh):
        # atribut instance
        self.id_transaksi = id_transaksi
        self.stasiun = stasiun
        self.kendaraan = kendaraan
        self.daya_kwh = daya_kwh
        self.tarif_per_kwh = tarif_per_kwh
        self.waktu_transaksi = datetime.now()
        
        # atribut private
        self.__biaya = 0
        self.__status_bayar = "BELUM BAYAR"
        self.__diskon = 0
    
    # instance method
    def hitung_total(self):
        """menghitung total biaya transaksi"""
        subtotal = self.daya_kwh * self.tarif_per_kwh
        self.__biaya = subtotal - self.__diskon
        print(f"[COST] total biaya: Rp{self.__biaya:,.0f}")
        print(f"    detail: {self.daya_kwh} kWh x Rp{self.tarif_per_kwh:,.0f} = Rp{subtotal:,.0f}")
        if self.__diskon > 0:
            print(f"    diskon: -Rp{self.__diskon:,.0f}")
        return self.__biaya
    
    def bayar(self):
        """proses pembayaran"""
        if self.__biaya <= 0:
            self.hitung_total()
        
        self.__status_bayar = "LUNAS"
        Transaksi.total_transaksi += 1
        Transaksi.total_pendapatan += self.__biaya
        
        print(f"[OK] pembayaran berhasil!")
        print(f"    status: {self.__status_bayar}")
        print(f"    total transaksi: {Transaksi.total_transaksi}")
        return True
    
    def info_transaksi(self):
        """menampilkan informasi transaksi"""
        print(f"\n{'='*50}")
        print(f"TRANSAKSI {self.id_transaksi}")
        print(f"{'='*50}")
        print(f"waktu: {self.waktu_transaksi.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"stasiun: {self.stasiun.nama}")
        print(f"kendaraan: {self.kendaraan.nomor_polisi} ({self.kendaraan.merek})")
        print(f"daya: {self.daya_kwh} kWh")
        print(f"tarif: Rp{self.tarif_per_kwh:,.0f}/kWh")
        print(f"total: Rp{self.__biaya:,.0f}")
        print(f"status: {self.__status_bayar}")
        print(f"{'='*50}\n")
    
    # class method
    @classmethod
    def ubah_prefix_id(cls, prefix_baru):
        """mengubah prefix ID transaksi"""
        cls.prefix_id = prefix_baru
        print(f"[INFO] prefix ID diubah menjadi: {prefix_baru}")
    
    @classmethod
    def get_statistik(cls):
        """menampilkan statistik transaksi"""
        print(f"\nSTATISTIK TRANSAKSI")
        print(f"    total transaksi: {cls.total_transaksi}")
        print(f"    total pendapatan: Rp{cls.total_pendapatan:,.0f}")
        if cls.total_transaksi > 0:
            rata_rata = cls.total_pendapatan / cls.total_transaksi
            print(f"    rata-rata per transaksi: Rp{rata_rata:,.0f}")
        print()
    
    # static method
    @staticmethod
    def validasi_id_transaksi(id_transaksi):
        """validasi format ID transaksi"""
        return id_transaksi.startswith("TRX") and len(id_transaksi) >= 6
    
    @staticmethod
    def hitung_diskon_persen(total, persen):
        """menghitung diskon berdasarkan persentase"""
        if persen < 0 or persen > 100:
            raise ValueError("persentase diskon harus 0-100")
        return total * (persen / 100)
    
    # getter dan setter
    @property
    def biaya(self):
        """getter untuk biaya"""
        return self.__biaya
    
    @property
    def status_bayar(self):
        """getter untuk status_bayar"""
        return self.__status_bayar
    
    @property
    def diskon(self):
        """getter untuk diskon"""
        return self.__diskon
    
    @diskon.setter
    def diskon(self, nilai_diskon):
        """setter untuk diskon dengan validasi"""
        if nilai_diskon < 0:
            raise ValueError("[ERROR] diskon tidak boleh negatif!")
        
        subtotal = self.daya_kwh * self.tarif_per_kwh
        if nilai_diskon > subtotal:
            raise ValueError("[ERROR] diskon tidak boleh lebih besar dari subtotal!")
        
        self.__diskon = nilai_diskon
        print(f"[INFO] diskon diterapkan: Rp{nilai_diskon:,.0f}")


# --> main program
if __name__ == "__main__":
    print("="*60)
    print("SISTEM MANAJEMEN STASIUN PENGISIAN KENDARAAN LISTRIK")
    print("KOTA SAMARINDA")
    print("="*60)
    
    # DEMONSTRASI CLASS (stasiunpengisian)
    print("\n" + "="*60)
    print("CLASS StasiunPengisian")
    print("="*60)
    
    stasiun1 = StasiunPengisian("SP-001", "EV STATION UNMUL", "JL. M.YAMIN", 10)
    stasiun2 = StasiunPengisian("SP-002", "EV STATION TEPIAN", "JL. GADJAH MADA", 8)
    
    print("\n[TEST] validasi ID stasiun:")
    print(f"  SP-001 valid? {StasiunPengisian.validasi_id_stasiun('SP-001')}")
    print(f"  ABC valid? {StasiunPengisian.validasi_id_stasiun('ABC')}")
    
    stasiun1.info_stasiun()
    stasiun1.tambah_kendaraan(3)
    stasiun1.tambah_kendaraan(2)
    stasiun1.kurangi_kendaraan(1)
    
    print("\n[TEST] setter saldo_kas dengan data valid:")
    stasiun1.saldo_kas = 5000000
    
    print("\n[TEST] setter saldo_kas dengan data tidak valid:")
    try:
        stasiun1.saldo_kas = -1000000
    except ValueError as e:
        print(f"  {e}")
    
    print("\n[TEST] class method - ubah kota operasional:")
    StasiunPengisian.ubah_kota_operasional("samarinda-seberang")
    stasiun2.info_stasiun()
    
    print("\n[TEST] factory method - dari_dict:")
    data_stasiun = {
        "id_stasiun": "SP-003",
        "nama": "EV station Loa Janan",
        "lokasi": "JL. Raya Loa Janan",
        "jumlah_slot": 6
    }
    stasiun3 = StasiunPengisian.dari_dict(data_stasiun)
    stasiun3.info_stasiun()
    
    # DEMONSTRASI CLASS (kendaraanlistrik)
    print("\n" + "="*60)
    print("CLASS KendaraanListrik")
    print("="*60)
    
    mobil1 = KendaraanListrik("KT 1234 AB", "Hyundai", "Ioniq 5", 72.6)
    motor1 = KendaraanListrik("KT 5678 CD", "Gesits", "Stella", 3.0)
    
    print("\n[TEST] validasi nomor polisi:")
    print(f"  KT 1234 AB valid? {KendaraanListrik.validasi_nomor_polisi('KT 1234 AB')}")
    print(f"  @#$ valid? {KendaraanListrik.validasi_nomor_polisi('@#$')}")
    
    print("\n[TEST] hitung estimasi jarak tempuh:")
    jarak_mobil = KendaraanListrik.hitung_jarak_tempuh(72.6)
    print(f"  Mobil 72.6 kWh: ~{jarak_mobil} km")
    
    mobil1.info_kendaraan()
    print("\n[TEST] mulai pengisian:")
    mobil1.mulai_pengisian(20)
    mobil1.mulai_pengisian(30)
    
    print("\n[TEST] setter persentase_baterai dengan data valid:")
    mobil1.persentase_baterai = 85
    
    print("\n[TEST] setter persentase_baterai dengan data tidak valid (>100):")
    try:
        mobil1.persentase_baterai = 150
    except ValueError as e:
        print(f"  {e}")
    
    print("\n[TEST] class method - reset total kendaraan:")
    KendaraanListrik.total_kendaraan = 5
    KendaraanListrik.reset_total_kendaraan()
    
    # DEMONSTRASI CLASS (transaksi)
    print("\n" + "="*60)
    print("CLASS Transaksi")
    print("="*60)
    
    trx1 = Transaksi("TRX-001", stasiun1, mobil1, 20, 2500)
    trx2 = Transaksi("TRX-002", stasiun2, motor1, 3, 1500)
    
    print("\n[TEST] validasi ID transaksi:")
    print(f"  TRX-001 valid? {Transaksi.validasi_id_transaksi('TRX-001')}")
    print(f"  ABC valid? {Transaksi.validasi_id_transaksi('ABC')}")
    
    print("\n[TEST] hitung diskon 10% dari Rp100.000:")
    diskon = Transaksi.hitung_diskon_persen(100000, 10)
    print(f"  diskon: Rp{diskon:,.0f}")
    
    trx1.info_transaksi()
    print("\n[TEST] hitung total dan bayar:")
    trx1.hitung_total()
    trx1.bayar()
    
    print("\n[TEST] setter diskon dengan data valid:")
    trx2.diskon = 1000
    
    print("\n[TEST] setter diskon dengan data tidak valid:")
    try:
        trx2.diskon = -500
    except ValueError as e:
        print(f"  {e}")
    
    print("\n[TEST] setter diskon dengan data tidak valid:")
    try:
        trx2.diskon = 1000000
    except ValueError as e:
        print(f"  {e}")
    
    print("\n[TEST] class method - statistik transaksi:")
    Transaksi.get_statistik()
    
    trx2.hitung_total()
    trx2.bayar()
    
    Transaksi.get_statistik()
    
    #  RINGKASAN SISTEM
    print("\n" + "="*60)
    print("RINGKASAN SISTEM")
    print("="*60)
    
    daftar_stasiun = [stasiun1, stasiun2, stasiun3]
    total_kapasitas = StasiunPengisian.hitung_kapasitas_total(daftar_stasiun)
    print(f"\ntotal kapasitas semua stasiun: {total_kapasitas} slot")
    print(f"kota operasional: {StasiunPengisian.kota_operasional}")
    print(f"jenis bahan bakar: {KendaraanListrik.jenis_bahan_bakar}")
    
    print("\n" + "="*60)
    print("PROGRAM BERHASIL DIJALANKAN")
    print("="*60)