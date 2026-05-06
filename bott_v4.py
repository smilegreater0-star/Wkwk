import pandas as pd
import numpy as np
from pybit.unified_trading import HTTP
import os
import time
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# ============================================================
# LOG SERVER — akses via https://xxx.up.railway.app/logs
# ============================================================
LOG_FILE = "bot.log"

class _Tee:
    """Redirect print() ke stdout DAN file sekaligus, dengan timestamp WIB per baris."""
    def __init__(self):
        self._out     = sys.__stdout__
        self._file    = open(LOG_FILE, 'a', buffering=1, encoding='utf-8')
        self._newline = True
    def write(self, msg):
        import datetime
        out = ''
        for ch in msg:
            if self._newline and ch != '\n':
                out += (datetime.datetime.utcnow() + datetime.timedelta(hours=7)).strftime('[%H:%M:%S] ')
                self._newline = False
            out += ch
            if ch == '\n':
                self._newline = True
        self._out.write(out)
        self._file.write(out)
    def flush(self):
        self._out.flush()
        self._file.flush()

sys.stdout = _Tee()

class _LogHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path not in ('/logs', '/logs?'):
            self.send_response(404); self.end_headers(); return
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            data = ''.join(lines[-200:]).encode('utf-8')
        except:
            data = b''
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(data)
    def log_message(self, *a):
        pass

PORT = int(os.environ.get('PORT', 8080))
threading.Thread(
    target=lambda: HTTPServer(('0.0.0.0', PORT), _LogHandler).serve_forever(),
    daemon=True
).start()
print(f"📡 Log server jalan di port {PORT} → /logs")

# ============================================================
# CONFIG
# ============================================================
API_KEY    = os.environ.get('API_KEY', '')
API_SECRET = os.environ.get('API_SECRET', '')
CATEGORY   = "linear"
TESTNET    = os.environ.get('TESTNET', 'false').lower() == 'true'

if not API_KEY or not API_SECRET:
    raise ValueError("❌ API_KEY dan API_SECRET belum diset!")

session = HTTP(testnet=TESTNET, api_key=API_KEY, api_secret=API_SECRET)

SYMBOLS = [
    'XVGUSDT', 'BELUSDT', 'TAOUSDT', '1000BONKUSDT', 'BERAUSDT',
    'DASHUSDT', 'DOGEUSDT', 'USUALUSDT',
    'FARTCOINUSDT', '1000PEPEUSDT',
]

pending          = {}
active_positions = {}
instrument_cache = {}


# ============================================================
# FUNGSI DATA
# ============================================================

def get_data(symbol, interval, limit=200):
    try:
        res = session.get_kline(
            category=CATEGORY, symbol=symbol,
            interval=interval, limit=limit
        )
        if res['retCode'] == 0:
            df = pd.DataFrame(
                res['result']['list'],
                columns=['ts','open','high','low','close','vol','turnover']
            )
            df[['open','high','low','close','ts']] = \
                df[['open','high','low','close','ts']].apply(pd.to_numeric)
            return df.iloc[::-1].reset_index(drop=True)
        print(f"⚠️ get_data {symbol} {interval}: {res.get('retMsg','')}")
        return None
    except Exception as e:
        print(f"⚠️ get_data {symbol} {interval}: {e}")
        return None


# ============================================================
# INSTRUMENT INFO
# ============================================================

def get_instrument_info(symbol):
    if symbol in instrument_cache:
        return instrument_cache[symbol]
    try:
        res = session.get_instruments_info(category=CATEGORY, symbol=symbol)
        if res['retCode'] == 0:
            info = res['result']['list'][0]
            lot  = info['lotSizeFilter']
            data = {
                'min_qty'  : float(lot['minOrderQty']),
                'qty_step' : float(lot['qtyStep']),
                'tick_size': float(info['priceFilter']['tickSize']),
            }
            instrument_cache[symbol] = data
            return data
    except Exception as e:
        print(f"⚠️ instrument_info {symbol}: {e}")
    return {'min_qty': 0.01, 'qty_step': 0.01, 'tick_size': 0.0001}


def round_qty(qty, step):
    precision = len(str(step).rstrip('0').split('.')[-1]) if '.' in str(step) else 0
    return round(int(qty / step) * step, precision)


def round_price(price, tick):
    precision = len(str(tick).rstrip('0').split('.')[-1]) if '.' in str(tick) else 0
    return round(round(price / tick) * tick, precision)


# ============================================================
# FUNGSI SWING
# ============================================================

