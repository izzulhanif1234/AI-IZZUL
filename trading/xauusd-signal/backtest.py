"""
Backtest logik signal XAUUSD (sama seperti xauusd_signal.pine).

Dua mode:
  --mode winrate (default) : Win Rate Tinggi, chart H1, trend H4
  --mode trend             : Trend TP3, chart M15, trend H1

Mode Win Rate Tinggi:
  1. Trend H4   : harga H4 di atas EMA200 -> cari BUY sahaja, di bawah -> SELL sahaja
  2. Entry      : RSI(2) < 30 (BUY) / > 70 (SELL), ADX < 30, sesi London+NY
  3. COLLECT    : entry +/- 0.5 ATR
  4. SL         : entry -/+ 2.5 ATR, dipindah ke entry bila untung 0.3 ATR
  5. Time stop  : tutup pada harga semasa selepas 12 candle

Mode Trend: Trend + Pullback + Confirmation
  1. Trend HTF  : harga HTF di atas EMA200 HTF (BUY) / di bawah (SELL)
  2. Trend LTF  : EMA21 > EMA50 (BUY) / EMA21 < EMA50 (SELL)
  3. Pullback   : dalam N bar terakhir harga sentuh EMA21
  4. Trigger    : candle tutup melepasi high/low candle sebelum, searah trend
  5. Penapis    : RSI 50-70 (BUY) / 30-50 (SELL), ADX > 20, sesi London+NY
  6. SL         : bawah/atas swing pullback + 0.2 ATR (risk 0.8-2.5 ATR)
  7. TP         : 1R / 2R / 3R

Guna:
  pip install yfinance pandas numpy
  python backtest.py                              # Win Rate Tinggi, H1, ~2 tahun
  python backtest.py --mode trend                 # Trend, M15, 60 hari
  python backtest.py --mode trend --tf 1h --htf 4h --period 730d
  python backtest.py --csv data.csv --tf 1h       # CSV sendiri (time,open,high,low,close)
"""
import argparse

import numpy as np
import pandas as pd


# ---------- indikator (sama formula dengan TradingView) ----------
def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()


def rma(s, n):
    return s.ewm(alpha=1 / n, adjust=False).mean()


def rsi(close, n=14):
    d = close.diff()
    up = rma(d.clip(lower=0), n)
    dn = rma(-d.clip(upper=0), n)
    return 100 - 100 / (1 + up / dn)


def atr(df, n=14):
    pc = df.close.shift()
    tr = pd.concat([df.high - df.low, (df.high - pc).abs(), (df.low - pc).abs()], axis=1).max(axis=1)
    return rma(tr, n)


def adx(df, n=14):
    up = df.high.diff()
    dn = -df.low.diff()
    plus_dm = np.where((up > dn) & (up > 0), up, 0.0)
    minus_dm = np.where((dn > up) & (dn > 0), dn, 0.0)
    tr = atr(df, n)
    plus_di = 100 * rma(pd.Series(plus_dm, index=df.index), n) / tr
    minus_di = 100 * rma(pd.Series(minus_dm, index=df.index), n) / tr
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    return rma(dx, n)


# ---------- data ----------
def load(args):
    if args.csv:
        df = pd.read_csv(args.csv)
        df.columns = [c.lower() for c in df.columns]
        df["time"] = pd.to_datetime(df["time"], utc=True)
        df = df.set_index("time")[["open", "high", "low", "close"]]
    else:
        import yfinance as yf

        raw = yf.download(args.symbol, period=args.period, interval=args.tf, progress=False, auto_adjust=False)
        if isinstance(raw.columns, pd.MultiIndex):
            raw.columns = raw.columns.get_level_values(0)
        df = raw.rename(columns=str.lower)[["open", "high", "low", "close"]].dropna()
        df.index = df.index.tz_convert("UTC")
    return df


