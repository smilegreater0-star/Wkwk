# 🤖 SMC Trading Bot v4

Bot trading otomatis berbasis **Smart Money Concepts (SMC)** untuk Bybit Futures (USDT Perpetual).

---

## 📐 Strategi

```
BOS H1 → FVG Kuat (C3 vol > avg20H, 3 candle warna sama) → OCL Touch M5
  → Entry limit di C1.close (SBR/RBS demand/supply zone)
  → SL di C1.low/C1.high + 10% buffer → Trail stop 0.15× dist → Reverse 2×
```

**Risk Management:**
- Risk per trade: **1% dari balance** (compound — tiap trade risk ikut balance live)
- Exit: **trailing stop** 0.15× dist (tidak ada fixed TP — exit mengikuti harga)
- Reverse: Long→SL→Short→SL→Long (max 2 kali reverse per setup)
- Leverage: otomatis sesuai limit coin, maks 10×

---

## 📊 Hasil Backtest — Jan 2025–Apr 2026

> Modal $10 | Risk 1%/trade compound (1 pot bersama) | TP 3R | ATR Filter Adaptif
> _23 Coin | Data Bybit Perpetual USDT | M5+H1 | Jan 2025–Apr 2026_
> _(Generated: 2026-05-21)_

### Per Coin (diurutkan PnL terbesar)

| Coin | Trade | WR% | PnL ($) | ROI% | MaxDD% | PF | ATR P25 |
|------|------:|----:|--------:|-----:|-------:|---:|--------:|
| DOTUSDT | 185 | 60% | +$10831.63 | +108316% | 7.4% | 1.30 | 0.0023 |
| XVGUSDT | 152 | 61% | +$10355.67 | +103557% | 5.9% | 1.39 | 0.0028 |
| RUNEUSDT | 227 | 53% | +$9579.87 | +95799% | 18.1% | 1.01 | 0.0020 |
| PNUTUSDT | 202 | 58% | +$9114.83 | +91148% | 9.2% | 1.40 | 0.0032 |
| ARBUSDT | 160 | 51% | +$7394.99 | +73950% | 20.9% | 0.95 | 0.0027 |
| OPUSDT | 213 | 53% | +$7036.43 | +70364% | 18.4% | 1.02 | 0.0028 |
| APEUSDT | 187 | 56% | +$5048.81 | +50488% | 12.8% | 1.17 | 0.0024 |
| SEIUSDT | 176 | 53% | +$4932.86 | +49329% | 14.1% | 0.97 | 0.0025 |
| JUPUSDT | 191 | 52% | +$4504.84 | +45048% | 13.1% | 1.04 | 0.0028 |
| EIGENUSDT | 206 | 58% | +$4335.53 | +43355% | 9.1% | 1.45 | 0.0033 |
| VIRTUALUSDT | 235 | 60% | +$4133.68 | +41337% | 6.3% | 1.50 | 0.0036 |
| ONDOUSDT | 199 | 53% | +$3431.91 | +34319% | 12.6% | 1.09 | 0.0025 |
| STXUSDT | 179 | 59% | +$3028.72 | +30287% | 6.6% | 1.29 | 0.0023 |
| 1000PEPEUSDT | 208 | 58% | +$2661.63 | +26616% | 11.4% | 1.22 | 0.0029 |
| BELUSDT | 156 | 58% | +$1409.12 | +14091% | 9.0% | 1.53 | 0.0021 |
| ALGOUSDT | 225 | 55% | +$1396.29 | +13963% | 8.0% | 1.10 | 0.0023 |
| ENAUSDT | 214 | 56% | +$1357.34 | +13573% | 13.0% | 1.14 | 0.0035 |
| BERAUSDT | 182 | 54% | +$732.70 | +7327% | 13.2% | 0.99 | 0.0031 |
| SHIB1000USDT | 184 | 56% | +$679.98 | +6800% | 10.6% | 1.07 | 0.0019 |
| ATOMUSDT | 214 | 52% | +$113.41 | +1134% | 22.6% | 0.87 | 0.0020 |
| LDOUSDT | 173 | 58% | $-450.74 | -4507% | 8.3% | 1.39 | 0.0028 |
| 1000FLOKIUSDT | 172 | 49% | $-2240.56 | -22406% | 16.1% | 0.90 | 0.0027 |
| 1000BONKUSDT | 171 | 53% | $-2355.42 | -23554% | 11.6% | 1.00 | 0.0031 |
| **TOTAL** | **4411** | **55%** | **+$87033.51** | **+870335%** | — | **18.25** | — |


