from datetime import datetime
from abc import ABC, abstractmethod


class SlotPengisian:
    def __init__(self, id_slot, tipe_charger):
        self.id_slot = id_slot
        self.tipe_charger = tipe_charger
        self.status = "kosong"
    
    def info_slot(self):
        return f"[{self.id_slot}] {self.tipe_charger} - status: {self.status}"

class Karyawan:
    def __init__(self, nama, nip, posisi):
        self.nama = nama
        self.nip = nip
        self.posisi = posisi
    
    def info_karyawan(self):
        return f"{self.nama} ({self.posisi}) - NIP: {self.nip}"

class Pelanggan:
    def __init__(self, nama, nomor_member):
        self.nama = nama
        self.nomor_member = nomor_member

    def isi_daya_di_stasiun(self, stasiun, kendaraan):
        print(f"\n[ASOSIASI] pelanggan {self.nama} menggunakan {stasiun.nama} untuk mengisi {kendaraan.merek}")
        stasiun.tambah_kendaraan(1)
        kendaraan.mulai_pengisian(20)


class MetodePembayaran(ABC):
    
    @abstractmethod
    def proses_pembayaran(self, nominal):
        pass
    
    @abstractmethod
    def cetak_struk(self, id_transaksi):
        pass

class PembayaranQRIS(MetodePembayaran):
    def __init__(self, nomor_qris):
        self.nomor_qris = nomor_qris
    
    def proses_pembayaran(self, nominal):
        print(f"[QRIS] pembayaran Rp{nominal:,.0f} via {self.nomor_qris} - BERHASIL")
        return True
    
    def cetak_struk(self, id_transaksi):
        print(f"[STRUK] transaksi {id_transaksi} dibayar via QRIS")

class PembayaranKartu(MetodePembayaran):
    def __init__(self, nomor_kartu):
        self.nomor_kartu = nomor_kartu
    
    def proses_pembayaran(self, nominal):
        print(f"[KARTU] pembayaran Rp{nominal:,.0f} via Kartu {self.nomor_kartu} - BERHASIL")
        return True
    
    def cetak_struk(self, id_transaksi):
        print(f"[STRUK] transaksi {id_transaksi} dibayar via Kartu")

class NotifikasiEmail:
    def __init__(self, alamat_email):
        self.alamat_email = alamat_email
    def kirim(self, pesan):
        print(f"  [EMAIL -> {self.alamat_email}] {pesan}")

class NotifikasiSMS:
    def __init__(self, nomor_hp):
        self.nomor_hp = nomor_hp
    def kirim(self, pesan):
        print(f"  [SMS -> {self.nomor_hp}] {pesan}")

def kirim_notifikasi_ke_pelanggan(daftar_notif, pesan):
    for notif in daftar_notif:
        notif.kirim(pesan)