def htf_values(df, rule, ema_len):
    """Nilai HTF bar yang SUDAH tutup (tiada repaint) - sama seperti close[1] + lookahead_on dalam Pine."""
    h = df.close.resample(rule, label="left", closed="left").last().dropna()
    e = ema(h, ema_len)
    prev = pd.DataFrame({"htf_close": h.shift(1), "htf_ema": e.shift(1)})
    return prev.reindex(df.index, method="ffill")


# ---------- signal ----------
def build_signals(df, p):
    d = df.copy()
    d["ema_f"] = ema(d.close, p.fast)
    d["ema_s"] = ema(d.close, p.slow)
    d["rsi"] = rsi(d.close, 14)
    d["atr"] = atr(d, 14)
    d["adx"] = adx(d, 14)
    d = d.join(htf_values(d, p.htf_rule, p.htf_ema))

    myt = d.index.tz_convert("Asia/Kuala_Lumpur")
    hour = myt.hour
    d["in_sess"] = (hour >= p.sess_start) | (hour < p.sess_end) if p.sess_start > p.sess_end else (hour >= p.sess_start) & (hour < p.sess_end)

    lo_n = d.low.rolling(p.pb).min()
    hi_n = d.high.rolling(p.pb).max()

    up = (d.htf_close > d.htf_ema) & (d.ema_f > d.ema_s) & (d.close > d.ema_s)
    dn = (d.htf_close < d.htf_ema) & (d.ema_f < d.ema_s) & (d.close < d.ema_s)

    filt = d.in_sess & ((d.adx > p.adx_min) if p.adx_min > 0 else True)

    d["buy"] = up & (lo_n <= d.ema_f) & (d.close > d.open) & (d.close > d.high.shift()) & (d.close > d.ema_f) \
        & (d.rsi > 50) & (d.rsi < 70) & filt
    d["sell"] = dn & (hi_n >= d.ema_f) & (d.close < d.open) & (d.close < d.low.shift()) & (d.close < d.ema_f) \
        & (d.rsi < 50) & (d.rsi > 30) & filt

    d["sl_buy"] = lo_n - 0.2 * d.atr
    d["sl_sell"] = hi_n + 0.2 * d.atr
    return d


def simulate(d, p):
    trades = []
    i, n = 0, len(d)
    o = d.to_dict("list")
    idx = d.index
    while i < n:
        side = 1 if o["buy"][i] else (-1 if o["sell"][i] else 0)
        if side == 0 or np.isnan(o["atr"][i]):
            i += 1
            continue
        entry = o["close"][i]
        a = o["atr"][i]
        sl = o["sl_buy"][i] if side == 1 else o["sl_sell"][i]
        risk = abs(entry - sl)
        if risk > 2.5 * a:          # SL terlalu jauh -> entry tak bagus, skip
            i += 1
            continue
        risk = max(risk, 0.8 * a)
        sl = entry - side * risk

        # ikut trade sampai SL atau TP3 (atau habis data)
        hit = {r: None for r in (1, 1.5, 2, 3)}
        sl_bar = None
        j = i + 1
        while j < n:
            hi, lo = o["high"][j], o["low"][j]
            sl_now = (lo <= sl) if side == 1 else (hi >= sl)
            for r in hit:
                tp = entry + side * r * risk
                if hit[r] is None and not sl_now and ((hi >= tp) if side == 1 else (lo <= tp)):
                    hit[r] = j
            if sl_now:                # SL & TP dalam bar sama -> anggap SL (konservatif)
                sl_bar = j
                break
            if hit[3] is not None:
                break
            j += 1
        trades.append(dict(time=idx[i], side="BUY" if side == 1 else "SELL", entry=entry, sl=sl, risk=risk,
                           **{f"tp{r}": hit[r] is not None for r in hit}, end=j))
        i = j + 1                     # satu trade pada satu masa
    return pd.DataFrame(trades)


