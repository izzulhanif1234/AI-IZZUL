"""SPD GREEN explainer video: storyboard + timeline as JPG pages.

Builds edits/spd-green/storyboard/storyboard.html (three 1920-wide pages) and renders
01-timeline.jpg, 02-storyboard-a.jpg, 03-storyboard-b.jpg, 04-spd2-homepage.jpg with Playwright.
Every scene thumbnail is a real 1920x1080 style frame scaled down, so the frames can be reused
as the starting point of the HyperFrames scenes later.
"""

import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "edits" / "spd-green" / "storyboard"

# ---------------------------------------------------------------- timeline data
# (id, start, end, title, slide ref, styles, visual/motion, sfx, vo)
SCENES = [
    ("S01", 0, 18, "Cold open: lakonan awal", "Bahan lakonan",
     ["LAKONAN", "DOODLE"],
     "Montaj footage (speed-ramp): pegawai masuk bilik fail & buka kabinet berkunci (klip 3) → selak fail gantung → "
     "cari fail di rak arkib (klip 1) → di meja (klip 2) dengan dialog asal \"Mana ni? Mana ni?… cek fail\" → freeze-frame. Doodle kapur putih atas footage: "
     "bulatan conteng, jam berdetik, \"Fail mana?!\". Bunyi asal kertas jadi foley; suara krew & latar dibuang.",
     "Kertas diselak (foley sebenar) · laci kabinet dihempas, pitch −12 → jadi impak bass semasa freeze · "
     "decit marker setiap kali doodle dilukis",
     "(Dialog asal klip 2.) Semasa freeze: Fail fizikal. Carian manual. Masa yang terbuang, setiap hari."),
    ("S02", 18, 27, "Tajuk: kertas jadi daun", "Slaid 1",
     ["HYPERMOTION"],
     "Kamera dolly menembusi kawanan kertas A4 3D (depth of field, motion blur). Kertas berlipat menjadi daun, "
     "daun membentuk tanda SPD. Light sweep emas pada tajuk.",
     "Lipatan kertas berlapis + piano terbalik (reverse swell) · desir daun granular · "
     "sub-drop lembut ketika logo terkunci",
     "Memperkenalkan, Sistem Pengurusan Data Bersepadu. SPD. Inovasi digital ke arah pengurusan hijau dan lestari."),
    ("S03", 27, 43, "Apa itu SPD", "Slaid 2 (butang merah: intro VO)",
     ["FORMAL", "HYPERMOTION"],
     "Lima jubin 3D mengorbit (Tanah, Bangunan, Penyewaan, Penilaian Aset, Dokumen Hak Milik). "
     "Garis data bercahaya menarik semuanya ke satu hab \"SATU PLATFORM BERPUSAT\". Kamera push-in + parallax.",
     "Ketukan pensel pada meja sebagai 'data tick' · selak kabinet logam (magnetic lock) bila jubin bercantum",
     "SPD ialah inisiatif transformasi digital M-Corp, yang menyatukan maklumat tanah, bangunan, penyewaan, "
     "penilaian aset, dan dokumen hak milik, dalam satu platform berpusat. Bukan sekadar cekap. Tetapi juga lebih hijau."),
    ("S04", 43, 57, "Penyataan masalah", "Slaid 3",
     ["DOODLE"],
     "Kertas kraft bergrid. Tangan melukis 6 ikon (line-boil 12 fps): timbunan kertas, almari sesak, "
     "fail berganda, jam pasir, fail hilang, RM menyusut. Nombor 01–06 ditulis tangan, muncul ikut VO.",
     "Geselan grafit pensel · decit pemadam · kertas direnyuk ketat · klik stop-motion pada setiap ikon",
     "Sebelum SPD, pengurusan data berdepan enam cabaran. Penggunaan kertas yang tinggi. Ruang simpanan fizikal yang besar. "
     "Pertindihan data. Carian maklumat yang lambat. Risiko kehilangan dokumen. Dan kos operasi yang tinggi."),
    ("S05", 57, 67, "Sebelum → Selepas: masuk sistem", "Slaid 4",
     ["HYPERMOTION", "FORMAL"],
     "Kertas doodle direnyuk → kamera terbang masuk ke dalam bola kertas → match-cut ke pelayar: spd.pknm.gov.my "
     "ditaip, Enter, sistem terbuka. Split fail fizikal vs SPD. Pil: BERPUSAT · ATAS TALIAN · LEBIH CEKAP.",
     "Renyuk kertas → tarikan udara terbalik · taipan URL (kekunci sebenar, ditala) · ketukan kaca bila halaman terbuka",
     "Hari ini, fail fizikal digantikan dengan data berpusat. Atas talian. Dan lebih cekap."),
    ("S06", 67, 83, "Demo sistem: Laman Utama", "Slaid 5 · skrin DASHBOARD",
     ["DEMO SISTEM", "HYPERMOTION"],
     "Kursor bergerak, scroll lancar ke bawah laman utama: peta taburan premis & tanah (zoom ke pin, popup), "
     "jadual Aset Alih & Aset Tak Alih, graf sewaan, kakitangan. Kamera 3D ikut kursor, punch-in pada angka.",
     "Klik tetikus sebenar (rapat, tak bergema) · roda scroll bertekstur · 'tick' halus setiap panel masuk",
     "Sebaik log masuk, papan pemuka utama memaparkan taburan premis dan tanah milik M-Corp di seluruh Melaka, "
     "bersama ringkasan aset alih, aset tak alih, sewaan, dan stor, dalam satu paparan."),
    ("S07", 83, 99, "Demo sistem: Aset Tak Alih", "Slaid 5 · skrin ASET TAK ALIH",
     ["DEMO SISTEM", "HYPERMOTION"],
     "Klik menu Pengurusan Aset Tak Alih → taip \"ELKAY\" dalam carian → senarai cadangan jatuh → klik → "
     "Maklumat Premis terbuka (Kod ATA, lot, status hak milik, koordinat) → klik pin Google → peta → scroll ke dokumen hak milik digital.",
     "Taipan kekunci (setiap huruf satu not) · 'drop' lembut senarai cadangan · klik + kaca bila panel terbuka",
     "Untuk aset tak alih, cukup taip nama lokasi. Rekod premis, lot, status hak milik, dan koordinat dipaparkan "
     "serta-merta, lengkap dengan peta, dan dokumen hak milik digital."),
    ("S08", 99, 115, "Demo sistem: modul lain", "Slaid 5 · skrin ASET ALIH, STOR, MODAL INSAN",
     ["DEMO SISTEM", "HYPERMOTION"],
     "Klik bertubi di sidebar, setiap klik = whip-pan 3D ke modul: Aset Alih (senarai + barcode) → Pengurusan Stor "
     "(senarai stok, scroll) → Modal Insan (kakitangan & latihan) → Pentadbiran (capaian pengguna). Label kinetik ikut VO.",
     "Satu klik + satu not kekunci setiap modul (4 not = melodi) · kibasan kain sebagai whoosh organik",
     "Aset alih direkod dan disemak menggunakan barcode. Pengurusan stor memantau permohonan serta baki stok. "
     "Modal insan mengurus cuti dan rekod berkaitan. Manakala pentadbiran mengawal capaian sistem."),
    ("S09", 115, 125, "Lima modul, satu ekosistem", "Slaid 5",
     ["FORMAL"],
     "5 kad modul dari slaid 5 (Aset Alih, Aset Tak Alih, Modal Insan, Pengurusan Stor, Pentadbiran), setiap satu dengan "
     "skrin sebenar modul; cip impak hijau tumbuh ikut VO, pokok menjalar di bawah.",
     "Kayu berkeriut diperlahankan (pertumbuhan) · petikan kalimba lembut setiap kad",
     "Setiap modul membawa impak hijau. Kurang dokumen fizikal. Kurang cetakan. Kurang fail. Dan kurang ruang arkib."),
    ("S10", 125, 129, "Bab: IMPAK SPD", "Slaid 7",
     ["HYPERMOTION"],
     "Tipografi 3D extruded menghentam skrin, kamera menembusi huruf A masuk ke babak seterusnya. Flash hijau.",
     "Hentakan cop getah sebenar + tape-stop pada muzik · 0.3 s sunyi",
     "Inilah, impak SPD."),
    ("S11", 129, 138, "Kecekapan sumber organisasi", "Slaid 8",
     ["FORMAL"],
     "Tiga tiang naik dari lantai (Masa · Tenaga Kerja · Ruang & Bahan). Ikon 18 → 9 orang.",
     "Ketukan blok kayu bertala, satu setiap tiang",
     "Carian dan semakan rekod menjadi lebih pantas. Keperluan tenaga kerja dianggarkan berkurang, "
     "daripada lapan belas, kepada sembilan orang."),
    ("S12", 138, 148, "Kurang pencemaran", "Slaid 9",
     ["DOODLE"],
     "Gaya kapur atas papan hijau: tong sampah kertas mengecil, laluan penghantar dokumen dipadam, "
     "bilik fail bertukar menjadi ruang kerja.",
     "Kapur di papan · pemadam papan hitam · kapur patah sebagai aksen",
     "Sisa kertas berkurang. Dokumen tidak lagi bergerak dari meja ke meja. Dan ruang simpanan kini digunakan "
     "untuk tujuan yang lebih produktif."),
    ("S13", 148, 158, "Sewaan: 14 → 3 hari", "Slaid 10",
     ["HYPERMOTION"],
     "Kalendar 3D: 11 helai tercabut dan terbang menjadi daun. Kaunter 14 → 3. Lencana \"11 HARI DIJIMATKAN\".",
     "Koyakan kalendar sebenar, makin laju · 'snap' kertas pada angka akhir",
     "Proses permohonan sewaan, daripada empat belas hari, kini hanya tiga hari. Sebelas hari dijimatkan."),
    ("S14", 158, 169, "Semakan aset: 20 → 2 hari", "Slaid 11",
     ["FORMAL", "HYPERMOTION"],
     "Foto semakan manual → foto imbas barcode, garis laser hijau menyapu skrin, rekod muncul dalam SPD. Kaunter 20 → 2.",
     "Bip pengimbas barcode dirakam & di-pitch menjadi kord · dengung laser halus",
     "Semakan aset alih, dua puluh hari secara manual. Kini, dua hari dengan imbasan barcode."),
    ("S15", 169, 180, "Penjimatan kos tenaga kerja", "Slaid 12",
     ["FORMAL"],
     "18 ikon manusia → 9 menyala. Jadual bulanan RM36,306 → RM18,153, tahunan RM435,672 → RM217,836. "
     "Kaunter besar beraksen emas.",
     "Manik sempoa bergolek · pukulan malet felt dalam pada angka akhir",
     "Anggaran penjimatan kos tenaga kerja, dua ratus tujuh belas ribu, lapan ratus tiga puluh enam ringgit, setahun."),
    ("S16", 180, 191, "Kertas A4 & dakwat", "Slaid 13 & 14",
     ["FORMAL", "DOODLE"],
     "Graf bar 3D tumbuh: A4 1,242 → 926 (−25.4%), dakwat 174 → 105 (−39.7%). Doodle: rim kertas menyusut, titisan dakwat.",
     "Hentakan rim kertas pada meja · titisan air di-pitch rendah sebagai 'dakwat'",
     "Antara tahun dua ribu dua puluh satu dan dua ribu dua puluh lima, permohonan kertas A4 berkurang dua puluh lima "
     "perpuluhan empat peratus. Dan dakwat pencetak, tiga puluh sembilan perpuluhan tujuh peratus."),
    ("S17", 191, 199, "Digitalisasi & bukti", "Slaid 15, 16 & 17",
     ["HYPERMOTION"],
     "Fail & borang fizikal larut jadi zarah → tersusun semula sebagai rekod SPD; montaj polaroid sebelum/selepas.",
     "Pasir granular + kilauan kaca · pengatup polaroid",
     "Fail dan borang fizikal kini digantikan dengan rekod digital. Buktinya jelas, dari permohonan stok, "
     "hingga pemeriksaan aset."),
    ("S18", 199, 207, "Pengiktirafan", "Slaid 18",
     ["FORMAL"],
     "Sijil hak cipta meluncur masuk, cop mohor ditekan. \"Hak Cipta · 2 Mac 2020\" + \"Platform utama MCORP\".",
     "Embosser (pengecap timbul) menggigit kertas",
     "SPD telah diiktiraf hak cipta sejak tahun dua ribu dua puluh, dan kini menjadi platform utama pengurusan data M-Corp."),
    ("S19", 207, 232, "Akan datang: SPD 2.0 + Green Dashboard", "Slaid 19",
     ["DEMO SISTEM", "HYPERMOTION"],
     "Label AKAN DATANG. Terowong cahaya hijau → laman utama SPD 2.0 (peta, kad aset). Laman di-scroll ke bawah sahaja "
     "(tiada klik menu): seksyen SPD 2.0 + GREEN DASHBOARD masuk, gauge naik ke 82, KPI dari slaid kira naik satu-satu, Green Impact Meter.",
     "Muzik drop ke pad lembut · roda scroll bertekstur · ketukan kaca bertala setiap KPI menyala · denyut sub pada gauge",
     "Dan ini baru permulaan. Akan datang, SPD dua titik kosong, bersama Green Dashboard. Setiap impak hijau kini "
     "diukur secara masa nyata. Kertas. Dakwat. Masa. Tenaga kerja. Dan kos. Kerana apa yang diukur, boleh diurus."),
    ("S20", 232, 240, "Penutup", "Slaid 20",
     ["HYPERMOTION"],
     "Jubin dashboard terbang dan bercantum membentuk tanda SPD. Tagline + slogan. Kad akhir MCORP.",
     "Satu not piano akhir + cop mohor · muzik resolve",
     "SPD. Mendigitalkan proses. Mengoptimumkan sumber. Mempercepat penyampaian. "
     "Ke arah pengurusan yang hijau dan lestari."),
]

