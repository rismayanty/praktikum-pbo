<<<<<<< HEAD

=======
# Sistem Manajemen Stasiun Pengisian Kendaraan Listrik

Program Python ini merupakan sistem sederhana untuk mengelola kendaraan listrik, stasiun pengisian, pelanggan, karyawan, dan transaksi pengisian daya. Program ini menerapkan konsep Object-Oriented Programming (OOP), seperti class dan object, encapsulation, inheritance, abstraction, polymorphism, duck typing, operator overloading, serta relasi antarobjek (asosiasi, agregasi, komposisi, dan dependency).

## Class Diagram UML

![alt text](<UML PBO.drawio.png>)

Keterangan relasi:
- **Inheritance**: `MobilListrik` dan `MotorListrik` mewarisi class `KendaraanListrik`.
- **Inheritance**: `PembayaranQRIS` dan `PembayaranKartu` mewarisi abstract class `MetodePembayaran`.
- **Agregasi**: `StasiunPengisian` menyimpan daftar objek `Karyawan` yang dapat dibuat secara terpisah dari stasiun.
- **Komposisi**: `StasiunPengisian` membuat dan memiliki objek `SlotPengisian` di dalam konstruktornya.
- **Asosiasi**: `Pelanggan` berhubungan dengan `StasiunPengisian` dan `KendaraanListrik` saat melakukan pengisian daya.
- **Asosiasi**: `Transaksi` menyimpan referensi ke `StasiunPengisian` dan `KendaraanListrik`.
- **Dependency**: `StasiunPengisian` menggunakan objek `MetodePembayaran` untuk memproses pembayaran.

## Penerapan Konsep OOP

### 1. Abstract Base Class
- `MetodePembayaran` mewarisi `ABC` dari modul `abc`.
- `proses_pembayaran()` dan `cetak_struk()` merupakan abstract method.
- `PembayaranQRIS` dan `PembayaranKartu` mengimplementasikan kedua abstract method tersebut.
- Program mencoba membuat objek `MetodePembayaran`. Python menghasilkan `TypeError` karena abstract method belum diimplementasikan.

### 2. Inheritance
- `MobilListrik` dan `MotorListrik` mewarisi atribut dan method dari `KendaraanListrik`.
- Keduanya memanggil `super().__init__(nomor_polisi, merek, model, kapasitas_baterai)` untuk menggunakan konstruktor class induk, lalu menambahkan atribut khusus (`jumlah_pintu` pada mobil, `tipe_baterai` pada motor).
- `PembayaranQRIS` dan `PembayaranKartu` mewarisi `MetodePembayaran` dan menyediakan implementasi metode pembayaran masing-masing.

### 3. Encapsulation
- Atribut `__riwayat_pengisian` pada `KendaraanListrik`, `__daftar_slot` dan `__daftar_karyawan` pada `StasiunPengisian`, serta `__biaya` dan `__status_bayar` pada `Transaksi` menggunakan penamaan private.
- Atribut `_kapasitas_baterai` dan `_persentase_baterai` pada `KendaraanListrik` menggunakan konvensi protected.
- `riwayat_pengisian` diakses melalui property yang mengembalikan salinan (`copy()`) list, sehingga data asli tidak bisa diubah dari luar.
- Method `mulai_pengisian()` memvalidasi bahwa daya pengisian lebih dari 0 dan membatasi daya agar tidak melebihi kapasitas baterai yang tersisa.

### 4. Polimorfisme via Pewarisan
Class `MobilListrik` dan `MotorListrik` meng-override method `info_kendaraan()`.
- Mobil menampilkan informasi dasar kendaraan beserta jumlah pintu.
- Motor menampilkan informasi dasar kendaraan beserta tipe baterai.
- Program memanggil `info_kendaraan()` pada setiap objek dalam satu daftar kendaraan. Hasilnya menyesuaikan implementasi class masing-masing.

