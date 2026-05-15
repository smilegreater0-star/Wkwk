# 🤖 SMC Trading Bot v4

Bot trading otomatis berbasis **Smart Money Concepts (SMC)** untuk Bybit Futures (USDT Perpetual).  
Deploy di [Railway](https://railway.app) — tinggal isi API key, langsung jalan.

---

## 📐 Strategi

Bot mengikuti alur SMC multi-timeframe secara otomatis:

```
BOS H1  →  EMA50 Filter  →  FVG Touch  →  IDM M5  →  BOS/Sweep M5  →  MSS  →  Entry
```

| Langkah | Keterangan |
|---------|-----------|
| **BOS H1** | Deteksi Break of Structure di timeframe 1 jam sebagai bias arah |
| **EMA50 Filter** | Harga harus di atas EMA50 (Long) atau di bawah (Short) |
| **FVG** | Fair Value Gap H1 sebagai zona pullback |
| **IDM M5** | Inducement M5 — konfirmasi likuiditas diambil |
| **BOS/Sweep M5** | Konfirmasi pergerakan M5 setelah IDM |
| **MSS** | Market Structure Shift — sinyal entry final |
| **Entry** | Breaker Block (prioritas) atau FVG fallback |

**Risk Management:**
- Risk per trade: **1% dari balance**
- TP: **3R** (3× jarak SL)
- Leverage: maks 10×, otomatis sesuai limit coin
- SL: ujung candle MSS atau Breaker Block

---

## 🚀 Deploy ke Railway

### 1. Fork / Clone repo ini

```bash
git clone https://github.com/username/bot-smc.git
cd bot-smc
```

### 2. Buat project baru di Railway

1. Buka [railway.app](https://railway.app) → **New Project**
2. Pilih **Deploy from GitHub repo**
3. Pilih repo ini

### 3. Set Environment Variables

Di Railway dashboard → **Variables**, tambahkan:

| Variable | Wajib | Contoh | Keterangan |
|----------|:-----:|--------|-----------|
| `API_KEY` | ✅ | `xxxxxxxxxxxx` | Bybit API Key |
| `API_SECRET` | ✅ | `xxxxxxxxxxxx` | Bybit API Secret |
| `TESTNET` | ❌ | `false` | `true` untuk Bybit Testnet, default `false` |

> ⚠️ **Pastikan API Key Bybit punya permission: `Trade` dan `Read`**  
> Tidak perlu permission Withdraw.

### 4. Deploy

Railway otomatis deploy saat push ke GitHub.  
Bot berjalan sebagai **worker** (bukan web server), sesuai `Procfile`.

---

## 📊 Monitoring Log

Bot punya built-in log server. Akses via:

```
https://<nama-project>.up.railway.app/logs
```

Menampilkan 200 baris log terakhir secara real-time (refresh manual).

---

## ⚙️ Konfigurasi Coin

Daftar coin yang dipantau bot ada di `bott_v4.py` baris 77:

```python
SYMBOLS = [
    'XVGUSDT', 'BELUSDT', 'TAOUSDT', '1000BONKUSDT', 'BERAUSDT',
    'ENAUSDT', 'DOGEUSDT', 'USUALUSDT',
    'FARTCOINUSDT', '1000PEPEUSDT',
]
```

Tambah atau hapus coin sesuai kebutuhan, lalu push ke GitHub — Railway otomatis redeploy.

---

## 📦 Dependencies

```
pandas
numpy
pybit
```

---

## 📈 Hasil Backtest

**10 Coin | Jan–Jun 2025 | Modal $30 | Risk 1%/trade | TP 3R**

| Metrik | Nilai |
|--------|------:|
| Total Trade | 34 |
| Win Rate | 55.9% |
| Total PnL | +$11.84 |
| ROI | +39.5% |
| Profit Factor | 3.25 |
| Expectancy | +$0.35/trade |
| Max Drawdown | 4.4% |

| Coin | Trade | WR% | PnL |
|------|------:|----:|----:|
| FARTCOINUSDT | 10 | 80% | +$6.92 |
| TAOUSDT | 4 | 50% | +$0.99 |
| BELUSDT | 3 | 67% | +$1.40 |
| ENAUSDT | 4 | 50% | +$0.97 |
| 1000PEPEUSDT | 4 | 50% | +$1.04 |
| XVGUSDT | 1 | 100% | +$0.86 |
| USUALUSDT | 2 | 50% | +$0.46 |
| 1000BONKUSDT | 4 | 25% | -$0.15 |
| DASHUSDT | 1 | 0% | -$0.35 |
| DOGEUSDT | 1 | 0% | -$0.31 |

---

## ⚠️ Disclaimer

Bot ini dibuat untuk keperluan pribadi. Trading crypto mengandung risiko tinggi.  
Gunakan dengan bijak dan hanya dengan modal yang siap hilang.