def find_swings(df, left=2, right=2):
    highs, lows = [], []
    for i in range(left, len(df) - right):
        h, l = df['high'].iloc[i], df['low'].iloc[i]
        if all(df['high'].iloc[i-j] < h for j in range(1, left+1)) and \
           all(df['high'].iloc[i+j] <= h for j in range(1, right+1)):
            highs.append({'val': h, 'idx': i, 'ts': df['ts'].iloc[i]})
        if all(df['low'].iloc[i-j] > l for j in range(1, left+1)) and \
           all(df['low'].iloc[i+j] >= l for j in range(1, right+1)):
            lows.append({'val': l, 'idx': i, 'ts': df['ts'].iloc[i]})
    return highs, lows


# ============================================================
# FIX BUG #1 — get_internal_gaps() hanya dari dalam range BOS
# + freshness hanya dicek sampai candle BOS, bukan post-BOS
# ============================================================

def get_internal_gaps(df, stype, bos_idx):
    """
    FVG dicari hanya di antara swing point dan candle BOS (start_idx..bos_idx).
    Freshness dicek hanya sampai bos_idx — candle setelah BOS belum terjadi
    saat FVG dinilai, jadi tidak boleh ikut menginvalidasi FVG.

    BUG LAMA: FVG diambil dari seluruh history termasuk post-BOS,
    sehingga FVG langsung dianggap broken oleh candle setelah BOS.
    """
    gaps = []
    # Hanya scan candle di dalam range BOS (bukan seluruh df)
    scan_end = bos_idx - 1
    for i in range(scan_end, 2, -1):
        gap = None
        if stype == "Long" and df['high'].iloc[i-2] < df['low'].iloc[i]:
            gap = {"top": df['low'].iloc[i], "bottom": df['high'].iloc[i-2]}
        elif stype == "Short" and df['low'].iloc[i-2] > df['high'].iloc[i]:
            gap = {"top": df['low'].iloc[i-2], "bottom": df['high'].iloc[i]}
        if gap:
            is_fresh = True
            # Freshness hanya dicek sampai bos_idx (bukan len(df))
            for j in range(i + 1, bos_idx + 1):
                if stype == "Long" and df['low'].iloc[j] < gap['bottom']:
                    is_fresh = False; break
                if stype == "Short" and df['high'].iloc[j] > gap['top']:
                    is_fresh = False; break
            if is_fresh:
                gaps.append(gap)
    return gaps


# ============================================================
# FIX BUG #2 — swing_ts diganti bos_ts agar M5 sinkron
# ============================================================
# swing_ts (ts swing high/low H1) bisa berbeda jauh dengan ts BOS.
# Akibatnya window M5 yang direplay salah — bisa terlalu jauh ke depan
# atau ke belakang. Solusi: gunakan bos_ts (ts candle BOS H1) sebagai
# anchor M5, karena IDM yang dicari harus terbentuk SETELAH BOS terjadi.


# ============================================================
# FUNGSI IDM (replay_m5) — tidak berubah, sudah benar
# ============================================================

def replay_m5(df, stype):
    """
    State machine IDM M5. Menggunakan while loop (bukan for)
    agar candle bisa di-reprocess saat transisi state.
    """
    if len(df) < 3:
        return {'phase': 'WAIT_IDM', 'idm_level': None}

    state = 'SINGLE_MOVE'
    candidate_high = None
    candidate_low  = None
    idm_start_idx  = 0

    i = 0
    while i < len(df) - 1:
        c = df.iloc[i]

        if stype == "Long":
            if state == 'SINGLE_MOVE':
                if candidate_low is None or c['low'] <= candidate_low:
                    candidate_low = c['low']; candidate_high = c['high']; i += 1
                else:
                    state = 'KONSOLIDASI'  # reprocess candle ini

            elif state == 'KONSOLIDASI':
                if c['low'] < candidate_low:
                    idm_high = candidate_high
                    candidate_low = c['low']; candidate_high = idm_high
                    idm_start_idx = i; state = 'TUNGGU_SENTUH'
                i += 1

            elif state == 'TUNGGU_SENTUH':
                if c['low'] < candidate_low:
                    candidate_low = c['low']; candidate_high = c['high']
                    state = 'SINGLE_MOVE'; i += 1
                elif c['high'] >= candidate_high:
                    du = df.iloc[idm_start_idx:i+1]
                    return {
                        'phase': 'IDM_TOUCHED', 'idm_level': candidate_high,
                        'freeze_high': du['high'].max(), 'freeze_low': du['low'].min(),
                        'freeze_ts': c['ts']
                    }
                else:
                    i += 1

        else:  # Short
            if state == 'SINGLE_MOVE':
                if candidate_high is None or c['high'] >= candidate_high:
                    candidate_high = c['high']; candidate_low = c['low']; i += 1
                else:
                    state = 'KONSOLIDASI'  # reprocess candle ini

            elif state == 'KONSOLIDASI':
                if c['high'] > candidate_high:
                    idm_low = candidate_low
                    candidate_high = c['high']; candidate_low = idm_low
                    idm_start_idx = i; state = 'TUNGGU_SENTUH'
                i += 1

            elif state == 'TUNGGU_SENTUH':
                if c['low'] <= candidate_low:
                    du = df.iloc[idm_start_idx:i+1]
                    return {
                        'phase': 'IDM_TOUCHED', 'idm_level': candidate_low,
                        'freeze_high': du['high'].max(), 'freeze_low': du['low'].min(),
                        'freeze_ts': c['ts']
                    }
                elif c['high'] > candidate_high:
                    candidate_high = c['high']; candidate_low = c['low']
                    state = 'SINGLE_MOVE'
                i += 1

    idm_level = candidate_high if stype == "Long" else candidate_low
    return {'phase': 'WAIT_IDM', 'idm_level': idm_level, 'state': state}


