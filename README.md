# 🤖 SMC Trading Bot v4

Bot trading otomatis berbasis **Smart Money Concepts (SMC)** untuk Bybit Futures (USDT Perpetual).

---

## 📐 Strategi

```
BOS H1 → FVG Kuat (C3 vol > avg20H) → SBR Touch M5
  → Entry market di C1.close (SBR/RBS demand/supply zone)
  → SL di C1.low/C1.high ± 10% gap buffer
  → Trail stop 0.15× dist (aktif setelah +1R) → Reverse max 2×
```

**Risk Management:**
- Risk per trade: **1% dari balance** (compound — tiap trade risk ikut balance live)
- Exit: **trailing stop** 0.15× dist, aktif setelah profit +1R
- Reverse: Long→SL→Short (max 2 kali per setup)
- Leverage: otomatis sesuai limit coin, maks 10×

---

## 📊 Hasil Backtest — Jan 2025–Apr 2026

> Modal $10 | Risk 1%/trade compound (1 pot bersama) | Trail 0.15R + Reverse | ATR Filter Adaptif
> _24 Coin | Data Bybit Perpetual USDT | M5+H1 | Jan 2025–Apr 2026_
> _(Generated: 2026-05-22)_

### Per Coin (diurutkan PnL terbesar)

| Coin | Trade | WR% | PnL ($) | ROI% | MaxDD% | PF | Avg R:R | ATR P25 |
|------|------:|----:|--------:|-----:|-------:|---:|--------:|--------:|
| ORCAUSDT | 233 | 61% | +$384048482249395388022784.00 | +3840484822493954282881024% | 7.2% | 1.94 | 1.78:1 | 0.0021 |
| TAOUSDT | 303 | 65% | +$367054363676863493046272.00 | +3670543636768635064680448% | 10.4% | 2.71 | 3.28:1 | 0.0031 |
| FLOWUSDT | 269 | 61% | +$332324860106752135266304.00 | +3323248601067521621098496% | 19.1% | 2.75 | 2.03:1 | 0.0020 |
| IMXUSDT | 390 | 62% | +$304640102156827659075584.00 | +3046401021568276859191296% | 13.2% | 1.94 | 1.71:1 | 0.0028 |
| SANDUSDT | 324 | 62% | +$278493800279201099546624.00 | +2784938002792011129683968% | 11.1% | 1.78 | 1.77:1 | 0.0022 |
| ONDOUSDT | 321 | 61% | +$260729368381724922216448.00 | +2607293683817249289273344% | 14.2% | 1.77 | 1.85:1 | 0.0025 |
| FARTCOINUSDT | 367 | 68% | +$254085443340055303159808.00 | +2540854433400553098706944% | 6.8% | 3.12 | 1.97:1 | 0.0050 |
| SOLUSDT | 286 | 62% | +$221487685607741152296960.00 | +2214876856077411455860736% | 10.7% | 1.54 | 1.58:1 | 0.0022 |
| BELUSDT | 291 | 63% | +$220265607601654375383040.00 | +2202656076016543820939264% | 8.4% | 2.88 | 2.31:1 | 0.0021 |
| XVGUSDT | 265 | 60% | +$217863372456997469290496.00 | +2178633724569974558687232% | 10.1% | 1.67 | 1.61:1 | 0.0028 |
| 1000BONKUSDT | 253 | 65% | +$186487190368807251083264.00 | +1864871903688072376614912% | 11.7% | 2.39 | 1.86:1 | 0.0031 |
| EIGENUSDT | 374 | 62% | +$123576093699486058020864.00 | +1235760936994860647317504% | 6.3% | 2.09 | 1.83:1 | 0.0033 |
| ENAUSDT | 325 | 65% | +$117715305813855501811712.00 | +1177153058138555152334848% | 13.7% | 2.15 | 1.66:1 | 0.0035 |
| ICPUSDT | 352 | 66% | +$109598228752156994830336.00 | +1095982287521570048966656% | 7.6% | 1.91 | 1.57:1 | 0.0023 |
| SUIUSDT | 305 | 62% | +$71715620718803203129344.00 | +717156207188031997739008% | 11.3% | 1.93 | 1.85:1 | 0.0026 |
| ALGOUSDT | 365 | 61% | +$68538843102359047897088.00 | +685388431023590512525312% | 12.9% | 1.50 | 1.53:1 | 0.0023 |
| XRPUSDT | 275 | 64% | +$56195740510342124404736.00 | +561957405103421277601792% | 8.5% | 1.62 | 1.57:1 | 0.0018 |
| STXUSDT | 289 | 61% | +$25106518182136956059648.00 | +251065181821369585762304% | 10.2% | 1.48 | 1.56:1 | 0.0023 |
| OPUSDT | 271 | 62% | +$21820556121069380960256.00 | +218205561210693809602560% | 12.8% | 1.81 | 1.64:1 | 0.0028 |
| LTCUSDT | 323 | 65% | +$4478582074370947022848.00 | +44785820743709474422784% | 7.3% | 1.64 | 1.44:1 | 0.0018 |
| 1000PEPEUSDT | 314 | 67% | $-11536109833411291512832.00 | -115361098334112923516928% | 10.8% | 2.32 | 1.73:1 | 0.0029 |
| VIRTUALUSDT | 405 | 62% | $-31383722800498595594240.00 | -313837228004985981108224% | 15.1% | 1.74 | 1.63:1 | 0.0036 |
| BERAUSDT | 287 | 63% | $-51635802108770889236480.00 | -516358021087708925919232% | 11.6% | 1.82 | 1.54:1 | 0.0031 |
| SHIB1000USDT | 293 | 63% | $-58696054044214708666368.00 | -586960540442147086663680% | 10.7% | 1.64 | 1.68:1 | 0.0019 |
| **TOTAL** | **7480** | **63%** | **+$3472974076413706762190848.00** | **+34729740764137065474424832%** | **14.2%** | **3.05** | **1.79:1** | — |


