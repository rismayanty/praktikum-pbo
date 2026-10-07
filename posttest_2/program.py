from datetime import datetime

# komposisi
class SlotPengisian:
    """class bagian dari komposisi stasiunpengisian"""
    def __init__(self, id_slot, tipe_charger):
        self.id_slot = id_slot
        self.tipe_charger = tipe_charger
        self.status = "kosong"
    
    def info_slot(self):
        return f"[{self.id_slot}] {self.tipe_charger} - Status: {self.status}"


# AGREGASI
class Karyawan:
    """class bagian dari agregasi stasiunpengisian"""
    def __init__(self, nama, nip, posisi):
        self.nama = nama
        self.nip = nip
        self.posisi = posisi
    
    def info_karyawan(self):
        return f"{self.nama} ({self.posisi}) - NIP: {self.nip}"


# ASOSIASI
class Pelanggan:
    """class untuk asosiasi"""
    def __init__(self, nama, nomor_member):
        self.nama = nama
        self.nomor_member = nomor_member

    def isi_daya_di_stasiun(self, stasiun, kendaraan):
        """asosiasi: stasiun dan kendaraan hanya dipakai sementara lewat parameter"""
        print(f"\n[ASOSIASI] pelanggan {self.nama} menggunakan {stasiun.nama} untuk mengisi {kendaraan.merek}")
        stasiun.tambah_kendaraan(1)
        kendaraan.mulai_pengisian(20)


# INHERITANCE-SUPERCLASS
class KendaraanListrik:
    """superclass / parent Class"""
    
    total_kendaraan = 0
    jenis_bahan_bakar = "listrik"
    
    def __init__(self, nomor_polisi, merek, model, kapasitas_baterai):
        self.nomor_polisi = nomor_polisi
        self.merek = merek
        self.model = model
        self.status = "tersedia"
        
        # PROTECTED
        self._kapasitas_baterai = kapasitas_baterai
        self._persentase_baterai = 0
        
        # PRIVATE
        self.__riwayat_pengisian = []
        self.__kode_rangka_rahasia = f"VR-{nomor_polisi}-SECRET"
    
    def mulai_pengisian(self, daya_kwh):
        """method dasar pengisian"""
        energi_maksimal = self._kapasitas_baterai - (self._persentase_baterai / 100 * self._kapasitas_baterai)
        
        if daya_kwh <= 0:
            print("[ERROR] daya pengisian harus lebih dari 0!")
            return False
        
        if daya_kwh > energi_maksimal:
            daya_kwh = energi_maksimal
        
        self._persentase_baterai = ((self._persentase_baterai / 100 * self._kapasitas_baterai) + daya_kwh) / self._kapasitas_baterai * 100

        self.__riwayat_pengisian.append({
            "tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "daya": daya_kwh
        })
        
        print(f"[CHARGING] {self.merek} {self.model} terisi {daya_kwh:.1f} kWh")
        print(f"    BATERAI: {self._persentase_baterai:.1f}%")
        return True

    def info_kendaraan(self):
        """method yang akan di-override oleh subclass"""
        print(f"\nkendaraan: {self.merek} {self.model}")
        print(f"polisi: {self.nomor_polisi}")
        print(f"baterai: {self._persentase_baterai:.1f}% / {self._kapasitas_baterai} kWh")
        print(f"jenis: {KendaraanListrik.jenis_bahan_bakar}")

    @property
    def riwayat_pengisian(self):
        return self.__riwayat_pengisian.copy()


class MobilListrik(KendaraanListrik):
    """subclass: mobil listrik"""
    def __init__(self, nomor_polisi, merek, model, kapasitas_baterai, jumlah_pintu):
        super().__init__(nomor_polisi, merek, model, kapasitas_baterai)

        self.jumlah_pintu = jumlah_pintu
        self.tipe_pengisian = "DC FAST CHARGING" 

    def info_kendaraan(self):
        super().info_kendaraan()
        print(f"[SPESIFIK MOBIL] jumlah pintu: {self.jumlah_pintu}")
        print(f"[SPESIFIK MOBIL] tipe pengisian: {self.tipe_pengisian}")
        print(f"[INFO] kapasitas baterai: {self._kapasitas_baterai} kWh")


class MotorListrik(KendaraanListrik):
    """subclass: motor listrik"""
    def __init__(self, nomor_polisi, merek, model, kapasitas_baterai, tipe_baterai):
        super().__init__(nomor_polisi, merek, model, kapasitas_baterai)
        
        self.tipe_baterai = tipe_baterai 

    def info_kendaraan(self):
        super().info_kendaraan()
        print(f"[SPESIFIK MOTOR] tipe baterai: {self.tipe_baterai} (lepas pasang)")


