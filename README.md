# Concurrency-Control-Protocol
Concurrency control untuk database transactions

## Format Input Text
- Baris pertama diisi dengan database yang digunakan
- Baris sisanya diisi dengan transaksi yang dilakukan
- Format transaksi adalah (Aksi)-database. Dimana aksi berupa R atau W

## Alur program (simple_locking)
Program akan membagi transaksi secara round robin bergantian antar transaksi dimulai dari T1
sehingga alur untuk contoh 

a b c 
R-a W-b
R-b R-a
R-c R-a

adalah R-a(T1), R-b(T2), R-c(T3), W-b(T1), R-a(T2), R-a(T3)

Ketika terjadi deadlock, akan dilakukan abort untuk transaksi terakhir yang menyebabkan terjadinya deadlock.
Transaksi yang di-abort akan dieksekusi di paling akhir satu per satu tanpa konkurensi.