### 5. Operator Overloading
Class `KendaraanListrik` mengimplementasikan:
- `__str__()` untuk menentukan tampilan objek kendaraan saat dikonversi menjadi string.
- `__eq__()` sehingga dua kendaraan dianggap sama jika `nomor_polisi` sama.
- `__lt__()` sehingga dua kendaraan dapat dibandingkan dengan operator `<` berdasarkan persentase baterai, dan dapat diurutkan menggunakan `sorted()`.

### 6. Class Attribute
- `KendaraanListrik.total_kendaraan` menghitung jumlah objek kendaraan yang dibuat.
- `KendaraanListrik.jenis_bahan_bakar` bernilai `"listrik"` dan dimiliki bersama oleh seluruh kendaraan.
- `StasiunPengisian.total_stasiun` menghitung jumlah objek stasiun yang dibuat.

### 7. Duck Typing
Class `NotifikasiEmail` dan `NotifikasiSMS` tidak memiliki hubungan inheritance, tetapi keduanya memiliki method `kirim(pesan)`. Fungsi `kirim_notifikasi_ke_pelanggan(daftar_notif, pesan)` dapat menggunakan kedua objek tersebut selama objek yang diberikan mempunyai method `kirim()`.

### 8. Relasi Antarobjek
- **Agregasi**: objek `Karyawan` ditambahkan ke daftar karyawan milik `StasiunPengisian` melalui `rekrut_karyawan()`.
- **Komposisi**: objek `SlotPengisian` dibuat di dalam konstruktor `StasiunPengisian` sesuai `jumlah_slot`.
- **Asosiasi**: `Pelanggan.isi_daya_di_stasiun()` menerima objek `StasiunPengisian` dan `KendaraanListrik`, sedangkan `Transaksi` menyimpan referensi ke keduanya.
- **Dependency**: objek metode pembayaran diterima oleh `StasiunPengisian.proses_pembayaran()` dan digunakan untuk menjalankan pembayaran.

### 9. OCP dan DIP
- `StasiunPengisian.proses_pembayaran()` bergantung pada abstraksi `MetodePembayaran`, bukan pada class konkret (Dependency Inversion Principle).
- Class baru `PembayaranGoPay` ditambahkan pada saat pengujian tanpa mengubah class `StasiunPengisian` (Open/Closed Principle).

## Alur Transaksi
1. Program membuat data kendaraan, stasiun, karyawan, dan pelanggan.
2. Pelanggan mengisi daya di stasiun dengan kendaraannya.
3. Stasiun memeriksa ketersediaan slot, lalu menambahkan kendaraan ke slot yang terisi.
4. Kendaraan memulai pengisian daya (maksimal sesuai sisa kapasitas baterai) dan mencatat riwayat pengisian.
5. `Transaksi` menghitung total biaya dari `daya_kwh` dikali `tarif_per_kwh`.
6. Pembayaran diproses melalui metode pembayaran yang dipilih (QRIS, Kartu, dan seterusnya) beserta pencetakan struk.
7. Status transaksi diubah menjadi `LUNAS` setelah pembayaran berhasil.

## Bukti Abstraksi
Pada bagian `[TEST 3] ABSTRAKSI`, program mencoba membuat objek `MetodePembayaran`. Karena class tersebut memiliki abstract method yang belum diimplementasikan, Python menangkap `TypeError` dan menampilkan pesan bahwa abstract class tidak dapat dibuat menjadi objek secara langsung.

Contoh hasil (teks pesan dapat berbeda bergantung versi Python):

[TEST] membuktikan class ABC tidak bisa di-instansiasi:
[ERROR TERDETEKSI] Can't instantiate abstract class MetodePembayaran without an implementation for abstract methods 'cetak_struk', 'proses_pembayaran'

## Output Program
![alt text](<OUTPUT 1.png>)
![alt text](<OUTPUT 2.png>)
>>>>>>> fb8b8d3 (UP PBO, PLS MATLIS HUAAAAAAAA)