class KendaraanListrik:
    total_kendaraan = 0
    jenis_bahan_bakar = "listrik"
    
    def __init__(self, nomor_polisi, merek, model, kapasitas_baterai):
        self.nomor_polisi = nomor_polisi
        self.merek = merek
        self.model = model
        self.status = "tersedia"
        
        self._kapasitas_baterai = kapasitas_baterai # Protected
        self._persentase_baterai = 0                # Protected
        self.__riwayat_pengisian = []               # Private
        
        KendaraanListrik.total_kendaraan += 1
    
    def mulai_pengisian(self, daya_kwh):
        energi_maksimal = self._kapasitas_baterai - (self._persentase_baterai / 100 * self._kapasitas_baterai)
        if daya_kwh <= 0:
            print("[ERROR] daya pengisian harus lebih dari 0!")
            return False
        if daya_kwh > energi_maksimal:
            daya_kwh = energi_maksimal
        
        self._persentase_baterai = ((self._persentase_baterai / 100 * self._kapasitas_baterai) + daya_kwh) / self._kapasitas_baterai * 100
        self.__riwayat_pengisian.append({"tanggal": datetime.now().strftime("%Y-%m-%d %H:%M"), "daya": daya_kwh})
        print(f"[CHARGING] {self.merek} {self.model} terisi {daya_kwh:.1f} kWh | Baterai: {self._persentase_baterai:.1f}%")
        return True

    def info_kendaraan(self):
        print(f"\nkendaraan: {self.merek} {self.model} | polisi: {self.nomor_polisi} | baterai: {self._persentase_baterai:.1f}%")

    # magic methods
    def __str__(self):
        return f"{self.merek} {self.model} ({self.nomor_polisi}) - baterai: {self._persentase_baterai:.1f}%"
    
    def __eq__(self, other):
        if not isinstance(other, KendaraanListrik): return False
        return self.nomor_polisi == other.nomor_polisi
    
    def __lt__(self, other):
        if not isinstance(other, KendaraanListrik): return NotImplemented
        return self._persentase_baterai < other._persentase_baterai

    @property
    def riwayat_pengisian(self):
        return self.__riwayat_pengisian.copy()

class MobilListrik(KendaraanListrik):
    def __init__(self, nomor_polisi, merek, model, kapasitas_baterai, jumlah_pintu):
        super().__init__(nomor_polisi, merek, model, kapasitas_baterai)
        self.jumlah_pintu = jumlah_pintu

    def info_kendaraan(self):
        super().info_kendaraan()
        print(f"[SPESIFIK MOBIL] jumlah pintu: {self.jumlah_pintu}")

class MotorListrik(KendaraanListrik):
    def __init__(self, nomor_polisi, merek, model, kapasitas_baterai, tipe_baterai):
        super().__init__(nomor_polisi, merek, model, kapasitas_baterai)
        self.tipe_baterai = tipe_baterai 

    def info_kendaraan(self):
        super().info_kendaraan()
        print(f"[SPESIFIK MOTOR] tipe baterai: {self.tipe_baterai}")


class StasiunPengisian:
    total_stasiun = 0
    
    def __init__(self, id_stasiun, nama, lokasi, jumlah_slot):
        self.id_stasiun = id_stasiun
        self.nama = nama
        self.lokasi = lokasi
        self.jumlah_slot = jumlah_slot
        self.slot_terisi = 0
        self.__daftar_slot = [SlotPengisian(f"SLOT-{i+1}", "FAST CHARGING 50kW") for i in range(jumlah_slot)]
        self.__daftar_karyawan = []
        StasiunPengisian.total_stasiun += 1
    
    def tambah_kendaraan(self, jumlah=1):
        if self.slot_terisi + jumlah <= self.jumlah_slot:
            self.slot_terisi += jumlah
            print(f"[OK] {jumlah} kendaraan masuk ke {self.nama}")
            return True
        print("[ERROR] slot penuh!")
        return False
    
    def rekrut_karyawan(self, karyawan):
        self.__daftar_karyawan.append(karyawan)
        print(f"[AGREGASI] {karyawan.nama} ditambahkan ke {self.nama}")

    def proses_pembayaran(self, metode: MetodePembayaran, nominal, id_transaksi):
        print(f"\n[PROSES PEMBAYARAN] transaksi {id_transaksi}")
        metode.proses_pembayaran(nominal)
        metode.cetak_struk(id_transaksi)

    def info_stasiun(self):
        print(f"\nstasiun: {self.nama} | lokasi: {self.lokasi} | slot: {self.slot_terisi}/{self.jumlah_slot}")

class Transaksi:
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
        if self.__biaya <= 0: self.hitung_total()
        self.__status_bayar = "LUNAS"
        print(f"[OK] pembayaran {self.id_transaksi} BERHASIL! status: {self.__status_bayar}")