STYLE_COL = {
    "FORMAL": ("#165A44", "#fff"),
    "DOODLE": ("#F3E3B5", "#3a2f12"),
    "HYPERMOTION": ("#111", "#E8C46A"),
    "LAKONAN": ("#8E1B33", "#fff"),
    "DEMO SISTEM": ("#2B5FD9", "#fff"),
}

ACTS = [
    (0, 57, "BABAK 1 · MASALAH & PENGENALAN"),
    (57, 125, "BABAK 2 · SISTEM SPD (DEMO)"),
    (125, 207, "BABAK 3 · IMPAK HIJAU"),
    (207, 240, "BABAK 4 · MASA DEPAN"),
]


def tc(s):
    return f"{int(s // 60)}:{int(s % 60):02d}"


# ---------------------------------------------------------------- shared CSS
CSS = r"""
:root{--g900:#0B2E22;--g800:#165A44;--g700:#26745A;--g200:#CAD9CF;--g100:#E9F2E7;--lime:#B6D973;
--gold:#D9AE52;--maroon:#8E1B33;--paper:#F3EEDF;--ink:#22302A;}
*{box-sizing:border-box;margin:0;padding:0}
body{background:#ECE8DD;font-family:'Plus Jakarta Sans',Inter,sans-serif;color:#1c2622}
.page{width:1920px;background:#F5F2EA;position:relative;overflow:hidden}
.hdr{background:var(--g900);color:#fff;padding:56px 80px 48px;position:relative;overflow:hidden}
.hdr .k{font:700 18px 'JetBrains Mono',monospace;letter-spacing:.24em;color:var(--lime)}
.hdr h1{font:800 64px/1.05 'Plus Jakarta Sans';margin:14px 0 10px;letter-spacing:-.02em}
.hdr p{font:500 22px 'Plus Jakarta Sans';color:#cfe3d6}
.hdr .meta{position:absolute;right:80px;top:60px;text-align:right;font:600 18px 'JetBrains Mono';color:#9fc2ae;line-height:1.7}
.hdr .meta b{color:#fff}
.hdr:after{content:"";position:absolute;right:-120px;bottom:-220px;width:620px;height:620px;border-radius:50%;
background:radial-gradient(circle,rgba(182,217,115,.28),transparent 65%)}
.sec{padding:44px 80px 10px}
.sec h2{font:800 30px 'Plus Jakarta Sans';letter-spacing:-.01em;margin-bottom:6px;color:var(--g900)}
.sec h2 span{font:600 15px 'JetBrains Mono';color:#7d8a83;letter-spacing:.14em;margin-left:14px}
.sub{font:500 17px 'Plus Jakarta Sans';color:#5b6762;margin-bottom:20px}
/* ruler */
.ruler{position:relative;height:430px;margin-top:10px}
.acts{position:absolute;left:0;right:0;top:0;height:40px}
.act{position:absolute;top:0;height:34px;border-left:2px solid var(--g800);padding:6px 10px;font:800 14px 'JetBrains Mono';
letter-spacing:.08em;color:var(--g800);background:linear-gradient(90deg,rgba(22,90,68,.10),transparent)}
.blocks{position:absolute;left:0;right:0;top:48px;height:150px}
.blk{position:absolute;top:0;height:150px;border-radius:10px;padding:10px 9px;overflow:hidden;border:2px solid #F5F2EA}
.blk .id{font:800 15px 'JetBrains Mono'}
.blk .t{font:700 14px/1.2 'Plus Jakarta Sans';margin-top:6px}
.blk .tm{position:absolute;bottom:8px;left:9px;font:600 12px 'JetBrains Mono';opacity:.75}
.lane{position:absolute;left:0;right:0;height:34px;border-radius:8px}
.lane .lbl{position:absolute;left:-0px;top:-22px;font:700 13px 'JetBrains Mono';letter-spacing:.1em;color:#6b766f}
.ticks{position:absolute;left:0;right:0;top:400px;height:30px}
.tick{position:absolute;top:0;font:600 13px 'JetBrains Mono';color:#69756e;transform:translateX(-50%)}
.tick:before{content:"";position:absolute;left:50%;top:-10px;height:8px;border-left:1px solid #9aa59f}
/* cards */
.grid{display:grid;grid-template-columns:1fr 1fr;gap:28px;padding:10px 80px 60px}
.card{background:#fff;border-radius:18px;overflow:hidden;box-shadow:0 1px 0 rgba(0,0,0,.04),0 10px 30px rgba(20,40,30,.08);display:flex;flex-direction:column}
.card .thumb{width:100%;aspect-ratio:16/9;position:relative;overflow:hidden;background:#000}
.card .thumb .frame{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0}
.card .body{padding:20px 24px 24px}
.card .row1{display:flex;align-items:center;gap:12px;margin-bottom:8px}
.card .sid{font:800 18px 'JetBrains Mono';color:var(--g800)}
.card .time{font:700 16px 'JetBrains Mono';color:#fff;background:var(--g900);padding:4px 10px;border-radius:6px}
.card .dur{font:600 14px 'JetBrains Mono';color:#7a857f}
.card h3{font:800 25px/1.2 'Plus Jakarta Sans';color:#14231d;margin-bottom:4px}
.card .ref{font:600 14px 'JetBrains Mono';color:#B5122B;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.card .ref:before{content:"";width:14px;height:14px;border-radius:50%;background:#FF0000;display:inline-block}
.tag{font:800 12px 'JetBrains Mono';letter-spacing:.1em;padding:4px 9px;border-radius:5px}
.fld{display:grid;grid-template-columns:120px 1fr;gap:10px;margin-top:10px;font:500 16px/1.45 'Plus Jakarta Sans';color:#2b3631}
.fld b{font:800 12px 'JetBrains Mono';letter-spacing:.12em;color:#7b8781;padding-top:4px}
.fld.vo{background:#F1F6EF;border-radius:10px;padding:12px 14px;margin-top:14px}
.fld.vo div{font-style:italic;color:#1f3a2e}
.legend{display:flex;gap:26px;flex-wrap:wrap;margin:6px 0 14px}
.legend div{display:flex;align-items:center;gap:10px;font:600 16px 'Plus Jakarta Sans';color:#2b3631}
.legend i{width:26px;height:18px;border-radius:4px;display:inline-block}
.pill3{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;padding:10px 80px 40px}
.box{background:#fff;border-radius:18px;padding:26px 28px;box-shadow:0 10px 30px rgba(20,40,30,.07)}
.box h4{font:800 20px 'Plus Jakarta Sans';margin-bottom:10px;color:var(--g900);display:flex;gap:10px;align-items:center}
.box h4 em{font:800 12px 'JetBrains Mono';font-style:normal;letter-spacing:.12em;padding:4px 8px;border-radius:5px}
.box ul{list-style:none}
.box li{font:500 16px/1.5 'Plus Jakarta Sans';color:#34413b;padding:5px 0 5px 20px;position:relative}
.box li:before{content:"";position:absolute;left:2px;top:14px;width:8px;height:8px;border-radius:2px;background:var(--g700)}
.foot{padding:18px 80px 36px;font:600 14px 'JetBrains Mono';color:#7d8983;display:flex;justify-content:space-between}

/* ============ FRAME ELEMENTS (1920x1080 coordinates) ============ */
.F{position:absolute;inset:0;overflow:hidden;font-family:'Plus Jakarta Sans'}
.badge{position:absolute;right:40px;top:30px;width:150px;height:100px;perspective:700px;z-index:50}
.badge img{width:150px;height:100px;object-fit:contain;transform:rotateY(-24deg) rotateX(4deg);
filter:drop-shadow(0 0 2px #fff) drop-shadow(0 0 2px #fff) drop-shadow(0 8px 12px rgba(0,0,0,.45))}
.badge:after{content:"↔ 3D";position:absolute;right:0;top:104px;font:800 18px 'JetBrains Mono';color:#fff;
background:rgba(0,0,0,.55);padding:3px 8px;border-radius:5px}
.doodle{font-family:'Caveat','Kalam',cursive}
.paperbg{background:#F3EEDF;background-image:linear-gradient(rgba(60,90,80,.09) 2px,transparent 2px),
linear-gradient(90deg,rgba(60,90,80,.09) 2px,transparent 2px);background-size:64px 64px}
.chalkbg{background:radial-gradient(ellipse at 50% 40%,#2c5a48,#163a2d 70%,#0e271f)}
.gdark{background:radial-gradient(ellipse at 60% 40%,#1d6a50 0%,#0B2E22 55%,#06190f 100%)}
.kin{position:absolute;font-weight:800;letter-spacing:-.02em;color:#fff}
.lbx:before,.lbx:after{content:"";position:absolute;left:0;right:0;height:120px;background:#000;z-index:5}
.lbx:before{top:0}.lbx:after{bottom:0}
.glass{background:rgba(255,255,255,.08);border:2px solid rgba(255,255,255,.22);border-radius:26px;backdrop-filter:blur(8px)}
.shot{position:absolute;border-radius:18px;overflow:hidden;box-shadow:0 40px 90px rgba(0,0,0,.55)}
.shot img{width:100%;height:100%;object-fit:cover;display:block}
.mblur{filter:blur(3px)}
.cnt{font:800 220px/1 'Plus Jakarta Sans';letter-spacing:-.04em}
"""

SVG_FILTER = """<svg width="0" height="0" style="position:absolute"><defs>
<filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"/>
<feDisplacementMap in="SourceGraphic" scale="7"/></filter>
<filter id="chalk"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="5" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 -1.6 1.3" result="m"/>
<feComposite in="SourceGraphic" in2="m" operator="in" result="c"/><feDisplacementMap in="c" in2="n" scale="4"/></filter>
<filter id="glow"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs></svg>"""

BADGE = '<div class="badge"><img src="assets/logo-pptx.png"></div>'
LEAF = ('<svg viewBox="0 0 100 100" style="{st}"><path d="M50 95 C10 70 8 30 50 5 C92 30 90 70 50 95Z" '
        'fill="{c}"/><path d="M50 92 L50 18" stroke="{v}" stroke-width="4" fill="none"/>'
        '<path d="M50 60 L32 44 M50 45 L68 30 M50 75 L66 62" stroke="{v}" stroke-width="3" fill="none"/></svg>')


def leaf(st, c="#B6D973", v="#0B2E22"):
    return LEAF.format(st=st, c=c, v=v)


def spd_mark(size=200, color="#fff", leafc="#B6D973"):
    return (f'<div style="display:flex;align-items:center;gap:{size*0.06}px">'
            f'<span style="font:800 {size}px/1 \'Plus Jakarta Sans\';letter-spacing:-.04em;color:{color}">SPD</span>'
            + leaf(f"width:{size*0.62}px;height:{size*0.62}px;transform:rotate(28deg) translateY(-{size*0.18}px)", leafc)
            + "</div>")