def report(t, cost):
    if t.empty:
        print("Tiada signal.")
        return
    print(f"Jumlah signal: {len(t)}  (BUY {sum(t.side=='BUY')}, SELL {sum(t.side=='SELL')})")
    print(f"Purata risk (jarak SL): ${t.risk.mean():.2f}   kos spread anggaran: ${cost:.2f}/trade\n")
    print(f"{'Target':>7} {'Win%':>6} {'Expect (R)':>11} {'Jumlah R':>9} {'Max DD (R)':>11}")
    for r in (1, 1.5, 2, 3):
        win = t[f"tp{r}"]
        res = np.where(win, r, -1.0) - cost / t.risk
        eq = np.cumsum(res)
        dd = (np.maximum.accumulate(np.concatenate([[0], eq]))[1:] - eq).max()
        print(f"{str(r)+'R':>7} {win.mean()*100:6.1f} {res.mean():11.3f} {res.sum():9.1f} {dd:11.1f}")
    print("\n5 signal terakhir:")
    print(t.tail(5)[["time", "side", "entry", "sl", "tp1", "tp2", "tp3"]].to_string(index=False))


# ---------- mode Win Rate Tinggi ----------
def simulate_winrate(df, p):
    d = df.copy()
    d["atr"] = atr(d, 14)
    d["rsi2"] = rsi(d.close, 2)
    d["adx"] = adx(d, 14)
    h = htf_values(d, p.htf_rule, 200)
    up, dn = (h.htf_close > h.htf_ema).values, (h.htf_close < h.htf_ema).values
    hour = d.index.tz_convert("Asia/Kuala_Lumpur").hour
    sess = (hour >= p.sess_start) | (hour < p.sess_end) if p.sess_start > p.sess_end else (hour >= p.sess_start) & (hour < p.sess_end)
    ok = np.asarray(sess) & (d.adx < p.wr_adx).values
    buy = up & (d.rsi2 < p.wr_rsi).values & ok
    sell = dn & (d.rsi2 > 100 - p.wr_rsi).values & ok

    H, L, C, A = d.high.values, d.low.values, d.close.values, d.atr.values
    out, i, n = [], 0, len(d)
    while i < n - 1:
        s = 1 if buy[i] else (-1 if sell[i] else 0)
        if s == 0 or np.isnan(A[i]):
            i += 1
            continue
        e, a = C[i], A[i]
        sl, tp, be_on = e - s * p.wr_sl * a, e + s * p.wr_tp * a, False
        j, px, why = i + 1, None, None
        while j < n:
            if (s == 1 and L[j] <= sl) or (s == -1 and H[j] >= sl):
                px, why = sl, ("BE" if be_on else "SL")
                break
            if (s == 1 and H[j] >= tp) or (s == -1 and L[j] <= tp):
                px, why = tp, "COLLECT"
                break
            if p.wr_be > 0 and not be_on and ((s == 1 and H[j] >= e + p.wr_be * a) or (s == -1 and L[j] <= e - p.wr_be * a)):
                sl, be_on = e, True
            if j - i >= p.wr_max:
                px, why = C[j], "TIME"
                break
            j += 1
        if px is None:
            break                     # trade masih terbuka di hujung data
        out.append(dict(time=d.index[i], side="BUY" if s == 1 else "SELL", entry=e, collect=tp,
                        sl=e - s * p.wr_sl * a, result=why, pnl=(px - e) * s - p.cost))
        i = j + 1
    return pd.DataFrame(out)


