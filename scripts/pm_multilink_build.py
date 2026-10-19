"""Generate the PM Multilink website pages (shared header, footer, icon sprite).

Usage: python3 scripts/pm_multilink_build.py [output_dir]   (default: website/pm-multilink)
"""
import pathlib, sys

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent.parent / "website" / "pm-multilink"

SPRITE = """<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <symbol id="i-cuci" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 17v-4l2.2-5A2 2 0 0 1 7 6.8h10A2 2 0 0 1 18.8 8L21 13v4"/><path d="M3 13h18M9.5 17h5"/><circle cx="6.5" cy="17" r="2"/><circle cx="17.5" cy="17" r="2"/><path d="M12 1.5s-1.4 1.6-1.4 2.6a1.4 1.4 0 0 0 2.8 0c0-1-1.4-2.6-1.4-2.6z"/></symbol>
    <symbol id="i-baiki" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94z"/></symbol>
    <symbol id="i-bersih" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 3l1.9 5.1L18 10l-5.1 1.9L11 17l-1.9-5.1L4 10l5.1-1.9z"/><path d="M19 3v4M17 5h4M19 16v4M17 18h4"/></symbol>
    <symbol id="i-kit" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 8l-9-5-9 5v8l9 5 9-5z"/><path d="M3 8l9 5 9-5M12 13v8M7.5 5.5l9 5"/></symbol>
    <symbol id="i-media" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="6" width="14" height="12" rx="2.5"/><path d="M16 10.5l6-3.5v10l-6-3.5z"/></symbol>
    <symbol id="i-panah" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></symbol>
    <symbol id="i-telefon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8.1 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></symbol>
    <symbol id="i-emel" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2.5"/><path d="M22 7l-10 6L2 7"/></symbol>
    <symbol id="i-lokasi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></symbol>
    <symbol id="i-jam" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></symbol>
    <symbol id="i-menu" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M4 7h16M4 12h16M4 17h16"/></symbol>
    <symbol id="i-visi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></symbol>
    <symbol id="i-misi" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 21V4M5 4h12l-2.5 4.5L17 13H5"/></symbol>
    <symbol id="i-perisai" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></symbol>
    <symbol id="i-wa" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.4 8.4 0 0 1-12.4 7.4L3 21l2.1-5.4A8.4 8.4 0 1 1 21 11.5z"/><path d="M8.8 9.2c.3 2.6 3 5.3 5.8 5.8l1.1-1.3-1.8-.9-.8.7c-.9-.4-2-1.5-2.5-2.5l.7-.8-.9-1.8z"/></symbol>
  </g>
</svg>"""


def ikon(nama, kelas=""):
    k = f' class="{kelas}"' if kelas else ""
    return f'<svg{k} aria-hidden="true"><use href="#i-{nama}"/></svg>'


LOGO = '<img class="logo" src="assets/logo.svg" alt="PM Multilink" width="150" height="41">'
MARK = '<img src="assets/logo-pm.svg" alt="" width="90" height="43">'

MENU = [
    ("index.html", "Utama"),
    ("tentang.html", "Tentang Kami"),
    ("perkhidmatan.html", "Perkhidmatan"),
    ("projek.html", "Projek"),
]

SERVIS = [
    # (id, ikon, nama, ringkasan)
    ("cuci-kereta", "cuci", "Cuci Kereta", "Cucian luar dan dalam untuk kenderaan persendirian, kenderaan jabatan dan armada syarikat."),
    ("pembaikan", "baiki", "Projek Pembaikan", "Kerja baik pulih dan penyelenggaraan bangunan, premis dan kemudahan awam."),
    ("pembersihan", "bersih", "Pembersihan", "Pembersihan pejabat, bangunan dan kawasan, termasuk pembersihan menyeluruh selepas acara."),
    ("pengagihan-kit", "kit", "Pengagihan Kit", "Pembungkusan, pengurusan dan penghantaran kit untuk program, bantuan dan acara."),
    ("media", "media", "Media", "Penerbitan video, fotografi, reka bentuk grafik dan liputan acara untuk organisasi anda."),
]