# ============================================================
# FVG TOUCH HELPERS
# ============================================================

def price_in_fvg(price_high, price_low, fvg):
    return price_low <= fvg['top'] and price_high >= fvg['bottom']

def candle_touches_fvg(candle, fvg, stype):
    """
    Cukup wick masuk zona FVG dari arah yang benar.
    Long  : low pullback ke dalam FVG (top..bottom dari atas)
    Short : high bounce ke dalam FVG (bottom..top dari bawah)
    """
    if stype == "Long":
        return candle['low'] <= fvg['top'] and candle['low'] >= fvg['bottom']
    else:
        return candle['high'] >= fvg['bottom'] and candle['high'] <= fvg['top']

def fvg_fully_broken(candle, fvg, stype):
    """FVG invalid jika close menembus sepenuhnya melewati zona."""
    if stype == "Long":  return candle['close'] < fvg['bottom']
    else:                return candle['close'] > fvg['top']


# ============================================================
# BREAKER BLOCK — entry terbaik setelah MSS
# ============================================================

def find_breaker_block(df_m5, mss_ts, stype):
    """
    Cari Breaker Block M5: candle berlawanan arah terakhir sebelum MSS.

    Long  → cari candle BEARISH terakhir sebelum MSS
            Entry : high candle bearish tersebut
            SL    : sedikit di bawah low candle bearish

    Short → cari candle BULLISH terakhir sebelum MSS
            Entry : low candle bullish tersebut
            SL    : sedikit di atas high candle bullish

    Kenapa lebih baik dari FVG H1 / MSS low:
    - SL lebih dalam dari low MSS yang obvious (tidak kena stop hunt)
    - Breaker block = zona yang pernah jadi resistance, setelah MSS
      ditembus menjadi support → valid sebagai area entry pullback
    - Dari backtesting: R:R 1:4.19 vs FVG H1 yang miss sama sekali
    """
    pre_mss = df_m5[df_m5['ts'] < mss_ts].tail(20).reset_index(drop=True)
    if pre_mss.empty:
        return None

    for _, c in pre_mss.iloc[::-1].iterrows():
        if stype == "Long":
            if float(c['close']) < float(c['open']):   # candle bearish
                body_size = abs(float(c['high']) - float(c['low']))
                return {
                    'entry'  : float(c['high']),
                    'sl'     : round(float(c['low']) - body_size * 0.1, 8),
                    'bb_high': float(c['high']),
                    'bb_low' : float(c['low']),
                    'ts'     : int(c['ts']),
                }
        else:
            if float(c['close']) > float(c['open']):   # candle bullish
                body_size = abs(float(c['high']) - float(c['low']))
                return {
                    'entry'  : float(c['low']),
                    'sl'     : round(float(c['high']) + body_size * 0.1, 8),
                    'bb_high': float(c['high']),
                    'bb_low' : float(c['low']),
                    'ts'     : int(c['ts']),
                }
    return None


# ============================================================
# FUNGSI ORDER
# ============================================================

