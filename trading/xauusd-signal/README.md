# Sistem Signal BUY / SELL XAUUSD

Dua fail:

| Fail | Guna |
|---|---|
| `xauusd_signal.pine` | Indikator TradingView: keluarkan label BUY/SELL dengan Entry, SL, TP1/TP2/TP3, panel status dan alert |
| `backtest.py` | Uji logik yang sama atas data emas sebenar (Python) |

## Logik entry

Signal hanya keluar bila **semua** syarat dipenuhi, dan hanya selepas candle **tutup** (tiada repaint):

1. **Trend besar (HTF)**: harga H1 di atas EMA200 H1 untuk BUY, di bawah untuk SELL.
2. **Trend chart**: EMA21 > EMA50 (BUY) atau EMA21 < EMA50 (SELL).
3. **Pullback**: dalam 5 candle terakhir harga turun (atau naik) menyentuh EMA21. Kita tak kejar harga.
4. **Confirmation**: candle searah trend tutup melepasi high candle sebelum (BUY) atau low candle sebelum (SELL).
5. **Penapis**: RSI 50–70 (BUY) / 30–50 (SELL), ADX > 20 (ada momentum), dan hanya dalam sesi London + New York (14:00–02:00 waktu Malaysia).
6. **SL**: di bawah swing low pullback (atau di atas swing high) + 0.2 ATR. Kalau SL lebih jauh dari 2.5 ATR, signal di-skip kerana entry tu dah lewat.
7. **TP**: 1R, 2R, 3R (R = jarak entry ke SL).

Satu trade pada satu masa. Signal baru hanya keluar selepas trade sebelumnya kena SL atau TP3.

## Cara pasang di TradingView

1. Buka chart **XAUUSD** (OANDA / broker anda), timeframe **M15**.
2. Buka **Pine Editor** → padam semua → paste isi `xauusd_signal.pine` → **Save** → **Add to chart**.
3. Untuk chart H1, tukar input *Timeframe trend (HTF)* ke **4 jam**.

### Alert ke telefon / Telegram

- **Alert biasa**: Create Alert → Condition: `XAU Signal` → `XAU BUY` atau `XAU SELL` → *Once per bar close*.
- **Alert dengan harga penuh (JSON)**: Condition: `XAU Signal` → **Any alert() function call**. Mesej alert akan mengandungi:
  `{"signal":"BUY","symbol":"XAUUSD","tf":"15","entry":4057.10,"sl":4040.40,"tp1":...,"tp2":...,"tp3":...}`
  Masukkan URL webhook (contohnya bot Telegram) kalau nak hantar automatik.

## Backtest

```bash
pip install yfinance pandas numpy
python backtest.py                                   # M15, trend H1, 60 hari
python backtest.py --tf 1h --htf 4h --period 730d    # H1, trend H4, ~2 tahun
python backtest.py --csv xauusd_m15.csv              # data broker sendiri (time,open,high,low,close)
```

### Keputusan (data GC=F gold futures, kos spread $0.30, dijalankan 10 Nov 2026)

**M15 / trend H1, 60 hari (41 trade)**

| Target | Win % | Purata per trade | Jumlah | Max drawdown |
|---|---|---|---|---|
| 1R | 48.8% | −0.05R | −1.8R | 6.3R |
| 2R | 34.1% | +0.00R | +0.2R | 10.3R |
| 3R | 34.1% | **+0.35R** | +14.2R | 9.2R |

**H1 / trend H4, ~2 tahun (118 trade)**

| Target | Win % | Purata per trade | Jumlah | Max drawdown |
|---|---|---|---|---|
| 1R | 48.3% | −0.05R | −5.9R | 10.3R |
| 2R | 33.1% | −0.03R | −2.9R | 12.5R |
| 3R | 28.0% | **+0.10R** | +12.1R | 8.2R |

### Apa maksud keputusan ni (baca betul-betul)

- **Tiada sistem yang bagi entry "tepat" setiap kali.** Sistem ni lebih kurang separuh kali salah pun pada TP1.
- **Kelebihan (edge) sistem ni kecil.** Ia untung hanya bila anda biarkan trade lari ke **TP3 (3R)**. Kalau ambil untung di TP1 sahaja, keputusannya rugi sedikit.
- Kami juga uji 36 kombinasi parameter (EMA HTF 50/200, pullback 3/5/8, ADX 0/20/25, dengan/tanpa sesi). Coraknya konsisten: target 1R biasanya rugi, target 3R biasanya untung sedikit. Penapis sesi London+NY membantu pada M15. Tetapan default **tidak** dipilih sebagai yang paling untung dalam ujian, supaya tak *overfit*.
- Data 60 hari M15 masih sikit (41 trade). Jangan anggap +0.35R itu pasti berulang.
- Drawdown 8–12R adalah biasa. Dengan risiko 1% seakaun per trade, itu bermakna akaun boleh turun 8–12% sebelum pulih.

### Cadangan guna

1. **Demo dulu** sekurang-kurangnya 1–2 bulan.
2. Risiko **0.5–1% akaun** per trade sahaja. Saiz lot = (baki × 1%) ÷ (jarak SL dalam $ × 100) untuk lot standard XAUUSD (1 lot = 100 oz).
3. Sasarkan **TP3**, atau ambil separuh di TP2 dan biarkan selebihnya ke TP3.
4. Elak trade 30 minit sebelum/selepas berita besar (NFP, CPI, FOMC). Spread emas melebar teruk dan SL mudah kena.
5. Panel di chart menunjukkan win rate sebenar indikator atas data broker anda. Semak panel tu sebelum percaya pada mana-mana nombor di atas.

> Ini alat bantuan analisis, bukan nasihat kewangan. Prestasi lepas tidak menjamin keputusan akan datang.
