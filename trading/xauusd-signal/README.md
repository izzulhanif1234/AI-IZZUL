# XAUUSD Signal A+

Indikator TradingView untuk **chart M15 atau H1**.

## Apa yang baru: ZON ENTRY nampak SEBELUM harga sampai
Indikator lukis **ZON ENTRY** di chart:
- **Hijau (ZON BUY):** EMA50 hingga EMA50 + 0.75 ATR, bila trend H4 naik
- **Merah (ZON SELL):** EMA50 − 0.75 ATR hingga EMA50, bila trend H4 turun

Panel beritahu harga zon tu lebih awal, contohnya *"Tunggu harga turun ke ZON BUY (4108.50)"*. Anda tahu di mana signal akan keluar, sebelum harga bergerak.

Signal **A+** keluar bila harga masuk zon **dan** baru jatuh mendadak (BUY) atau naik mendadak (SELL):

```
BUY SEKARANG  |  GRED A+
ENTRY    4119.20
COLLECT  4129.15  (+9.95$ / 100 pip)    <- wajib close (untung), minimum 50 pip
SL       4059.50  (-59.70$ / 597 pip)   <- wajib close (rugi)
```
Kotak hijau = kawasan untung, kotak merah = kawasan risiko.

## Kenapa zon EMA50?
Daripada lebih 2,000 kombinasi yang diuji, faktor ini paling jelas memisahkan signal bagus dan lemah:

| | H1 | M15 |
|---|---|---|
| Signal **dekat** EMA50 | win 89%, PF 1.77 | win 89%, PF 1.38 |
| Signal **jauh** dari EMA50 | win 86%, PF 0.98 (**rugi**) | win 84%, PF 0.88 (**rugi**) |

Beli dip pada "lantai" trend (EMA50) jauh lebih kukuh daripada beli bila harga masih tinggi melambung.

## Syarat penuh signal

| | BUY | SELL |
|---|---|---|
| Trend H4 | harga H4 atas EMA200 | harga H4 bawah EMA200 |
| Struktur | harga atas EMA50 dan EMA200 | harga bawah EMA50 dan EMA200 |
| Zon | dalam 0.75 ATR dari EMA50 | sama |
| Pergerakan | RSI(2) < 30 | RSI(2) > 70 |
| Penapis | ADX < 30, sesi London + NY (14:00–02:00 waktu Malaysia) | sama |

Signal dikira bila candle **tutup** dan tak berubah selepas tu (tiada repaint).

## Keputusan backtest (COLLECT minimum 50 pip, kos spread $0.30)

Pilih **Jenis SL** dalam Settings:

| | SL purata | COLLECT purata | **Kena COLLECT** | Profit factor |
|---|---|---|---|---|
| **H1 + SL Rapat** | $22.64 | $8.49 | **74.0%** | 1.23 |
| **H1 + SL Normal** | $47.73 | $8.47 | **87.0%** | 1.66 |
| M15 + SL Rapat | $11.64 | $4.77 | 70.3% | 0.99 (**rugi**, jangan guna) |
| **M15 + SL Normal** (default) | $24.55 | $4.76 | **89.2%** | 1.72 |

- **SL Rapat** = 1 ATR di bawah EMA50 (BUY) / di atas EMA50 (SELL). SL separuh lebih kecil, tapi win rate lebih rendah. **Guna di H1 sahaja.**
- **SL Normal** = 3 ATR dari entry. Win rate paling tinggi.
- **Win rate tinggi + SL rapat + COLLECT 50 pip** serentak dah diuji, dan hasilnya rugi. Contohnya SL $3 (win 25–28%) dan SL tetap $10–20 (win 54–76%) semuanya rugi di H1.
- H1: Jun 2024 – Nov 2026. M15: 60 hari sahaja.

## Perkara penting
1. **Harga selalu melawan dulu lepas entry** (purata ~$8 di H1). Jangan close awal.
2. **Satu SL ≈ 5 COLLECT.** Jangan sesekali alihkan atau buang SL.
3. **SL tetap 30 pip dah diuji, dan hasilnya rugi.** Pilih SL Rapat (H1) atau SL Normal. Kawal rugi dengan **saiz lot**: satu SL tak lebih 1–2% akaun.
   - **Formula:** lot = (akaun × 1%) ÷ (jarak SL dalam $ × 100)
4. Settings → *1 pip = berapa $* ikut broker ($0.10 atau $1).
5. **Data M15 cuma 60 hari.** H1 lebih kukuh. Uji di demo dulu. Ini alat bantuan analisis, bukan nasihat kewangan.

## Cara pasang
1. TradingView → chart **XAUUSD**, timeframe **M15** atau **H1**.
2. **Pine Editor** → padam semua → paste seluruh isi `xauusd_signal.pine` → **Save** → **Add to chart**.
3. **Alert:** `XAU BUY A+`, `XAU SELL A+`, `XAU sampai COLLECT`, `XAU kena SL`, `XAU bersedia`, atau **Any alert() function call** untuk semua.

## Backtest sendiri
```bash
pip install yfinance pandas numpy
python backtest.py              # H1
python backtest.py --tf 15m     # M15
python backtest.py --zone 99    # tanpa penapis zon (untuk banding)
```