def doodle_icon(kind):
    """Hand-drawn icons (rough filter applied by the parent)."""
    s = 'stroke="#22302A" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    hi = 'fill="#B6D973" opacity=".75"'
    red = 'stroke="#D62839" stroke-width="7" fill="none" stroke-linecap="round"'
    d = {
        "paper": f'<rect x="40" y="70" width="150" height="30" {hi}/><path {s} d="M40 170 h150 M40 140 h150 M40 110 h150 M40 80 h150 M40 80 v90 M190 80 v90"/>'
                 f'<path {s} d="M60 60 l20 -30 l20 30 M140 60 l20 -30 l20 30"/>',
        "cabinet": f'<rect x="60" y="30" width="110" height="150" rx="6" {hi}/><path {s} d="M60 30 h110 v150 h-110z M60 80 h110 M60 130 h110 M100 55 h30 M100 105 h30 M100 155 h30"/>'
                   f'<path {red} d="M175 40 l25 -15 M178 70 l28 0"/>',
        "dup": f'<rect x="40" y="50" width="90" height="120" {hi}/><path {s} d="M40 50 h90 v120 h-90z M100 30 h90 v120 h-60 M60 85 h50 M60 110 h50 M60 135 h40"/>'
               f'<path {red} d="M150 165 a12 12 0 1 0 0.1 0"/>',
        "hourglass": f'<path {hi} d="M75 140 h80 l-40 -40z"/><path {s} d="M60 30 h110 M60 190 h110 M70 30 c0 60 90 60 90 80 c0 20 -90 20 -90 80 M160 30 c0 60 -90 60 -90 80 c0 20 90 20 90 80"/>',
        "lost": f'<rect x="40" y="70" width="100" height="120" {hi}/><path {s} d="M40 70 h100 v120 h-100z M60 100 h60 M60 125 h60"/>'
                f'<path {s} stroke-dasharray="4 18" d="M150 80 q40 -40 70 -10"/><path {red} d="M175 15 q20 0 20 18 q0 14 -15 18 v14 M180 92 v2"/>',
        "cost": f'<circle cx="115" cy="105" r="70" {hi}/><path {s} d="M115 105 m-70 0 a70 70 0 1 0 140 0 a70 70 0 1 0 -140 0"/>'
                f'<text x="72" y="125" font-family="Caveat" font-weight="700" font-size="64" fill="#22302A">RM</text>'
                f'<path {red} d="M200 40 v60 m-14 -14 l14 14 l14 -14"/>',
    }[kind]
    return f'<svg viewBox="0 0 230 210" style="width:330px;height:300px;filter:url(#rough)">{d}</svg>'


def person(c):
    return (f'<svg viewBox="0 0 40 60" style="width:58px;height:86px"><circle cx="20" cy="12" r="10" fill="{c}"/>'
            f'<path d="M3 58 v-22 a17 17 0 0 1 34 0 v22z" fill="{c}"/></svg>')


# ---------------------------------------------------------------- frames
def F01():
    return f"""<div class="F lbx" style="background:#111">
<img src="assets/lk1-22.jpg" style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:grayscale(.45) contrast(1.1) brightness(.6);transform:scale(1.08) rotate(-1.5deg)">
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;filter:url(#chalk)">
<path d="M560 330 C760 220 1140 250 1220 420 C1300 600 980 760 700 700 C470 650 420 420 600 320" stroke="#fff" stroke-width="12" fill="none"/>
<path d="M1300 300 l120 -90 M1420 210 l-50 6 M1420 210 l-12 48" stroke="#fff" stroke-width="10" fill="none"/>
<circle cx="1530" cy="560" r="105" stroke="#fff" stroke-width="10" fill="none"/><path d="M1530 560 v-70 M1530 560 l50 30" stroke="#fff" stroke-width="10"/>
</svg>
<div class="doodle" style="position:absolute;left:1380px;top:120px;font:700 110px Caveat;color:#fff;transform:rotate(-8deg)">Fail mana?!</div>
<div class="kin" style="left:120px;bottom:170px;font-size:64px">Fail fizikal. <span style="color:#B6D973">Carian manual.</span></div><div style="position:absolute;left:1180px;top:760px;width:220px;height:124px;border:4px solid #fff;transform:rotate(-4deg);box-shadow:0 10px 24px rgba(0,0,0,.6);z-index:6;background:url(assets/lk3-3.jpg) center/cover"></div><div style="position:absolute;left:1415px;top:760px;width:220px;height:124px;border:4px solid #fff;transform:rotate(3deg);box-shadow:0 10px 24px rgba(0,0,0,.6);z-index:6;background:url(assets/lk3-22.jpg) center/cover"></div><div style="position:absolute;left:1650px;top:760px;width:220px;height:124px;border:4px solid #fff;transform:rotate(-2deg);box-shadow:0 10px 24px rgba(0,0,0,.6);z-index:6;background:url(assets/lk2-8.jpg) center/cover"></div>
<div style="position:absolute;left:120px;top:150px;font:800 22px 'JetBrains Mono';color:#fff;background:#8E1B33;padding:8px 14px;border-radius:6px;z-index:6">FOOTAGE LAKONAN · MONTAJ 3 KLIP · SPEED-RAMP → FREEZE</div>
{BADGE}</div>"""


def F02():
    sheets = ""
    import random
    r = random.Random(4)
    for i in range(26):
        x, y = r.randint(-100, 1900), r.randint(-60, 1040)
        w = r.randint(90, 260)
        rot = r.randint(-60, 60)
        ry = r.randint(-60, 60)
        bl = 0 if 500 < x < 1400 and 300 < y < 800 else r.choice([0, 3, 6, 10])
        op = .9 if bl < 5 else .5
        sheets += (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{w*1.41:.0f}px;background:#fff;'
                   f'opacity:{op};filter:blur({bl}px);transform:perspective(900px) rotateY({ry}deg) rotate({rot}deg);'
                   f'box-shadow:0 20px 40px rgba(0,0,0,.35);background-image:repeating-linear-gradient(#fff 0 22px,#dfe8e3 22px 24px)"></div>')
    return f"""<div class="F gdark">{sheets}
<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 52%,rgba(11,46,34,.92) 0 30%,rgba(11,46,34,.0) 62%)"></div>
<div style="position:absolute;left:0;right:0;top:250px;text-align:center;font:800 26px 'JetBrains Mono';letter-spacing:.32em;color:#B6D973">PERBADANAN MELAKA (MCORP)</div>
<div style="position:absolute;left:0;right:0;top:330px;display:flex;justify-content:center">{spd_mark(260)}</div>
<div style="position:absolute;left:0;right:0;top:640px;text-align:center;font:700 46px 'Plus Jakarta Sans';color:#fff">Pembangunan Sistem Pengurusan Data Bersepadu</div>
<div style="position:absolute;left:0;right:0;top:716px;text-align:center;font:600 italic 34px 'Plus Jakarta Sans';color:#D9AE52">Inovasi digital ke arah pengurusan hijau dan lestari</div>
<div style="position:absolute;left:-200px;top:610px;width:2400px;height:6px;background:linear-gradient(90deg,transparent,#D9AE52,transparent);transform:rotate(-4deg);opacity:.7;filter:blur(1px)"></div>
{BADGE}</div>"""


def F03():
    items = ["Tanah", "Bangunan", "Penyewaan", "Penilaian Aset", "Dokumen Hak Milik"]
    pos = [(250, 230), (1330, 200), (180, 690), (1370, 690), (760, 840)]
    tiles, lines = "", ""
    for (x, y), t in zip(pos, items):
        tiles += (f'<div class="glass" style="position:absolute;left:{x}px;top:{y}px;width:330px;height:130px;display:flex;align-items:center;'
                  f'justify-content:center;font:700 34px \'Plus Jakarta Sans\';color:#fff;transform:perspective(800px) rotateY({(960-x-165)/40:.0f}deg)">{t}</div>')
        lines += f'<line x1="{x+165}" y1="{y+65}" x2="960" y2="520" stroke="#B6D973" stroke-width="4" stroke-dasharray="2 16" stroke-linecap="round"/>'
    return f"""<div class="F gdark">
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;filter:url(#glow)">{lines}
<circle cx="960" cy="520" r="250" stroke="rgba(182,217,115,.35)" stroke-width="3" fill="none"/>
<circle cx="960" cy="520" r="330" stroke="rgba(182,217,115,.15)" stroke-width="2" fill="none"/></svg>
<div style="position:absolute;left:760px;top:320px;width:400px;height:400px;border-radius:50%;background:radial-gradient(circle,#2a8a66,#165A44);
box-shadow:0 0 120px rgba(182,217,115,.55);display:flex;flex-direction:column;align-items:center;justify-content:center">
{spd_mark(120)}<div style="font:800 20px 'JetBrains Mono';letter-spacing:.2em;color:#d9f0c0;margin-top:10px">SATU PLATFORM</div>
<div style="font:800 20px 'JetBrains Mono';letter-spacing:.2em;color:#d9f0c0">BERPUSAT</div></div>{tiles}
{BADGE}</div>"""


