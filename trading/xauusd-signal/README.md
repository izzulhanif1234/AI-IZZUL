# Sistem Signal BUY / SELL XAUUSD

Indikator TradingView untuk **chart M15 atau H1**. Bila signal keluar, anda pasang **order LIMIT**:

```
BUY LIMIT
ENTRY    4114.22                       <- pasang BUY LIMIT di sini
COLLECT  4129.16  (+14.94$ / 149 pip)  <- wajib close (untung), letak sebagai TP
SL       4059.42  (-54.80$ / 548 pip)  <- wajib close (rugi)
Batal lepas 6 candle
```

## Kenapa order LIMIT, bukan masuk terus?
Selepas signal, harga biasanya "cucuk" lagi sedikit sebelum lantun. Purata trade yang menang turun $7.80 dulu.

Dengan LIMIT 0.25 ATR di bawah harga signal (untuk BUY), anda masuk pada harga lebih baik:
- COLLECT jadi lebih besar (+$10.93 berbanding +$7.20 di H1)
- SL jadi lebih dekat
- Harga kurang "melawan" anda selepas entry

Kosnya: lebih kurang 1 daripada 4 order tak kena, sebab harga terus naik tanpa turun dulu. Order tu batal, jadi anda tak untung dan tak rugi.

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

## Cara guna
1. Signal keluar → pasang **BUY LIMIT / SELL LIMIT** di ENTRY, dengan **TP = COLLECT** dan **SL** ikut label.
2. Kalau order tak kena dalam **6 candle**, padamkan order (ada alert *XAU batal order*).
3. Lepas order kena, biar TP/SL yang tutup. Ada alert *sampai COLLECT* dan *kena SL*.

Panel di kanan atas tunjuk trend H4, struktur, RSI, ADX, sesi, status (contohnya *BUY LIMIT menunggu 2/6*), paras trade, untung/rugi terapung dan rekod chart.

## Keputusan backtest (kos spread $0.30 setiap trade)

| | **H1** (Jun 2024 – Nov 2026) | **M15** (Sep – Nov 2026, 60 hari) |
|---|---|---|
| Trade (order kena) | 213 | 43 |
| Order batal | 75 | 15 |
| **Kena COLLECT** | **80.8%** | **81.4%** |
| Purata COLLECT (0.01 lot) | +$10.93 | +$5.97 |
| Purata SL (0.01 lot) | −$32.95 | −$21.30 |
| Jarak SL purata | $39.55 | $22.63 |
| Profit factor | **1.39** | **1.23** |
| SL berturut paling banyak | 2 | 3 |

## Tentang saiz SL
SL ikut volatiliti (3 ATR dari harga signal), bukan pip tetap. **SL tetap 30 pip dah diuji, dan hasilnya rugi:**

| SL 30 pip | H1 | M15 |
|---|---|---|
| $3 (1 pip = $0.10) | win 20–31%, rugi teruk | win 23–43%, rugi teruk |
| $30 (1 pip = $1) | win ~79%, PF 1.22 tapi tak stabil | rugi |

Emas H1 biasa bergerak ~$16 dalam satu candle, jadi SL $3 kena oleh pergerakan biasa. **Kawal rugi dengan saiz lot:** pastikan satu SL tak lebih 1–2% akaun.

**Formula:** lot = (akaun × 1%) ÷ (jarak SL dalam $ × 100)

Settings → *1 pip = berapa $* ikut broker anda ($0.10 atau $1), supaya label tunjuk pip dengan betul.

## Yang anda kena tahu
1. **Satu SL ≈ 3 COLLECT** (H1). Jangan sesekali alihkan atau buang SL.
2. **Data M15 cuma 60 hari** (hampir semua SELL). H1 lebih kukuh.
3. **Spread broker penting**, lebih-lebih lagi di M15.
4. Prestasi lepas tak menjamin masa depan. Uji di demo dulu. Ini alat bantuan analisis, bukan nasihat kewangan.

## Cara pasang
1. TradingView → chart **XAUUSD**, timeframe **M15** atau **H1**.
2. **Pine Editor** → padam semua → paste seluruh isi `xauusd_signal.pine` → **Save** → **Add to chart**.
3. **Alert** (Create Alert → Condition: XAU Signal):
   - `XAU BUY LIMIT` / `XAU SELL LIMIT`: pasang order (*Once per bar close*)
   - `XAU order kena`: position aktif
   - `XAU batal order`: padam order
   - `XAU sampai COLLECT` / `XAU kena SL`: close
   - `XAU bersedia`: setup sedang terbentuk
   - Atau pilih **Any alert() function call** untuk semua di atas, dengan harga penuh.

## Backtest sendiri
```bash
pip install yfinance pandas numpy
python backtest.py              # H1, ~2 tahun
python backtest.py --tf 15m     # M15, 60 hari
python backtest.py --lim 0      # masuk terus (untuk banding)
python backtest.py --csv data_broker.csv --tf 15m   # data sendiri: time,open,high,low,close
```