**$10.00 → $87043.51 dalam setahun (+870335% ROI)**

### Analisis Win/Loss per Coin

> Format: Direction · Vol C3 (FVG strength) · Gap size · Sesi dominan

| Coin | ✅ Win (pola rata-rata) | ❌ Loss (pola rata-rata) | 💡 Insight |
|------|------------------------|-------------------------|------------|
| **TOTAL** | **Short 51% · C3 2.2× · Tch 5.5× · Gap 0.79% · London** | **Long 51% · C3 2.2× · Tch 4.9× · Gap 0.80% · London** | **Vol sentuh SBR lebih besar saat win (5.5× vs 4.9×) · 38% loss = CHOCH nyata · 62% loss = drift (konsolidasi/ambiguous)** |
| DOTUSDT | Short 54% · C3 2.0× · Tch 4.4× · Gap 0.49% · NY | Short 51% · C3 2.0× · Tch 4.0× · Gap 0.57% · NY | Vol sentuh SBR lebih besar saat win (4.4× vs 4.0×) · FVG lebih kecil saat win (0.49% vs 0.57%) · 39% loss = CHOCH nyata · 61% loss = drift (konsolidasi/ambiguous) |
| XVGUSDT | Short 52% · C3 2.7× · Tch 7.9× · Gap 0.90% · London | Long 53% · C3 4.0× · Tch 5.2× · Gap 1.15% · London | Vol C3 justru lebih lemah saat win (2.7× vs 4.0×) · Vol sentuh SBR lebih besar saat win (7.9× vs 5.2×) · FVG lebih kecil saat win (0.90% vs 1.15%) · 35% loss = CHOCH nyata · 65% loss = drift (konsolidasi/ambiguous) |
| RUNEUSDT | Long 50% · C3 2.2× · Tch 7.3× · Gap 0.65% · London | Long 50% · C3 2.1× · Tch 6.0× · Gap 0.76% · London | Vol sentuh SBR lebih besar saat win (7.3× vs 6.0×) · FVG lebih kecil saat win (0.65% vs 0.76%) · 30% loss = CHOCH nyata · 70% loss = drift (konsolidasi/ambiguous) |
| PNUTUSDT | Short 51% · C3 2.5× · Tch 4.5× · Gap 1.00% · London | Short 59% · C3 2.2× · Tch 5.1× · Gap 1.13% · NY | Vol C3 lebih kuat saat win (2.5× vs 2.2×) · Vol sentuh SBR lebih kecil saat win (4.5× vs 5.1×) · FVG lebih kecil saat win (1.00% vs 1.13%) · Win dominan sesi London (loss: NY) · 38% loss = CHOCH nyata · 62% loss = drift (konsolidasi/ambiguous) |
| ARBUSDT | Short 56% · C3 2.3× · Tch 3.9× · Gap 0.75% · London | Long 57% · C3 2.4× · Tch 4.2× · Gap 0.73% · London | 33% loss = CHOCH nyata · 67% loss = drift (konsolidasi/ambiguous) |
| OPUSDT | Long 50% · C3 1.9× · Tch 4.0× · Gap 0.63% · London | Long 54% · C3 2.0× · Tch 4.3× · Gap 0.66% · London | 41% loss = CHOCH nyata · 59% loss = drift (konsolidasi/ambiguous) |
| APEUSDT | Short 56% · C3 2.4× · Tch 5.4× · Gap 0.70% · NY | Long 57% · C3 2.2× · Tch 3.9× · Gap 0.56% · London | Vol sentuh SBR lebih besar saat win (5.4× vs 3.9×) · FVG lebih besar saat win (0.70% vs 0.56%) · Win dominan sesi NY (loss: London) · 43% loss = CHOCH nyata · 57% loss = drift (konsolidasi/ambiguous) |
| SEIUSDT | Long 50% · C3 2.1× · Tch 3.8× · Gap 0.60% · Asia | Long 56% · C3 1.9× · Tch 3.9× · Gap 0.75% · London | FVG lebih kecil saat win (0.60% vs 0.75%) · Win dominan sesi Asia (loss: London) · 44% loss = CHOCH nyata · 56% loss = drift (konsolidasi/ambiguous) |
| JUPUSDT | Short 52% · C3 1.9× · Tch 5.8× · Gap 0.83% · London | Short 52% · C3 2.1× · Tch 5.2× · Gap 0.76% · Asia | Vol sentuh SBR lebih besar saat win (5.8× vs 5.2×) · FVG lebih besar saat win (0.83% vs 0.76%) · Win dominan sesi London (loss: Asia) · 42% loss = CHOCH nyata · 58% loss = drift (konsolidasi/ambiguous) |
| EIGENUSDT | Short 51% · C3 2.0× · Tch 5.2× · Gap 1.19% · London | Short 51% · C3 1.8× · Tch 5.3× · Gap 0.94% · London | FVG lebih besar saat win (1.19% vs 0.94%) · 41% loss = CHOCH nyata · 59% loss = drift (konsolidasi/ambiguous) |
| VIRTUALUSDT | Short 53% · C3 1.9× · Tch 5.9× · Gap 1.04% · Asia | Long 52% · C3 1.8× · Tch 4.2× · Gap 0.98% · London | Vol sentuh SBR lebih besar saat win (5.9× vs 4.2×) · FVG lebih besar saat win (1.04% vs 0.98%) · Win dominan sesi Asia (loss: London) · 35% loss = CHOCH nyata · 65% loss = drift (konsolidasi/ambiguous) |
| ONDOUSDT | Long 54% · C3 2.0× · Tch 8.4× · Gap 0.67% · London | Short 61% · C3 1.9× · Tch 7.0× · Gap 0.54% · London | Vol sentuh SBR lebih besar saat win (8.4× vs 7.0×) · FVG lebih besar saat win (0.67% vs 0.54%) · 39% loss = CHOCH nyata · 61% loss = drift (konsolidasi/ambiguous) |
| STXUSDT | Short 50% · C3 2.2× · Tch 8.8× · Gap 0.78% · London | Short 53% · C3 2.3× · Tch 7.8× · Gap 0.76% · London | Vol sentuh SBR lebih besar saat win (8.8× vs 7.8×) · 36% loss = CHOCH nyata · 64% loss = drift (konsolidasi/ambiguous) |
| 1000PEPEUSDT | Short 53% · C3 2.1× · Tch 4.0× · Gap 0.68% · NY | Long 52% · C3 2.1× · Tch 3.9× · Gap 0.90% · NY | FVG lebih kecil saat win (0.68% vs 0.90%) · 33% loss = CHOCH nyata · 67% loss = drift (konsolidasi/ambiguous) |
| BELUSDT | Long 53% · C3 4.6× · Tch 9.3× · Gap 0.50% · Asia | Short 56% · C3 4.9× · Tch 9.5× · Gap 0.74% · London | Vol C3 justru lebih lemah saat win (4.6× vs 4.9×) · FVG lebih kecil saat win (0.50% vs 0.74%) · Win dominan sesi Asia (loss: London) · 27% loss = CHOCH nyata · 73% loss = drift (konsolidasi/ambiguous) |
| ALGOUSDT | Short 54% · C3 2.0× · Tch 5.0× · Gap 0.66% · London | Short 52% · C3 2.4× · Tch 4.1× · Gap 0.67% · NY | Vol C3 justru lebih lemah saat win (2.0× vs 2.4×) · Vol sentuh SBR lebih besar saat win (5.0× vs 4.1×) · Win dominan sesi London (loss: NY) · 37% loss = CHOCH nyata · 63% loss = drift (konsolidasi/ambiguous) |
| ENAUSDT | Short 51% · C3 1.9× · Tch 4.7× · Gap 1.05% · London | Long 55% · C3 2.0× · Tch 5.0× · Gap 1.01% · London | 44% loss = CHOCH nyata · 56% loss = drift (konsolidasi/ambiguous) |
| BERAUSDT | Long 51% · C3 2.4× · Tch 2.8× · Gap 1.16% · London | Short 52% · C3 2.3× · Tch 2.8× · Gap 0.85% · Asia | FVG lebih besar saat win (1.16% vs 0.85%) · Win dominan sesi London (loss: Asia) · 36% loss = CHOCH nyata · 64% loss = drift (konsolidasi/ambiguous) |
| SHIB1000USDT | Short 57% · C3 2.1× · Tch 5.2× · Gap 0.52% · London | Long 55% · C3 2.3× · Tch 4.9× · Gap 0.63% · London | FVG lebih kecil saat win (0.52% vs 0.63%) · 41% loss = CHOCH nyata · 59% loss = drift (konsolidasi/ambiguous) |
| ATOMUSDT | Short 53% · C3 2.1× · Tch 4.2× · Gap 0.56% · London | Long 55% · C3 2.1× · Tch 4.4× · Gap 0.59% · Asia | Win dominan sesi London (loss: Asia) · 41% loss = CHOCH nyata · 59% loss = drift (konsolidasi/ambiguous) |
| LDOUSDT | Short 51% · C3 1.9× · Tch 5.8× · Gap 0.75% · London | Short 56% · C3 2.0× · Tch 3.9× · Gap 0.81% · London | Vol sentuh SBR lebih besar saat win (5.8× vs 3.9×) · FVG lebih kecil saat win (0.75% vs 0.81%) · 34% loss = CHOCH nyata · 66% loss = drift (konsolidasi/ambiguous) |
| 1000FLOKIUSDT | Long 53% · C3 1.7× · Tch 5.1× · Gap 0.80% · London | Long 54% · C3 2.0× · Tch 5.3× · Gap 0.92% · London | Vol C3 justru lebih lemah saat win (1.7× vs 2.0×) · FVG lebih kecil saat win (0.80% vs 0.92%) · 36% loss = CHOCH nyata · 64% loss = drift (konsolidasi/ambiguous) |
| 1000BONKUSDT | Short 51% · C3 2.6× · Tch 4.2× · Gap 1.25% · Asia | Long 53% · C3 1.9× · Tch 4.8× · Gap 1.07% · NY | Vol C3 lebih kuat saat win (2.6× vs 1.9×) · Vol sentuh SBR lebih kecil saat win (4.2× vs 4.8×) · FVG lebih besar saat win (1.25% vs 1.07%) · Win dominan sesi Asia (loss: NY) · 42% loss = CHOCH nyata · 58% loss = drift (konsolidasi/ambiguous) |