def F04():
    names = [("01", "Penggunaan kertas tinggi", "paper"), ("02", "Ruang simpanan fizikal besar", "cabinet"),
             ("03", "Pertindihan data", "dup"), ("04", "Carian maklumat lambat", "hourglass"),
             ("05", "Risiko kehilangan dokumen", "lost"), ("06", "Kos operasi tinggi", "cost")]
    cells = ""
    for i, (n, t, k) in enumerate(names):
        x, y = 150 + (i % 3) * 560, 190 + (i // 3) * 430
        cells += (f'<div style="position:absolute;left:{x}px;top:{y}px;width:520px;height:400px;text-align:center">'
                  f'<div class="doodle" style="position:absolute;left:10px;top:-10px;font:700 80px Caveat;color:#D62839">{n}</div>'
                  f'<div style="margin-top:10px">{doodle_icon(k)}</div>'
                  f'<div class="doodle" style="font:700 46px Caveat;color:#22302A;margin-top:-6px">{t}</div></div>')
    return f"""<div class="F paperbg">
<div class="doodle" style="position:absolute;left:150px;top:60px;font:700 92px Caveat;color:#165A44">Sebelum SPD…</div>
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;filter:url(#rough)"><path d="M150 165 C400 150 600 175 700 160" stroke="#B6D973" stroke-width="16" fill="none" stroke-linecap="round"/></svg>
{cells}{BADGE}</div>"""


def F05():
    return f"""<div class="F" style="background:#0B2E22">
<div style="position:absolute;inset:0;clip-path:polygon(0 0,58% 0,42% 100%,0 100%)">
<img src="assets/before-files.jpg" style="width:100%;height:100%;object-fit:cover;filter:grayscale(1) contrast(1.15) brightness(.8)"></div>
<div style="position:absolute;inset:0;clip-path:polygon(58% 0,100% 0,100% 100%,42% 100%)">
<img src="assets/ui-asettakalih.jpg" style="width:100%;height:100%;object-fit:cover;object-position:left top"></div>
<div style="position:absolute;left:0;top:0;width:100%;height:100%;background:linear-gradient(115deg,transparent 46%,rgba(182,217,115,.9) 49.6%,#fff 50%,rgba(182,217,115,.9) 50.4%,transparent 54%)"></div>
<div style="position:absolute;left:80px;top:90px;font:800 30px 'JetBrains Mono';letter-spacing:.2em;color:#fff;background:rgba(0,0,0,.6);padding:10px 18px;border-radius:8px">SEBELUM · FAIL FIZIKAL</div>
<div style="position:absolute;right:240px;bottom:250px;font:800 30px 'JetBrains Mono';letter-spacing:.2em;color:#fff;background:#165A44;padding:10px 18px;border-radius:8px">SELEPAS · CARIAN SPD</div>
<div style="position:absolute;left:0;right:0;bottom:80px;display:flex;justify-content:center;gap:28px">
{''.join(f'<div style="font:800 34px Plus Jakarta Sans;color:#0B2E22;background:#B6D973;padding:16px 36px;border-radius:60px;box-shadow:0 14px 30px rgba(0,0,0,.4)">{t}</div>' for t in ["BERPUSAT","ATAS TALIAN","LEBIH CEKAP"])}</div>
<div style="position:absolute;left:800px;top:380px;width:230px;height:230px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#fff,#d8d2c2 60%,#a9a28f);
box-shadow:0 30px 60px rgba(0,0,0,.6);filter:url(#rough)"></div>
{BADGE}</div>"""


def F06():
    return f"""<div class="F" style="background:radial-gradient(ellipse at 50% 30%,#1b2a25,#070b09 75%)">
<div style="position:absolute;inset:0;perspective:1800px">
<div class="shot mblur" style="left:-260px;top:250px;width:900px;height:428px;transform:rotateY(48deg);opacity:.7"><img src="assets/ui-asetalih.jpg"></div>
<div class="shot" style="left:430px;top:170px;width:1060px;height:504px;transform:rotateY(-10deg) rotateX(6deg);box-shadow:0 0 0 3px #B6D973,0 60px 120px rgba(0,0,0,.7)"><img src="assets/ui-asettakalih.jpg"></div>
<div class="shot mblur" style="left:1340px;top:250px;width:900px;height:428px;transform:rotateY(-48deg);opacity:.7"><img src="assets/ui-modalinsan.jpg" style="filter:blur(2px)"></div>
</div>
<div style="position:absolute;left:520px;top:750px;font:800 26px 'JetBrains Mono';letter-spacing:.24em;color:#B6D973">MODUL 02 / 05</div>
<div class="kin" style="left:520px;top:792px;font-size:86px">Aset Tak Alih</div>
<div style="position:absolute;left:520px;top:900px;font:500 34px 'Plus Jakarta Sans';color:#cfd9d3">Carian · cukai · hak milik · laporan</div>
<div style="position:absolute;left:1380px;top:820px;display:flex;gap:16px">{''.join(f'<i style="width:{60 if i==1 else 18}px;height:18px;border-radius:9px;background:{"#B6D973" if i==1 else "#3d4a44"};display:block"></i>' for i in range(5))}</div>
<svg viewBox="0 0 60 80" style="position:absolute;left:1010px;top:420px;width:54px;filter:drop-shadow(0 0 20px #B6D973)"><path d="M5 5 L5 65 L20 50 L32 75 L42 70 L30 46 L52 46Z" fill="#fff" stroke="#000" stroke-width="3"/></svg>
{BADGE}</div>"""


def F07():
    comps = [("Digital Land Management", "Rekod tanah & hak milik digital", "Kurang dokumen fizikal"),
             ("Digital Property Management", "Maklumat bangunan & premis", "Kurang penyimpanan fail"),
             ("Digital Tenancy Management", "Rekod sewaan, pajakan & kontrak", "Kurang cetakan dokumen"),
             ("Digital Asset Valuation", "Laporan & rekod penilaian aset", "Kurang penggunaan kertas"),
             ("Centralised Document Repository", "Pusat simpanan dokumen bersepadu", "Kurang pertindihan & ruang arkib")]
    cards = ""
    for i, (a, b, c) in enumerate(comps):
        x = 90 + i * 352
        cards += (f'<div style="position:absolute;left:{x}px;top:300px;width:330px;height:560px;background:#fff;border-radius:24px;'
                  f'box-shadow:0 20px 50px rgba(11,46,34,.18);padding:30px 26px;border-top:10px solid #165A44">'
                  f'<div style="font:800 22px JetBrains Mono;color:#26745A">0{i+1}</div>'
                  f'<div style="font:800 31px/1.15 Plus Jakarta Sans;color:#0B2E22;margin-top:10px;height:110px">{a}</div>'
                  f'<div style="font:500 24px/1.35 Plus Jakarta Sans;color:#4c5a53;margin-top:16px;height:110px">{b}</div>'
                  f'<div style="position:absolute;left:20px;right:20px;bottom:24px;background:#E9F2E7;border-radius:16px;padding:18px 18px 18px 74px;'
                  f'font:700 23px/1.3 Plus Jakarta Sans;color:#165A44">{leaf("position:absolute;left:14px;top:50%;transform:translateY(-50%) rotate(20deg);width:48px;height:48px","#7DB544")}{c}</div></div>')
    return f"""<div class="F" style="background:linear-gradient(#F5F2EA,#E9F2E7)">
<div style="position:absolute;left:90px;top:90px;font:800 24px 'JetBrains Mono';letter-spacing:.24em;color:#26745A">INOVASI HIJAU SPD</div>
<div style="position:absolute;left:90px;top:130px;font:800 76px 'Plus Jakarta Sans';color:#0B2E22;letter-spacing:-.02em">Lima komponen utama</div>
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0"><path d="M60 960 C400 900 600 1010 960 950 S1600 900 1880 960" stroke="#7DB544" stroke-width="8" fill="none"/>
{''.join(f'<g transform="translate({255+i*352},{948 + (8 if i%2 else -6)}) rotate({-30 if i%2 else 30})"><path d="M0 0 C-20 -18 -20 -44 0 -60 C20 -44 20 -18 0 0Z" fill="#7DB544"/></g>' for i in range(5))}</svg>
{cards}{BADGE}</div>"""


def F08():
    layers = "".join(
        f'<div style="position:absolute;left:0;right:0;top:{330+i*3}px;text-align:center;font:900 300px/1 \'Plus Jakarta Sans\';letter-spacing:-.04em;'
        f'color:{"#0f3f2f" if i<14 else "#fff"};transform:translateX({i*2}px)">IMPAK SPD</div>' for i in range(15))
    streaks = "".join(f'<div style="position:absolute;left:{x}px;top:0;width:{w}px;height:1080px;background:linear-gradient(transparent,rgba(182,217,115,.35),transparent);transform:skewX(-20deg)"></div>'
                      for x, w in [(200, 6), (520, 2), (1300, 10), (1650, 3)])
    return f"""<div class="F" style="background:#050806">{streaks}
<div style="position:absolute;inset:0;transform:perspective(1200px) rotateX(10deg) scale(1.05)">{layers}</div>
<div style="position:absolute;left:0;right:0;top:720px;text-align:center;font:800 30px 'JetBrains Mono';letter-spacing:.5em;color:#B6D973">BAB 03</div>
{BADGE}</div>"""


def F09():
    cols = [("MASA", "Carian & semakan rekod lebih pantas", "⏱", 520),
            ("TENAGA KERJA", "18 → 9 orang (senario anggaran kos upah)", "", 640),
            ("RUANG & BAHAN", "Dokumen fizikal dikurangkan; ruang dimanfaat semula", "", 470)]
    html = ""
    for i, (a, b, ic, h) in enumerate(cols):
        x = 200 + i * 540
        extra = ""
        if a == "TENAGA KERJA":
            extra = '<div style="display:flex;flex-wrap:wrap;width:330px;gap:6px;margin:14px auto 0">' + "".join(
                person("#B6D973" if j < 9 else "rgba(255,255,255,.18)") for j in range(18)) + "</div>"
        html += (f'<div style="position:absolute;left:{x}px;bottom:0;width:440px;height:{h}px;background:linear-gradient(#26745A,#165A44);'
                 f'border-radius:26px 26px 0 0;padding:40px 34px;box-shadow:0 -10px 60px rgba(0,0,0,.35)">'
                 f'<div style="font:800 46px Plus Jakarta Sans;color:#fff">{a}</div>'
                 f'<div style="font:500 28px/1.35 Plus Jakarta Sans;color:#d8ecdf;margin-top:12px">{b}</div>{extra}</div>')
    return f"""<div class="F gdark">
<div style="position:absolute;left:200px;top:100px;font:800 24px 'JetBrains Mono';letter-spacing:.24em;color:#B6D973">HASIL · KRITERIA 7</div>
<div class="kin" style="left:200px;top:140px;font-size:72px">Kecekapan sumber organisasi</div>{html}{BADGE}</div>"""


def F10():
    return f"""<div class="F chalkbg">
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;filter:url(#chalk)" stroke="#f1f5ee" fill="none" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">
<path d="M220 420 h220 l-26 300 h-168z M200 420 h260 M290 390 h80"/><path d="M270 470 l20 200 M330 470 v200 M390 470 l-20 200"/>
<path d="M500 560 l60 0 M540 530 l30 30 l-30 30" stroke="#B6D973"/><path d="M640 560 h120 l-14 160 h-92z M630 560 h140"/>
<path d="M880 700 c120 -260 260 -260 380 -40" stroke-dasharray="6 30"/><path d="M860 700 h90 l14 -40 h-110z M870 710 a14 14 0 1 0 1 0 M940 710 a14 14 0 1 0 1 0"/>
<path d="M1060 520 l140 130 M1200 520 l-140 130" stroke="#ff8a8a" stroke-width="12"/>
<path d="M1400 420 h300 v300 h-300z M1430 460 h80 v100 h-80z M1530 460 h80 v100 h-80z"/><path d="M1620 470 l40 -60 M1660 410 l-38 6"/>
<path d="M1440 640 h220 M1470 640 v70 M1630 640 v70 M1500 600 a24 24 0 1 0 1 0 M1600 600 a24 24 0 1 0 1 0" stroke="#B6D973"/></svg>
<div class="doodle" style="position:absolute;left:180px;top:90px;font:700 96px Caveat;color:#fff">Kurang pencemaran, lebih produktif</div>
<div class="doodle" style="position:absolute;left:220px;top:780px;font:700 50px Caveat;color:#e9f0e4">sisa kertas ↓</div>
<div class="doodle" style="position:absolute;left:920px;top:780px;font:700 50px Caveat;color:#e9f0e4">tiada perjalanan fail</div>
<div class="doodle" style="position:absolute;left:1400px;top:780px;font:700 50px Caveat;color:#e9f0e4">bilik fail → ruang kerja</div>
{BADGE}</div>"""


def F11():
    flying = "".join(
        f'<div style="position:absolute;left:{x}px;top:{y}px;width:150px;height:170px;background:#fff;border-radius:10px;transform:perspective(600px) rotateX({rx}deg) rotate({r}deg);'
        f'opacity:{o};box-shadow:0 20px 30px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;font:800 70px Plus Jakarta Sans;color:#165A44">{n}</div>'
        for x, y, rx, r, o, n in [(980, 360, 50, 14, .85, 13), (1150, 240, 60, -20, .7, 11), (1320, 160, 66, 30, .55, 9),
                                  (1480, 110, 70, -10, .4, 7), (1620, 60, 74, 40, .3, 5)])
    leaves = "".join(leaf(f"position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;transform:rotate({r}deg);opacity:.85", "#7DB544")
                     for x, y, s, r in [(1500, 300, 70, 40), (1700, 200, 54, -30), (1780, 380, 44, 10), (1580, 460, 36, 70)])
    return f"""<div class="F gdark">
<div style="position:absolute;left:170px;top:250px;width:640px;height:620px;background:#fff;border-radius:30px;box-shadow:0 50px 100px rgba(0,0,0,.5);
transform:perspective(1400px) rotateY(18deg);overflow:hidden">
<div style="height:150px;background:#8E1B33;display:flex;align-items:center;justify-content:center;font:800 54px Plus Jakarta Sans;color:#fff;letter-spacing:.1em">SEWAAN</div>
<div style="text-align:center;margin-top:40px;font:900 300px/1 Plus Jakarta Sans;color:#165A44;letter-spacing:-.05em">3</div>
<div style="text-align:center;font:800 54px Plus Jakarta Sans;color:#165A44">HARI</div></div>
{flying}{leaves}
<div style="position:absolute;left:900px;top:640px;font:800 120px Plus Jakarta Sans;color:rgba(255,255,255,.4);text-decoration:line-through;text-decoration-color:#ff5a5a">14 HARI</div>
<div style="position:absolute;left:900px;top:800px;font:800 50px Plus Jakarta Sans;color:#0B2E22;background:#B6D973;padding:18px 40px;border-radius:16px">11 HARI DIJIMATKAN</div>
{BADGE}</div>"""


def F12():
    return f"""<div class="F" style="background:#081310">
<div class="shot" style="left:120px;top:170px;width:560px;height:452px;transform:rotate(-4deg)"><img src="assets/manual-check.jpg" style="filter:grayscale(1) brightness(.85)"></div>
<div class="shot" style="left:700px;top:200px;width:620px;height:500px;transform:rotate(2deg)"><img src="assets/barcode.jpg"></div>
<div style="position:absolute;left:640px;top:430px;width:760px;height:8px;background:#44ff88;box-shadow:0 0 30px 10px rgba(68,255,136,.6),0 0 80px 30px rgba(68,255,136,.25);transform:rotate(2deg)"></div>
<div class="shot" style="left:1360px;top:250px;width:470px;height:340px;transform:perspective(900px) rotateY(-18deg)"><img src="assets/spd-record.jpg"></div>
<div style="position:absolute;left:160px;top:760px;font:800 130px Plus Jakarta Sans;color:rgba(255,255,255,.35);text-decoration:line-through;text-decoration-color:#ff5a5a">20</div>
<div style="position:absolute;left:400px;top:770px;font:800 70px Plus Jakarta Sans;color:#fff">→</div>
<div style="position:absolute;left:520px;top:740px;font:900 170px/1 Plus Jakarta Sans;color:#44ff88">2 <span style="font-size:70px">HARI</span></div>
<div style="position:absolute;left:1080px;top:820px;font:600 36px Plus Jakarta Sans;color:#cfe">Semakan SPD / barcode · <b style="color:#fff">18 hari dijimatkan</b></div>
{BADGE}</div>"""


def F13():
    people = "".join(person("#D9AE52" if j < 9 else "rgba(255,255,255,.16)") for j in range(18))
    return f"""<div class="F gdark">
<div style="position:absolute;left:130px;top:130px;font:800 24px 'JetBrains Mono';letter-spacing:.24em;color:#B6D973">PENJIMATAN KOS TENAGA KERJA</div>
<div style="position:absolute;left:130px;top:200px;display:flex;flex-wrap:wrap;width:620px;gap:10px">{people}</div>
<div style="position:absolute;left:130px;top:420px;font:700 34px Plus Jakarta Sans;color:#fff">18 orang → <span style="color:#D9AE52">9 orang</span></div>
<table style="position:absolute;left:130px;top:520px;width:700px;border-collapse:separate;border-spacing:0 12px;font:700 32px Plus Jakarta Sans;color:#fff">
<tr style="color:#B6D973;font-size:24px;letter-spacing:.14em"><td>UKURAN</td><td>SEBELUM</td><td>SELEPAS</td></tr>
<tr><td>Kos bulanan</td><td style="opacity:.55">RM36,306</td><td>RM18,153</td></tr>
<tr><td>Kos tahunan</td><td style="opacity:.55">RM435,672</td><td>RM217,836</td></tr></table>
<div style="position:absolute;right:120px;top:300px;text-align:right">
<div style="font:800 30px 'JetBrains Mono';letter-spacing:.2em;color:#D9AE52">ANGGARAN PENJIMATAN TAHUNAN</div>
<div style="font:900 190px/1.05 Plus Jakarta Sans;letter-spacing:-.04em;background:linear-gradient(180deg,#fff3c8,#D9AE52 60%,#9b7424);-webkit-background-clip:text;color:transparent">RM217,836</div>
<div style="font:600 30px Plus Jakarta Sans;color:#cfe3d6">kos tenaga kerja (kaedah anggaran)</div></div>
{BADGE}</div>"""


def F14():
    def bars(x, title, a, b, mx, pct, unit):
        ha, hb = a / mx * 440, b / mx * 440
        return (f'<div style="position:absolute;left:{x}px;top:170px;width:700px">'
                f'<div style="font:800 40px Plus Jakarta Sans;color:#0B2E22">{title}</div>'
                f'<div style="position:absolute;top:120px;left:40px;width:620px;height:500px;border-bottom:4px solid #22302A">'
                f'<div style="position:absolute;bottom:0;left:60px;width:200px;height:{ha:.0f}px;background:linear-gradient(90deg,#5f7d8c,#3d5866);border-radius:10px 10px 0 0;box-shadow:16px -8px 0 #2b414c"></div>'
                f'<div style="position:absolute;bottom:{ha+12:.0f}px;left:60px;width:200px;text-align:center;font:800 44px Plus Jakarta Sans">{a:,}</div>'
                f'<div style="position:absolute;bottom:0;left:360px;width:200px;height:{hb:.0f}px;background:linear-gradient(90deg,#3fa877,#26745A);border-radius:10px 10px 0 0;box-shadow:16px -8px 0 #1a5a43"></div>'
                f'<div style="position:absolute;bottom:{hb+12:.0f}px;left:360px;width:200px;text-align:center;font:800 44px Plus Jakarta Sans;color:#165A44">{b:,}</div>'
                f'<div style="position:absolute;bottom:-50px;left:60px;width:200px;text-align:center;font:700 28px JetBrains Mono">2021</div>'
                f'<div style="position:absolute;bottom:-50px;left:360px;width:200px;text-align:center;font:700 28px JetBrains Mono">2025</div></div>'
                f'<div class="doodle" style="position:absolute;top:110px;right:-10px;font:700 84px Caveat;color:#D62839;transform:rotate(-6deg)">{pct}</div>'
                f'<div style="position:absolute;top:700px;left:40px;font:600 28px Plus Jakarta Sans;color:#3b4842">{unit}</div></div>')
    return f"""<div class="F paperbg">
{bars(140, "Permohonan kertas A4", 1242, 926, 1300, "−25.4%", "Pengurangan 316 unit")}
{bars(1040, "Permohonan dakwat pencetak", 174, 105, 182, "−39.7%", "Pengurangan 69 unit")}
<svg viewBox="0 0 1920 1080" style="position:absolute;inset:0;filter:url(#rough)"><path d="M960 200 v700" stroke="#22302A" stroke-width="5" stroke-dasharray="10 20"/></svg>
{BADGE}</div>"""


def F15():
    parts = ""
    import random
    r = random.Random(9)
    for _ in range(260):
        x = r.randint(700, 1250)
        y = r.randint(200, 900)
        s = r.randint(4, 16)
        c = r.choice(["#e8e1cf", "#f6f1e3", "#B6D973", "#ffffff", "#c9c1ad"])
        parts += f'<i style="position:absolute;left:{x}px;top:{y}px;width:{s}px;height:{s}px;background:{c};opacity:{r.random()*.8+.2:.2f};display:block;transform:rotate({r.randint(0,90)}deg)"></i>'
    return f"""<div class="F gdark">
<div class="shot" style="left:110px;top:250px;width:640px;height:520px;transform:perspective(1000px) rotateY(20deg);
-webkit-mask-image:linear-gradient(90deg,#000 55%,transparent 100%)"><img src="assets/files-cabinet.jpg"></div>
{parts}
<div class="shot" style="left:1180px;top:250px;width:640px;height:520px;transform:perspective(1000px) rotateY(-20deg);box-shadow:0 0 0 3px #B6D973,0 40px 90px rgba(0,0,0,.6)"><img src="assets/spd-record.jpg" style="object-fit:contain;background:#fff"></div>
<div class="kin" style="left:0;right:0;top:860px;text-align:center;font-size:96px;letter-spacing:.12em">DIGITALISASI</div>
{BADGE}</div>"""


def F16():
    pol = [("manual-stock1.jpg", "Manual: permohonan stok", 140, 220, -8, True),
           ("spd-stock.jpg", "SPD: permohonan stok", 600, 160, 4, False),
           ("manual-check.jpg", "Sebelum: pemeriksaan manual", 1060, 250, -3, True),
           ("barcode.jpg", "Selepas: imbas barcode", 1420, 140, 7, False)]
    html = "".join(
        f'<div style="position:absolute;left:{x}px;top:{y}px;width:420px;background:#fff;padding:20px 20px 70px;transform:rotate({r}deg);box-shadow:0 30px 60px rgba(0,0,0,.45)">'
        f'<img src="assets/{f}" style="width:380px;height:330px;object-fit:cover;display:block;{"filter:grayscale(1)" if g else ""}">'
        f'<div class="doodle" style="position:absolute;left:20px;bottom:12px;font:700 38px Caveat;color:#22302A">{t}</div></div>'
        for f, t, x, y, r, g in pol)
    return f"""<div class="F" style="background:radial-gradient(ellipse at 50% 40%,#7a5a3c,#3b2a1b 80%)">{html}
<div style="position:absolute;left:140px;top:860px;font:800 26px 'JetBrains Mono';letter-spacing:.24em;color:#F3E3B5">BUKTI PELAKSANAAN · SEBELUM & SELEPAS</div>
{BADGE}</div>"""


def F17():
    return f"""<div class="F" style="background:linear-gradient(120deg,#F5F2EA,#E9F2E7)">
<div class="shot" style="left:200px;top:120px;width:560px;height:762px;transform:rotate(-5deg);border-radius:6px"><img src="assets/copyright.png" style="object-fit:contain;background:#fff"></div>
<div style="position:absolute;left:600px;top:700px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle at 40% 35%,#d43a3a,#8E1B33 70%);
box-shadow:0 20px 40px rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center;font:800 30px JetBrains Mono;color:#ffd9d9;transform:rotate(-12deg)">HAK<br>CIPTA</div>
<div style="position:absolute;left:960px;top:260px;width:820px">
<div style="font:800 24px 'JetBrains Mono';letter-spacing:.24em;color:#26745A">KELANGSUNGAN · KRITERIA 18</div>
<div style="font:800 80px/1.05 Plus Jakarta Sans;color:#0B2E22;margin-top:16px;letter-spacing:-.02em">Diiktiraf. Diguna pakai sepenuhnya.</div>
<div style="margin-top:40px;background:#fff;border-left:10px solid #165A44;border-radius:16px;padding:26px 30px;font:600 32px/1.35 Plus Jakarta Sans;color:#2b3a33">
Sijil Pemberitahuan Hak Cipta<br><b style="color:#165A44">2 Mac 2020</b></div>
<div style="margin-top:20px;background:#fff;border-left:10px solid #B6D973;border-radius:16px;padding:26px 30px;font:600 32px/1.35 Plus Jakarta Sans;color:#2b3a33">
Platform utama pengurusan data MCORP</div></div>
{BADGE}</div>"""


# ---- SPD 2.0 dummy homepage (laman utama), styled like the live SPD (maroon sidebar, MCORP header)
# the five SPD Green Dashboard modules from the user's proposal (name, weight %, score)
GPS = [("Paperless Index", 30, 86), ("Carbon Saving Index", 20, 72), ("Resource Efficiency Index", 20, 88),
       ("Green Performance Monitoring", 15, 84), ("Green Analytics & Strategic Decision", 15, 78)]
GREEN_INDEX = round(sum(w * s for _, w, s in GPS) / 100)  # 82 -> "Advanced Green Performance" (80-89)


SCROLLHINT = ('<div style="position:absolute;left:330px;top:84px;font:800 22px JetBrains Mono;letter-spacing:.24em;color:#0B2E22;'
              'background:#B6D973;padding:8px 16px;border-radius:6px;z-index:40">AKAN DATANG</div>'
              '<div style="position:absolute;right:30px;top:300px;width:12px;height:600px;border-radius:6px;background:rgba(0,0,0,.15);z-index:40">'
              '<i style="position:absolute;left:0;right:0;top:330px;height:170px;border-radius:6px;background:#165A44;display:block"></i></div>'
              '<svg viewBox="0 0 60 90" style="position:absolute;right:70px;top:520px;width:56px;z-index:40;filter:drop-shadow(0 6px 12px rgba(0,0,0,.4))">'
              '<rect x="8" y="4" width="44" height="78" rx="22" fill="#fff" stroke="#0B2E22" stroke-width="4"/>'
              '<rect x="27" y="16" width="6" height="16" rx="3" fill="#26745A"/><path d="M30 92 l-8 -8 h16z" fill="#0B2E22"/></svg>')


def spd2_homepage(scroll=0, full=False, click=None, soon=False):
    """1920x1080 browser frame. scroll shifts the page up to reveal the Green Dashboard section."""
    # values from the user's KPI table (kpi.jpeg); carbon card uses the proposal's own example (8,000 helai)
    kpis = [("PAPERLESS · KERTAS A4", "−25.4%", "1,242 → 926 unit", "316 unit · RM3,634 dijimatkan"),
            ("CARBON SAVING", "8,000", "helai cetakan dielakkan", "× faktor pelepasan = kg CO₂e"),
            ("RESOURCE · DAKWAT", "−39.7%", "174 → 105 unit", "69 unit · RM7,107 dijimatkan"),
            ("MASA CARIAN DOKUMEN", "−90%", "30 → 3 minit", "27 minit dijimatkan"),
            ("RUANG SIMPANAN FAIL", "1,550", "kaki persegi dibebaskan", "kini disewakan (Aras 10)"),
            ("JUMLAH PENJIMATAN & HASIL", "RM178,141", "kertas + dakwat + sewaan ruang", "RM3,634 + RM7,107 + RM167,400")]
    kh = "".join(
        f'<div style="background:#fff;border-radius:14px;padding:18px 20px;box-shadow:0 2px 10px rgba(0,0,0,.06);border-top:5px solid {"#D9AE52" if i==5 else "#26745A"}">'
        f'<div style="font:800 13px JetBrains Mono;letter-spacing:.12em;color:#6b7a73">{a}</div>'
        f'<div style="font:800 {40 if i==5 else 48}px/1.1 Plus Jakarta Sans;color:{"#9b7424" if i==5 else "#165A44"};margin-top:8px">{b}</div>'
        f'<div style="font:600 17px Plus Jakarta Sans;color:#2b3a33;margin-top:6px">{c}</div>'
        f'<div style="font:500 14px Plus Jakarta Sans;color:#8a958f">{d}</div></div>' for i, (a, b, c, d) in enumerate(kpis))
    gps_rows = "".join(
        f'<div style="display:grid;grid-template-columns:250px 1fr 40px;gap:10px;align-items:center;font:600 15px Plus Jakarta Sans;color:#2b3a33;margin:7px 0">'
        f'<span>{n} <span style="color:#8a958f">({w}%)</span></span><span style="height:10px;border-radius:5px;background:#E3EBE5;position:relative">'
        f'<i style="position:absolute;left:0;top:0;bottom:0;width:{s}%;border-radius:5px;background:linear-gradient(90deg,#26745A,#B6D973);display:block"></i></span>'
        f'<b style="text-align:right">{s}</b></div>' for n, w, s in GPS)
    div_rows = "".join(
        f'<div style="display:grid;grid-template-columns:230px 1fr 54px 130px;gap:12px;align-items:center;font:600 16px Plus Jakarta Sans;color:#2b3a33;margin:12px 0">'
        f'<span>{n}</span><span style="height:12px;border-radius:6px;background:#E3EBE5;position:relative">'
        f'<i style="position:absolute;left:0;top:0;bottom:0;width:{v}%;border-radius:6px;background:linear-gradient(90deg,#26745A,#B6D973);display:block"></i></span>'
        f'<b style="text-align:right">{v}%</b><span style="font:700 14px Plus Jakarta Sans;color:{c};background:{bg};padding:4px 10px;border-radius:20px;text-align:center">{r}</span></div>'
        for n, v, r, c, bg in [("Pentadbiran", 90, "Cemerlang", "#165A44", "#E9F2E7"), ("Kewangan", 85, "Baik", "#26745A", "#EEF5EC"),
                               ("Pengurusan Hartanah", 95, "Cemerlang", "#165A44", "#E9F2E7"), ("Pengurusan Projek", 75, "Memuaskan", "#9b7424", "#F7EFDC")])
    # real figures from the KPI table: where the RM178,141 comes from
    parts = [("Sewaan ruang pejabat Aras 10", 167400, "#D9AE52"), ("Dakwat pencetak", 7107, "#26745A"), ("Kertas A4", 3634, "#B6D973")]
    tot = sum(v for _, v, _ in parts)
    C, acc, arcs = 2 * 3.14159 * 78, 0.0, ""
    for _, v, col in parts:
        ln = C * v / tot
        arcs += (f'<circle cx="100" cy="100" r="78" fill="none" stroke="{col}" stroke-width="34" stroke-dasharray="{max(ln - 2, 3):.1f} {C:.1f}" '
                 f'stroke-dashoffset="{-acc:.1f}" transform="rotate(-90 100 100)"/>')
        acc += ln
    donut = (f'<svg viewBox="0 0 200 200" style="width:210px;height:210px;flex:none">{arcs}'
             f'<text x="100" y="96" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="21" fill="#0B2E22">RM178,141</text>'
             f'<text x="100" y="120" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="12" fill="#6b7a73">JUMLAH</text></svg>')
    legend = "".join(f'<div style="display:grid;grid-template-columns:18px 1fr auto 52px;gap:12px;align-items:center;font:600 17px Plus Jakarta Sans;color:#2b3a33;margin:14px 0">'
                     f'<i style="width:18px;height:18px;border-radius:5px;background:{col};display:block"></i><span>{n}</span>'
                     f'<b style="font-weight:800;color:#0B2E22">RM{v:,}</b><span style="text-align:right;color:#6b7a73">{v * 100 / tot:.0f}%</span></div>'
                     for n, v, col in parts)
    split = f'<div style="display:flex;align-items:center;gap:30px;margin-top:6px">{donut}<div style="flex:1">{legend}</div></div>'
    gi = GREEN_INDEX
    circ = 2 * 3.14159 * 110
    gauge = (f'<svg viewBox="0 0 260 260" style="width:250px;height:250px"><circle cx="130" cy="130" r="110" stroke="#E3EBE5" stroke-width="22" fill="none"/>'
             f'<circle cx="130" cy="130" r="110" stroke="url(#gg)" stroke-width="22" fill="none" stroke-linecap="round" '
             f'stroke-dasharray="{circ*gi/100:.0f} {circ:.0f}" transform="rotate(-90 130 130)"/>'
             f'<defs><linearGradient id="gg"><stop offset="0" stop-color="#26745A"/><stop offset="1" stop-color="#B6D973"/></linearGradient></defs>'
             f'<text x="130" y="138" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="76" fill="#0B2E22">{gi}</text>'
             f'<text x="130" y="176" text-anchor="middle" font-family="JetBrains Mono" font-weight="700" font-size="18" fill="#6b7a73">/ 100</text></svg>')
    trend = ('<svg viewBox="0 0 520 210" style="width:100%;height:210px">'
             '<line x1="40" y1="180" x2="510" y2="180" stroke="#cfd8d2" stroke-width="2"/>'
             '<rect x="90" y="30" width="80" height="150" rx="6" fill="#5f7d8c"/><rect x="190" y="68" width="80" height="112" rx="6" fill="#3fa877"/>'
             '<rect x="320" y="30" width="80" height="150" rx="6" fill="#5f7d8c"/><rect x="420" y="89" width="80" height="91" rx="6" fill="#3fa877"/>'
             '<text x="130" y="22" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="18">1,242</text>'
             '<text x="230" y="60" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="18" fill="#165A44">926</text>'
             '<text x="360" y="22" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="18">174</text>'
             '<text x="460" y="81" text-anchor="middle" font-family="Plus Jakarta Sans" font-weight="800" font-size="18" fill="#165A44">105</text>'
             '<text x="180" y="204" text-anchor="middle" font-family="JetBrains Mono" font-size="15">Kertas A4</text>'
             '<text x="410" y="204" text-anchor="middle" font-family="JetBrains Mono" font-size="15">Dakwat</text></svg>')
    side = "".join(
        f'<div style="display:flex;align-items:center;gap:12px;padding:14px 22px;font:600 17px Plus Jakarta Sans;color:#fff;'
        f'{"background:rgba(255,255,255,.14);border-left:4px solid #fff;" if i==0 and not full else ""}">'
        f'<i style="width:18px;height:18px;border:2px solid currentColor;border-radius:4px;display:block"></i>{t}</div>'
        for i, t in enumerate(["Utama", "Pengurusan Aset Tak Alih", "Pengurusan Aset Alih", "Pengurusan Stor",
                               "Pengurusan Modal Insan", "Sistem", "Bantuan", "Log Keluar"]))
    modules = "".join(f'<span style="font:700 14px Plus Jakarta Sans;color:#165A44;background:#E9F2E7;border:1px solid #cfe1d3;padding:7px 12px;border-radius:30px">{m}</span>'
                      for m in [f"{n} · {sc}" for n, _, sc in GPS])
    meter = "".join(f'<div style="flex:1;text-align:center;padding:10px 6px;border-right:1px solid rgba(255,255,255,.15)">'
                    f'<div style="font:800 30px Plus Jakarta Sans;color:#fff">{a}</div><div style="font:600 13px JetBrains Mono;color:#cfe3d6;letter-spacing:.06em">{b}</div></div>'
                    for a, b in [("316", "UNIT A4 DIJIMAT"), ("69", "UNIT DAKWAT"), ("27 min", "MASA CARIAN"), ("1,550 kp", "RUANG DIBEBAS"), ("RM167k", "HASIL SEWAAN"), ("RM178k", "JUMLAH")])
    page = f"""
<div style="height:96px;background:#fff;display:flex;align-items:center;padding:0 34px;gap:26px;box-shadow:0 2px 8px rgba(0,0,0,.06);position:relative;z-index:3">
<div style="width:30px;height:20px;border-top:4px solid #8E1B33;border-bottom:4px solid #8E1B33;position:relative"><i style="position:absolute;left:0;right:0;top:4px;border-top:4px solid #8E1B33;display:block"></i></div>
<img src="assets/logo-pptx.png" style="height:62px">
<div style="border-left:2px solid #ddd;padding-left:22px;font:800 30px Plus Jakarta Sans;color:#1f2a5a;letter-spacing:.01em">SISTEM PENGURUSAN DATA <span style="background:#165A44;color:#fff;padding:2px 12px;border-radius:8px;font-size:24px;vertical-align:middle">2.0</span></div>
<div style="margin-left:auto;width:330px;height:44px;border:1px solid #ccc;border-radius:22px;padding:10px 18px;font:500 17px Plus Jakarta Sans;color:#999">Carian Aset/Penyewa/Pembeli</div>
<div style="font:700 17px Plus Jakarta Sans;color:#333;margin-right:190px">PEGAWAI SPD ▾</div></div>
<div style="display:flex">
<div style="width:300px;background:#8E1B33;min-height:2000px;padding-top:20px">{side}</div>
<div style="flex:1;padding:26px 34px;background:#F1F3F2">
<div style="background:#fff;border-radius:12px;padding:20px 26px;box-shadow:0 2px 10px rgba(0,0,0,.05)">
<div style="font:800 20px Plus Jakarta Sans;color:#2a3a8a">TABURAN LOKASI PREMIS & TANAH MILIK PKNM</div>
<div style="height:300px;margin-top:14px;border-radius:8px;overflow:hidden;background:url(assets/ui-map.jpg) center 62%/cover"></div></div>
<div style="display:grid;grid-template-columns:2fr 1fr;gap:24px;margin-top:24px">
<div style="background:#fff;border-radius:12px;padding:20px 26px;height:190px;box-shadow:0 2px 10px rgba(0,0,0,.05)"><div style="font:800 20px Plus Jakarta Sans;color:#2a3a8a">ASET ALIH</div>
<div style="margin-top:14px;height:110px;background:url(assets/ui-dash2.jpg) left 30%/cover;border-radius:6px;opacity:.9"></div></div>
<div style="background:#fff;border-radius:12px;padding:20px 26px;height:190px;box-shadow:0 2px 10px rgba(0,0,0,.05)"><div style="font:800 20px Plus Jakarta Sans;color:#2a3a8a">ASET TAK ALIH</div>
<div style="margin-top:14px;height:110px;background:url(assets/ui-dash3.jpg) left 40%/cover;border-radius:6px;opacity:.9"></div></div></div>

<div style="margin-top:30px;border-radius:18px;overflow:hidden;box-shadow:0 0 0 3px #B6D973,0 20px 50px rgba(11,46,34,.25)">
<div style="background:linear-gradient(110deg,#0B2E22,#165A44 60%,#26745A);padding:24px 30px;display:flex;align-items:center;gap:18px">
{leaf("width:54px;height:54px;transform:rotate(25deg)")}
<div><div style="font:800 34px Plus Jakarta Sans;color:#fff;letter-spacing:-.01em">SPD 2.0 + GREEN DASHBOARD</div>
<div style="font:600 16px JetBrains Mono;color:#B6D973;letter-spacing:.14em">SPD GREEN INDEX · PEMANTAUAN IMPAK HIJAU</div></div>
<div style="margin-left:auto;display:flex;gap:10px">{''.join(f'<span style="font:700 15px Plus Jakarta Sans;color:#fff;border:1px solid rgba(255,255,255,.35);padding:8px 14px;border-radius:8px">{t}</span>' for t in ["Tahun: 2025 ▾","Jabatan: Semua ▾","Kategori aset: Semua ▾"])}</div></div>
<div style="background:#F7FAF7;padding:24px 30px">
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px">{modules}</div>
<div style="display:grid;grid-template-columns:330px 1fr;gap:24px">
<div style="background:#fff;border-radius:14px;padding:20px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,.06)">
<div style="font:800 14px JetBrains Mono;letter-spacing:.14em;color:#6b7a73">OVERALL GREEN INDEX</div>{gauge}
<div style="font:800 17px Plus Jakarta Sans;color:#0B2E22;background:#E9F2E7;border-radius:30px;padding:8px 12px">Advanced Green Performance</div></div>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px">{kh}</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-top:24px">
<div style="background:#fff;border-radius:14px;padding:20px 24px;box-shadow:0 2px 10px rgba(0,0,0,.06)"><div style="font:800 14px JetBrains Mono;letter-spacing:.14em;color:#6b7a73">PECAHAN PENJIMATAN &amp; HASIL · RM178,141</div>{split}</div>
<div style="background:#fff;border-radius:14px;padding:20px 24px;box-shadow:0 2px 10px rgba(0,0,0,.06)"><div style="font:800 14px JetBrains Mono;letter-spacing:.14em;color:#6b7a73">TREND PERMOHONAN BAHAN CETAKAN · 2021 vs 2025</div>{trend}</div></div>
<div style="margin-top:24px;background:linear-gradient(90deg,#0B2E22,#165A44);border-radius:14px;padding:14px 10px;display:flex;align-items:center">
<div style="padding:0 20px;font:800 16px JetBrains Mono;color:#B6D973;letter-spacing:.12em;line-height:1.3">GREEN<br>IMPACT<br>METER</div>{meter}</div>
</div></div></div></div>"""
    chrome = ('<div style="height:64px;background:#2b2f33;display:flex;align-items:center;padding:0 24px;gap:14px">'
              + "".join(f'<i style="width:16px;height:16px;border-radius:50%;background:{c};display:block"></i>' for c in ["#ff5f57", "#febc2e", "#28c840"])
              + '<div style="margin-left:30px;flex:1;max-width:900px;height:38px;background:#1d2023;border-radius:19px;padding:8px 20px;font:500 17px Plus Jakarta Sans;color:#c8ccd0">🔒 spd.pknm.gov.my/v2/utama</div></div>')
    h = 2000 if full else 1016
    return (f'<div class="F" style="background:#1d2023">{chrome}<div style="position:absolute;top:64px;left:0;right:0;height:{h}px;overflow:hidden">'
            f'<div style="transform:translateY(-{scroll}px)">{page}</div>'
            f'{f"<div style=position:absolute;left:0;top:96px;width:300px;bottom:0;background:#8E1B33;padding-top:20px>{side}</div>" if scroll and not full else ""}'
            f'</div>{cursor(*click, click=True) if click else ""}{SCROLLHINT if soon else ""}{"" if full else BADGE}</div>')


def F18():
    return spd2_homepage(scroll=560)


def F19():
    return f"""<div class="F" style="background:#0B2E22">
<div style="position:absolute;left:0;top:0;bottom:0;width:22px;background:#B6D973"></div>
<div style="position:absolute;inset:0;background:radial-gradient(ellipse at 50% 40%,rgba(182,217,115,.22),transparent 60%)"></div>
<div style="position:absolute;left:0;right:0;top:220px;display:flex;justify-content:center">{spd_mark(220, "#B6D973", "#B6D973")}</div>
<div style="position:absolute;left:0;right:0;top:520px;text-align:center;font:800 54px/1.2 Plus Jakarta Sans;color:#fff">INOVASI DIGITAL KE ARAH<br>PENGURUSAN HIJAU DAN LESTARI</div>
<div style="position:absolute;left:0;right:0;top:700px;text-align:center;font:600 30px Plus Jakarta Sans;color:#cfe3d6">Mendigitalkan proses  •  Mengoptimumkan sumber  •  Mempercepat penyampaian</div>
<div style="position:absolute;left:0;right:0;top:780px;text-align:center;font:600 italic 34px Plus Jakarta Sans;color:#D9AE52">Less Paper. Smarter Assets. Greener Future.</div>
<div style="position:absolute;left:0;right:0;top:920px;text-align:center;font:800 24px 'JetBrains Mono';letter-spacing:.2em;color:#B6D973">PERBADANAN MELAKA (MCORP) | 2026</div>
{BADGE}</div>"""



def cursor(x, y, click=False):
    ring = (f'<div style="position:absolute;left:{x-46}px;top:{y-46}px;width:92px;height:92px;border-radius:50%;'
            f'border:5px solid #B6D973;box-shadow:0 0 30px #B6D973;opacity:.9"></div>'
            f'<div style="position:absolute;left:{x-24}px;top:{y-24}px;width:48px;height:48px;border-radius:50%;'
            f'background:rgba(182,217,115,.45)"></div>') if click else ""
    return (ring + f'<svg viewBox="0 0 60 80" style="position:absolute;left:{x-4}px;top:{y-4}px;width:46px;z-index:30;'
            f'filter:drop-shadow(0 6px 10px rgba(0,0,0,.5))"><path d="M5 5 L5 65 L20 50 L32 75 L42 70 L30 46 L52 46Z" '
            f'fill="#fff" stroke="#111" stroke-width="3"/></svg>')


def browser(img, x, y, w, rot="", pos="left top", url="spd.pknm.gov.my", extra=""):
    h = int(w * 0.52)
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;transform:{rot};border-radius:16px;overflow:hidden;'
            f'box-shadow:0 50px 110px rgba(0,0,0,.6),0 0 0 2px rgba(255,255,255,.12)">'
            f'<div style="height:44px;background:#2b2f33;display:flex;align-items:center;gap:10px;padding:0 18px">'
            + "".join(f'<i style="width:12px;height:12px;border-radius:50%;background:{c};display:block"></i>' for c in ["#ff5f57", "#febc2e", "#28c840"])
            + f'<div style="margin-left:18px;height:28px;flex:1;max-width:520px;background:#1d2023;border-radius:14px;padding:4px 16px;'
            f'font:500 15px Plus Jakarta Sans;color:#c8ccd0">🔒 {url}</div></div>'
            f'<div style="height:{h}px;background:url(assets/{img}) {pos}/cover;position:relative">{extra}</div></div>')


