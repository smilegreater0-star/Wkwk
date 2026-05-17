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
| PENGUUSDT | 45 | 56% | +$720.96 | +7210% | 4.5% | 3.00 | 0.0040 |
| BERAUSDT | 43 | 53% | +$600.27 | +6003% | 4.1% | 2.83 | 0.0032 |
| VIRTUALUSDT | 46 | 50% | +$587.61 | +5876% | 5.6% | 2.44 | 0.0040 |
| EIGENUSDT | 45 | 44% | +$550.84 | +5508% | 10.3% | 2.05 | 0.0037 |
| WIFUSDT | 57 | 33% | +$541.22 | +5412% | 10.5% | 1.24 | 0.0038 |
| 1000PEPEUSDT | 43 | 40% | +$434.69 | +4347% | 5.0% | 1.63 | 0.0031 |
| USUALUSDT | 45 | 42% | +$374.54 | +3745% | 7.8% | 1.77 | 0.0034 |
| NEARUSDT | 38 | 47% | +$371.54 | +3715% | 5.7% | 2.16 | 0.0029 |
| DOGEUSDT | 30 | 47% | +$348.75 | +3487% | 3.5% | 2.12 | 0.0024 |
| BELUSDT | 38 | 42% | +$305.05 | +3051% | 6.7% | 1.80 | 0.0024 |
| ENAUSDT | 55 | 44% | +$304.96 | +3050% | 9.1% | 1.87 | 0.0039 |
| SHIB1000USDT | 21 | 43% | +$244.30 | +2443% | 5.2% | 1.80 | 0.0020 |
| 1000BONKUSDT | 44 | 59% | +$227.84 | +2278% | 4.0% | 3.18 | 0.0035 |
| PNUTUSDT | 48 | 50% | +$214.58 | +2146% | 6.7% | 2.31 | 0.0036 |
| ADAUSDT | 27 | 41% | +$172.40 | +1724% | 4.5% | 1.62 | 0.0025 |
| ONDOUSDT | 30 | 50% | +$149.07 | +1491% | 5.4% | 2.41 | 0.0027 |
| STORJUSDT | 23 | 52% | +$111.25 | +1112% | 2.3% | 2.53 | 0.0017 |
| ARBUSDT | 33 | 36% | +$49.93 | +499% | 6.7% | 1.38 | 0.0028 |
| LINKUSDT | 21 | 43% | +$30.11 | +301% | 4.6% | 1.80 | 0.0025 |
| XVGUSDT | 30 | 40% | $-0.22 | -2% | 6.4% | 1.61 | 0.0030 |
| AVAXUSDT | 32 | 44% | $-49.59 | -496% | 8.8% | 1.79 | 0.0025 |
| ORCAUSDT | 24 | 33% | $-72.22 | -722% | 5.6% | 1.21 | 0.0024 |
| **TOTAL** | **818** | **45%** | **+$6217.88** | **+62179%** | — | **51.95** | — |


**$10.00 → $6227.88 dalam setahun (+62179% ROI)**

### Analisis Win/Loss per Coin

> Format: Direction · Entry Type · IDM depth · MSS body · Volume ratio

