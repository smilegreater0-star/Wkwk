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

> Modal $10 | Risk 1%/trade compound (1 pot bersama) | WR 65% | AVG RR 1:1.2
> _35 Coin | Data Bybit Perpetual USDT | M5+H1 | Jan 2025–Apr 2026_
> _(Generated: 2026-05-21)_

### Per Coin (diurutkan PnL terbesar)

| Coin | Trade | WR% | PnL ($) | ROI% | MaxDD% | PF | Avg R:R | ATR P25 |
|------|------:|----:|--------:|-----:|-------:|---:|--------:|--------:|
| JUPUSDT | 66 | 62% | +$10552.66 | +105527% | 4.8% | 1.81 | 1.39:1 | 0.0028 |
| TAOUSDT | 51 | 75% | +$9988.08 | +99881% | 2.1% | 3.13 | 1.29:1 | 0.0031 |
| OPUSDT | 41 | 68% | +$6827.03 | +68270% | 3.4% | 1.80 | 1.05:1 | 0.0028 |
| FLOWUSDT | 66 | 65% | +$6781.50 | +67815% | 2.6% | 2.02 | 1.36:1 | 0.0020 |
| SANDUSDT | 59 | 63% | +$6460.55 | +64605% | 6.7% | 1.47 | 1.11:1 | 0.0022 |
| ENAUSDT | 79 | 72% | +$6010.87 | +60109% | 4.3% | 2.29 | 1.09:1 | 0.0035 |
| ORCAUSDT | 47 | 64% | +$5733.63 | +57336% | 4.3% | 2.56 | 1.72:1 | 0.0021 |
| FARTCOINUSDT | 58 | 62% | +$5568.44 | +55684% | 5.4% | 1.71 | 1.22:1 | 0.0050 |
| XRPUSDT | 68 | 63% | +$5193.23 | +51932% | 3.3% | 1.55 | 1.26:1 | 0.0018 |
| SUIUSDT | 67 | 72% | +$5167.92 | +51679% | 2.8% | 2.65 | 1.35:1 | 0.0026 |
| APEUSDT | 52 | 63% | +$4682.62 | +46826% | 5.0% | 1.79 | 1.34:1 | 0.0024 |
| DYDXUSDT | 51 | 57% | +$4102.26 | +41023% | 6.4% | 1.43 | 1.34:1 | 0.0026 |
| ALGOUSDT | 69 | 65% | +$4002.02 | +40020% | 3.7% | 1.79 | 1.25:1 | 0.0023 |
| TIAUSDT | 53 | 66% | +$3279.23 | +32792% | 6.5% | 1.57 | 1.00:1 | 0.0030 |
| ONDOUSDT | 69 | 55% | +$3257.68 | +32577% | 3.7% | 1.29 | 1.36:1 | 0.0025 |
| XVGUSDT | 48 | 65% | +$3208.88 | +32089% | 4.3% | 1.84 | 1.24:1 | 0.0028 |
| IMXUSDT | 54 | 61% | +$3183.44 | +31834% | 4.8% | 1.51 | 1.17:1 | 0.0028 |
| STXUSDT | 51 | 69% | +$3063.69 | +30637% | 2.1% | 2.03 | 1.21:1 | 0.0023 |
| AAVEUSDT | 34 | 68% | +$3006.34 | +30063% | 2.9% | 2.04 | 1.25:1 | 0.0026 |
| SHIB1000USDT | 54 | 61% | +$2957.84 | +29578% | 7.3% | 1.31 | 1.20:1 | 0.0019 |
| 1000PEPEUSDT | 65 | 63% | +$2789.65 | +27896% | 4.2% | 1.51 | 1.11:1 | 0.0029 |
| ICPUSDT | 64 | 64% | +$2635.55 | +26356% | 5.8% | 1.56 | 1.08:1 | 0.0023 |
| 1000BONKUSDT | 41 | 68% | +$1773.95 | +17739% | 3.2% | 2.06 | 1.17:1 | 0.0031 |
| AXSUSDT | 62 | 63% | +$1614.21 | +16142% | 3.6% | 1.72 | 1.24:1 | 0.0023 |
| XAUTUSDT | 32 | 56% | +$1586.09 | +15861% | 3.6% | 1.26 | 1.77:1 | 0.0003 |
| GALAUSDT | 69 | 67% | +$1581.18 | +15812% | 2.4% | 2.19 | 1.30:1 | 0.0028 |
| SOLUSDT | 69 | 68% | +$1352.10 | +13521% | 2.6% | 2.07 | 1.34:1 | 0.0022 |
| GMXUSDT | 64 | 66% | +$1324.81 | +13248% | 4.1% | 2.51 | 1.75:1 | 0.0020 |
| BERAUSDT | 44 | 61% | +$1095.99 | +10960% | 5.8% | 1.55 | 1.18:1 | 0.0031 |
| BELUSDT | 56 | 62% | +$1072.25 | +10722% | 5.0% | 1.88 | 1.45:1 | 0.0021 |
| LTCUSDT | 55 | 67% | +$908.27 | +9083% | 4.2% | 1.89 | 1.23:1 | 0.0018 |
| VIRTUALUSDT | 69 | 72% | +$495.88 | +4959% | 2.4% | 2.70 | 1.24:1 | 0.0036 |
| HBARUSDT | 59 | 64% | +$246.55 | +2465% | 4.9% | 1.96 | 1.46:1 | 0.0022 |
| SEIUSDT | 60 | 63% | $-23.11 | -231% | 4.9% | 1.45 | 1.05:1 | 0.0025 |
| EIGENUSDT | 54 | 70% | $-2297.54 | -22975% | 5.1% | 2.39 | 1.20:1 | 0.0033 |
| **TOTAL** | **2000** | **65%** | **+$119183.70** | **+1191837%** | — | **52.36** | — |


