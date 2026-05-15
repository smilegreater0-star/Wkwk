# 🤖 SMC Trading Bot v4

Bot trading otomatis berbasis **Smart Money Concepts (SMC)** untuk Bybit Futures (USDT Perpetual).  
Deploy di [Railway](https://railway.app) — tinggal isi API key, langsung jalan.

---

## 📐 Strategi

Bot mengikuti alur SMC multi-timeframe secara otomatis:

```
BOS H1 → EMA50 Filter → FVG Touch → IDM M5 → BOS/Sweep M5 → MSS → Entry
```

| Langkah | Keterangan |
|---------|-----------|
| **BOS H1** | Break of Structure timeframe 1 jam sebagai bias arah |
| **EMA50 Filter** | Harga harus di atas EMA50 (Long) atau di bawah (Short) |
| **FVG H1** | Fair Value Gap sebagai zona pullback |
| **IDM M5** | Inducement M5 — konfirmasi likuiditas diambil |
| **BOS/Sweep M5** | Konfirmasi pergerakan M5 setelah IDM |
| **MSS** | Market Structure Shift — sinyal entry final |
| **Entry** | Breaker Block (prioritas) atau FVG fallback |

**Risk Management:**
- Risk per trade: **1% dari balance**
- TP: **3R** (3× jarak SL dari entry)
- Leverage: otomatis sesuai limit coin, maks 10×
- SL: ujung candle MSS atau Breaker Block

**Pembatalan Setup (CHOCH):**
- BOS Long → harga tembus swing low referensi → setup batal, struktur berganti Short
- BOS Short → harga tembus swing high referensi → setup batal, struktur berganti Long
- Jika harga ke swing high baru tanpa sentuh FVG → BOS tetap valid, tunggu pullback ke FVG terbaru

---

## 📊 Hasil Backtest — Full Year 2025

**8 Coin | Modal $30 | Risk 1%/trade | TP 3R | ATR Filter Adaptif**

| Coin | Trade | W | L | WR% | PnL | ROI% | PF | Max DD% |
|------|------:|--:|--:|----:|----:|-----:|---:|--------:|
| FARTCOINUSDT | 36 | 27 | 9 | 75% | +$28.60 | +95.3% | 7.87 | 2.2% |
| TAOUSDT | 23 | 16 | 7 | 70% | +$13.10 | +43.7% | 5.68 | 2.4% |
| 1000BONKUSDT | 24 | 15 | 9 | 62% | +$11.07 | +36.9% | 3.97 | 3.3% |
| XVGUSDT | 13 | 9 | 4 | 69% | +$6.93 | +23.1% | 5.57 | 2.2% |
| 1000PEPEUSDT | 20 | 11 | 9 | 55% | +$6.62 | +22.1% | 2.95 | 4.5% |
| BELUSDT | 11 | 8 | 3 | 73% | +$6.24 | +20.8% | 6.47 | 2.3% |
| USUALUSDT | 23 | 11 | 12 | 48% | +$5.42 | +18.1% | 2.18 | 3.5% |
| DOGEUSDT | 13 | 6 | 7 | 46% | +$2.59 | +8.6% | 2.02 | 3.5% |
| **TOTAL** | **163** | **103** | **60** | **63%** | **+$80.56** | **+268.5%** | **4.38** | — |

### Statistik Gabungan

| Metrik | Nilai |
|--------|------:|
| Modal Awal | $30.00 |
| Final Balance | **$110.56** |
| Total Trade | 163 |
| Win Rate | **63.2%** |
| Total PnL | **+$80.56** |
| ROI Setahun | **+268.5%** |
| Avg Win / trade | +$1.014 |
| Avg Loss / trade | −$0.398 |
| Profit Factor | **4.38** |
| Expectancy / trade | **+$0.494** |
| Max Consecutive Loss | 4 |

### Long vs Short

| Arah | Trade | WR% | PnL |
|------|------:|----:|----:|
| Long | 76 | 68.4% | +$42.40 |
| Short | 87 | 58.6% | +$38.17 |

### Catatan Coin

- **FARTCOINUSDT** — coin terbaik, 36 trade, WR 75%, PF 7.87. Volatilitas tinggi dan trending sangat cocok dengan strategi SMC.
- **TAOUSDT & BELUSDT** — paling konsisten, MDD rendah (2.3–2.4%), PF tinggi (5.6–6.5).
- **DOGEUSDT & USUALUSDT** — WR di bawah 50% tapi tetap profit karena Avg Win:Avg Loss ratio 2.5:1.
- **ENAUSDT** — dikeluarkan: bearish 3 dari 4 kuartal 2025, ATR tinggi justru choppy (bukan trending).

---

## 🔧 ATR Filter Adaptif

Setiap coin punya threshold ATR minimum berbeda sesuai karakter volatilitasnya:

| Coin | Threshold | Median ATR | Lolos Filter |
|------|:---------:|:----------:|:------------:|
| FARTCOINUSDT | 0.56% | 0.78% | 75% waktu |
| XVGUSDT | 0.30% | 0.42% | 75% waktu |
| 1000PEPEUSDT | 0.31% | 0.41% | 75% waktu |
| DOGEUSDT | 0.24% | 0.33% | 75% waktu |
| Lainnya (default) | 0.35% | — | — |

Filter ini mencegah entry saat market sideways/momentum lemah.

---

## 🚀 Deploy ke Railway

### 1. Clone repo

```bash
git clone https://github.com/username/bot-smc.git
cd bot-smc
```

### 2. Buat project di Railway

1. [railway.app](https://railway.app) → **New Project** → **Deploy from GitHub repo**
2. Pilih repo ini

### 3. Set Environment Variables

| Variable | Wajib | Keterangan |
|----------|:-----:|-----------|
| `API_KEY` | ✅ | Bybit API Key |
| `API_SECRET` | ✅ | Bybit API Secret |
| `TESTNET` | ❌ | `true` untuk Testnet, default `false` |

> ⚠️ API Key Bybit harus punya permission: **Trade** dan **Read**

### 4. Deploy

Railway otomatis deploy saat push ke GitHub. Bot berjalan sebagai **worker**.

---

## 📡 Monitoring Log

```
https://<nama-project>.up.railway.app/logs
```

---

## 📦 Dependencies

```
pandas
numpy
pybit
```

---

## ⚠️ Disclaimer

Bot ini untuk keperluan pribadi. Trading crypto mengandung risiko tinggi.  
Hasil backtest tidak menjamin performa di masa depan.