def place_limit_order(symbol, side, entry, sl, tp):
    try:
        info     = get_instrument_info(symbol)
        res_bal  = session.get_wallet_balance(accountType="UNIFIED", coin="USDT")
        balance  = float(res_bal['result']['list'][0]['totalEquity'])
        risk_usd = balance * 0.01
        dist     = abs(entry - sl)
        if dist == 0:
            print(f"⚠️ {symbol}: dist entry-SL = 0, skip.")
            return False

        raw_qty = risk_usd / dist
        qty     = round_qty(raw_qty, info['qty_step'])
        if qty < info['min_qty']:
            print(f"⚠️ {symbol}: Qty {qty} < minOrderQty {info['min_qty']}, skip.")
            return False

        entry_r = round_price(entry, info['tick_size'])
        sl_r    = round_price(sl,    info['tick_size'])
        tp_r    = round_price(tp,    info['tick_size'])

        print(f"   Balance:{balance:.2f} Risk:{risk_usd:.2f} Dist:{dist} Qty:{qty}")
        res = session.place_order(
            category=CATEGORY, symbol=symbol, side=side,
            orderType="Limit", qty=str(qty), price=str(entry_r),
            stopLoss=str(sl_r), takeProfit=str(tp_r),
            timeInForce="GTC"
        )
        if res['retCode'] == 0:
            return True
        print(f"⚠️ {symbol}: Order ditolak → {res.get('retMsg','')} (code:{res['retCode']})")
        return False
    except Exception as e:
        print(f"⚠️ {symbol}: place_order error → {e}")
        return False


def get_open_position(symbol):
    try:
        res = session.get_positions(category=CATEGORY, symbol=symbol)
        if res['retCode'] == 0:
            for pos in res['result']['list']:
                if float(pos['size']) > 0:
                    return pos
        return None
    except:
        return None


def move_sl(symbol, new_sl):
    try:
        res = session.set_trading_stop(
            category=CATEGORY, symbol=symbol,
            stopLoss=str(new_sl), positionIdx=0
        )
        return res['retCode'] == 0
    except:
        return False


# ============================================================
# TRAILING SL
# ============================================================

def check_trailing_sl(coin):
    if coin not in active_positions: return
    p = active_positions[coin]
    if p.get('sl_moved'): return
    pos = get_open_position(coin)
    if pos is None:
        print(f"📭 {coin}: Posisi tutup.")
        del active_positions[coin]
        return
    entry = p['entry']
    side  = p['side']
    try:
        curr = float(pos['markPrice'])
    except:
        return
    if side == "Buy":
        pnl_pct = (curr - entry) / entry * 100
        if pnl_pct >= 2.0:
            new_sl = round(entry * 1.01, 8)
            if move_sl(coin, new_sl):
                active_positions[coin]['sl_moved'] = True
                print(f"🔒 {coin} LONG +{pnl_pct:.2f}% → SL ke +1% ({new_sl})")
    elif side == "Sell":
        pnl_pct = (entry - curr) / entry * 100
        if pnl_pct >= 2.0:
            new_sl = round(entry * 0.99, 8)
            if move_sl(coin, new_sl):
                active_positions[coin]['sl_moved'] = True
                print(f"🔒 {coin} SHORT +{pnl_pct:.2f}% → SL ke -1% ({new_sl})")


# ============================================================
# CEK TREN H1 BERUBAH
# ============================================================

def h1_trend_broken(curr_h1, setup, sh_h1, sl_h1):
    """
    Setup batal jika harga sudah melewati TP (swing searah BOS terlampaui).
    Long  : close > swing high terakhir → harga sudah lari, tidak ada pullback
    Short : close < swing low terakhir  → harga sudah lari, tidak ada pullback
    """
    if setup['type'] == "Long" and sh_h1 and curr_h1['close'] > sh_h1[-1]['val']:
        return True
    if setup['type'] == "Short" and sl_h1 and curr_h1['close'] < sl_h1[-1]['val']:
        return True
    return False


# ============================================================
# KONEKSI
# ============================================================

def test_connection():
    try:
        res = session.get_server_time()
        if res['retCode'] == 0:
            print(f"✅ Koneksi Bybit OK | Server time: {res['result']['timeSecond']}")
            return True
        print(f"❌ Bybit error: {res}")
        return False
    except Exception as e:
        print(f"❌ Gagal konek: {e}")
        return False


# ============================================================
# REPLAY H1 — reconstruct state saat startup
# FIX BUG #2: gunakan bos_ts sebagai anchor M5, bukan swing_ts
# FIX BUG #1: get_internal_gaps hanya dalam range BOS
# FIX BUG #3: FVG touch memakai candle_touches_fvg, bukan wick_only
# ============================================================