**$10.00 → $119193.70 dalam setahun (+1191837% ROI)**

### Analisis Win/Loss per Coin

> Format: Direction · Vol C3 (FVG strength) · Gap size · Sesi dominan

| Coin | ✅ Win (pola rata-rata) | ❌ Loss (pola rata-rata) | 💡 Insight |
|------|------------------------|-------------------------|------------|
| **TOTAL** | **Short 52% · C3 2.2× · Tch 11.5× · Gap 0.70% · London** | **Long 52% · C3 2.1× · Tch 6.5× · Gap 0.76% · London** | **Vol sentuh SBR lebih besar saat win (11.5× vs 6.5×) · FVG lebih kecil saat win (0.70% vs 0.76%) · 29% loss = CHOCH nyata · 71% loss = drift (konsolidasi/ambiguous)** |
| JUPUSDT | Short 56% · C3 1.9× · Tch 7.9× · Gap 0.83% · London | Long 52% · C3 2.1× · Tch 6.3× · Gap 0.90% · NY | Vol sentuh SBR lebih besar saat win (7.9× vs 6.3×) · FVG lebih kecil saat win (0.83% vs 0.90%) · Win dominan sesi London (loss: NY) · 32% loss = CHOCH nyata · 68% loss = drift (konsolidasi/ambiguous) |
| TAOUSDT | Long 53% · C3 2.4× · Tch 6.5× · Gap 0.49% · London | Long 54% · C3 2.7× · Tch 8.0× · Gap 0.96% · London | Vol C3 justru lebih lemah saat win (2.4× vs 2.7×) · Vol sentuh SBR lebih kecil saat win (6.5× vs 8.0×) · FVG lebih kecil saat win (0.49% vs 0.96%) · 92% loss = drift (konsolidasi/ambiguous) |
| OPUSDT | Short 57% · C3 2.1× · Tch 3.9× · Gap 0.57% · NY | Long 54% · C3 3.0× · Tch 2.1× · Gap 0.68% · London | Vol C3 justru lebih lemah saat win (2.1× vs 3.0×) · Vol sentuh SBR lebih besar saat win (3.9× vs 2.1×) · FVG lebih kecil saat win (0.57% vs 0.68%) · Win dominan sesi NY (loss: London) · 38% loss = CHOCH nyata · 62% loss = drift (konsolidasi/ambiguous) |
| FLOWUSDT | Short 53% · C3 2.0× · Tch 15.8× · Gap 0.82% · London | Short 52% · C3 2.2× · Tch 10.0× · Gap 0.70% · London | Vol sentuh SBR lebih besar saat win (15.8× vs 10.0×) · FVG lebih besar saat win (0.82% vs 0.70%) · 87% loss = drift (konsolidasi/ambiguous) |
| SANDUSDT | Long 54% · C3 2.2× · Tch 9.9× · Gap 0.56% · London | Short 55% · C3 2.3× · Tch 3.8× · Gap 0.56% · Asia | Vol sentuh SBR lebih besar saat win (9.9× vs 3.8×) · Win dominan sesi London (loss: Asia) · 36% loss = CHOCH nyata · 64% loss = drift (konsolidasi/ambiguous) |
| ENAUSDT | Short 56% · C3 1.8× · Tch 5.8× · Gap 0.52% · London | Long 68% · C3 2.0× · Tch 6.9× · Gap 0.94% · NY | Short lebih baik (56% vs 32%) · Vol sentuh SBR lebih kecil saat win (5.8× vs 6.9×) · FVG lebih kecil saat win (0.52% vs 0.94%) · Win dominan sesi London (loss: NY) · 41% loss = CHOCH nyata · 59% loss = drift (konsolidasi/ambiguous) |
| ORCAUSDT | Long 53% · C3 2.7× · Tch 68.7× · Gap 0.71% · Asia | Short 59% · C3 1.8× · Tch 18.5× · Gap 0.92% · Asia | Vol C3 lebih kuat saat win (2.7× vs 1.8×) · Vol sentuh SBR lebih besar saat win (68.7× vs 18.5×) · FVG lebih kecil saat win (0.71% vs 0.92%) · 29% loss = CHOCH nyata · 71% loss = drift (konsolidasi/ambiguous) |
| FARTCOINUSDT | Short 58% · C3 1.5× · Tch 3.0× · Gap 0.91% · NY | Long 64% · C3 1.4× · Tch 3.8× · Gap 1.17% · NY | Short lebih baik (58% vs 36%) · Vol sentuh SBR lebih kecil saat win (3.0× vs 3.8×) · FVG lebih kecil saat win (0.91% vs 1.17%) · 36% loss = CHOCH nyata · 64% loss = drift (konsolidasi/ambiguous) |
| XRPUSDT | Short 53% · C3 1.7× · Tch 3.0× · Gap 0.44% · London | Short 52% · C3 1.9× · Tch 3.0× · Gap 0.56% · London | FVG lebih kecil saat win (0.44% vs 0.56%) · 76% loss = drift (konsolidasi/ambiguous) |
| SUIUSDT | Short 56% · C3 1.8× · Tch 4.7× · Gap 0.67% · London | Long 53% · C3 1.8× · Tch 2.2× · Gap 0.65% · London | Vol sentuh SBR lebih besar saat win (4.7× vs 2.2×) · 84% loss = drift (konsolidasi/ambiguous) |
| APEUSDT | Short 55% · C3 2.1× · Tch 6.0× · Gap 0.82% · London | Long 68% · C3 2.3× · Tch 3.5× · Gap 0.56% · London | Short lebih baik (55% vs 32%) · Vol sentuh SBR lebih besar saat win (6.0× vs 3.5×) · FVG lebih besar saat win (0.82% vs 0.56%) · 32% loss = CHOCH nyata · 68% loss = drift (konsolidasi/ambiguous) |
| DYDXUSDT | Short 52% · C3 2.3× · Tch 4.3× · Gap 0.91% · NY | Long 59% · C3 2.7× · Tch 4.7× · Gap 1.14% · Asia | Vol C3 justru lebih lemah saat win (2.3× vs 2.7×) · Vol sentuh SBR lebih kecil saat win (4.3× vs 4.7×) · FVG lebih kecil saat win (0.91% vs 1.14%) · Win dominan sesi NY (loss: Asia) · 32% loss = CHOCH nyata · 68% loss = drift (konsolidasi/ambiguous) |
| ALGOUSDT | Short 60% · C3 1.7× · Tch 7.6× · Gap 0.70% · London | Long 67% · C3 2.0× · Tch 5.5× · Gap 0.58% · NY | Short lebih baik (60% vs 33%) · Vol sentuh SBR lebih besar saat win (7.6× vs 5.5×) · FVG lebih besar saat win (0.70% vs 0.58%) · Win dominan sesi London (loss: NY) · 75% loss = drift (konsolidasi/ambiguous) |
| TIAUSDT | Short 51% · C3 1.9× · Tch 6.2× · Gap 0.63% · London | Short 56% · C3 2.0× · Tch 3.8× · Gap 0.78% · NY | Vol sentuh SBR lebih besar saat win (6.2× vs 3.8×) · FVG lebih kecil saat win (0.63% vs 0.78%) · Win dominan sesi London (loss: NY) · 39% loss = CHOCH nyata · 61% loss = drift (konsolidasi/ambiguous) |
| ONDOUSDT | Long 53% · C3 2.2× · Tch 9.9× · Gap 0.68% · NY | Short 52% · C3 1.9× · Tch 8.6× · Gap 0.53% · London | Vol sentuh SBR lebih besar saat win (9.9× vs 8.6×) · FVG lebih besar saat win (0.68% vs 0.53%) · Win dominan sesi NY (loss: London) · 26% loss = CHOCH nyata · 74% loss = drift (konsolidasi/ambiguous) |
| XVGUSDT | Long 55% · C3 2.3× · Tch 17.3× · Gap 0.79% · Asia | Long 53% · C3 3.6× · Tch 10.5× · Gap 0.88% · London | Vol C3 justru lebih lemah saat win (2.3× vs 3.6×) · Vol sentuh SBR lebih besar saat win (17.3× vs 10.5×) · FVG lebih kecil saat win (0.79% vs 0.88%) · Win dominan sesi Asia (loss: London) · 76% loss = drift (konsolidasi/ambiguous) |
| IMXUSDT | Short 58% · C3 2.0× · Tch 22.1× · Gap 0.79% · London | Short 57% · C3 1.8× · Tch 6.5× · Gap 0.71% · Asia | Vol sentuh SBR lebih besar saat win (22.1× vs 6.5×) · FVG lebih besar saat win (0.79% vs 0.71%) · Win dominan sesi London (loss: Asia) · 29% loss = CHOCH nyata · 71% loss = drift (konsolidasi/ambiguous) |
| STXUSDT | Long 51% · C3 1.8× · Tch 3.6× · Gap 0.47% · London | Short 69% · C3 1.7× · Tch 4.2× · Gap 0.57% · London | Long lebih baik (51% vs 31%) · Vol sentuh SBR lebih kecil saat win (3.6× vs 4.2×) · FVG lebih kecil saat win (0.47% vs 0.57%) · 31% loss = CHOCH nyata · 69% loss = drift (konsolidasi/ambiguous) |
| AAVEUSDT | Long 52% · C3 2.1× · Tch 12.6× · Gap 0.75% · NY | Long 64% · C3 2.2× · Tch 7.1× · Gap 0.86% · London | Vol sentuh SBR lebih besar saat win (12.6× vs 7.1×) · FVG lebih kecil saat win (0.75% vs 0.86%) · Win dominan sesi NY (loss: London) · 36% loss = CHOCH nyata · 64% loss = drift (konsolidasi/ambiguous) |
| SHIB1000USDT | Short 58% · C3 2.0× · Tch 5.8× · Gap 0.41% · London | Long 52% · C3 2.0× · Tch 4.2× · Gap 0.52% · London | Vol sentuh SBR lebih besar saat win (5.8× vs 4.2×) · FVG lebih kecil saat win (0.41% vs 0.52%) · 38% loss = CHOCH nyata · 62% loss = drift (konsolidasi/ambiguous) |
| 1000PEPEUSDT | Long 51% · C3 2.4× · Tch 3.5× · Gap 0.66% · London | Short 58% · C3 2.7× · Tch 3.3× · Gap 0.90% · London | Vol C3 justru lebih lemah saat win (2.4× vs 2.7×) · FVG lebih kecil saat win (0.66% vs 0.90%) · 75% loss = drift (konsolidasi/ambiguous) |
| ICPUSDT | Long 61% · C3 2.1× · Tch 8.2× · Gap 0.52% · NY | Short 57% · C3 2.0× · Tch 7.0× · Gap 0.60% · NY | Vol sentuh SBR lebih besar saat win (8.2× vs 7.0×) · FVG lebih kecil saat win (0.52% vs 0.60%) · 39% loss = CHOCH nyata · 61% loss = drift (konsolidasi/ambiguous) |
| 1000BONKUSDT | Long 50% · C3 1.9× · Tch 6.2× · Gap 1.00% · NY | Long 54% · C3 2.4× · Tch 4.7× · Gap 1.00% · NY | Vol C3 justru lebih lemah saat win (1.9× vs 2.4×) · Vol sentuh SBR lebih besar saat win (6.2× vs 4.7×) · 85% loss = drift (konsolidasi/ambiguous) |
| AXSUSDT | Short 54% · C3 2.5× · Tch 5.4× · Gap 0.99% · London | Short 55% · C3 2.5× · Tch 13.8× · Gap 0.66% · NY | Vol sentuh SBR lebih kecil saat win (5.4× vs 13.8×) · FVG lebih besar saat win (0.99% vs 0.66%) · Win dominan sesi London (loss: NY) · 36% loss = CHOCH nyata · 64% loss = drift (konsolidasi/ambiguous) |
| XAUTUSDT | Short 56% · C3 2.0× · Tch 5.4× · Gap 0.30% · London | Long 64% · C3 2.0× · Tch 6.3× · Gap 0.28% · London | Vol sentuh SBR lebih kecil saat win (5.4× vs 6.3×) · 86% loss = drift (konsolidasi/ambiguous) |
| GALAUSDT | Short 52% · C3 1.9× · Tch 7.9× · Gap 0.84% · NY | Short 52% · C3 1.8× · Tch 4.5× · Gap 0.98% · London | Vol sentuh SBR lebih besar saat win (7.9× vs 4.5×) · FVG lebih kecil saat win (0.84% vs 0.98%) · Win dominan sesi NY (loss: London) · 78% loss = drift (konsolidasi/ambiguous) |
| SOLUSDT | Long 51% · C3 1.7× · Tch 3.2× · Gap 0.61% · London | Long 55% · C3 1.7× · Tch 3.8× · Gap 0.66% · Asia | Vol sentuh SBR lebih kecil saat win (3.2× vs 3.8×) · FVG lebih kecil saat win (0.61% vs 0.66%) · Win dominan sesi London (loss: Asia) · 27% loss = CHOCH nyata · 73% loss = drift (konsolidasi/ambiguous) |
| GMXUSDT | Short 52% · C3 2.3× · Tch 90.0× · Gap 0.66% · Asia | Long 59% · C3 2.2× · Tch 16.8× · Gap 0.59% · Asia | Vol sentuh SBR lebih besar saat win (90.0× vs 16.8×) · FVG lebih besar saat win (0.66% vs 0.59%) · 77% loss = drift (konsolidasi/ambiguous) |
| BERAUSDT | Long 52% · C3 2.0× · Tch 4.0× · Gap 0.88% · London | Long 53% · C3 1.7× · Tch 3.3× · Gap 0.99% · Asia | Vol sentuh SBR lebih besar saat win (4.0× vs 3.3×) · FVG lebih kecil saat win (0.88% vs 0.99%) · Win dominan sesi London (loss: Asia) · 29% loss = CHOCH nyata · 71% loss = drift (konsolidasi/ambiguous) |
| BELUSDT | Long 51% · C3 6.4× · Tch 14.6× · Gap 0.43% · London | Short 57% · C3 3.8× · Tch 14.6× · Gap 0.56% · London | Vol C3 lebih kuat saat win (6.4× vs 3.8×) · FVG lebih kecil saat win (0.43% vs 0.56%) · 81% loss = drift (konsolidasi/ambiguous) |
| LTCUSDT | Short 54% · C3 2.1× · Tch 6.6× · Gap 0.57% · Asia | Short 56% · C3 1.8× · Tch 6.4× · Gap 0.60% · Asia | Vol C3 lebih kuat saat win (2.1× vs 1.8×) · 78% loss = drift (konsolidasi/ambiguous) |
| VIRTUALUSDT | Short 58% · C3 2.1× · Tch 9.2× · Gap 0.98% · NY | Long 53% · C3 1.9× · Tch 5.3× · Gap 0.94% · London | Vol sentuh SBR lebih besar saat win (9.2× vs 5.3×) · Win dominan sesi NY (loss: London) · 32% loss = CHOCH nyata · 68% loss = drift (konsolidasi/ambiguous) |
| HBARUSDT | Short 55% · C3 2.2× · Tch 10.1× · Gap 0.69% · London | Long 57% · C3 2.0× · Tch 4.5× · Gap 0.82% · London | Vol sentuh SBR lebih besar saat win (10.1× vs 4.5×) · FVG lebih kecil saat win (0.69% vs 0.82%) · 38% loss = CHOCH nyata · 62% loss = drift (konsolidasi/ambiguous) |
| SEIUSDT | Long 50% · C3 2.0× · Tch 4.5× · Gap 0.59% · Asia | Long 59% · C3 2.0× · Tch 3.5× · Gap 0.76% · London | Vol sentuh SBR lebih besar saat win (4.5× vs 3.5×) · FVG lebih kecil saat win (0.59% vs 0.76%) · Win dominan sesi Asia (loss: London) · 32% loss = CHOCH nyata · 68% loss = drift (konsolidasi/ambiguous) |
| EIGENUSDT | Short 53% · C3 2.1× · Tch 3.4× · Gap 1.30% · London | Short 56% · C3 2.1× · Tch 4.3× · Gap 1.27% · London | Vol sentuh SBR lebih kecil saat win (3.4× vs 4.3×) · 50% loss = CHOCH nyata |