**$10.00 → $3472974076413706762190848.00 dalam setahun (+34729740764137065474424832% ROI)**

### Analisis Win/Loss per Coin

> Format: Direction · Vol C3 (FVG strength) · Gap size · Sesi dominan

| Coin | ✅ Win (pola rata-rata) | ❌ Loss (pola rata-rata) | 💡 Insight |
|------|------------------------|-------------------------|------------|
| **TOTAL** | **Short 52% · C3 2.2× · Tch — · Gap 0.81% · London** | **Short 51% · C3 2.2× · Tch — · Gap 0.76% · London** | **FVG lebih besar saat win (0.81% vs 0.76%) · 33% loss = CHOCH nyata · 67% loss = drift (konsolidasi/ambiguous)** |
| ORCAUSDT | Short 54% · C3 2.5× · Tch — · Gap 0.79% · London | Short 52% · C3 2.6× · Tch — · Gap 0.94% · London | FVG lebih kecil saat win (0.79% vs 0.94%) · 34% loss = CHOCH nyata · 66% loss = drift (konsolidasi/ambiguous) |
| TAOUSDT | Long 51% · C3 2.1× · Tch — · Gap 0.81% · NY | Long 52% · C3 2.0× · Tch — · Gap 0.71% · NY | FVG lebih besar saat win (0.81% vs 0.71%) · 38% loss = CHOCH nyata · 62% loss = drift (konsolidasi/ambiguous) |
| FLOWUSDT | Short 54% · C3 2.1× · Tch — · Gap 0.65% · London | Long 52% · C3 2.0× · Tch — · Gap 0.70% · London | 33% loss = CHOCH nyata · 67% loss = drift (konsolidasi/ambiguous) |
| IMXUSDT | Short 56% · C3 2.1× · Tch — · Gap 0.75% · London | Short 53% · C3 2.1× · Tch — · Gap 0.66% · London | FVG lebih besar saat win (0.75% vs 0.66%) · 28% loss = CHOCH nyata · 72% loss = drift (konsolidasi/ambiguous) |
| SANDUSDT | Short 51% · C3 2.4× · Tch — · Gap 0.62% · London | Short 57% · C3 2.6× · Tch — · Gap 0.51% · London | FVG lebih besar saat win (0.62% vs 0.51%) · 30% loss = CHOCH nyata · 70% loss = drift (konsolidasi/ambiguous) |
| ONDOUSDT | Long 53% · C3 2.2× · Tch — · Gap 0.70% · London | Short 61% · C3 1.9× · Tch — · Gap 0.63% · NY | FVG lebih besar saat win (0.70% vs 0.63%) · Win dominan sesi London (loss: NY) · 34% loss = CHOCH nyata · 66% loss = drift (konsolidasi/ambiguous) |
| FARTCOINUSDT | Long 50% · C3 1.8× · Tch — · Gap 1.34% · NY | Short 51% · C3 1.7× · Tch — · Gap 1.44% · NY | FVG lebih kecil saat win (1.34% vs 1.44%) · 39% loss = CHOCH nyata · 61% loss = drift (konsolidasi/ambiguous) |
| SOLUSDT | Long 50% · C3 2.3× · Tch — · Gap 0.55% · London | Long 51% · C3 2.1× · Tch — · Gap 0.57% · NY | Win dominan sesi London (loss: NY) · 30% loss = CHOCH nyata · 70% loss = drift (konsolidasi/ambiguous) |
| BELUSDT | Short 54% · C3 3.7× · Tch — · Gap 0.73% · London | Long 55% · C3 3.4× · Tch — · Gap 0.70% · London | 36% loss = CHOCH nyata · 64% loss = drift (konsolidasi/ambiguous) |
| XVGUSDT | Long 50% · C3 2.4× · Tch — · Gap 0.76% · London | Short 57% · C3 2.9× · Tch — · Gap 0.81% · London | Vol C3 justru lebih lemah saat win (2.4× vs 2.9×) · FVG lebih kecil saat win (0.76% vs 0.81%) · 31% loss = CHOCH nyata · 69% loss = drift (konsolidasi/ambiguous) |
| 1000BONKUSDT | Short 54% · C3 2.6× · Tch — · Gap 1.01% · NY | Short 51% · C3 2.2× · Tch — · Gap 0.84% · NY | Vol C3 lebih kuat saat win (2.6× vs 2.2×) · FVG lebih besar saat win (1.01% vs 0.84%) · 34% loss = CHOCH nyata · 66% loss = drift (konsolidasi/ambiguous) |
| EIGENUSDT | Short 52% · C3 1.8× · Tch — · Gap 1.05% · London | Long 53% · C3 1.9× · Tch — · Gap 1.16% · London | FVG lebih kecil saat win (1.05% vs 1.16%) · 32% loss = CHOCH nyata · 68% loss = drift (konsolidasi/ambiguous) |
| ENAUSDT | Long 51% · C3 2.0× · Tch — · Gap 0.94% · London | Short 51% · C3 1.8× · Tch — · Gap 0.83% · London | FVG lebih besar saat win (0.94% vs 0.83%) · 35% loss = CHOCH nyata · 65% loss = drift (konsolidasi/ambiguous) |
| ICPUSDT | Short 52% · C3 2.0× · Tch — · Gap 0.60% · NY | Short 51% · C3 1.9× · Tch — · Gap 0.55% · Asia | Win dominan sesi NY (loss: Asia) · 26% loss = CHOCH nyata · 74% loss = drift (konsolidasi/ambiguous) |
| SUIUSDT | Short 53% · C3 1.9× · Tch — · Gap 0.87% · London | Long 51% · C3 2.0× · Tch — · Gap 0.79% · London | FVG lebih besar saat win (0.87% vs 0.79%) · 28% loss = CHOCH nyata · 72% loss = drift (konsolidasi/ambiguous) |
| ALGOUSDT | Short 57% · C3 2.0× · Tch — · Gap 0.76% · London | Long 54% · C3 2.3× · Tch — · Gap 0.67% · NY | FVG lebih besar saat win (0.76% vs 0.67%) · Win dominan sesi London (loss: NY) · 36% loss = CHOCH nyata · 64% loss = drift (konsolidasi/ambiguous) |
| XRPUSDT | Short 53% · C3 2.1× · Tch — · Gap 0.70% · London | Short 51% · C3 2.3× · Tch — · Gap 0.60% · NY | FVG lebih besar saat win (0.70% vs 0.60%) · Win dominan sesi London (loss: NY) · 28% loss = CHOCH nyata · 72% loss = drift (konsolidasi/ambiguous) |
| STXUSDT | Short 54% · C3 2.2× · Tch — · Gap 0.66% · London | Short 54% · C3 2.2× · Tch — · Gap 0.62% · London | 32% loss = CHOCH nyata · 68% loss = drift (konsolidasi/ambiguous) |
| OPUSDT | Short 53% · C3 2.1× · Tch — · Gap 0.67% · London | Long 52% · C3 1.9× · Tch — · Gap 0.72% · London | FVG lebih kecil saat win (0.67% vs 0.72%) · 37% loss = CHOCH nyata · 63% loss = drift (konsolidasi/ambiguous) |
| LTCUSDT | Short 53% · C3 2.1× · Tch — · Gap 0.66% · London | Short 54% · C3 2.0× · Tch — · Gap 0.61% · NY | FVG lebih besar saat win (0.66% vs 0.61%) · Win dominan sesi London (loss: NY) · 33% loss = CHOCH nyata · 67% loss = drift (konsolidasi/ambiguous) |
| 1000PEPEUSDT | Short 50% · C3 2.1× · Tch — · Gap 0.84% · London | Short 56% · C3 2.0× · Tch — · Gap 0.86% · London | 38% loss = CHOCH nyata · 62% loss = drift (konsolidasi/ambiguous) |
| VIRTUALUSDT | Short 55% · C3 1.9× · Tch — · Gap 0.98% · London | Short 50% · C3 2.0× · Tch — · Gap 0.96% · London | 33% loss = CHOCH nyata · 67% loss = drift (konsolidasi/ambiguous) |
| BERAUSDT | Long 50% · C3 2.1× · Tch — · Gap 1.14% · Asia | Long 51% · C3 2.1× · Tch — · Gap 0.71% · Asia | FVG lebih besar saat win (1.14% vs 0.71%) · 28% loss = CHOCH nyata · 72% loss = drift (konsolidasi/ambiguous) |
| SHIB1000USDT | Short 54% · C3 2.3× · Tch — · Gap 0.67% · London | Long 52% · C3 2.3× · Tch — · Gap 0.56% · NY | FVG lebih besar saat win (0.67% vs 0.56%) · Win dominan sesi London (loss: NY) · 33% loss = CHOCH nyata · 67% loss = drift (konsolidasi/ambiguous) |