def replay_h1(coin, df_h1):
    sh_h1, sl_h1 = find_swings(df_h1, left=20, right=20)
    if not sh_h1 or not sl_h1:
        return None

    closed_h1 = df_h1.iloc[-2]
    is_long  = closed_h1['close'] > sh_h1[-1]['val']
    is_short = closed_h1['close'] < sl_h1[-1]['val']
    if not (is_long or is_short):
        return None

    stype   = "Long" if is_long else "Short"
    # ref_idx = indeks candle terakhir sebelum BOS (swing point yang dilanggar)
    ref_idx = sl_h1[-1]['idx'] if is_long else sh_h1[-1]['idx']
    # bos_idx = candle yang menutup melampaui swing → candle BOS itu sendiri
    # Cari candle pertama setelah ref_idx yang close melampaui swing
    bos_idx = None
    swing_val = sh_h1[-1]['val'] if is_long else sl_h1[-1]['val']
    for j in range(ref_idx + 1, len(df_h1)):
        c = df_h1.iloc[j]
        if is_long  and c['close'] > swing_val: bos_idx = j; break
        if is_short and c['close'] < swing_val: bos_idx = j; break
    if bos_idx is None:
        bos_idx = ref_idx + 1

    # FIX #1: FVG hanya dari dalam range BOS
    df_snap = df_h1.copy()
    gaps    = get_internal_gaps(df_snap, stype, bos_idx)
    if not gaps:
        return None

    since_bos = df_snap.iloc[bos_idx:]
    tp_val    = since_bos['high'].max() if stype == "Long" else since_bos['low'].min()
    # FIX #2: bos_ts sebagai anchor M5
    bos_ts    = df_snap['ts'].iloc[bos_idx]

    state = {
        'type': stype, 'df_h1': df_snap,
        'fvg_list': gaps, 'fvg_idx': 0,
        'tp': tp_val, 'bos_ts': bos_ts,
        'bos_idx': bos_idx,
        'phase': "WAIT_FVG_TOUCH", 'fvg_touch_ts': 0,
        'm5_freeze_high': None, 'm5_freeze_low': None, 'm5_freeze_ts': None,
        'idm_list': [], 'idm_touched_val': None,
    }

    fvg_idx = 0; fvg_touch_ts = 0; phase = "WAIT_FVG_TOUCH"

    # Replay candle H1 setelah BOS
    for _, candle in df_snap.iloc[bos_idx + 1:-1].iterrows():
        if fvg_idx >= len(gaps):
            return None
        fvg = gaps[fvg_idx]

        if phase == "WAIT_FVG_TOUCH":
            if stype == "Long" and candle['close'] >= tp_val: return None
            if stype == "Short" and candle['close'] <= tp_val: return None
            if fvg_fully_broken(candle, fvg, stype):
                fvg_idx += 1; continue
            if candle_touches_fvg(candle, fvg, stype):
                phase = "WAIT_IDM_TOUCH"; fvg_touch_ts = candle['ts']
        elif phase in ("WAIT_IDM_TOUCH", "WAIT_BOS_BREAK", "WAIT_MSS"):
            if stype == "Long" and candle['close'] >= tp_val: return None
            if stype == "Short" and candle['close'] <= tp_val: return None

    state['fvg_idx'] = fvg_idx
    state['phase']   = phase
    state['fvg_touch_ts'] = fvg_touch_ts

    print(f"\n📊 {coin}: BOS {stype} | H:{sh_h1[-1]['val']} L:{sl_h1[-1]['val']}")
    print(f"🔄 {coin}: Replay → Phase:{phase} FVG:{fvg_idx+1}/{len(gaps)}")
    return state


def reconstruct_state():
    for coin in SYMBOLS:
        try:
            time.sleep(1)
            df_h1 = get_data(coin, "60", limit=100)
            if df_h1 is None: continue
            state = replay_h1(coin, df_h1)
            if state:
                pending[coin] = state
        except Exception as e:
            print(f"⚠️ Replay {coin}: {e}")
    print(f"🔍 Selesai. {len(pending)} coin dimonitor.\n")


# ============================================================
# CORE LOOP
# FIX BUG #1 & #2 & #3 diterapkan di sini juga:
# - get_internal_gaps() pakai bos_idx
# - M5 anchor = bos_ts bukan swing_ts
# - FVG touch = candle_touches_fvg (wick masuk zona)
# ============================================================

