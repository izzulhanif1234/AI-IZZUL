# Sistem Signal BUY / SELL XAUUSD

Indikator TradingView untuk **chart M15 atau H1**. Setiap signal tunjuk:

```
BUY SEKARANG
ENTRY    4119.20                      <- BUY / SELL terus pada harga ni
COLLECT  4129.15  (+9.95$ / 100 pip)  <- wajib close (untung), letak sebagai TP
SL       4059.50  (-59.70$ / 597 pip) <- wajib close (rugi)
```

## Bila signal keluar

| | BUY | SELL |
|---|---|---|
| Trend besar (H4) | harga H4 atas EMA200 | harga H4 bawah EMA200 |
| Struktur chart | harga atas EMA50 **dan** EMA200 | harga bawah EMA50 **dan** EMA200 |
| Entry | harga baru **jatuh mendadak** (RSI 2 < 30) | harga baru **naik mendadak** (RSI 2 > 70) |
| Penapis | ADX < 30, sesi London + New York (14:00–02:00 waktu Malaysia) | sama |

- Signal dikira bila candle **tutup** dan tak berubah selepas tu (tiada repaint).
- **BERSEDIA** (kuning) = setup sedang terbentuk, belum signal.
- Satu trade pada satu masa. Hanya trade terkini dilukis, supaya chart sentiasa bersih.
- Panel di kanan atas tunjuk trend H4, struktur, RSI, ADX, sesi, status, paras trade, untung/rugi terapung dan rekod chart.

## Cara guna
1. Signal keluar → **BUY / SELL terus**. Letak **TP = COLLECT** dan **SL** ikut label.
2. Biar TP/SL yang tutup trade. Ada alert *XAU sampai COLLECT* dan *XAU kena SL*.

## Keputusan backtest (kos spread $0.30 setiap trade)

| | **H1** (Jun 2024 – Nov 2026) | **M15** (Sep – Nov 2026, 60 hari) |
|---|---|---|
| Trade | 297 (BUY 203, SELL 94) | 60 (BUY 5, SELL 55) |
| **Kena COLLECT** | **87.5%** | **88.3%** |
| Purata COLLECT (0.01 lot) | +$7.16 | +$3.88 |
| Purata SL (0.01 lot) | −$37.53 | −$23.00 |
| Jarak SL purata | $43.80 | $24.82 |
| Profit factor | 1.34 | 1.28 |
| SL berturut paling banyak | 2 | 3 |

## Perkara penting
1. **Harga selalu melawan dulu lepas entry.** Di H1, 37% trade yang akhirnya menang turun lebih $5 dulu (purata $7.80). Jangan close awal.
2. **Satu SL ≈ 5 COLLECT.** Jangan sesekali alihkan atau buang SL.
3. **SL ikut volatiliti (3 ATR), bukan pip tetap.** SL tetap 30 pip ($3 atau $30) dah diuji, dan hasilnya rugi di H1 dan M15. Kawal rugi dengan **saiz lot**: satu SL tak lebih 1–2% akaun.
   - **Formula:** lot = (akaun × 1%) ÷ (jarak SL dalam $ × 100)
4. Settings → *1 pip = berapa $* ikut broker anda ($0.10 atau $1).
5. **Data M15 cuma 60 hari.** H1 lebih kukuh. Uji di demo dulu. Ini alat bantuan analisis, bukan nasihat kewangan.

## Cara pasang
1. TradingView → chart **XAUUSD**, timeframe **M15** atau **H1**.
2. **Pine Editor** → padam semua → paste seluruh isi `xauusd_signal.pine` → **Save** → **Add to chart**.
3. **Alert** (Create Alert → Condition: XAU Signal): `XAU BUY`, `XAU SELL`, `XAU sampai COLLECT`, `XAU kena SL`, `XAU bersedia`, atau **Any alert() function call** untuk semua.

## Backtest sendiri
```bash
pip install yfinance pandas numpy
python backtest.py              # H1, ~2 tahun
python backtest.py --tf 15m     # M15, 60 hari
python backtest.py --csv data_broker.csv --tf 15m   # data sendiri: time,open,high,low,close
```