def halaman(fail, tajuk, huraian, isi):
    nav = "\n".join(
        f'          <li><a href="{h}"{" aria-current=\"page\"" if h == fail else ""}>{n}</a></li>' for h, n in MENU
    )
    servis_pengaki = "\n".join(f'            <li><a href="perkhidmatan.html#{s[0]}">{s[2]}</a></li>' for s in SERVIS)
    return f"""<!doctype html>
<html lang="ms">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{tajuk}</title>
  <meta name="description" content="{huraian}">
  <meta name="theme-color" content="#8b2cf5">
  <link rel="icon" type="image/svg+xml" href="assets/logo-pm.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/style.css">
</head>
<body>
{SPRITE}

  <header class="pengepala">
    <div class="bekas">
      <a class="jenama" href="index.html" aria-label="PM Multilink, halaman utama">
        {LOGO}
        <small>Anak Syarikat<br>MCORP</small>
      </a>
      <button class="togol-menu" aria-label="Buka menu" aria-expanded="false" aria-controls="menu-utama">{ikon("menu")}</button>
      <nav aria-label="Menu utama">
        <ul class="menu" id="menu-utama">
{nav}
          <li><a class="butang" href="hubungi.html"{" aria-current=\"page\"" if fail == "hubungi.html" else ""}>Hubungi Kami</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main>
{isi}
  </main>

  <footer class="pengaki">
    <div class="bekas">
      <div class="grid">
        <div>
          <a class="jenama jenama-pengaki" href="index.html">{LOGO}</a>
          <p style="margin-top:16px">Pelbagai perkhidmatan, satu pasukan. Melayani individu, syarikat dan agensi di Melaka.</p>
          <div class="induk"><img src="assets/mcorp.png" alt="Logo MCORP, Melaka Corporation"><span>Ahli Kumpulan<br>Melaka Corporation</span></div>
        </div>
        <div>
          <h4>Perkhidmatan</h4>
          <ul>
{servis_pengaki}
          </ul>
        </div>
        <div>
          <h4>Syarikat</h4>
          <ul>
            <li><a href="tentang.html">Tentang Kami</a></li>
            <li><a href="projek.html">Projek</a></li>
            <li><a href="hubungi.html">Hubungi Kami</a></li>
            <li><a href="hubungi.html#soalan">Soalan Lazim</a></li>
          </ul>
        </div>
        <div>
          <h4>Hubungi</h4>
          <ul>
            <li><span class="isi">Alamat syarikat</span></li>
            <li><span class="isi">No. telefon</span></li>
            <li><span class="isi">Emel syarikat</span></li>
          </ul>
        </div>
      </div>
      <div class="bawah">
        <span>&copy; <span data-tahun>2026</span> PM Multilink <span class="isi">No. pendaftaran SSM</span>. Hak cipta terpelihara.</span>
        <span>Anak syarikat Melaka Corporation (MCORP)</span>
      </div>
    </div>
  </footer>

  <a class="wa-terapung" data-wa href="hubungi.html#borang" aria-label="WhatsApp kami">{ikon("wa")}</a>

  <script src="assets/main.js"></script>
</body>
</html>
"""


def cta(tajuk="Ada projek atau tugasan untuk kami?", teks="Beritahu kami keperluan anda. Pasukan kami akan memberi sebut harga yang jelas secepat mungkin."):
    return f"""    <section class="seksyen">
      <div class="bekas">
        <div class="cta muncul">
          <h2>{tajuk}</h2>
          <p>{teks}</p>
          <div class="tindakan">
            <a class="butang putih" href="hubungi.html#borang">Minta Sebut Harga {ikon("panah")}</a>
            <a class="butang kaca" data-wa href="hubungi.html#borang">{ikon("wa")} WhatsApp Kami</a>
          </div>
        </div>
      </div>
    </section>"""


