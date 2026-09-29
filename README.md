# Homepage Retro Rafael

Prototipe homepage bergaya internet tahun 90-an, dibuat dengan HTML dan backend Python sederhana untuk buku tamu.

## Yang dibutuhkan

- Visual Studio Code
- Python 3 terpasang di komputer
- Folder project ini sudah diunduh dan diekstrak

Tidak perlu memasang package tambahan.

## Menjalankan di Windows

1. Unduh project dari GitHub dengan tombol **Code > Download ZIP**, lalu ekstrak ZIP-nya.
2. Di VS Code, pilih **File > Open Folder...** dan buka folder hasil ekstrak yang berisi `server.py` dan `home.html`.
3. Buka terminal lewat **Terminal > New Terminal**.
4. Cek Python dengan perintah:

   ```powershell
   py --version
   ```

   Kalau perintah `py` tidak dikenali, pasang Python 3 dari [python.org](https://www.python.org/downloads/) dan buka ulang VS Code.

5. Jalankan server:

   ```powershell
   py server.py
   ```

6. Buka alamat ini di browser: <http://127.0.0.1:8000>

Jangan membuka `home.html` langsung dari File Explorer. Guestbook perlu backend yang dijalankan pada langkah 5.

## Menggunakan buku tamu

Pesan yang dikirim tersimpan sebagai satu baris JSON per pesan di `guestbook-log.jsonl`, di folder project yang sama. Buka file itu di VS Code untuk melihat log. Halaman menampilkan paling banyak 50 pesan terbaru, sementara log menyimpan seluruh pesan.

File log bisa berisi pesan pengunjung. Jangan unggah atau membagikan `guestbook-log.jsonl` tanpa izin mereka.

Untuk menghentikan server, kembali ke terminal lalu tekan `Ctrl+C`.

## Batas demo lokal

Alamat `127.0.0.1` hanya bisa diakses dari komputer yang menjalankan server. Orang yang mengunduh dan menjalankan project ini akan memiliki log mereka sendiri. GitHub Pages hanya menyajikan file statis, jadi tidak bisa menjalankan backend Python atau mengumpulkan pesan ke satu file bersama.

Agar pengunjung internet bisa memakai satu guestbook bersama, backend perlu di-deploy ke hosting yang mendukung Python dan penyimpanan persisten. Backend prototipe ini belum memiliki login admin, pembatasan spam, atau perlindungan untuk penggunaan publik.
