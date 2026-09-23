--> Sistem Manajemen Stasiun Pengisian Kendaraan Listrik di Kota Samarinda

Program ini merupakan program sederhana dengan tema Sistem Manajemen Stasiun Pengisian Kendaraan Listrik di Kota Samarinda dan digunakan untuk mengelola data stasiun pengisian, kendaraan listrik, dan transaksi pengisian daya.

--> Program terdiri dari 3 class utama:

1. class StasiunPengisian: digunakan untuk menyimpan ID, nama, lokasi, jumlah slot, dan saldo kas. Pada class ini terdapat instance method untuk mengelola slot stasiun, class method untuk mengubah data operasional, dan static method untuk validasi ID stasiun.
2. class KendaraanListrik: digunakan untuk menyimpan data kendaraan seperti nomor polisi, merek, model, dan kapasitas baterai. Persentase baterai dan riwayat pengisian dibuat sebagai private attribute dan diakses menggunakan property getter dan setter.
3. class Transaksi: digunakan untuk menyimpan data transaksi, stasiun, kendaraan yang mengisi daya, dan jumlah daya yang diisi. Class ini juga menghitung total biaya berdasarkan daya dan tarif.

Program menggunakan list untuk mengelompokkan objek dan for loop untuk menghitung total kapasitas. Property setter juga digunakan untuk memvalidasi saldo kas, persentase baterai, dan diskon agar tidak menerima nilai yang tidak sesuai.