def hero_kecil(jejak, tajuk, teks):
    return f"""    <section class="hero kecil">
      <div class="bekas">
        <div>
          <div class="jejak"><a href="index.html">Utama</a> / {jejak}</div>
          <h1>{tajuk}</h1>
          <p class="utama">{teks}</p>
        </div>
      </div>
    </section>"""


# ---------------- Utama ----------------
nod = "\n".join(f'          <div class="nod">{ikon(s[1])}<span>{s[2]}</span></div>' for s in SERVIS)
kad = "\n".join(
    f"""          <a class="kad muncul" href="perkhidmatan.html#{s[0]}">
            <div class="ikon">{ikon(s[1])}</div>
            <h3>{s[2]}</h3>
            <p>{s[3]}</p>
            <span class="lagi">Ketahui lagi {ikon("panah")}</span>
          </a>"""
    for s in SERVIS
)

utama = f"""    <section class="hero">
      <div class="bekas">
        <div>
          <div class="lencana"><span>MCORP</span> Anak syarikat Melaka Corporation</div>
          <h1>Satu pasukan, <em>pelbagai perkhidmatan</em> untuk anda.</h1>
          <p class="utama">Dari cuci kereta dan pembersihan, kerja pembaikan, pengagihan kit hinggalah penerbitan media. PM Multilink menghubungkan keperluan anda dengan pasukan yang boleh diharap.</p>
          <div class="tindakan">
            <a class="butang putih" href="perkhidmatan.html">Lihat Perkhidmatan {ikon("panah")}</a>
            <a class="butang kaca" href="hubungi.html#borang">Minta Sebut Harga</a>
          </div>
        </div>
        <div class="orbit" aria-hidden="true">
          <div class="gelang"></div>
          <div class="teras"><div>{MARK}<span>Multilink</span></div></div>
{nod}
        </div>
      </div>
    </section>

    <section class="seksyen">
      <div class="bekas">
        <div class="kepala-seksyen muncul">
          <span class="label">Perkhidmatan Kami</span>
          <h2>Lima perkhidmatan di bawah satu bumbung</h2>
          <p>Tak perlu cari banyak kontraktor. Satu panggilan kepada PM Multilink, kami uruskan.</p>
        </div>
        <div class="grid-servis">
{kad}
        </div>
      </div>
    </section>

    <section class="seksyen lembut">
      <div class="bekas">
        <div class="kepala-seksyen muncul">
          <span class="label">Kenapa PM Multilink</span>
          <h2>Mudah berurusan, jelas hasilnya</h2>
        </div>
        <div class="grid-4">
          <div class="kelebihan muncul"><span class="no">01</span><h3>Satu pihak, banyak servis</h3><p>Satu titik hubungan untuk pelbagai kerja, jadi urusan anda lebih ringkas.</p></div>
          <div class="kelebihan muncul"><span class="no">02</span><h3>Kumpulan MCORP</h3><p>Sebahagian daripada kumpulan syarikat Melaka Corporation, perbadanan pembangunan negeri Melaka.</p></div>
          <div class="kelebihan muncul"><span class="no">03</span><h3>Sebut harga jelas</h3><p>Skop kerja dan kos dinyatakan dengan terang sebelum kerja dimulakan.</p></div>
          <div class="kelebihan muncul"><span class="no">04</span><h3>Pasukan tempatan</h3><p>Berpangkalan di Melaka, dekat dengan pelanggan dan cepat bergerak ke lokasi.</p></div>
        </div>
      </div>
    </section>

    <section class="seksyen">
      <div class="bekas dua-lajur">
        <div class="muncul">
          <span class="label">Tentang Kami</span>
          <h2 style="font-size:clamp(1.8rem,3.6vw,2.4rem)">Anak syarikat Melaka Corporation</h2>
          <p style="color:var(--teks-lembut)">PM Multilink ialah anak syarikat Melaka Corporation (MCORP). Kami menyediakan perkhidmatan sokongan harian kepada individu, syarikat swasta dan agensi, dengan menggabungkan beberapa kepakaran dalam satu organisasi.</p>
          <ul class="senarai-tanda">
            <li>Melayani orang awam, syarikat dan agensi kerajaan</li>
            <li>Kerja kecil atau projek berskala besar</li>
            <li>Pakej gabungan beberapa perkhidmatan</li>
          </ul>
          <a class="butang garis" href="tentang.html">Kenali Kami {ikon("panah")}</a>
        </div>
        <div class="panel-induk muncul">
          <img src="assets/mcorp.png" alt="Logo MCORP, Melaka Corporation">
          <strong>Melaka Corporation (MCORP)</strong>
          <p style="color:var(--teks-lembut);margin:4px 0 0">Perbadanan Melaka, syarikat induk</p>
          <div class="garis-hubung">anak syarikat</div>
          <div class="anak">{LOGO}</div>
        </div>
      </div>
    </section>

{cta()}"""

