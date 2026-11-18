# Izzul Gold System (XAUUSD)

A single-page website (`index.html`) that shows XAUUSD signals: Entry, Stop Loss, TP1/TP2/TP3, bias strength, a lot calculator and a backtest.

## Running it
- **On your computer:** double-click `index.html` to open it in your browser (an internet connection is needed for the price data).
- **Live on the internet (free):**
  - **GitHub Pages:** repo Settings → Pages → Source: *Deploy from a branch* → choose the branch & folder, then open `.../xauusd-system/`.
  - **Netlify Drop:** drag the `xauusd-system` folder to https://app.netlify.com/drop.

## Data
- Candles: Binance `PAXGUSDT` (backup: OKX `XAUT-USDT`), adjusted to the XAU spot price from gold-api.com.
- Refreshes automatically every 30 seconds. Signals are confirmed only when a candle closes.

## Rules
See the "Cara Sistem Ini Berfungsi" section on the page. This is not financial advice.