| Coin | ✅ Win (pola rata-rata) | ❌ Loss (pola rata-rata) | 💡 Insight |
|------|------------------------|-------------------------|------------|
| PENGUUSDT | Long 52% · BB 100% · IDM 0.2× · Body 70% · Vol 1.4× | Long 60% · BB 100% · IDM 0.1× · Body 69% · Vol 1.0× | Volume MSS lebih tinggi saat win (1.4× vs 1.0×) |
| BERAUSDT | Short 70% · BB 100% · IDM 0.3× · Body 63% · Vol 1.7× | Short 55% · BB 100% · IDM 0.5× · Body 70% · Vol 1.2× | Volume MSS lebih tinggi saat win (1.7× vs 1.2×) |
| VIRTUALUSDT | Short 57% · BB 100% · IDM 0.2× · Body 64% · Vol 1.3× | Long 61% · BB 100% · IDM 0.2× · Body 73% · Vol 1.2× | Tidak ada pola dominan |
| EIGENUSDT | Long 55% · BB 100% · IDM 0.1× · Body 73% · Vol 1.4× | Short 56% · BB 100% · IDM 0.2× · Body 69% · Vol 1.2× | Tidak ada pola dominan |
| WIFUSDT | Long 53% · BB 100% · IDM 0.3× · Body 72% · Vol 1.4× | Long 50% · BB 100% · IDM 0.3× · Body 62% · Vol 1.0× | MSS body kuat (72% vs 62%) · Volume MSS lebih tinggi saat win (1.4× vs 1.0×) |
| 1000PEPEUSDT | Long 53% · BB 100% · IDM 0.6× · Body 68% · Vol 1.1× | Long 65% · BB 100% · IDM 0.2× · Body 61% · Vol 1.2× | Setup lebih dalam prediktif (IDM 0.6×) · MSS body kuat (68% vs 61%) |
| USUALUSDT | Long 63% · BB 100% · IDM 0.2× · Body 74% · Vol 1.3× | Short 65% · BB 100% · IDM 0.0× · Body 75% · Vol 1.2× | Long lebih baik (63% vs 35%) |
| NEARUSDT | Long 67% · BB 100% · IDM 0.3× · Body 66% · Vol 1.2× | Long 55% · BB 100% · IDM 0.6× · Body 62% · Vol 1.0× | Setup cepat lebih baik (IDM 0.3×) |
| DOGEUSDT | Long 57% · BB 100% · IDM 0.2× · Body 70% · Vol 1.4× | Long 62% · BB 100% · IDM 0.2× · Body 69% · Vol 1.7× | Tidak ada pola dominan |
| BELUSDT | Long 50% · BB 100% · IDM 0.1× · Body 75% · Vol 1.6× | Short 55% · BB 100% · IDM 0.3× · Body 74% · Vol 1.3× | Volume MSS lebih tinggi saat win (1.6× vs 1.3×) |
| ENAUSDT | Short 58% · BB 100% · IDM 0.3× · Body 66% · Vol 1.1× | Long 65% · BB 100% · IDM 0.5× · Body 62% · Vol 1.0× | Short lebih baik (58% vs 35%) |
| SHIB1000USDT | Long 56% · BB 100% · IDM 0.3× · Body 68% · Vol 1.1× | Long 58% · BB 100% · IDM 0.2× · Body 62% · Vol 1.0× | MSS body kuat (68% vs 62%) |
| 1000BONKUSDT | Long 69% · BB 100% · IDM 0.2× · Body 66% · Vol 1.4× | Long 50% · BB 100% · IDM 0.2× · Body 59% · Vol 1.0× | MSS body kuat (66% vs 59%) · Volume MSS lebih tinggi saat win (1.4× vs 1.0×) |
| PNUTUSDT | Long 50% · BB 100% · IDM 0.7× · Body 67% · Vol 1.3× | Long 71% · BB 100% · IDM 0.3× · Body 66% · Vol 0.9× | Short lebih baik (50% vs 29%) · Setup lebih dalam prediktif (IDM 0.7×) · Volume MSS lebih tinggi saat win (1.3× vs 0.9×) |
| ADAUSDT | Long 55% · BB 100% · IDM 0.1× · Body 53% · Vol 1.1× | Long 56% · BB 100% · IDM 0.3× · Body 66% · Vol 1.0× | Tidak ada pola dominan |
| ONDOUSDT | Long 60% · BB 100% · IDM 0.2× · Body 68% · Vol 1.3× | Long 53% · BB 100% · IDM 0.3× · Body 77% · Vol 1.3× | Tidak ada pola dominan |
| STORJUSDT | Long 50% · BB 100% · IDM 0.6× · Body 74% · Vol 1.8× | Long 82% · BB 100% · IDM 0.0× · Body 61% · Vol 1.7× | Short lebih baik (50% vs 18%) · Setup lebih dalam prediktif (IDM 0.6×) · MSS body kuat (74% vs 61%) |
| ARBUSDT | Short 67% · BB 100% · IDM 0.3× · Body 74% · Vol 1.4× | Long 67% · BB 100% · IDM 0.2× · Body 67% · Vol 1.1× | Short lebih baik (67% vs 33%) · MSS body kuat (74% vs 67%) |
| LINKUSDT | Long 56% · BB 100% · IDM 0.4× · Body 55% · Vol 1.1× | Long 75% · BB 100% · IDM 0.3× · Body 61% · Vol 1.0× | Tidak ada pola dominan |
| XVGUSDT | Long 58% · BB 100% · IDM 0.2× · Body 74% · Vol 2.2× | Short 56% · BB 100% · IDM 0.2× · Body 75% · Vol 1.4× | Volume MSS lebih tinggi saat win (2.2× vs 1.4×) |
| AVAXUSDT | Short 57% · BB 100% · IDM 0.1× · Body 71% · Vol 1.4× | Long 56% · BB 100% · IDM 0.2× · Body 72% · Vol 1.1× | Tidak ada pola dominan |
| ORCAUSDT | Long 50% · BB 100% · IDM 0.6× · Body 70% · Vol 1.7× | Short 62% · BB 100% · IDM 0.4× · Body 83% · Vol 1.1× | Volume MSS lebih tinggi saat win (1.7× vs 1.1×) |

### Per Kuartal

| Kuartal | Trade | WR% | PnL | ROI Kuartal | Bal Awal → Akhir |
|---------|------:|----:|----:|:-----------:|:----------------:|
| Q1 | 230 | 42% | +$34.41 | +344.1% | $10.00 → $44.41 |
| Q2 | 207 | 54% | +$423.97 | +954.7% | $44.41 → $468.38 |
| Q3 | 184 | 40% | +$913.36 | +195.0% | $468.38 → $1381.75 |
| Q4 | 197 | 45% | +$4846.13 | +350.7% | $1381.75 → $6227.88 |

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

Strategi: **Recursive IDM** (IDM#1 → mandatory BOS → IDM#2 dalam BOS → WAIT_MSS → entry atau BOS lagi).
Filter FVG-CHOCH aktif: FVG harus sepenuhnya di atas CHOCH level (Long) / di bawah CHOCH (Short).

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