def run_bot():
    print("BEGO MONEY CONCEPTS")
    if not test_connection():
        print("⛔ Tidak bisa konek ke Bybit.")
        return
    reconstruct_state()

    while True:

        for coin in list(active_positions.keys()):
            try:
                check_trailing_sl(coin)
            except Exception as e:
                print(f"⚠️ Trailing SL {coin}: {e}")

        for coin in SYMBOLS:
            try:
                time.sleep(2)

                df_h1_live = get_data(coin, "60", limit=100)
                if df_h1_live is None: continue

                sh_h1, sl_h1 = find_swings(df_h1_live, left=20, right=20)
                if not sh_h1 or not sl_h1: continue

                curr_h1   = df_h1_live.iloc[-1]
                closed_h1 = df_h1_live.iloc[-2]

                # ── PROSES SETUP PENDING ──────────────────────────────
                if coin in pending:
                    setup    = pending[coin]
                    stype    = setup['type']
                    fvg_list = setup['fvg_list']
                    fvg_idx  = setup['fvg_idx']

                    if h1_trend_broken(curr_h1, setup, sh_h1, sl_h1):
                        print(f"🔄 {coin}: Harga melewati TP tanpa pullback. Setup batal.")
                        del pending[coin]; continue

                    if fvg_idx >= len(fvg_list):
                        print(f"🗑️ {coin}: Semua FVG habis.")
                        del pending[coin]; continue

                    active_fvg = fvg_list[fvg_idx]

                    # ── PHASE 1: TUNGGU FVG H1 DISENTUH ──────────────
                    if setup['phase'] == "WAIT_FVG_TOUCH":
                        if fvg_fully_broken(closed_h1, active_fvg, stype):
                            print(f"❌ {coin}: FVG {fvg_idx+1} ditembus → coba berikutnya.")
                            pending[coin]['fvg_idx'] += 1; continue

                        if candle_touches_fvg(closed_h1, active_fvg, stype):
                            print(f"✅ {coin}: FVG {fvg_idx+1} disentuh. Masuk M5.")
                            pending[coin]['phase']        = "WAIT_IDM_TOUCH"
                            pending[coin]['fvg_touch_ts'] = closed_h1['ts']
                        else:
                            if stype == "Long" and curr_h1['close'] >= setup['tp']:
                                print(f"🗑️ {coin}: TP kena sebelum FVG."); del pending[coin]
                            elif stype == "Short" and curr_h1['close'] <= setup['tp']:
                                print(f"🗑️ {coin}: TP kena sebelum FVG."); del pending[coin]
                        continue

                    # ── AMBIL DATA M5 ─────────────────────────────────
                    time.sleep(1)
                    df_m5_live = get_data(coin, "5", limit=200)
                    if df_m5_live is None: continue

                    # Anchor M5 dari fvg_touch_ts — IDM harus terbentuk SETELAH
                    # FVG disentuh, bukan dari BOS yang bisa jauh ke belakang.
                    anchor_ts = setup.get("fvg_touch_ts") or setup["bos_ts"]
                    df_m5     = df_m5_live[df_m5_live["ts"] >= anchor_ts].reset_index(drop=True)
                    if len(df_m5) < 5:
                        df_m5 = df_m5_live.tail(80).reset_index(drop=True)

                    curr_m5 = df_m5.iloc[-1]

                    # ── PHASE 2: TUNGGU IDM TERSENTUH ────────────────
                    if setup['phase'] == "WAIT_IDM_TOUCH":
                        m5_state = replay_m5(df_m5, stype)

                        if m5_state['phase'] == 'WAIT_IDM':
                            idm_level = m5_state.get('idm_level')
                            if idm_level:
                                print(f"⏳ {coin}: IDM @ {idm_level} | Menunggu sentuhan...")
                            else:
                                print(f"⏳ {coin}: Belum ada IDM.")
                            if stype == "Long" and curr_m5['close'] >= setup['tp']:
                                print(f"🗑️ {coin}: TP kena tanpa IDM."); del pending[coin]
                            elif stype == "Short" and curr_m5['close'] <= setup['tp']:
                                print(f"🗑️ {coin}: TP kena tanpa IDM."); del pending[coin]
                            continue

                        idm_level   = m5_state['idm_level']
                        freeze_high = m5_state['freeze_high']
                        freeze_low  = m5_state['freeze_low']
                        freeze_ts   = m5_state['freeze_ts']

                        print(f"💧 {coin}: IDM tersentuh @ {idm_level}")
                        print(f"   → Target BOS M5: {freeze_low if stype=='Long' else freeze_high}")
                        print(f"   → Target MSS   : {freeze_high if stype=='Long' else freeze_low}")

                        pending[coin]['phase']           = "WAIT_BOS_BREAK"
                        pending[coin]['idm_touched_val'] = idm_level
                        pending[coin]['m5_freeze_high']  = freeze_high
                        pending[coin]['m5_freeze_low']   = freeze_low
                        pending[coin]['m5_freeze_ts']    = freeze_ts
                        continue

                    # ── PHASE 3: TUNGGU BOS M5 ────────────────────────
                    if setup['phase'] == "WAIT_BOS_BREAK":
                        freeze_low  = setup['m5_freeze_low']
                        freeze_high = setup['m5_freeze_high']
                        freeze_ts   = setup['m5_freeze_ts']

                        df_after = df_m5[df_m5['ts'] > freeze_ts]
                        if df_after.empty: continue

                        bos_broken = False; bos_candle_ts = None
                        for _, c in df_after.iterrows():
                            if stype == "Long" and c['close'] < freeze_low:
                                bos_broken = True; bos_candle_ts = c['ts']
                                print(f"📉 {coin}: BOS Bearish M5 @ {c['close']:.6f}. Masuk WAIT_MSS."); break
                            elif stype == "Short" and c['close'] > freeze_high:
                                bos_broken = True; bos_candle_ts = c['ts']
                                print(f"📈 {coin}: BOS Bullish M5 @ {c['close']:.6f}. Masuk WAIT_MSS."); break

                        if bos_broken:
                            # FIX BUG #4: nfh/nfl hanya dari candle antara IDM dan BOS M5
                            # Sebelumnya pakai max seluruh dai → range terlalu lebar → MSS tidak pernah tercapai
                            df_idm_to_bos = df_m5[(df_m5['ts'] > freeze_ts) & (df_m5['ts'] <= bos_candle_ts)]
                            new_fh = df_idm_to_bos['high'].max() if not df_idm_to_bos.empty else freeze_high
                            new_fl = df_idm_to_bos['low'].min()  if not df_idm_to_bos.empty else freeze_low
                            pending[coin]['phase']           = "WAIT_MSS"
                            pending[coin]['m5_freeze_high']  = new_fh
                            pending[coin]['m5_freeze_low']   = new_fl
                            pending[coin]['m5_freeze_ts']    = bos_candle_ts
                            pending[coin]['idm_touched_val'] = None
                        else:
                            if stype == "Long" and curr_m5['close'] >= setup['tp']:
                                print(f"🗑️ {coin}: TP kena tanpa BOS M5."); del pending[coin]
                            elif stype == "Short" and curr_m5['close'] <= setup['tp']:
                                print(f"🗑️ {coin}: TP kena tanpa BOS M5."); del pending[coin]
                        continue

                    # ── PHASE 4: TUNGGU MSS ───────────────────────────
                    if setup['phase'] == "WAIT_MSS":
                        freeze_low  = setup['m5_freeze_low']
                        freeze_high = setup['m5_freeze_high']
                        freeze_ts   = setup['m5_freeze_ts']

                        df_after = df_m5[df_m5['ts'] > freeze_ts]
                        if df_after.empty: continue

                        mss_candle = None; reset_to_idm = False
                        for _, c in df_after.iterrows():
                            if stype == "Long":
                                if c['close'] > freeze_high:
                                    mss_candle = c; break
                                elif c['close'] < freeze_low:
                                    reset_to_idm = True
                                    print(f"🔄 {coin}: Break bawah lagi. Cari IDM baru.")
                                    pending[coin].update({
                                        'phase': "WAIT_IDM_TOUCH",
                                        'm5_freeze_high': None, 'm5_freeze_low': None, 'm5_freeze_ts': None
                                    }); break
                            else:
                                if c['close'] < freeze_low:
                                    mss_candle = c; break
                                elif c['close'] > freeze_high:
                                    reset_to_idm = True
                                    print(f"🔄 {coin}: Break atas lagi. Cari IDM baru.")
                                    pending[coin].update({
                                        'phase': "WAIT_IDM_TOUCH",
                                        'm5_freeze_high': None, 'm5_freeze_low': None, 'm5_freeze_ts': None
                                    }); break

                        if reset_to_idm or mss_candle is None:
                            if not reset_to_idm:
                                if stype == "Long" and curr_m5['close'] >= setup['tp']:
                                    print(f"🗑️ {coin}: TP kena tanpa MSS."); del pending[coin]
                                elif stype == "Short" and curr_m5['close'] <= setup['tp']:
                                    print(f"🗑️ {coin}: TP kena tanpa MSS."); del pending[coin]
                            continue

                        # MSS confirmed — cari entry terbaik
                        # Prioritas: Breaker Block > FVG H1
                        side_order = "Buy" if stype == "Long" else "Sell"

                        bb = find_breaker_block(df_m5, mss_candle['ts'], stype)

                        if bb is not None:
                            # Gunakan Breaker Block sebagai entry
                            entry_price = bb['entry']
                            sl_price    = bb['sl']
                            print(f"🧱 {coin}: Breaker Block @ {entry_price:.6f} | SL {sl_price:.6f}")
                        else:
                            # Fallback: FVG H1 jika Breaker Block tidak ditemukan
                            entry_fvg = None; entry_price = None
                            for fvg in fvg_list:
                                if price_in_fvg(mss_candle['high'], mss_candle['low'], fvg):
                                    entry_fvg   = fvg
                                    entry_price = fvg['top'] if stype == "Long" else fvg['bottom']
                                    break

                            if entry_fvg is None:
                                # Tidak ada BB dan tidak ada FVG → gunakan nfh/nfl sebagai RBS
                                entry_price = freeze_high if stype == "Long" else freeze_low
                                print(f"↩️ {coin}: No BB/FVG, fallback RBS @ {entry_price:.6f}")

                            sl_price = mss_candle['low'] if stype == "Long" else mss_candle['high']
                            print(f"🎯 {coin}: FVG/RBS entry @ {entry_price} | SL {sl_price}")

                        if entry_price is None or sl_price is None:
                            print(f"⚠️ {coin}: Tidak bisa tentukan entry, skip.")
                            continue

                        dist = abs(entry_price - sl_price)
                        if dist == 0:
                            print(f"⚠️ {coin}: Entry = SL, skip.")
                            continue

                        print(f"🎯 {coin}: {side_order} @ {entry_price} | SL {sl_price} | TP {setup['tp']}")

                        if place_limit_order(coin, side_order, entry_price, sl_price, setup['tp']):
                            print(f"✅ {coin}: ORDER TERPASANG!")
                            active_positions[coin] = {
                                'side': side_order, 'entry': entry_price,
                                'sl': sl_price, 'tp': setup['tp'], 'sl_moved': False
                            }
                            del pending[coin]
                        else:
                            print(f"⚠️ {coin}: Gagal pasang order.")
                    continue

                # ── SCAN BOS H1 BARU ──────────────────────────────────
                is_long  = closed_h1['close'] > sh_h1[-1]['val']
                is_short = closed_h1['close'] < sl_h1[-1]['val']
                if not (is_long or is_short): continue

                stype   = "Long" if is_long else "Short"
                ref_idx = sl_h1[-1]['idx'] if is_long else sh_h1[-1]['idx']

                # Cari bos_idx: candle yang menutup melampaui swing
                swing_val = sh_h1[-1]['val'] if is_long else sl_h1[-1]['val']
                bos_idx   = None
                for j in range(ref_idx + 1, len(df_h1_live)):
                    c = df_h1_live.iloc[j]
                    if is_long  and c['close'] > swing_val: bos_idx = j; break
                    if is_short and c['close'] < swing_val: bos_idx = j; break
                if bos_idx is None:
                    bos_idx = ref_idx + 1

                df_h1_snap = df_h1_live.copy()

                # FIX #1: FVG hanya dari dalam range BOS
                gaps = get_internal_gaps(df_h1_snap, stype, bos_idx)
                if not gaps:
                    print(f"⚠️ {coin}: BOS {stype} tapi tidak ada FVG di dalam range.")
                    continue

                since_bos = df_h1_snap.iloc[bos_idx:]
                tp_val    = since_bos['high'].max() if stype == "Long" else since_bos['low'].min()
                # FIX #2: anchor M5 dari bos_ts
                bos_ts    = df_h1_snap['ts'].iloc[bos_idx]

                pending[coin] = {
                    'type': stype, 'df_h1': df_h1_snap,
                    'fvg_list': gaps, 'fvg_idx': 0,
                    'tp': tp_val, 'bos_ts': bos_ts, 'bos_idx': bos_idx,
                    'phase': "WAIT_FVG_TOUCH", 'fvg_touch_ts': 0,
                    'm5_freeze_high': None, 'm5_freeze_low': None, 'm5_freeze_ts': None,
                    'idm_list': [], 'idm_touched_val': None,
                }
                print(f"\n📊 {coin} | H:{sh_h1[-1]['val']} C:{curr_h1['close']} L:{sl_h1[-1]['val']}")
                print(f"🎯 {coin}: BOS {stype} | {len(gaps)} FVG | TP:{tp_val}")
                for i, g in enumerate(gaps):
                    print(f"   FVG {i+1}: bottom:{g['bottom']} top:{g['top']}")

            except Exception as e:
                print(f"⚠️ Error {coin}: {e}"); continue

        time.sleep(10)


if __name__ == "__main__":
    run_bot()