# ---------------- Tentang ----------------
tentang = f"""{hero_kecil("Tentang Kami", "Tentang PM Multilink", "Anak syarikat Melaka Corporation (MCORP) yang menyediakan pelbagai perkhidmatan sokongan untuk komuniti, syarikat dan agensi.")}

    <section class="seksyen">
      <div class="bekas dua-lajur">
        <div class="muncul">
          <span class="label">Siapa Kami</span>
          <h2 style="font-size:clamp(1.8rem,3.6vw,2.4rem)">Menghubungkan keperluan dengan penyelesaian</h2>
          <p style="color:var(--teks-lembut)">Nama <strong>Multilink</strong> membawa maksud kami: satu syarikat yang menghubungkan beberapa bidang perkhidmatan. Daripada menjaga kebersihan dan keadaan premis, menguruskan pengagihan kit, hinggalah menerbitkan kandungan media, kami berusaha menjadi rakan kerja yang boleh diharap.</p>
          <p style="color:var(--teks-lembut)">Sebagai ahli kumpulan Melaka Corporation, kami membawa nilai yang sama: berkhidmat untuk pembangunan negeri Melaka dan rakyatnya.</p>
          <p><span class="isi">Tahun ditubuhkan, latar belakang ringkas syarikat</span></p>
        </div>
        <div class="panel-induk muncul">
          <img src="assets/mcorp.png" alt="Logo MCORP, Melaka Corporation">
          <strong>Melaka Corporation (MCORP)</strong>
          <p style="color:var(--teks-lembut);margin:4px 0 0">Perbadanan Melaka, syarikat induk</p>
          <div class="garis-hubung">anak syarikat</div>
          <div class="anak">{LOGO}</div>
        </div>
      </div>
    </section>

    <section class="seksyen lembut">
      <div class="bekas">
        <div class="grid-3">
          <div class="kad-visi gelap muncul"><div class="ikon">{ikon("visi")}</div><h3>Visi</h3><p><span class="isi">Visi syarikat</span></p><p>Contoh: Menjadi penyedia perkhidmatan pelbagai yang utama dan dipercayai di negeri Melaka.</p></div>
          <div class="kad-visi muncul"><div class="ikon">{ikon("misi")}</div><h3>Misi</h3><p><span class="isi">Misi syarikat</span></p><p style="color:var(--teks-lembut)">Contoh: Menyampaikan perkhidmatan yang berkualiti, tepat masa dan berpatutan kepada setiap pelanggan.</p></div>
          <div class="kad-visi muncul"><div class="ikon">{ikon("perisai")}</div><h3>Komitmen</h3><p style="color:var(--teks-lembut)">Setiap kerja dirancang dengan skop yang jelas, dilaksanakan dengan selamat dan diserahkan dalam keadaan yang memuaskan hati pelanggan.</p></div>
        </div>
      </div>
    </section>

    <section class="seksyen">
      <div class="bekas">
        <div class="kepala-seksyen muncul">
          <span class="label">Nilai Kami</span>
          <h2>Cara kami bekerja</h2>
        </div>
        <div class="grid-4">
          <div class="nilai muncul"><div class="huruf">A</div><h3>Amanah</h3><p>Menjaga kepercayaan pelanggan dan harta benda mereka.</p></div>
          <div class="nilai muncul"><div class="huruf">P</div><h3>Profesional</h3><p>Kerja yang kemas, berdisiplin dan ikut skop yang dipersetujui.</p></div>
          <div class="nilai muncul"><div class="huruf">P</div><h3>Pantas</h3><p>Respons dan penyiapan kerja mengikut jadual.</p></div>
          <div class="nilai muncul"><div class="huruf">P</div><h3>Prihatin</h3><p>Mendengar keperluan pelanggan dan komuniti setempat.</p></div>
        </div>
      </div>
    </section>

{cta("Mari bekerjasama", "Sama ada anda individu, syarikat atau agensi, kami sedia membantu.")}"""