def callout(x, y, k, t, w=520):
    return (f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;background:rgba(11,46,34,.92);border-left:8px solid #B6D973;'
            f'border-radius:14px;padding:18px 24px;box-shadow:0 20px 40px rgba(0,0,0,.45);z-index:20">'
            f'<div style="font:800 18px JetBrains Mono;letter-spacing:.18em;color:#B6D973">{k}</div>'
            f'<div style="font:800 40px/1.15 Plus Jakarta Sans;color:#fff;margin-top:6px">{t}</div></div>')


DEMO_BG = "background:radial-gradient(ellipse at 50% 35%,#20352d,#08110d 75%)"


def FD_utama():
    sb = ('<div style="position:absolute;right:14px;top:60px;width:10px;height:880px;border-radius:5px;background:rgba(255,255,255,.12)">'
          '<i style="position:absolute;left:0;right:0;top:220px;height:160px;border-radius:5px;background:#B6D973;display:block"></i></div>')
    return f"""<div class="F" style="{DEMO_BG}">
{browser("ui-map.jpg", 150, 90, 1500, "perspective(2200px) rotateY(-9deg) rotateX(4deg)")}
<div class="shot" style="left:1150px;top:520px;width:640px;height:304px;transform:perspective(1400px) rotateY(-14deg);box-shadow:0 0 0 3px #B6D973,0 40px 90px rgba(0,0,0,.6)"><img src="assets/ui-dash2.jpg"></div>
{cursor(1290, 640)}{sb}
<svg viewBox="0 0 60 90" style="position:absolute;left:1370px;top:580px;width:46px"><rect x="8" y="4" width="44" height="78" rx="22" fill="none" stroke="#fff" stroke-width="4"/><rect x="27" y="16" width="6" height="16" rx="3" fill="#B6D973"/></svg>
{callout(120, 820, "LAMAN UTAMA · SCROLL", "Semua aset dalam satu paparan")}
{BADGE}</div>"""


