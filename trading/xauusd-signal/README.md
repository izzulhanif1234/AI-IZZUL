# Sistem Signal BUY / SELL XAUUSD

| Fail | Guna |
|---|---|
| `xauusd_signal.pine` | Indikator TradingView: label BUY/SELL dengan **ENTRY**, **COLLECT** (ambil untung) dan **SL**, panel status, alert |
| `backtest.py` | Uji logik yang sama atas data emas sebenar (Python) |

Indikator ada **dua mode** (tukar dalam Settings → *Mode*):

| | Win Rate Tinggi (default) | Trend TP3 |
|---|---|---|
| Chart | **H1 sahaja** | M15 |
| Ambil untung | 1 COLLECT, kecil (0.5 ATR, ~$7–10) | COLLECT 1 / 2 / 3 (1R / 2R / 3R) |
| Kena COLLECT | ~66% | ~28–48% |
| Tidak rugi (COLLECT + breakeven) | **~93%** | – |
| Kena SL penuh | **~5%** | ~52–72% |
| Profit factor | **2.17** | ~1.2–1.5 (bila sasar COLLECT 3) |
| Kekerapan | ~1.7 signal seminggu (BUY sahaja) | ~4 seminggu |

---

## Mode 1: Win Rate Tinggi (H1), signal solid sahaja

### Bila signal BUY keluar (semua syarat mesti betul)
1. **Trend H4 naik**: harga H4 di atas EMA200 H4.
2. **Struktur H1 masih kukuh**: harga H1 di atas EMA50 **dan** EMA200 H1. Ini maksudnya harga cuma "turun sekejap", bukan trend yang sedang patah.
3. **Dip**: RSI(2) bawah 30, iaitu harga baru jatuh mendadak. Kita beli "diskaun" sebelum harga lantun.
4. **Penapis**: ADX bawah 30, dan sesi London + New York sahaja (14:00–02:00 waktu Malaysia).

**SELL ditutup secara default.** Dalam backtest, SELL tak untung (PF 0.94), dan SELL masa chart naik kuat itulah yang selalu kena SL besar. Bila trend H4 turun, sistem **berehat** (panel tunjuk "TURUN (rehat)"). Contohnya, dari 25 Ogos hingga 9 Nov 2026 tiada langsung signal semasa emas jatuh dari $4,700 ke $4,000.

### Adakah signal keluar sebelum harga bergerak?
Ya. Signal dikira bila candle H1 **tutup**, dan tak berubah selepas tu (tiada repaint). Dalam 3 jam sebelum signal, harga jatuh purata **−$8**. Signal keluar di bawah dip tu, sebelum lantunan.

Supaya anda lebih awal bersedia: tanda kuning **BERSEDIA** muncul pada candle yang masih bergerak bila setup sedang terbentuk. Ini **belum** signal. Tanda tu boleh hilang kalau candle tutup tanpa memenuhi syarat. Masuk hanya bila segi tiga hijau BUY keluar.

### Apa yang anda nampak di chart
```
BUY SEKARANG
ENTRY    4119.20     <- masuk pada harga ni (tutup candle)
COLLECT  4129.15     <- ambil untung di sini (letak TP)
SL       4069.45     <- stop loss
SL ke entry bila harga 4125.17
Tutup sendiri lepas 12 candle
```
- **Trade terkini sahaja** dilukis penuh (label, garisan ENTRY / COLLECT / SL dengan harga). Lukisan trade lama dipadam bila signal baru keluar.
- **Signal lama** hanya ditanda dengan segi tiga kecil.
- **Keputusan trade lama** ditanda dengan titik kecil di harga keluar: hijau = COLLECT, kelabu = BE, X merah = SL, segi empat oren = time stop.
- Panel di kanan atas tunjuk ENTRY / COLLECT / SL untuk trade yang sedang aktif.

### Cara urus trade (penting)
1. Masuk pada harga **ENTRY**. Letak **TP = COLLECT** dan **SL** dalam MT4/MT5.
2. Bila harga sampai paras **"SL ke entry"**, alihkan SL ke harga ENTRY. Kalau harga patah balik, anda keluar tanpa rugi (cuma spread).
3. Kalau selepas **12 candle H1** belum kena COLLECT atau SL, **tutup trade sendiri**.
4. Langkah 2 dan 3 ada alert: *XAU pindah SL ke entry* dan *XAU time stop*.

### Keputusan backtest (GC=F, H1, Jun 2024 – Nov 2026, kos $0.30/trade)

| Keputusan | Bil. | % | Purata per trade (1 oz = 0.01 lot) |
|---|---|---|---|
| COLLECT (untung) | 142 | 66.0% | +$6.49 |
| BE (SL di entry, keluar kosong) | 57 | 26.5% | −$0.30 (spread) |
| SL (rugi penuh) | 10 | 4.7% | −$33.26 |
| Time stop | 6 | 2.8% | −$12.67 |

- **Tidak rugi: 92.6%** · Profit factor **2.17** · Loss berturut paling banyak: **2**
- Untung bersih +$497 per oz, drawdown terbesar $125 per oz
- **10 daripada 10 suku tahun untung**

### Kenapa SL lebar (2.5 ATR)?
SL lebih rapat sudah diuji, dan hasilnya lebih teruk:

