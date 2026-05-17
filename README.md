# 🤖 SMC Trading Bot v4

Bot trading otomatis berbasis **Smart Money Concepts (SMC)** untuk Bybit Futures (USDT Perpetual).

---

## 📐 Strategi

```
BOS H1 → EMA50 Filter → FVG Touch → IDM M5 → BOS/Sweep M5 → MSS → Entry
```

**Risk Management:**
- Risk per trade: **1% dari balance** (compound — tiap trade risk ikut balance live)
- TP: **3R** (3× jarak SL dari entry)
- Leverage: otomatis sesuai limit coin, maks 10×

---

## 📊 Hasil Backtest — Full Year 2025

> Modal $10 | Risk 1%/trade compound (1 pot bersama) | TP 3R | ATR Filter Adaptif
> _22 Coin | Data Bybit Perpetual USDT | M5+H1 | Jan–Des 2025_
> _(Generated: 2026-05-17)_

### Per Coin (diurutkan PnL terbesar)

| Coin | Trade | WR% | PnL ($) | ROI% | MaxDD% | PF | ATR P25 |
|------|------:|----:|--------:|-----:|-------:|---:|--------:|
| PENGUUSDT | 60 | 53% | +$3967.71 | +39677% | 7.6% | 2.81 | 0.0040 |
| USUALUSDT | 50 | 42% | +$3190.72 | +31907% | 8.2% | 1.81 | 0.0034 |
| DOGEUSDT | 34 | 56% | +$2550.20 | +25502% | 5.7% | 3.17 | 0.0024 |
| VIRTUALUSDT | 58 | 48% | +$2332.43 | +23324% | 5.5% | 2.27 | 0.0040 |
| 1000BONKUSDT | 57 | 58% | +$2237.77 | +22378% | 3.6% | 3.02 | 0.0035 |
| SHIB1000USDT | 35 | 43% | +$2089.62 | +20896% | 8.9% | 1.81 | 0.0020 |
| NEARUSDT | 44 | 45% | +$2088.24 | +20882% | 5.1% | 2.05 | 0.0029 |
| EIGENUSDT | 55 | 42% | +$1631.44 | +16314% | 12.1% | 1.82 | 0.0037 |
| XVGUSDT | 46 | 43% | +$1532.66 | +15327% | 5.7% | 1.90 | 0.0030 |
| ARBUSDT | 43 | 44% | +$1411.16 | +14112% | 6.6% | 1.89 | 0.0028 |
| PNUTUSDT | 60 | 55% | +$1395.34 | +13953% | 7.8% | 2.88 | 0.0036 |
| STORJUSDT | 30 | 43% | +$1269.14 | +12691% | 3.9% | 1.83 | 0.0017 |
| BERAUSDT | 51 | 45% | +$1255.92 | +12559% | 3.5% | 1.96 | 0.0032 |
| 1000PEPEUSDT | 58 | 41% | +$1107.84 | +11078% | 7.5% | 1.72 | 0.0031 |
| BELUSDT | 38 | 37% | +$1058.40 | +10584% | 5.1% | 1.44 | 0.0024 |
| ADAUSDT | 30 | 40% | +$772.22 | +7722% | 5.3% | 1.58 | 0.0025 |
| ONDOUSDT | 41 | 39% | +$298.28 | +2983% | 5.7% | 1.54 | 0.0027 |
| LINKUSDT | 32 | 41% | +$285.04 | +2850% | 4.6% | 1.63 | 0.0025 |
| WIFUSDT | 74 | 43% | +$207.96 | +2080% | 7.5% | 1.78 | 0.0038 |
| ORCAUSDT | 36 | 36% | +$99.21 | +992% | 10.9% | 1.39 | 0.0024 |
| ENAUSDT | 70 | 37% | +$0.46 | +5% | 6.9% | 1.43 | 0.0039 |
| AVAXUSDT | 33 | 48% | $-104.71 | -1047% | 6.3% | 2.15 | 0.0025 |
| **TOTAL** | **1035** | **45%** | **+$30677.08** | **+306771%** | — | **293.99** | — |


**$10.00 → $30687.08 dalam setahun (+306771% ROI)**

### Per Kuartal

| Kuartal | Trade | WR% | PnL | ROI Kuartal | Bal Awal → Akhir |
|---------|------:|----:|----:|:-----------:|:----------------:|
| Q1 | 270 | 40% | +$39.72 | +397.2% | $10.00 → $49.72 |
| Q2 | 279 | 54% | +$1095.92 | +2204.2% | $49.72 → $1145.64 |
| Q3 | 244 | 43% | +$4922.37 | +429.7% | $1145.64 → $6068.01 |
| Q4 | 242 | 42% | +$24619.07 | +405.7% | $6068.01 → $30687.08 |

### Konfigurasi

| Parameter | Nilai |
|-----------|-------|
| Modal Awal | $10 |
| Risk per Trade | 1% balance (compound) |
| TP | 3R |
| Leverage | maks 10× |
| Fee | 0.055%/sisi (Bybit taker) |
| ATR Filter | P25 per coin |
| Min RR | 2.8 |
| Min SL distance | 0.5% |

---

## ⚙️ Daftar Coin (22 coin aktif)

```python
SYMBOLS = ['XVGUSDT', 'BELUSDT', '1000BONKUSDT', 'BERAUSDT', 'USUALUSDT', '1000PEPEUSDT', 'WIFUSDT', 'PENGUUSDT', 'PNUTUSDT', 'AVAXUSDT', 'ONDOUSDT', 'EIGENUSDT', 'LINKUSDT', 'VIRTUALUSDT', 'ORCAUSDT', 'DOGEUSDT', 'ARBUSDT', 'NEARUSDT', 'STORJUSDT', 'ENAUSDT', 'ADAUSDT', 'SHIB1000USDT']
```

## Catatan

Ini adalah backtest **khusus coin yang sebelumnya dibuang**, diuji ulang dengan strategi **Recursive IDM**
(IDM#1 → mandatory BOS → IDM#2 dalam BOS → WAIT_MSS → entry atau BOS lagi).

| Coin | Alasan Dibuang (strategi lama) |
|------|-------------------------------|
| DOGEUSDT | WR 46%, PF 2.02 — dianggap lemah |
| 1000FLOKIUSDT | WR 45.8%, PF 1.92 — borderline |
| ENAUSDT | Bearish 3/4 kuartal, choppy |
| INJUSDT | WR 40.7%, PF 1.62 |
| ICPUSDT | Hanya 9 trade/tahun |
| ARBUSDT | WR 40%, PF 1.57 |
| TONUSDT | PF 0.82 (losing) |
| ADAUSDT | 9 trade/tahun |
| STORJUSDT | 5 trade/tahun |
| NEARUSDT | WR 44% |
| SHIB1000USDT | Ditest di run ini dengan symbol yang benar |

---

## 🚀 Deploy ke Railway

Set environment variables:

| Variable | Keterangan |
|----------|-----------|
| `API_KEY` | Bybit API Key (permission: Trade + Read) |
| `API_SECRET` | Bybit API Secret |
| `TESTNET` | `true` untuk testnet, default `false` |

Log monitoring: `https://<project>.up.railway.app/logs`

---

> ⚠️ Hasil backtest tidak menjamin performa di masa depan. Trading crypto mengandung risiko tinggi.