def FD_ata():
    pop = ('<div style="position:absolute;right:-6%;top:6%;width:62%;border-radius:12px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.6),0 0 0 4px #B6D973">'
           '<img src="assets/ui-premis.jpg" style="width:100%;display:block"></div>')
    return f"""<div class="F" style="{DEMO_BG}">
{browser("ui-search.jpg", 110, 120, 1350, "perspective(2200px) rotateY(8deg)", url="spd.pknm.gov.my/asettakalih")}
<div class="shot" style="left:960px;top:330px;width:880px;height:418px;transform:perspective(1600px) rotateY(-12deg) translateZ(80px);box-shadow:0 0 0 4px #B6D973,0 50px 100px rgba(0,0,0,.7)"><img src="assets/ui-premis.jpg"></div>
<div style="position:absolute;left:560px;top:205px;padding:10px 20px;background:#fff;border:3px solid #B6D973;border-radius:24px;font:700 34px Plus Jakarta Sans;color:#111;z-index:25">ELKAY<span style="color:#8E1B33">|</span></div>
{cursor(520, 420, click=True)}
{callout(110, 820, "ASET TAK ALIH · CARIAN", "Taip lokasi → rekod premis terbuka", 640)}
{BADGE}</div>"""


def FD_modul():
    tiles = [("ui-asetalih.jpg", "ASET ALIH", "Rekod & barcode", 90, 250, -18),
             ("ui-stor.jpg", "PENGURUSAN STOR", "Permohonan & baki stok", 520, 180, -6),
             ("ui-modalinsan.jpg", "MODAL INSAN", "Kakitangan & latihan", 980, 180, 6),
             ("ui-dash5.jpg", "PENTADBIRAN", "Capaian sistem", 1420, 250, 18)]
    html = ""
    for i, (img, k, t, x, y, r) in enumerate(tiles):
        on = i == 1
        html += (f'<div style="position:absolute;left:{x}px;top:{y}px;width:420px;transform:perspective(1400px) rotateY({r}deg) {"scale(1.12)" if on else ""};'
                 f'{"" if on else "filter:brightness(.55) blur(1px);"}z-index:{5 if on else 1}">'
                 f'<div style="border-radius:14px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.6){",0 0 0 4px #B6D973" if on else ""}">'
                 f'<img src="assets/{img}" style="width:420px;height:300px;object-fit:cover;object-position:left top;display:block"></div>'
                 f'<div style="font:800 18px JetBrains Mono;letter-spacing:.16em;color:#B6D973;margin-top:22px">0{i+1} · {k}</div>'
                 f'<div style="font:800 32px Plus Jakarta Sans;color:#fff;margin-top:4px">{t}</div></div>')
    side = "".join(f'<div style="padding:13px 18px;font:600 19px Plus Jakarta Sans;color:#fff;{"background:rgba(255,255,255,.2);border-left:5px solid #B6D973" if i==2 else ""}">{t}</div>'
                   for i, t in enumerate(["Utama", "Pengurusan Aset Alih", "Pengurusan Stor", "Pengurusan Modal Insan", "Pentadbiran"]))
    return f"""<div class="F" style="{DEMO_BG}">{html}
<div style="position:absolute;left:90px;top:700px;width:330px;background:#8E1B33;border-radius:14px;padding:10px 0;box-shadow:0 30px 60px rgba(0,0,0,.5)">{side}</div>
{cursor(300, 800, click=True)}
<div style="position:absolute;left:480px;top:760px;font:800 26px JetBrains Mono;letter-spacing:.2em;color:#B6D973">KLIK → WHIP-PAN 3D KE MODUL SETERUSNYA</div>
{BADGE}</div>"""