### Per Kuartal

| Kuartal | Trade | WR% | PnL | ROI Kuartal | Bal Awal → Akhir |
|---------|------:|----:|----:|:-----------:|:----------------:|
| Q1 2025 | 1537 | 65% | +$1777209.17 | +17772091.7% | $10.00 → $1777219.17 |
| Q2 2025 | 1485 | 60% | +$11511386319.60 | +647719.0% | $1777219.17 → $11513163538.78 |
| Q3 2025 | 1456 | 63% | +$277455459743458.50 | +2409897.7% | $11513163538.78 → $277466972906997.28 |
| Q4 2025 | 1333 | 64% | +$25353871176007610368.00 | +9137617.7% | $277466972906997.28 → $25354148642980515840.00 |
| Q1 2026 | 1233 | 64% | +$301359699566380669992960.00 | +1188601.1% | $25354148642980515840.00 → $301385053715023662153728.00 |
| Q2 2026 | 436 | 63% | +$3171589022698681086771200.00 | +1052.3% | $301385053715023662153728.00 → $3472974076413704614707200.00 |

### Konfigurasi

| Parameter | Nilai |
|-----------|-------|
| Modal Awal | $10 |
| Risk per Trade | 1% balance (compound) |
| Entry Mode | fvg_limit (SBR — C1.close) |
| Exit | Trail stop 0.15× dist + Reverse 2× |
| Leverage | maks 10× |
| Fee | 0.055%/sisi (Bybit taker) |
| Touch Vol Min | 0.8× avg20M5 |
| Max Gap | 0.60% dari harga |
| Min SL distance | 0.2% |

---

## ⚙️ Daftar Coin (24 coin aktif)

```python
SYMBOLS = ['XVGUSDT', 'BELUSDT', '1000BONKUSDT', 'BERAUSDT', '1000PEPEUSDT', 'ONDOUSDT', 'EIGENUSDT', 'VIRTUALUSDT', 'ENAUSDT', 'SHIB1000USDT', 'OPUSDT', 'STXUSDT', 'ALGOUSDT', 'ORCAUSDT', 'XRPUSDT', 'FARTCOINUSDT', 'TAOUSDT', 'SOLUSDT', 'SUIUSDT', 'IMXUSDT', 'SANDUSDT', 'LTCUSDT', 'FLOWUSDT', 'ICPUSDT']
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
