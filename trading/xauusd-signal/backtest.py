"""
Backtest signal XAUUSD (logik sama dengan xauusd_signal.pine).

BUY : trend H4 naik (harga H4 atas EMA200), harga atas EMA50 & EMA200,
      RSI(2) < 30, ADX < 30, sesi London + New York
SELL: trend H4 turun, harga bawah EMA50 & EMA200, RSI(2) > 70, ADX < 30, sesi
ENTRY   = harga tutup candle signal
COLLECT = entry +/- 0.5 ATR   (wajib close untung)
SL      = entry -/+ 3 ATR     (wajib close rugi)
Kalau COLLECT dan SL kena dalam candle yang sama, dikira SL (konservatif).
Satu trade pada satu masa.

Guna:
  pip install yfinance pandas numpy
  python backtest.py                 # H1, ~2 tahun
  python backtest.py --tf 15m        # M15, 60 hari (had data Yahoo)
  python backtest.py --csv data.csv --tf 15m   # data broker sendiri (time,open,high,low,close)
"""
import argparse

import numpy as np
import pandas as pd


# ---------- indikator (formula sama dengan TradingView) ----------
def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()


def rma(s, n):
    return s.ewm(alpha=1 / n, adjust=False).mean()


def rsi(close, n):
    d = close.diff()
    return 100 - 100 / (1 + rma(d.clip(lower=0), n) / rma(-d.clip(upper=0), n))


def atr(df, n=14):
    pc = df.close.shift()
    tr = pd.concat([df.high - df.low, (df.high - pc).abs(), (df.low - pc).abs()], axis=1).max(axis=1)
    return rma(tr, n)


def adx(df, n=14):
    up, dn = df.high.diff(), -df.low.diff()
    pdm = pd.Series(np.where((up > dn) & (up > 0), up, 0.0), index=df.index)
    mdm = pd.Series(np.where((dn > up) & (dn > 0), dn, 0.0), index=df.index)
    tr = atr(df, n)
    pdi, mdi = 100 * rma(pdm, n) / tr, 100 * rma(mdm, n) / tr
    return rma(100 * (pdi - mdi).abs() / (pdi + mdi), n)


def htf_trend(df, rule):
    """Close & EMA200 H4 dari candle H4 yang SUDAH tutup (sama seperti close[1] + lookahead_on)."""
    h = df.close.resample(rule, label="left", closed="left").last().dropna()
    prev = pd.DataFrame({"c": h.shift(1), "e": ema(h, 200).shift(1)})
    return prev.reindex(df.index, method="ffill")


# ---------- data ----------
def load(a):
    if a.csv:
        df = pd.read_csv(a.csv)
        df.columns = [c.lower() for c in df.columns]
        df["time"] = pd.to_datetime(df["time"], utc=True)
        return df.set_index("time")[["open", "high", "low", "close"]]
    import yfinance as yf

    raw = yf.download(a.symbol, period=a.period, interval=a.tf, progress=False, auto_adjust=False)
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)
    df = raw.rename(columns=str.lower)[["open", "high", "low", "close"]].dropna()
    df.index = df.index.tz_convert("UTC")
    return df


# ---------- signal & simulasi ----------
def run(df, a):
    d = df.copy()
    d["rsi2"], d["atr"], d["adx"] = rsi(d.close, 2), atr(d), adx(d)
    e50, e200 = ema(d.close, 50), ema(d.close, 200)
    h = htf_trend(d, a.htf)
    hour = d.index.tz_convert("Asia/Kuala_Lumpur").hour
    ok = np.asarray((hour >= 14) | (hour < 2)) & (d.adx < 30).values

    buy = ((h.c > h.e) & (d.close > e50) & (d.close > e200) & (d.rsi2 < 30)).values & ok & (not a.no_buy)
    sell = ((h.c < h.e) & (d.close < e50) & (d.close < e200) & (d.rsi2 > 70)).values & ok & (not a.no_sell)

    H, L, C, A = d.high.values, d.low.values, d.close.values, d.atr.values
    out, i, n = [], 0, len(d)
    while i < n - 1:
        s = 1 if buy[i] else (-1 if sell[i] else 0)
        if s == 0 or np.isnan(A[i]):
            i += 1
            continue
        e = C[i]
        tp, sl = e + s * a.tp * A[i], e - s * a.sl * A[i]
        j, res = i + 1, None
        while j < n:
            if (s == 1 and L[j] <= sl) or (s == -1 and H[j] >= sl):
                res = ("SL", sl)
                break
            if (s == 1 and H[j] >= tp) or (s == -1 and L[j] <= tp):
                res = ("COLLECT", tp)
                break
            j += 1
        if res is None:
            break                                   # trade masih terbuka di hujung data
        out.append(dict(time=d.index[i], side="BUY" if s == 1 else "SELL", entry=e, collect=tp, sl=sl,
                        result=res[0], pnl=(res[1] - e) * s - a.cost, candles=j - i))
        i = j + 1
    return pd.DataFrame(out)


def report(t):
    if t.empty:
        print("Tiada signal.")
        return
    w = t.pnl > 0
    eq = t.pnl.cumsum()
    dd = (eq.cummax().clip(lower=0) - eq).max()
    lose = (~w).astype(int)
    streak = lose.groupby((lose != lose.shift()).cumsum()).cumsum().max()
    print(f"Jumlah trade    : {len(t)}  (BUY {sum(t.side == 'BUY')}, SELL {sum(t.side == 'SELL')})")
    print(f"Kena COLLECT    : {w.mean() * 100:.1f}%   (BUY {w[t.side == 'BUY'].mean() * 100:.0f}%, SELL {w[t.side == 'SELL'].mean() * 100:.0f}%)")
    print(f"Purata COLLECT  : +${t.pnl[w].mean():.2f} per 0.01 lot")
    print(f"Purata SL       : ${t.pnl[~w].mean():.2f} per 0.01 lot  (paling teruk ${t.pnl.min():.2f})")
    print(f"Profit factor   : {t.pnl[w].sum() / -t.pnl[~w].sum():.2f}")
    print(f"Untung bersih   : ${t.pnl.sum():.0f} per 0.01 lot,  drawdown terbesar ${dd:.0f}")
    print(f"SL berturut     : paling banyak {streak}")
    print(f"Tempoh trade    : separuh selesai dalam {t.candles.median():.0f} candle, 90% dalam {t.candles.quantile(.9):.0f} candle")
    print("\n5 trade terakhir:")
    print(t.tail(5)[["time", "side", "entry", "collect", "sl", "result", "pnl"]].to_string(index=False, float_format=lambda x: f"{x:.2f}"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tf", default="1h", choices=["15m", "1h"])
    ap.add_argument("--period", help="default: 730d (1h) / 60d (15m)")
    ap.add_argument("--symbol", default="GC=F")
    ap.add_argument("--csv")
    ap.add_argument("--htf", default="4h")
    ap.add_argument("--sl", type=float, default=3.0, help="SL x ATR")
    ap.add_argument("--tp", type=float, default=0.5, help="COLLECT x ATR")
    ap.add_argument("--cost", type=float, default=0.30, help="spread + komisen ($ per oz)")
    ap.add_argument("--no-buy", action="store_true")
    ap.add_argument("--no-sell", action="store_true")
    a = ap.parse_args()
    a.period = a.period or ("730d" if a.tf == "1h" else "60d")

    df = load(a)
    print(f"Data {a.tf}: {len(df)} candle, {df.index[0]:%Y-%m-%d} -> {df.index[-1]:%Y-%m-%d}\n")
    report(run(df, a))