def FD_spd2():
    return spd2_homepage(scroll=560, soon=True)


FRAMES = [F01, F02, F03, F04, F05, FD_utama, FD_ata, FD_modul, F07, F08, F09, F10, F11, F12, F13, F14, F15, F17, FD_spd2, F19]


# ---------------------------------------------------------------- pages
def tagspan(s):
    bg, fg = STYLE_COL[s]
    return f'<span class="tag" style="background:{bg};color:{fg}">{s}</span>'


def card(sc, frame_fn):
    sid, a, b, title, ref, styles, vis, sfx, vo = sc
    return f"""<div class="card"><div class="thumb"><div class="frame" style="transform:scale(.45104)">{frame_fn()}</div></div>
<div class="body"><div class="row1"><span class="sid">{sid}</span><span class="time">{tc(a)} – {tc(b)}</span><span class="dur">{b-a}s</span>
<span style="margin-left:auto;display:flex;gap:6px">{''.join(tagspan(s) for s in styles)}</span></div>
<h3>{title}</h3><div class="ref">{ref}</div>
<div class="fld"><b>VISUAL</b><div>{vis}</div></div>
<div class="fld"><b>SFX</b><div>{sfx}</div></div>
<div class="fld vo"><b>VO</b><div>{vo}</div></div></div></div>"""


SHORT = {"S01": "Lakonan awal", "S02": "Tajuk", "S05": "Masuk sistem", "S06": "Demo: Laman Utama",
         "S07": "Demo: Aset Tak Alih", "S08": "Demo: modul lain", "S09": "Komponen", "S11": "Kecekapan",
         "S12": "Pencemaran", "S13": "Sewaan 14 → 3", "S14": "Aset 20 → 2", "S15": "Kos tenaga kerja",
         "S16": "Kertas & dakwat", "S17": "Digitalisasi", "S19": "SPD 2.0 + Green Dashboard"}


