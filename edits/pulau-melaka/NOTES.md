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

## Draf v3: rakaman sebenar + motion grafik
- Sumber: folder Google Drive 1J3_zN8Z5kXVF18ytVQccn0rqWSQqK3_P (16 video 1080p ±2:30, Upeh 3:51 dari
  saluran lain, + "Display Poster ( MCORP ) FINAL.png" = peta HD 2394x3263 → `draft/assets/img/peta-hd.jpg`).
  Muat turun semula: `gdown --folder <url>` ke `media/pulau/src/` (tidak dalam git).
- `scripts/pulau_scan.py`: imbas setiap video (4 fps) untuk tulisan overlay (warna pil kuning/kotak merah jambu siri
  "Tambo Pulau Di Mulaqah"), pergerakan, ketajaman; keluarkan contact sheet ke `media/pulau/scan/`.
  Tulisan overlay muncul dua kali setiap video (awal ±0:05–0:22 dan hujung ±2:00–2:25).
- `cuts.json`: potongan A/B/C (Besar ada D) setiap pulau, masa dalam video asal; semua disahkan tiada tulisan &
  tiada crossfade. Frame tengah setiap potongan di `draft/assets/img/cuts-hd/`.
- Pulau Upeh: ada watermark kecil "AerialTrooper" penjuru kanan atas sepanjang video → crop/scale dari kiri bawah.
- Peringgi: rakaman hampir statik → push-in digital + speed-ramp.
- Motion grafik baharu: `f15` teks-mask zoom-through, `f16` triptych menyerong, `f17` glitch/RGB slice
  (`draft/out/gaya-motion-grafik.jpg`). Logo MPPM tidak digunakan (arahan pengguna).

## Draf v4: perjalanan bot atas peta (struktur semasa)
Rujukan pengguna: intro → peta Melaka → turun ke setiap pulau; video pop keluar dari pin lalu full screen.
Pengguna mahu pergerakan guna **bot** (pulau → bot).
- `draft/journey.html`: animasi sebenar (GSAP timeline, paused, seek dengan `?t=` atau `window.tl.seek`).
  Rig kamera `#zoom > #cam (3D tilt) > #world` (peta HD 2394x3263, origin 0 0). Bot SVG pandangan atas
  dengan buih ombak, berpusing ikut tangen laluan. Kad video setiap pulau (`#c-<pulau>`) pop dari pin,
  membesar ke 1920x1080, main Cut A → B → C (draf guna frame `cuts-hd`; final guna klip video).
- Pin diukur pada poster HD (piksel merah): masjid 89,624 · keramat 454,755 · konet 606,989 · upeh 850,1330 ·
  melaka 1229,1532 · panjang 1352,1718 · menatang 1683,1824 · serimbun 1207,2049 · lalang 1684,2099 ·
  peringgi 1980,2210 · hanyut 774,2292 · burung 1979,2360 · besar 1440,2365 · dodol 1515,2521 ·
  nangka 1406,2710 · undan 1227,2838.
- Laluan bot (zon tidak bercampur): Masjid, Keramat, Konet | Upeh, Melaka, Panjang, Menatang, Peringgi, Burung |
  Lalang, Serimbun, Hanyut, Besar, Dodol, Nangka, Undan.
- Masa: intro 0–7, peta 7–12, pulau ke-i bermula 12 + 9i (belayar 1.8, kad 1.2, besar 0.6, full 4.6, balik 0.8),
  penutup 156–175 s.
- Capture: `node draft/render_journey.js nama=masa ...`; pratonton gerak: `node draft/preview_journey.js <dari> <hingga> <fps> <out.mp4>`.
  Nota: `page.evaluate` mesti tidak memulangkan objek timeline (Playwright cuba serialise → hang), dan elak
  CSS blur/filter pada lapisan peta yang besar (paint perisian sangat perlahan).
- Quiz & babak Taman Laut berasingan digugurkan; Taman Laut jadi lencana di Dodol/Nangka/Undan, "ANDA DI SINI" di Besar.

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
- Keputusan suara latar (VO Bahasa Melayu) atau muzik + teks sahaja.