# ---------------- Perkhidmatan ----------------
BUTIRAN = {
    "cuci-kereta": (
        ["Cucian luaran dan pengeringan", "Pembersihan dalaman dan vakum", "Wax dan polish", "Pakej cucian berkala untuk armada kenderaan"],
        ["Individu", "Kenderaan jabatan", "Armada syarikat"],
    ),
    "pembaikan": (
        ["Baik pulih bangunan dan premis", "Kerja mengecat, bumbung dan siling", "Penyelenggaraan paip dan kemudahan asas", "Penyelenggaraan berkala mengikut kontrak"],
        ["Agensi kerajaan", "Pejabat dan kedai", "Kemudahan awam"],
    ),
    "pembersihan": (
        ["Pembersihan harian atau berjadual untuk pejabat", "Pembersihan menyeluruh (deep cleaning)", "Pembersihan kawasan dan landskap", "Pembersihan sebelum dan selepas majlis"],
        ["Pejabat", "Bangunan", "Penganjur acara"],
    ),
    "pengagihan-kit": (
        ["Pembungkusan kit mengikut senarai", "Pengurusan stok dan senarai penerima", "Penghantaran ke lokasi atau terus kepada penerima", "Laporan pengagihan selepas program"],
        ["Program bantuan", "Sekolah dan komuniti", "Acara korporat"],
    ),
    "media": (
        ["Penerbitan video korporat dan promosi", "Fotografi dan liputan acara", "Reka bentuk grafik dan bahan cetak", "Kandungan media sosial"],
        ["Syarikat", "Agensi", "Program dan acara"],
    ),
}

blok = []
for i, s in enumerate(SERVIS, 1):
    skop, untuk = BUTIRAN[s[0]]
    skop_html = "\n".join(f"              <li>{x}</li>" for x in skop)
    untuk_html = "".join(f"<li>{x}</li>" for x in untuk)
    blok.append(f"""        <article class="blok-servis muncul" id="{s[0]}">
          <div class="visual">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;position:relative;z-index:1">{ikon(s[1])}<span class="nombor">0{i}</span></div>
            <h3>{s[2]}</h3>
          </div>
          <div>
            <p style="font-size:1.08rem">{s[3]}</p>
            <h4>Skop perkhidmatan</h4>
            <ul class="senarai-tanda">
{skop_html}
            </ul>
            <h4>Sesuai untuk</h4>
            <ul class="pelanggan">{untuk_html}</ul>
            <a class="butang" href="hubungi.html?servis={s[0]}#borang">Tempah {s[2]} {ikon("panah")}</a>
          </div>
        </article>""")