| SL | Kena SL | Profit factor | Untung bersih ($/oz) |
|---|---|---|---|
| 1.0 ATR | 23% | 1.09 | 65 |
| 1.5 ATR | 13% | 1.39 | 245 |
| 2.0 ATR | 9% | 1.61 | 340 |
| **2.5 ATR** | **5%** | **2.17** | **497** |

Emas H1 biasa "goyang" $15–25 sebelum lantun. SL rapat akan kena dulu sebelum harga sempat naik. **Kawal rugi dengan saiz lot, bukan dengan SL rapat** (lihat bahagian Saiz lot di bawah).

### Bagaimana tetapan ni dipilih
- Diuji **lebih 2,000 kombinasi**. Data dibahagi dua: 60% pertama untuk pilih tetapan, 40% terakhir untuk uji tetapan tu atas data yang ia tak pernah "nampak".
- Tetapan asas lulus kedua-dua bahagian (PF 1.29 → 1.23).
- Penapis struktur EMA50/EMA200 memperbaiki kedua-dua bahagian (PF 2.19 → 2.15).
- Penapis yang hanya nampak bagus di satu bahagian sahaja dibuang, contohnya waktu overlap London-NY dan RSI lebih dalam.

### Risiko yang anda kena tahu
- **Satu SL penuh (−$33) memadam ~5 COLLECT (+$6.49).** Jangan sesekali alihkan SL lebih jauh atau buang SL.
- **Mesti ikut breakeven dan time stop**, kalau tidak keputusan anda tak sama dengan backtest.
- **Hanya H1.** Pada M15/M5 COLLECT terlalu kecil berbanding spread. Panel akan tunjuk "AMARAN: Guna chart H1".
- **Sistem BUY sahaja bergantung pada trend naik.** Emas naik kuat sepanjang 2024–2026. Kalau emas masuk trend turun yang panjang, sistem akan senyap berminggu-minggu. Itu memang disengajakan.
- Data cuma 215 trade dalam ~2.4 tahun. Keputusan masa depan mungkin lebih lemah daripada backtest.
- Spread broker anda penting. Kalau spread biasa melebihi $0.50, untung banyak terhakis.

---

## Mode 2: Trend TP3 (M15)

1. **Trend H1**: harga di atas EMA200 H1 (BUY) atau di bawah (SELL).
2. **Struktur**: EMA21 > EMA50 (BUY) atau EMA21 < EMA50 (SELL).
3. **Pullback**: dalam 5 candle terakhir harga menyentuh EMA21.
4. **Pengesahan**: candle tutup melepasi high (BUY) atau low (SELL) candle sebelum.
5. **Penapis**: RSI 50–70 / 30–50, ADX > 20, sesi London + NY.
6. **SL** di bawah swing pullback. **COLLECT 1 / 2 / 3** = 1R / 2R / 3R.

Keputusan: sistem ni untung hanya bila trade dibiarkan sampai **COLLECT 3**. Di M15 (60 hari) purata +0.35R per trade, di H1 (2 tahun) +0.10R. Pada COLLECT 1 hasilnya rugi sikit.

---

## Cara pasang di TradingView
1. Buka chart **XAUUSD**, pilih timeframe **H1** (atau M15 untuk mode Trend).
2. Klik **Pine Editor**, padam semua kod sedia ada, paste **seluruh** isi `xauusd_signal.pine` (mula dari `//@version=6`).
3. Klik **Save**, kemudian **Add to chart**.

### Alert
Create Alert → Condition: **XAU Signal**, kemudian pilih:
- `XAU BUY` / `XAU SELL`: signal baru
- `XAU bersedia`: setup sedang terbentuk (pilih *Once per bar*), belum signal
- `XAU pindah SL ke entry`: masa untuk alihkan SL ke harga entry
- `XAU time stop`: tutup trade sekarang
- **Any alert() function call**: semua di atas, dengan harga penuh dalam format JSON (sesuai untuk webhook / bot Telegram):
  `{"signal":"BUY","mode":"winrate","entry":4119.20,"tp":4129.15,"sl":4069.45,"be_trigger":4125.17,"max_bars":12}`

Pilih *Once per bar close*.

## Backtest sendiri
```bash
pip install yfinance pandas numpy
python backtest.py                     # Win Rate Tinggi, H1, ~2 tahun
python backtest.py --wr-be 0           # tanpa breakeven (untuk banding)
python backtest.py --wr-sell           # termasuk SELL (untuk banding)
python backtest.py --mode trend        # mode Trend, M15, 60 hari
python backtest.py --csv data.csv --tf 1h   # data broker sendiri (time,open,high,low,close)
```

## Saiz lot
Risiko **0.5–1% akaun** setiap trade:

lot = (baki akaun × 1%) ÷ (jarak SL dalam $ × 100)

Contoh: akaun $1,000 dan SL $50 → (1000 × 0.01) ÷ (50 × 100) = **0.002 lot**. Ini bawah lot minimum 0.01, maknanya akaun $1,000 terlalu kecil untuk SL selebar ni pada risiko 1%. Gunakan 0.01 lot hanya kalau anda terima risiko ~5% setiap trade.

> Ini alat bantuan analisis, bukan nasihat kewangan. Prestasi lepas tidak menjamin keputusan akan datang. Uji di akaun demo dahulu sekurang-kurangnya 1–2 bulan.