def report_winrate(t):
    if t.empty:
        print("Tiada signal.")
        return
    n = len(t)
    win, loss = t.pnl[t.pnl > 0], t.pnl[t.pnl < 0]
    eq = t.pnl.cumsum()
    dd = (eq.cummax().clip(lower=0) - eq).max()
    print(f"Jumlah trade: {n}  (BUY {sum(t.side == 'BUY')}, SELL {sum(t.side == 'SELL')})\n")
    for k in ("COLLECT", "BE", "SL", "TIME"):
        x = t[t.result == k]
        print(f"  {k:8s} {len(x):5d}  {len(x) / n * 100:5.1f}%   purata ${x.pnl.mean() if len(x) else 0:7.2f}/oz")
    print(f"\nWin (kena COLLECT)   : {(t.result == 'COLLECT').mean() * 100:.1f}%")
    print(f"Tidak rugi (+ BE)    : {t.result.isin(['COLLECT', 'BE']).mean() * 100:.1f}%")
    print(f"Profit factor        : {win.sum() / -loss.sum():.2f}")
    print(f"Untung bersih        : ${t.pnl.sum():.0f} per oz  (0.01 lot = 1 oz)")
    print(f"Drawdown terbesar    : ${dd:.0f} per oz")
    big = (t.pnl < -1).astype(int)
    print(f"Loss berturut paling banyak: {big.groupby((big != big.shift()).cumsum()).cumsum().max()}")
    q = t.set_index("time").pnl.resample("QE")
    print("\nIkut suku tahun ($/oz): " + "  ".join(f"{k:%Y}Q{(k.month - 1) // 3 + 1} {v:+.0f}" for k, v in q.sum().items() if q.count()[k] > 0))
    print("\n5 trade terakhir:")
    print(t.tail(5)[["time", "side", "entry", "collect", "sl", "result", "pnl"]].to_string(index=False, float_format=lambda x: f"{x:.2f}"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["winrate", "trend"], default="winrate")
    ap.add_argument("--symbol", default="GC=F")
    ap.add_argument("--tf", help="default: 1h (winrate) / 15m (trend)")
    ap.add_argument("--htf", help="timeframe trend, default: 4h (winrate) / 1h (trend)")
    ap.add_argument("--period", help="default: 730d (winrate) / 60d (trend)")
    ap.add_argument("--csv")
    ap.add_argument("--fast", type=int, default=21)
    ap.add_argument("--slow", type=int, default=50)
    ap.add_argument("--htf-ema", type=int, default=200)
    ap.add_argument("--pb", type=int, default=5, help="bar lookback pullback")
    ap.add_argument("--adx-min", type=float, default=20)
    ap.add_argument("--sess-start", type=int, default=14, help="jam mula sesi (waktu Malaysia)")
    ap.add_argument("--sess-end", type=int, default=2, help="jam tamat sesi (waktu Malaysia)")
    ap.add_argument("--cost", type=float, default=0.30, help="spread+komisen dalam USD per oz")
    ap.add_argument("--wr-rsi", type=float, default=30, help="winrate: RSI(2) BUY bawah nilai ni")
    ap.add_argument("--wr-adx", type=float, default=30, help="winrate: ADX maksimum")
    ap.add_argument("--wr-sl", type=float, default=2.5, help="winrate: SL x ATR")
    ap.add_argument("--wr-tp", type=float, default=0.5, help="winrate: COLLECT x ATR")
    ap.add_argument("--wr-be", type=float, default=0.3, help="winrate: pindah SL ke entry bila untung x ATR (0 = tutup)")
    ap.add_argument("--wr-max", type=int, default=12, help="winrate: time stop (candle)")
    p = ap.parse_args()
    wr = p.mode == "winrate"
    p.tf = p.tf or ("1h" if wr else "15m")
    p.htf = p.htf or ("4h" if wr else "1h")
    p.period = p.period or ("730d" if wr else "60d")
    p.htf_rule = p.htf[:-1] + "min" if p.htf.endswith("m") else p.htf

    df = load(p)
    print(f"Data: {len(df)} bar {p.tf}, {df.index[0]:%Y-%m-%d} -> {df.index[-1]:%Y-%m-%d}, trend {p.htf}\n")
    if wr:
        report_winrate(simulate_winrate(df, p))
    else:
        report(simulate(build_signals(df, p), p), p.cost)