nav_servis = "\n".join(f'          <a href="#{s[0]}">{s[2]}</a>' for s in SERVIS)
perkhidmatan = f"""{hero_kecil("Perkhidmatan", "Perkhidmatan Kami", "Lima bidang perkhidmatan yang boleh ditempah secara berasingan atau digabungkan dalam satu pakej.")}

    <section class="seksyen">
      <div class="bekas">
        <nav class="navigasi-servis" aria-label="Senarai perkhidmatan">
{nav_servis}
        </nav>
{chr(10).join(blok)}
      </div>
    </section>

{cta("Perlukan lebih daripada satu perkhidmatan?", "Kami boleh sediakan pakej gabungan, contohnya pembersihan dan pembaikan premis, atau pengagihan kit bersama liputan media.")}"""

# ---------------- Projek ----------------
PROJEK = [
    ("media", "media", "Media", "Video pertandingan MCORP EstiMATE", "Video promosi inovasi MCORP EstiMATE dengan grafik bergerak, suara latar dan testimoni pengguna."),
    ("media", "media", "Media", "Video ulasan pengguna MCORP Estimate", "Video testimoni pengguna dengan grafik dan sari kata."),
    ("cuci-kereta", "cuci", "Cuci Kereta", "Contoh: Cucian armada kenderaan", "Gantikan dengan nama projek, pelanggan dan gambar sebenar."),
    ("pembaikan", "baiki", "Projek Pembaikan", "Contoh: Baik pulih premis", "Gantikan dengan nama projek, pelanggan dan gambar sebenar."),
    ("pembersihan", "bersih", "Pembersihan", "Contoh: Pembersihan bangunan pejabat", "Gantikan dengan nama projek, pelanggan dan gambar sebenar."),
    ("pengagihan-kit", "kit", "Pengagihan Kit", "Contoh: Pengagihan kit program komuniti", "Gantikan dengan nama projek, pelanggan dan gambar sebenar."),
]
penapis = '            <button type="button" data-kategori="semua" aria-pressed="true">Semua</button>\n' + "\n".join(
    f'            <button type="button" data-kategori="{s[0]}" aria-pressed="false">{s[2]}</button>' for s in SERVIS
)
kad_projek = "\n".join(
    f"""          <article class="projek muncul" data-kategori="{k}">
            <div class="gambar">{ikon(ik)}<span class="tag">{label}</span></div>
            <div class="isi-projek">
              <div class="meta"><span class="isi">Tarikh / lokasi</span></div>
              <h3>{t}</h3>
              <p>{d}</p>
            </div>
          </article>"""
    for k, ik, label, t, d in PROJEK
)
projek = f"""{hero_kecil("Projek", "Projek &amp; Hasil Kerja", "Sebahagian daripada kerja yang telah kami laksanakan untuk pelanggan.")}

    <section class="seksyen">
      <div class="bekas">
        <div class="penapis" role="group" aria-label="Tapis mengikut perkhidmatan">
{penapis}
        </div>
        <div class="galeri">
{kad_projek}
        </div>
      </div>
    </section>

{cta("Mahu projek anda di sini?", "Hubungi kami untuk berbincang tentang keperluan anda.")}"""

