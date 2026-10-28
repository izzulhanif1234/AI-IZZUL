# Gugusan Pulau-Pulau Melaka: video pameran Pusat Informasi (MCORP)

Video pengenalan ±3:00, 1920x1080, untuk pelawat Pusat Informasi. Sumber: dokumen
"GUGUSAN PULAU-PULAU MELAKA" (16 pulau, keterangan + pautan YouTube setiap pulau) dan peta
"Gugusan Pulau-Pulau Melaka" dari dokumen yang sama (`draft/assets/img/peta.png`, 634x865).

## Draf v1 (JPG untuk semakan)
- `draft/out/f1.jpg` … `f10.jpg`: 10 frame utama (hook, peta pop keluar, 3 zon, transisi zon,
  templat pulau, variasi sejarah, kuiz, Pulau Besar "Anda di sini", Taman Laut, penutup).
- `draft/out/storyboard.jpg`: garis masa 3:00 + motion/SFX setiap babak.
- `draft/out/teks-ringkas-16-pulau.jpg`: keterangan setiap pulau dipadatkan (1 ayat + 2 fakta).
- Render semula: `node draft/render.js` (frame) dan `node draft/render_sheets.js` (helaian).

## Arahan pengguna
- Peta mesti "pop keluar" dari video.
- Hypermotion, SFX, motion; interaktif, tidak membosankan.
- Jangan guna tulisan/tajuk yang ada dalam video YouTube; semua teks direka baharu.
  Gambar draf dipotong supaya tiada tulisan overlay (Hanyut, Konet, Melaka, Panjang, Keramat,
  Masjid guna frame lain atau crop).
- Keterangan diringkaskan supaya pelancong mudah faham.

## Struktur (±180 s)
Hook 8 · Peta pop 10 · 3 Zon 8 · Zon Utara 24 · Zon Tengah 52 · Kuiz 8 · Zon Selatan 52 ·
Taman Laut 10 · Penutup 8. Warna zon ikut legenda peta: Utara oren, Tengah merah jambu, Selatan hijau.

## Perlu sebelum video akhir
- Peta resolusi tinggi (fail asal AI/PSD/PNG besar); yang ada hanya 634x865.
- Logo MPPM (tempat simpan sedia di penutup).
- Rakaman dron: muat turun 16 video YouTube, guna bahagian tanpa tulisan sahaja.
- Keputusan suara latar (VO Bahasa Melayu) atau muzik + teks sahaja.
