# Sistem Signal BUY / SELL XAUUSD

Indikator TradingView untuk **chart M15 atau H1**. Setiap signal hanya tunjuk tiga perkara:

```
BUY
ENTRY    4119.20     <- masuk di sini
COLLECT  4129.15     <- wajib close (untung)
SL       4059.50     <- wajib close (rugi)
```

Anda close position sendiri secara manual. Sebaiknya letak COLLECT sebagai TP dan SL terus dalam MT4/MT5 sebaik masuk.

## Bila signal keluar

| | BUY | SELL |
|---|---|---|
| Trend besar (H4) | harga H4 atas EMA200 | harga H4 bawah EMA200 |
| Struktur chart | harga atas EMA50 **dan** EMA200 | harga bawah EMA50 **dan** EMA200 |
| Entry | harga baru **jatuh mendadak** (RSI 2 < 30) | harga baru **naik mendadak** (RSI 2 > 70) |
| Penapis | ADX < 30, sesi London + New York (14:00–02:00 waktu Malaysia) | sama |

- **Tiada SELL masa trend naik, tiada BUY masa trend turun.** Kita hanya masuk searah trend besar, pada harga "diskaun".
- **Signal keluar sebelum harga bergerak.** Signal dikira bila candle **tutup**, dan tak berubah selepas tu (tiada repaint). Dalam 3 candle sebelum signal, harga bergerak purata −$9 (H1) / −$5 (M15) melawan arah signal. Signal keluar di hujung pergerakan tu, sebelum lantunan.
- **BERSEDIA** (tanda kuning) muncul semasa candle masih bergerak bila setup sedang terbentuk. Ini **belum** signal dan boleh hilang. Masuk hanya bila segi tiga BUY/SELL keluar.
- **Satu trade pada satu masa.** Signal baru hanya keluar selepas trade sebelumnya kena COLLECT atau SL.
- **Chart sentiasa bersih.** Hanya trade terkini dilukis penuh. Signal lama tinggal segi tiga kecil.

## Panel monitor (kanan atas)

| Baris | Maksud |
|---|---|
| Trend H4 | NAIK = cari BUY sahaja, TURUN = cari SELL sahaja |
| Struktur EMA50 / EMA200 | ATAS sokong BUY, BAWAH sokong SELL, CAMPUR = tiada signal |
| RSI(2) | DIP (bawah 30) atau LONJAK (atas 70) = harga baru bergerak mendadak |
| ADX | OK bila bawah 30 |
| Sesi London + NY | Signal hanya keluar bila AKTIF |
| Status | *Tunggu dip untuk BUY*, *Tunggu lonjakan untuk SELL*, *BERSEDIA*, *BUY / SELL aktif*, atau *Tiada setup* |
| ENTRY / COLLECT / SL | Paras trade yang sedang berjalan |
| Rekod chart ni | % trade yang kena COLLECT atas data broker anda |

## Keputusan backtest (kos spread $0.30 setiap trade)

| | **H1** | **M15** |
|---|---|---|
| Tempoh data | Jun 2024 – Nov 2026 (2.4 tahun) | Sep – Nov 2026 (60 hari) |
| Jumlah trade | 297 (BUY 203, SELL 94) | 60 (BUY 5, SELL 55) |
| **Kena COLLECT** | **87.5%** | **88.3%** |
| Purata COLLECT (0.01 lot) | +$7.16 | +$3.88 |
| Purata SL (0.01 lot) | −$37.53 | −$23.00 |
| Profit factor | 1.34 | 1.28 |
| SL berturut paling banyak | 2 | 3 |
| Signal seminggu | ~2.4 | ~6 |
| Tempoh trade biasa | 2 candle (90% siap dalam 8) | 2 candle (90% siap dalam 10) |

Tetapan yang sama digunakan untuk M15 dan H1 (tiada tuning khas untuk setiap timeframe). Di H1, tetapan ni untung dalam kedua-dua separuh data (separuh pertama dan kedua).

## Yang anda kena tahu sebelum guna

1. **Satu SL ≈ 5 COLLECT.** Win rate tinggi sebab COLLECT kecil dan SL lebar. Sistem untung hanya kalau anda **tak pernah alihkan atau buang SL**.
2. **Saiz lot ikut akaun.** Satu SL boleh sampai −$150 per 0.01 lot bila pasaran liar (purata −$38 di H1, −$23 di M15). Pastikan satu SL tak lebih 1–2% akaun.
   - **Formula:** lot = (akaun × 1%) ÷ (jarak SL dalam $ × 100)
3. **Data M15 cuma 60 hari** dan hampir semuanya SELL, sebab emas jatuh dalam tempoh tu. Keputusan M15 kurang kukuh berbanding H1. Uji di demo dulu.
4. **Spread broker penting**, lebih-lebih lagi di M15 (COLLECT ~$4). Kalau spread anda selalu atas $0.40, guna H1.
5. **Trade jarang tersangkut lama.** Ada satu trade H1 ambil 188 candle (~8 hari) sebelum selesai. Bila SL dan COLLECT dah diletak dalam MT4/MT5, anda tak perlu tengok chart.
6. Prestasi lepas tak menjamin masa depan. Ini alat bantuan analisis, bukan nasihat kewangan.

## Cara pasang

1. TradingView → chart **XAUUSD**, timeframe **M15** atau **H1**.
2. **Pine Editor** → padam semua → paste seluruh isi `xauusd_signal.pine` → **Save** → **Add to chart**.
3. **Alert** (Create Alert → Condition: XAU Signal):
   - `XAU BUY` / `XAU SELL`: signal baru (*Once per bar close*)
   - `XAU sampai COLLECT` / `XAU kena SL`: masa untuk close (*Once per bar*)
   - `XAU bersedia`: setup sedang terbentuk (*Once per bar*)
   - Atau pilih **Any alert() function call** untuk semua alert, dengan harga penuh.

## Backtest sendiri

```bash
pip install yfinance pandas numpy
python backtest.py              # H1, ~2 tahun
python backtest.py --tf 15m     # M15, 60 hari
python backtest.py --csv data_broker.csv --tf 15m   # data sendiri: time,open,high,low,close
```
