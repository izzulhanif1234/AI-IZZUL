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

## Draf v2: video setiap pulau
- Pengguna mahu setiap pulau ada rakaman video dari pautan YouTube yang diberi, dengan potongan yang menarik.
- `draft/out/pelan-potongan-video.jpg`: 3 frame pratonton setiap video (YouTube hq1-3), ditanda GUNA / ELAK
  (ELAK = ada tajuk/tulisan dari video asal) + idea potongan setiap pulau.
- `draft/out/contoh-segmen-pulau-undan.jpg` (`f11`-`f14`): formula segmen ±7 s:
  zoom peta 1 s → Cut A 2.5 s (lebar, nama slam) → Cut B 2 s (orbit/speed-ramp, fakta pop) →
  Cut C 1.5 s (detail, Tahukah Anda, whip-pan keluar).
- Muat turun video dari container cloud disekat YouTube ("Sign in to confirm you're not a bot").
  Perlu fail MP4 dari pengguna (atau folder Google Drive) untuk pilih timestamp sebenar.

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
- Rakaman dron: 16 video sebagai fail MP4 (versi asal tanpa tulisan paling baik); guna bahagian tanpa tulisan sahaja.
- Keputusan suara latar (VO Bahasa Melayu) atau muzik + teks sahaja.