# ---------------- Hubungi ----------------
pilihan = "\n".join(f'                <option value="{s[0]}">{s[2]}</option>' for s in SERVIS)
hubungi = f"""{hero_kecil("Hubungi Kami", "Hubungi Kami", "Isi borang di bawah untuk mendapatkan sebut harga, atau hubungi kami terus melalui telefon dan WhatsApp.")}

    <section class="seksyen">
      <div class="bekas grid-hubungi">
        <div>
          <div class="maklumat">
            <div class="item muncul"><div class="ikon">{ikon("lokasi")}</div><div><h3>Alamat</h3><p><span class="isi">Alamat penuh syarikat</span><br>Melaka, Malaysia</p></div></div>
            <div class="item muncul"><div class="ikon">{ikon("telefon")}</div><div><h3>Telefon</h3><p><span class="isi">No. telefon pejabat</span></p></div></div>
            <div class="item muncul"><div class="ikon">{ikon("wa")}</div><div><h3>WhatsApp</h3><p><a data-wa href="#borang">Mesej kami di WhatsApp</a></p></div></div>
            <div class="item muncul"><div class="ikon">{ikon("emel")}</div><div><h3>Emel</h3><p><span class="isi">Emel syarikat</span></p></div></div>
            <div class="item muncul"><div class="ikon">{ikon("jam")}</div><div><h3>Waktu Operasi</h3><p><span class="isi">Hari dan waktu operasi</span></p></div></div>
          </div>
          <div class="peta muncul"><span><span class="isi">Peta Google Maps</span><br>Tampal kod iframe Google Maps di sini</span></div>
        </div>

        <form class="borang muncul" id="borang" novalidate>
          <h2>Minta Sebut Harga</h2>
          <p style="color:var(--teks-lembut)">Isi maklumat ringkas. Mesej anda akan dihantar terus kepada kami melalui WhatsApp.</p>
          <div class="baris">
            <div class="medan"><label for="nama">Nama</label><input id="nama" name="nama" autocomplete="name" required></div>
            <div class="medan"><label for="telefon">No. telefon</label><input id="telefon" name="telefon" type="tel" autocomplete="tel" inputmode="tel" required></div>
          </div>
          <div class="baris">
            <div class="medan">
              <label for="servis">Perkhidmatan</label>
              <select id="servis" name="servis" required>
{pilihan}
                <option value="gabungan">Gabungan / lain-lain</option>
              </select>
            </div>
            <div class="medan"><label for="lokasi">Lokasi</label><input id="lokasi" name="lokasi" placeholder="Contoh: Ayer Keroh"></div>
          </div>
          <div class="medan"><label for="mesej">Butiran keperluan</label><textarea id="mesej" name="mesej" placeholder="Terangkan skop kerja, tarikh dan apa-apa maklumat lain" required></textarea></div>
          <button class="butang" type="submit">{ikon("wa")} Hantar Melalui WhatsApp</button>
          <p class="nota" id="status-borang" role="status"></p>
        </form>
      </div>
    </section>

    <section class="seksyen lembut" id="soalan">
      <div class="bekas">
        <div class="kepala-seksyen muncul">
          <span class="label">Soalan Lazim</span>
          <h2>Ada soalan?</h2>
        </div>
        <div class="soalan">
          <details class="muncul"><summary>Kawasan mana yang PM Multilink liputi?</summary><p>Kami berpangkalan di Melaka. <span class="isi">Nyatakan kawasan liputan</span></p></details>
          <details class="muncul"><summary>Boleh saya tempah lebih daripada satu perkhidmatan?</summary><p>Boleh. Nyatakan semua keperluan anda dalam borang dan kami akan sediakan sebut harga gabungan.</p></details>
          <details class="muncul"><summary>Bagaimana cara mendapatkan sebut harga?</summary><p>Isi borang di atas atau hubungi kami melalui WhatsApp. Kami akan menghubungi anda untuk mendapatkan butiran lanjut sebelum memberi sebut harga.</p></details>
          <details class="muncul"><summary>Adakah anda menerima kerja daripada agensi kerajaan dan syarikat?</summary><p>Ya. Kami melayani individu, syarikat swasta dan agensi kerajaan.</p></details>
        </div>
      </div>
    </section>"""

HURAIAN = "PM Multilink, anak syarikat Melaka Corporation (MCORP): cuci kereta, projek pembaikan, pembersihan, pengagihan kit dan media."
PAGES = [
    ("index.html", "PM Multilink | Anak Syarikat MCORP", HURAIAN, utama),
    ("tentang.html", "Tentang Kami | PM Multilink", HURAIAN, tentang),
    ("perkhidmatan.html", "Perkhidmatan | PM Multilink", HURAIAN, perkhidmatan),
    ("projek.html", "Projek | PM Multilink", HURAIAN, projek),
    ("hubungi.html", "Hubungi Kami | PM Multilink", HURAIAN, hubungi),
]
for f, t, h, isi in PAGES:
    (OUT / f).write_text(halaman(f, t, h, isi), encoding="utf-8")
    print("wrote", f)