### Per Kuartal

| Kuartal | Trade | WR% | PnL | ROI Kuartal | Bal Awal → Akhir |
|---------|------:|----:|----:|:-----------:|:----------------:|
| Q1 2025 | 824 | 56% | +$44.63 | +446.3% | $10.00 → $54.63 |
| Q2 2025 | 867 | 55% | +$150.40 | +275.3% | $54.63 → $205.03 |
| Q3 2025 | 870 | 54% | +$721.91 | +352.1% | $205.03 → $926.94 |
| Q4 2025 | 729 | 56% | +$4137.67 | +446.4% | $926.94 → $5064.61 |
| Q1 2026 | 825 | 56% | +$46137.32 | +911.0% | $5064.61 → $51201.93 |
| Q2 2026 | 296 | 56% | +$35841.59 | +70.0% | $51201.93 → $87043.51 |

### Konfigurasi

| Parameter | Nilai |
|-----------|-------|
| Modal Awal | $10 |
| Risk per Trade | 1% balance (compound) |
| Entry Mode | fvg_sbr (SBR — C1.close) |
| Exit | Trail stop 0.15× dist + Reverse 2× |
| Leverage | maks 10× |
| Fee | 0.055%/sisi (Bybit taker) |
| Touch Vol Min | 0.8× avg20M5 |
| Max Gap | 0.60% dari harga |
| Min SL distance | 0.2% |

---

## ⚙️ Daftar Coin (23 coin aktif)

```python
SYMBOLS = ['XVGUSDT', 'BELUSDT', '1000BONKUSDT', 'BERAUSDT', '1000PEPEUSDT', 'PNUTUSDT', 'ONDOUSDT', 'EIGENUSDT', 'VIRTUALUSDT', 'ARBUSDT', 'ENAUSDT', 'SHIB1000USDT', '1000FLOKIUSDT', 'JUPUSDT', 'DOTUSDT', 'SEIUSDT', 'OPUSDT', 'RUNEUSDT', 'STXUSDT', 'ATOMUSDT', 'APEUSDT', 'LDOUSDT', 'ALGOUSDT']
```

## Catatan

Strategi: **FVG SBR** (BOS H1 → FVG kuat → OCL touch → entry limit di C1.close dengan trailing stop).
Filter aktif: C3 vol > avg20H, CHOCH invalidasi setup, TOUCH_VOL_MIN di fill candle, MAX_GAP_PCT.

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