### Per Kuartal

| Kuartal | Trade | WR% | PnL | ROI Kuartal | Bal Awal → Akhir |
|---------|------:|----:|----:|:-----------:|:----------------:|
| Q1 2025 | 334 | 60% | +$20.52 | +205.2% | $10.00 → $30.52 |
| Q2 2025 | 407 | 66% | +$153.53 | +503.0% | $30.52 → $184.05 |
| Q3 2025 | 380 | 64% | +$885.47 | +481.1% | $184.05 → $1069.52 |
| Q4 2025 | 343 | 67% | +$7668.59 | +717.0% | $1069.52 → $8738.10 |
| Q1 2026 | 397 | 66% | +$55891.15 | +639.6% | $8738.10 → $64629.25 |
| Q2 2026 | 139 | 69% | +$54564.45 | +84.4% | $64629.25 → $119193.70 |

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

## ⚙️ Daftar Coin (35 coin aktif)

```python
SYMBOLS = ['XVGUSDT', 'BELUSDT', '1000BONKUSDT', 'BERAUSDT', '1000PEPEUSDT', 'ONDOUSDT', 'EIGENUSDT', 'VIRTUALUSDT', 'ENAUSDT', 'SHIB1000USDT', 'JUPUSDT', 'SEIUSDT', 'OPUSDT', 'STXUSDT', 'APEUSDT', 'ALGOUSDT', 'ORCAUSDT', 'XRPUSDT', 'XAUTUSDT', 'FARTCOINUSDT', 'TAOUSDT', 'SOLUSDT', 'SUIUSDT', 'TIAUSDT', 'AAVEUSDT', 'GALAUSDT', 'IMXUSDT', 'GMXUSDT', 'HBARUSDT', 'SANDUSDT', 'AXSUSDT', 'LTCUSDT', 'DYDXUSDT', 'FLOWUSDT', 'ICPUSDT']
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