def ruler():
    W = 1760
    px = lambda s: s / 240 * W
    acts = "".join(f'<div class="act" style="left:{px(a)}px;width:{px(b-a)}px">{t}</div>' for a, b, t in ACTS)
    blks = ""
    for sc in SCENES:
        sid, a, b, title, *_ = sc
        st = sc[5][0]
        bg, fg = STYLE_COL[st]
        stripe = ""
        if len(sc[5]) > 1:
            bg2, _ = STYLE_COL[sc[5][1]]
            stripe = f'<i style="position:absolute;left:0;right:0;bottom:0;height:10px;background:{bg2};display:block"></i>'
        blks += (f'<div class="blk" style="left:{px(a)}px;width:{px(b-a)}px;background:{bg};color:{fg}">'
                 f'<div class="id">{sid}</div><div class="t">{SHORT.get(sid, title) if b-a>=10 else ""}</div><div class="tm">{tc(a)}</div>{stripe}</div>')
    # energy curve (music intensity)
    pts = [(0, .35), (10, .5), (12, .2), (22, .6), (40, .45), (55, .55), (67, .7), (89, .75), (102, .55), (104, .95),
           (108, .7), (130, .75), (154, .85), (181, .9), (199, .7), (208, .35), (220, .6), (232, 1.0), (240, .4)]
    path = " ".join(f"{'M' if i==0 else 'L'}{px(t):.0f} {70-v*62:.0f}" for i, (t, v) in enumerate(pts))
    sfx_marks = [3, 9, 12, 21, 26, 38, 42, 48, 52, 56, 60, 70, 74, 78, 82, 86, 92, 97, 102, 104, 110, 116, 122, 128, 133, 138,
                 141, 145, 149, 160, 166, 170, 176, 183, 191, 196, 202, 206, 211, 216, 221, 226, 234, 239]
    marks = "".join(f'<i style="position:absolute;left:{px(t)-4:.0f}px;top:8px;width:8px;height:18px;border-radius:3px;background:#D9AE52;display:block"></i>' for t in sfx_marks)
    vo_spans = [(max(a + 0.6, b - 4.5) if sid == "S01" else a + 0.6, b - 0.6) for sid, a, b, *_ in SCENES]
    vo = "".join(f'<i style="position:absolute;left:{px(a):.0f}px;width:{px(b-a):.0f}px;top:6px;height:22px;border-radius:5px;background:#26745A;display:block"></i>' for a, b in vo_spans)
    ticks = "".join(f'<div class="tick" style="left:{px(t)}px">{tc(t)}</div>' for t in range(0, 241, 15))
    return f"""<div class="ruler">
<div class="acts">{acts}</div><div class="blocks">{blks}</div>
<div class="lane" style="top:238px;background:#fff">{vo}<div class="lbl">VOICE-OVER (skrip akhir · Charon)</div></div>
<div class="lane" style="top:292px;background:#fff;height:36px"><div class="lbl">SFX FOLEY "KERTAS → PIKSEL"</div>{marks}</div>
<div class="lane" style="top:346px;background:#fff;height:44px"><div class="lbl">MUZIK · TENAGA</div>
<svg viewBox="0 0 {W} 44" preserveAspectRatio="none" style="position:absolute;inset:0;width:100%;height:100%"><path d="{path.replace('70-','44-')}" fill="none"/></svg>
<svg viewBox="0 0 {W} 70" preserveAspectRatio="none" style="position:absolute;left:0;top:-13px;width:100%;height:70px"><path d="{path}" stroke="#165A44" stroke-width="3" fill="none"/></svg></div>
<div class="ticks">{ticks}</div>
</div>"""


def page1():
    legend = "".join(f'<div><i style="background:{STYLE_COL[k][0]}"></i>{d}</div>' for k, d in [
        ("FORMAL", "Formal korporat (hijau zamrud + putih + emas)"), ("DOODLE", "Doodle lukisan tangan / kapur"),
        ("HYPERMOTION", "Hypermotion: kamera 3D, speed-ramp, match-cut"), ("LAKONAN", "Footage lakonan"), ("DEMO SISTEM", "Demo sistem: klik, taip, scroll")])
    return f"""<div class="page" id="p1">
<div class="hdr"><div class="k">STORYBOARD & TIMELINE · DRAF 2</div>
<h1>SPD GREEN: Video Penerangan Sistem</h1>
<p>Pembangunan Sistem Pengurusan Data Bersepadu (SPD) · Perbadanan Melaka (MCORP)</p>
<div class="meta"><b>4:00</b> durasi<br><b>1920×1080</b> · 30 fps<br><b>20</b> babak · 4 babak besar</div></div>
<div class="sec"><h2>Timeline 4 minit <span>0:00 → 4:00</span></h2>
<div class="sub">Setiap blok = satu babak. Jalur bawah blok = gaya kedua. Butang merah dalam PowerPoint dipetakan kepada babak S03–S19.</div>
<div class="legend">{legend}</div>
<div style="display:inline-block;margin:0 0 22px;font:700 15px 'JetBrains Mono';color:#8E1B33;background:#fff;border:2px solid #8E1B33;border-radius:6px;padding:5px 12px">
MCORP LOGO 3D (KANAN ATAS) · 0:00 – 4:00 · ayun kiri-kanan ±25°, tak pusing penuh</div>{ruler()}</div>
<div class="pill3">
<div class="box"><h4><em style="background:#111;color:#E8C46A">HYPERMOTION</em> Rupa "mahal"</h4><ul>
<li>Kamera 3D sebenar: dolly, orbit, parallax berlapis dengan depth-of-field</li>
<li>Speed-ramp + motion blur pada setiap peralihan besar</li>
<li>Match-cut bercerita: kertas → daun, bola kertas → skrin, kalendar → daun, jubin → logo</li>
<li>Light sweep emas & glow hijau, grain filem halus, vignette</li>
<li>Tipografi kinetik dengan mask reveal, bukan fade biasa</li></ul></div>
<div class="box"><h4><em style="background:#F3E3B5;color:#3a2f12">DOODLE</em> Babak lukisan tangan</h4><ul>
<li>S01 (atas footage), S04 masalah, S12 pencemaran, S16 graf</li>
<li>Garis "boil" 12 fps supaya nampak hidup, ditapis tekstur kapur / pensel</li>
<li>Kertas kraft bergrid & papan kapur hijau: kontras dengan bahagian formal</li>
<li>Peralihan doodle → formal: kertas direnyuk dan "dimakan" kamera</li></ul></div>
<div class="box"><h4><em style="background:#D9AE52;color:#3a2a00">SFX</em> Bukan whoosh/ding biasa</h4><ul>
<li>Konsep <b>"Kertas → Piksel"</b>: semua bunyi dari bahan pejabat sebenar</li>
<li>Selakan kertas, cop getah, laci kabinet, embosser, bip barcode, pensel, kapur</li>
<li>Diproses: pitch turun, reverse, granular, ditala ikut kunci muzik</li>
<li>Bip barcode & ketukan kekunci jadi not melodi (bunyi = muzik)</li>
<li>Muzik: piano felt + marimba/pluck berdenyut, naik di Babak 3, drop di SPD 2.0</li></ul></div></div>
<div class="sec" style="padding-top:0"><h2>Frame utama: SPD 2.0 + Green Dashboard <span>S19 · 3:27 – 3:52</span></h2>
<div class="sub">Laman utama SPD "versi 2.0" (rupa sama seperti sistem sebenar). Bahagian penutup "akan datang": laman utama di-scroll ke bawah sahaja sehingga seksyen Green Dashboard kelihatan. Angka KPI diambil terus dari PowerPoint; Green Index {GREEN_INDEX}/100 dikira guna formula pemberat dalam PDF Cadangan Dashboard.</div></div>
<div style="padding:0 80px 20px;display:grid;grid-template-columns:1fr 1fr;gap:28px">
<div class="card"><div class="thumb"><div class="frame" style="transform:scale(.45104)">{spd2_homepage(0)}</div></div>
<div class="body" style="padding:14px 20px"><b style="font:800 14px JetBrains Mono;color:#26745A">A · 3:32</b> &nbsp;Laman utama SPD 2.0 muncul (atas: peta premis & tanah, kad Aset)</div></div>
<div class="card"><div class="thumb"><div class="frame" style="transform:scale(.45104)">{spd2_homepage(560)}</div></div>
<div class="body" style="padding:14px 20px"><b style="font:800 14px JetBrains Mono;color:#26745A">B · 3:40</b> &nbsp;Scroll ke bawah: seksyen <b>SPD 2.0 + GREEN DASHBOARD</b> menyala, KPI kira naik satu-satu</div></div></div>
<div class="foot"><span>Halaman 1 / 3 · Timeline & konsep</span><span>Bahan: Slaid SPD 2026 · Footage lakonan · Cadangan Dashboard SPD Green Index · Screenshot sistem SPD</span></div></div>"""


NOTES = """<div class="card" style="background:#0B2E22;color:#fff;padding:34px 36px">
<div style="font:800 15px JetBrains Mono;letter-spacing:.2em;color:#B6D973">NOTA SEBELUM BUAT VIDEO</div>
<div style="font:800 34px Plus Jakarta Sans;margin:10px 0 18px">Perlu disahkan / dihantar</div>
<ol style="font:500 19px/1.55 Plus Jakarta Sans;color:#dbe9df;padding-left:24px">
<li><b style="color:#fff">Footage lakonan</b>: sedang dimuat naik. S01 guna gambar fail sebagai pengganti sementara.</li>
<li><b style="color:#fff">Skrip VO</b>: siap (lihat setiap babak). Suara Gemini TTS "Charon", nada sama seperti MCORP Estimate; masa babak akhir ikut rakaman VO.</li>
<li><b style="color:#fff">Green Index 82/100</b> dikira daripada formula pemberat PDF (skor komponen dianggar dari angka slaid). Boleh tukar angka jika ada sasaran rasmi.</li>

<li><b style="color:#fff">Logo</b>: logo MCORP korporat (dari slaid 1) dipusing 3D kiri-kanan di kanan atas sepanjang video.</li></ol>
<div style="margin-top:22px;font:700 17px JetBrains Mono;color:#B6D973">Bila timeline ini OK → arahkan "create video".</div></div>"""


def page_cards(pid, scenes_frames, label):
    cards = "".join(card(s, f) for s, f in scenes_frames)
    if pid == "p3":
        cards += NOTES
    return f"""<div class="page" id="{pid}"><div class="sec" style="padding-top:40px"><h2>Storyboard babak demi babak <span>{label}</span></h2>
<div class="sub">Imej kecil = frame gaya sebenar 1920×1080. Logo MCORP 3D sentiasa di kanan atas. VO = skrip akhir (suara Charon, gaya MCORP Estimate).</div></div>
<div class="grid">{cards}</div><div class="foot"><span>{label}</span><span>SPD GREEN · Storyboard draf 2</span></div></div>"""


def build():
    pairs = list(zip(SCENES, FRAMES))
    html = f"""<!doctype html><html lang="ms"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;1,600&family=Caveat:wght@500;700&family=JetBrains+Mono:wght@500;600;700;800&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{SVG_FILTER}
{page1()}
{page_cards("p2", pairs[:10], "Halaman 2 / 3 · S01 – S10 (0:00 – 2:07)")}
{page_cards("p3", pairs[10:], "Halaman 3 / 3 · S11 – S20 (2:07 – 4:00)")}
<div class="page" id="p4" style="width:1920px;height:2080px;background:#1d2023"><div style="position:relative;width:1920px;height:2080px">{spd2_homepage(0, full=True)}</div></div>
</body></html>"""
    (OUT / "storyboard.html").write_text(html, encoding="utf-8")
    (OUT / "timeline.json").write_text(json.dumps(
        [dict(id=s[0], start=s[1], end=s[2], title=s[3], ref=s[4], styles=s[5], visual=s[6], sfx=s[7], vo=s[8]) for s in SCENES],
        ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    build()
    total = sum(b - a for _, a, b, *_ in SCENES)
    assert total == 240 and all(SCENES[i][2] == SCENES[i + 1][1] for i in range(len(SCENES) - 1)), total
    print("built", OUT / "storyboard.html", "green index", GREEN_INDEX)
