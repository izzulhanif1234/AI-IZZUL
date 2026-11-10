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
| Kena COLLECT | ~65% | ~28–48% |
| Tidak rugi (COLLECT + breakeven) | **~89%** | – |
| Profit factor | 1.25 | ~1.2–1.5 (bila sasar COLLECT 3) |
| Sifat | Selalu menang sikit, sekali-sekala rugi besar | Selalu rugi sikit, sekali-sekala menang besar |

---

## Mode 1: Win Rate Tinggi (H1)

### Bila signal keluar
1. **Trend besar (H4)**: harga H4 di atas EMA200 → cari **BUY sahaja**. Di bawah → cari **SELL sahaja**.
2. **Entry**: harga jatuh mendadak melawan trend, iaitu RSI(2) bawah 30 untuk BUY atau atas 70 untuk SELL. Kita beli "diskaun" dalam trend naik.
3. **Penapis**: ADX bawah 30 (pasaran tak terlalu meluncur sehala), dan sesi London + New York sahaja (14:00–02:00 waktu Malaysia).

### Apa yang anda nampak di chart
```
BUY SEKARANG
ENTRY    4119.20     <- masuk pada harga ni (tutup candle)
COLLECT  4129.15     <- ambil untung di sini (letak TP)
SL       4069.45     <- stop loss
SL ke entry bila harga 4125.17
Tutup sendiri lepas 12 candle
```
Setiap paras juga dilukis sebagai garisan dengan nama dan harga di hujungnya. Panel di kanan atas tunjuk ENTRY / COLLECT / SL untuk trade yang sedang aktif.

### Cara urus trade (penting)
1. Masuk pada harga **ENTRY**. Letak **TP = COLLECT** dan **SL** dalam MT4/MT5.
2. Bila harga sampai paras **"SL ke entry"**, alihkan SL ke harga ENTRY. Inilah yang kurangkan rugi: kalau harga patah balik, anda keluar tanpa rugi (cuma spread).
3. Kalau selepas **12 candle H1** belum kena COLLECT atau SL, **tutup trade sendiri**.
4. Langkah 2 dan 3 ada alert: *XAU pindah SL ke entry* dan *XAU time stop*.

### Keputusan backtest (GC=F, H1, Jun 2024 – Nov 2026, kos $0.30/trade)

| Keputusan | Bil. | % | Purata per trade (1 oz = 0.01 lot) |
|---|---|---|---|
| COLLECT (untung) | 485 | 65.4% | +$6.74 |
| BE (SL di entry, keluar kosong) | 175 | 23.6% | −$0.30 (spread) |
| SL (rugi penuh) | 60 | 8.1% | −$38.14 |
| Time stop | 22 | 3.0% | −$11.88 |

- **Tidak rugi: 88.9%** · Profit factor **1.25** · Loss berturut paling banyak: **2**
- Untung bersih +$666 per oz, drawdown terbesar $220 per oz
- 9 daripada 11 suku tahun untung. Dua suku rugi: 2025Q4 (−$120) dan 2026Q3 (−$101).

### Bagaimana tetapan ni dipilih
- Diuji **lebih 2,000 kombinasi**. Data dibahagi dua: 60% pertama untuk pilih tetapan, 40% terakhir untuk uji tetapan tu atas data yang ia tak pernah "nampak".
- Tetapan ni lulus kedua-dua bahagian (PF 1.29 → 1.23).
- Kebanyakan sistem "win rate 80%" lain gagal di bahagian ujian. Sebabnya, kerugian yang besar memadam semua kemenangan kecil.

### Risiko yang anda kena tahu
- **Satu SL penuh (−$38) memadam ~6 COLLECT (+$6.74).** Jangan sesekali alihkan SL lebih jauh atau buang SL. Itulah cara akaun hangus dengan sistem win rate tinggi.
- **Mesti ikut breakeven dan time stop.** Tanpa BE, purata rugi naik dari $10 ke $30. Win rate memang naik ke ~84%, tapi rugi lebih besar setiap kali kalah.
- **Hanya H1.** Pada M15/M5 COLLECT terlalu kecil berbanding spread, dan hasilnya rugi (PF 0.85–0.96). Panel akan tunjuk "AMARAN: Guna chart H1".
- Emas naik kuat sepanjang 2024–2026, jadi kebanyakan trade dalam ujian ni ialah BUY (503 BUY vs 239 SELL). Bila pasaran berubah, prestasi boleh berbeza.
- Spread broker anda penting. Kalau spread biasa melebihi $0.50, untung sistem ni banyak terhakis.

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
python backtest.py --mode trend        # mode Trend, M15, 60 hari
python backtest.py --csv data.csv --tf 1h   # data broker sendiri (time,open,high,low,close)
```

## Saiz lot
Risiko **0.5–1% akaun** setiap trade:

lot = (baki akaun × 1%) ÷ (jarak SL dalam $ × 100)

Contoh: akaun $1,000 dan SL $50 → (1000 × 0.01) ÷ (50 × 100) = **0.002 lot**. Ini bawah lot minimum 0.01, maknanya akaun $1,000 terlalu kecil untuk SL selebar ni pada risiko 1%. Gunakan 0.01 lot hanya kalau anda terima risiko ~5% setiap trade.

> Ini alat bantuan analisis, bukan nasihat kewangan. Prestasi lepas tidak menjamin keputusan akan datang. Uji di akaun demo dahulu sekurang-kurangnya 1–2 bulan.