if __name__ == "__main__":
    
    print("\n--- [TEST 1] POLIMORFISME VIA PEWARISAN ---")
    mobil = MobilListrik("KT 1234 AB", "Hyundai", "Ioniq 5", 72.6, 4)
    motor = MotorListrik("KT 5678 CD", "Gesits", "Stella", 3.0, "Lepas Pasang")
    mobil2 = MobilListrik("KT 9999 ZZ", "Tesla", "Model 3", 60.0, 4)
    
    print("[INFO] satu loop, banyak implementasi:")
    for k in [mobil, motor, mobil2]:
        k.info_kendaraan()
        print("-" * 40)

    # 2. UML RELATIONSHIPS
    print("\n--- [TEST 2] UML RELATIONSHIPS ---")
    stasiun = StasiunPengisian("SP-001", "EV STATION UNMUL", "Jl. M.Yamin", 5)
    karyawan1 = Karyawan("Budi", "EMP01", "Teknisi")
    stasiun.rekrut_karyawan(karyawan1)
    
    pelanggan = Pelanggan("milo", "MEM-001")
    pelanggan.isi_daya_di_stasiun(stasiun, mobil)

    # 3. ABSTRAKSI
    print("\n--- [TEST 3] ABSTRAKSI ---")
    qris = PembayaranQRIS("QRIS-12345")
    kartu = PembayaranKartu("4111-****-1234")
    
    print("[TEST] polimorfisme pada metode pembayaran:")
    for metode in [qris, kartu]:
        metode.proses_pembayaran(50000)
        metode.cetak_struk("TRX-DEMO")
    
    print("\n[TEST] membuktikan class ABC tidak bisa di-instansiasi:")
    try:
        MetodePembayaran()
    except TypeError as e:
        print(f"[ERROR TERDETEKSI] {e}")

    # 4. DUCK TYPING
    print("\n--- [TEST 4] DUCK TYPING ---")
    kanal_notif = [NotifikasiEmail("milo@mail.com"), NotifikasiSMS("0812-1234-5678")]
    print("[TEST] mengirim notifikasi via berbagai kanal:")
    kirim_notifikasi_ke_pelanggan(kanal_notif, "pengisian daya 20 kWh berhasil!")

    # 5. OPERATOR OVERLOADING
    print("\n--- [TEST 5] OPERATOR OVERLOADING ---")
    print(f"[TEST] __str__: {mobil}")
    
    mobil_sama = MobilListrik("KT 1234 AB", "Hyundai", "Ioniq 5", 72.6, 4)
    print(f"[TEST] __eq__ (mobil == mobil_sama): {mobil == mobil_sama}")
    
    mobil.mulai_pengisian(30)
    motor.mulai_pengisian(2)
    mobil2.mulai_pengisian(50)
    
    print("[TEST] __lt__ (sorting berdasarkan baterai terendah):")
    for k in sorted([mobil, motor, mobil2]):
        print(f"  - {k}")

    # 6. TRANSAKSI & ENCAPSULATION
    print("\n--- [TEST 6] TRANSAKSI & ENCAPSULATION ---")
    trx = Transaksi("TRX-001", stasiun, mobil, 20, 2500)
    trx.hitung_total()
    trx.bayar()

    # 7. OCP & DIP
    print("\n--- [TEST 7] OCP & DIP ---")
    class PembayaranGoPay(MetodePembayaran):
        def proses_pembayaran(self, nominal):
            print(f"[GOPAY] pembayaran Rp{nominal:,.0f} via GoPay - BERHASIL")
            return True
        def cetak_struk(self, id_transaksi):
            print(f"[STRUK] transaksi {id_transaksi} via GoPay")
    
    print("[OCP] menambah pembayaranGoPay tanpa ubah class StasiunPengisian:")
    stasiun.proses_pembayaran(PembayaranGoPay(), 75000, "TRX-GOPAY-001")

    print("\n" + "="*60)
    print("PROGRAM BERHASIL DIJALANKAN")
    print("="*60)