class StasiunPengisian:
    """class untuk mengelola stasiun pengisian kendaraan listrik"""
    
    total_stasiun = 0
    kota_operasional = "samarinda"
    
    def __init__(self, id_stasiun, nama, lokasi, jumlah_slot):
        self.id_stasiun = id_stasiun
        self.nama = nama
        self.lokasi = lokasi
        self.jumlah_slot = jumlah_slot
        self.slot_terisi = 0
        
        self.__kode_rahasia = f"SP-{id_stasiun}-2026"
        self.__saldo_kas = 0

        self.__daftar_slot = []
        for i in range(jumlah_slot):
            slot = SlotPengisian(f"SLOT-{i+1}", "FAST CHARGING 50kW")
            self.__daftar_slot.append(slot)

        self.__daftar_karyawan = []
        
        StasiunPengisian.total_stasiun += 1
    
    def tambah_kendaraan(self, jumlah=1):
        if self.slot_terisi + jumlah <= self.jumlah_slot:
            self.slot_terisi += jumlah
            print(f"[OK] {jumlah} kendaraan masuk ke {self.nama}")
            return True
        else:
            print(f"[ERROR] slot penuh!")
            return False
    
    def rekrut_karyawan(self, karyawan):
        if isinstance(karyawan, Karyawan):
            self.__daftar_karyawan.append(karyawan)
            print(f"[AGREGASI] {karyawan.nama} ditambahkan ke {self.nama}")

    def info_stasiun(self):
        print(f"\n{'='*50}")
        print(f"stasiun: {self.nama}")
        print(f"ID: {self.id_stasiun}")
        print(f"lokasi: {self.lokasi}")
        print(f"slot: {self.slot_terisi}/{self.jumlah_slot}")
        print(f"total slot fisik: {len(self.__daftar_slot)} slot")
        print(f"total karyawan: {len(self.__daftar_karyawan)} orang")
        print(f"kota: {StasiunPengisian.kota_operasional}")
        print(f"{'='*50}\n")

    @property
    def saldo_kas(self):
        return self.__saldo_kas
    
    @saldo_kas.setter
    def saldo_kas(self, jumlah):
        if jumlah < 0:
            raise ValueError("[ERROR] saldo kas tidak boleh negatif!")
        self.__saldo_kas = jumlah


class Transaksi:
    """class untuk mengelola transaksi pengisian daya"""
    total_transaksi = 0
    
    def __init__(self, id_transaksi, stasiun, kendaraan, daya_kwh, tarif_per_kwh):
        self.id_transaksi = id_transaksi
        self.stasiun = stasiun
        self.kendaraan = kendaraan
        self.daya_kwh = daya_kwh
        self.tarif_per_kwh = tarif_per_kwh
        self.__biaya = 0
        self.__status_bayar = "BELUM BAYAR"
    
    def hitung_total(self):
        self.__biaya = self.daya_kwh * self.tarif_per_kwh
        return self.__biaya
    
    def bayar(self):
        if self.__biaya <= 0:
            self.hitung_total()
        self.__status_bayar = "LUNAS"
        Transaksi.total_transaksi += 1
        print(f"[OK] pembayaran {self.id_transaksi} berhasil! Status: {self.__status_bayar}")

    def info_transaksi(self):
        print(f"\nTRANSAKSI {self.id_transaksi}")
        print(f"stasiun: {self.stasiun.nama}")
        print(f"kendaraan: {self.kendaraan.nomor_polisi}")
        print(f"total: Rp{self.__biaya:,.0f}")
        print(f"status: {self.__status_bayar}\n")


# MAIN
if __name__ == "__main__":
    print("="*60)
    print("SISTEM MANAJEMEN STASIUN PENGISIAN EV")
    print("="*60)
    
    # DEMONSTRASI INHERITANCE
    print("\n--- [TEST] INHERITANCE ---")
    
    mobil = MobilListrik("KT 1234 AB", "Hyundai", "Ioniq 5", 72.6, 4)
    motor = MotorListrik("KT 5678 CD", "Gesits", "Stella", 3.0, "Lepas Pasang")
    
    print("\n[INFO] memanggil method override pada mobillistrik:")
    mobil.info_kendaraan()
    
    print("\n[INFO] memanggil method override pada motorListrik:")
    motor.info_kendaraan()

    print(f"\n[CEK] apakah mobil adalah kendaraan listrik? {isinstance(mobil, KendaraanListrik)}")
    print(f"[CEK] apakah motor adalah kendaraan listrik? {isinstance(motor, KendaraanListrik)}")


    # DEMONSTRASI UML RELATIONSHIPS
    print("\n--- [TEST] UML RELATIONSHIPS ---")
    
    print("\n[TEST] KOMPOSISI (stasiun terdiri dari slot):")
    stasiun = StasiunPengisian("SP-001", "EV STATION UNMUL", "JL. M.YAMIN", 5)
    stasiun.info_stasiun()
    
    print("\n[TEST] AGREGASI (stasiun memiliki karyawan):")
    karyawan1 = Karyawan("Budi", "EMP01", "Teknisi")
    karyawan2 = Karyawan("Siti", "EMP02", "Kasir")
    
    stasiun.rekrut_karyawan(karyawan1)
    stasiun.rekrut_karyawan(karyawan2)
    stasiun.info_stasiun()
    
    print("[INFO] bukti agregasi: karyawan tetap ada meski stasiun dihapus.")
    print(f"   data karyawan: {karyawan1.info_karyawan()}")
    
    print("\n[TEST] ASOSIASI (pelanggan menggunakan Stasiun):")
    pelanggan = Pelanggan("Andi", "MEM-001")
    pelanggan.isi_daya_di_stasiun(stasiun, mobil)


    # DEMONSTRASI TRANSAKSI & ENCAPSULATION
    print("\n--- [TEST] TRANSAKSI & ENCAPSULATION ---")
    trx = Transaksi("TRX-001", stasiun, mobil, 20, 2500)
    trx.hitung_total()
    trx.bayar()
    trx.info_transaksi()

    print("\n[TEST] ENCAPSULATION:")
    print(f"riwayat pengisian: {mobil.riwayat_pengisian}")
    print("mencoba akses private __riwayat_pengisian langsung akan menyebabkan AttributeError.")

    print("\n" + "="*60)
    print("PROGRAM BERHASIL DIJALANKAN")
    print("="*60)