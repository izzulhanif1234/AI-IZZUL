# Website PM Multilink

Website statik berbilang halaman untuk PM Multilink, anak syarikat Melaka Corporation (MCORP).
Tiada server atau pemasangan diperlukan: buka `index.html` dalam browser.

| Fail | Halaman |
|---|---|
| `index.html` | Utama |
| `tentang.html` | Tentang Kami (visi, misi, nilai) |
| `perkhidmatan.html` | Cuci Kereta, Projek Pembaikan, Pembersihan, Pengagihan Kit, Media |
| `projek.html` | Galeri projek dengan penapis kategori |
| `hubungi.html` | Maklumat hubungan, borang sebut harga (dihantar melalui WhatsApp), soalan lazim |
| `assets/style.css` | Reka bentuk dan warna |
| `assets/main.js` | Menu telefon, borang, penapis projek, nombor WhatsApp |
| `assets/logo.svg`, `assets/logo-pm.svg` | Logo dilukis semula sebagai SVG daripada logo syarikat |
| `assets/mcorp.png` | Logo MCORP (syarikat induk) |

## Perlu diisi sebelum dilancarkan

Semua maklumat yang belum ada ditanda dengan kotak kuning bergaris putus (`class="isi"`).
Cari `class="isi"` untuk senarai penuh. Antaranya:

1. **Nombor WhatsApp dan emel**: `assets/main.js`, objek `SYARIKAT` di atas fail
   (contoh `whatsapp: "60123456789"`). Borang dan semua butang WhatsApp akan terus berfungsi.
2. **Alamat, telefon, emel, waktu operasi**: `hubungi.html` dan pengaki (footer) setiap halaman.
3. **No. pendaftaran SSM**: pengaki.
4. **Visi, misi, latar belakang**: `tentang.html` (teks "Contoh:" ialah cadangan sahaja).
5. **Kawasan liputan**: soalan lazim di `hubungi.html`.
6. **Peta**: gantikan kotak peta di `hubungi.html` dengan kod iframe Google Maps.
7. **Projek sebenar**: `projek.html`. Kad bertanda "Contoh:" perlu diganti dengan projek dan gambar sebenar
   (letak gambar dalam `assets/` dan tukar ikon dalam `<div class="gambar">` kepada `<img src="assets/nama.jpg" alt="...">`).
   Dua video MCORP Estimate disenaraikan di bawah Media; padam jika bukan hasil kerja PM Multilink.
8. **Logo asal**: jika ada fail logo asal (PNG/SVG), boleh ganti `assets/logo.svg` supaya 100% tepat.

## Edit header, footer atau senarai perkhidmatan

Kelima-lima halaman dijana oleh `scripts/pm_multilink_build.py` (header, footer dan ikon dikongsi).
Untuk perubahan yang melibatkan semua halaman, edit skrip itu kemudian jalankan:

```bash
python3 scripts/pm_multilink_build.py
```

Nota: menjalankan skrip akan menulis semula fail HTML, jadi masukkan juga maklumat syarikat ke dalam skrip
(bukan terus dalam HTML) jika anda guna cara ini.

## Hosting (GitHub Pages)

Website ini live di **https://izzulhanif1234.github.io/AI-IZZUL/**, dihoskan dari branch `gh-pages`
(branch itu hanya mengandungi fail website, tanpa video atau fail lain dalam repo).

Untuk kemas kini website selepas mengubah fail di folder ini:

```bash
git worktree add /tmp/gh-pages gh-pages
cp -r website/pm-multilink/. /tmp/gh-pages/ && rm /tmp/gh-pages/README.md
cd /tmp/gh-pages && git add -A && git commit -m "Kemas kini website" && git push origin gh-pages
```

Jika bertukar ke domain sendiri, tukar `SITE_URL` dalam `scripts/pm_multilink_build.py`, jana semula halaman,
dan tetapkan domain di GitHub: Settings > Pages > Custom domain.

## Google

`sitemap.xml` disediakan untuk Google. Untuk muncul di Google lebih cepat, daftar laman di
[Google Search Console](https://search.google.com/search-console) (jenis "URL prefix", alamat di atas),
sahkan pemilikan dengan kod tag HTML yang diberi (letak dalam `<head>` melalui skrip penjana), kemudian hantar `sitemap.xml`.
