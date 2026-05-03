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
    """Redirect print() ke stdout DAN file sekaligus, dengan timestamp per baris."""
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
        if self.path != '/logs':
            self.send_response(404); self.end_headers(); return
        try:
            data = open(LOG_FILE, 'rb').read()
        except:
            data = b''
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(data)
    def log_message(self, *a):
        pass  # silent, tidak spam console

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
    'XVGUSDT', 'BELUSDT', 'TAOUSDT', '1000BONKUSDT',  'BERAUSDT',
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
# INSTRUMENT INFO — FIX #6: lot size & qty step per symbol
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
# FUNGSI IDM — FIX #1 & #2
# ============================================================

def replay_m5(df, stype):
    """
    Replay candle M5 dari kiri ke kanan, state machine IDM.
    FIX #1: Gunakan while loop supaya candle bisa di-reprocess saat transisi state.
    FIX #2: Reset IDM Short tidak overwrite candidate_low (IDM level).
    """
    if len(df) < 3:
        return {'phase': 'WAIT_IDM', 'idm_level': None}

    state          = 'SINGLE_MOVE'
    candidate_high = None
    candidate_low  = None
    idm_start_idx  = 0

    i = 0
    while i < len(df) - 1:
        c = df.iloc[i]

        if stype == "Long":

            if state == 'SINGLE_MOVE':
                if candidate_low is None or c['low'] <= candidate_low:
                    candidate_low  = c['low']
                    candidate_high = c['high']
                    i += 1
                else:
                    # Tidak increment i — candle ini diproses ulang di KONSOLIDASI
                    state = 'KONSOLIDASI'

            elif state == 'KONSOLIDASI':
                if c['low'] < candidate_low:
                    idm_high       = candidate_high
                    candidate_low  = c['low']
                    candidate_high = idm_high
                    idm_start_idx  = i
                    state          = 'TUNGGU_SENTUH'
                i += 1

            elif state == 'TUNGGU_SENTUH':
                if c['low'] < candidate_low:
                    candidate_low  = c['low']
                    candidate_high = c['high']
                    state          = 'SINGLE_MOVE'
                    i += 1
                elif c['high'] >= candidate_high:
                    df_until = df.iloc[idm_start_idx:i+1]
                    return {
                        'phase'      : 'IDM_TOUCHED',
                        'idm_level'  : candidate_high,
                        'freeze_high': df_until['high'].max(),
                        'freeze_low' : df_until['low'].min(),
                        'freeze_ts'  : c['ts']
                    }
                else:
                    i += 1

        else:  # Short

            if state == 'SINGLE_MOVE':
                if candidate_high is None or c['high'] >= candidate_high:
                    candidate_high = c['high']
                    candidate_low  = c['low']
                    i += 1
                else:
                    # Tidak increment i — candle ini diproses ulang di KONSOLIDASI
                    state = 'KONSOLIDASI'

            elif state == 'KONSOLIDASI':
                if c['high'] > candidate_high:
                    idm_low        = candidate_low
                    candidate_high = c['high']
                    # FIX #2: Pertahankan IDM level, jangan overwrite
                    candidate_low  = idm_low
                    idm_start_idx  = i
                    state          = 'TUNGGU_SENTUH'
                i += 1

            elif state == 'TUNGGU_SENTUH':
                if c['low'] <= candidate_low:
                    df_until = df.iloc[idm_start_idx:i+1]
                    return {
                        'phase'      : 'IDM_TOUCHED',
                        'idm_level'  : candidate_low,
                        'freeze_high': df_until['high'].max(),
                        'freeze_low' : df_until['low'].min(),
                        'freeze_ts'  : c['ts']
                    }
                elif c['high'] > candidate_high:
                    # FIX #2: Reset dengan high baru, low juga update
                    candidate_high = c['high']
                    candidate_low  = c['low']
                    state          = 'SINGLE_MOVE'
                i += 1

    idm_level = candidate_high if stype == "Long" else candidate_low
    return {'phase': 'WAIT_IDM', 'idm_level': idm_level, 'state': state}


# ============================================================
# FUNGSI FVG H1 — FIX #5: freshness check pakai wick
# ============================================================

def get_internal_gaps(df, stype, start_idx):
    gaps    = []
    end_idx = len(df) - 2
    for i in range(end_idx, start_idx + 2, -1):
        gap = None
        if stype == "Long" and df['high'].iloc[i-2] < df['low'].iloc[i]:
            gap = {"top": df['low'].iloc[i], "bottom": df['high'].iloc[i-2]}
        elif stype == "Short" and df['low'].iloc[i-2] > df['high'].iloc[i]:
            gap = {"top": df['low'].iloc[i-2], "bottom": df['high'].iloc[i]}
        if gap:
            is_fresh = True
            for j in range(i + 1, len(df)):
                # FIX #5: Pakai wick bukan close
                if stype == "Long" and df['low'].iloc[j] < gap['bottom']:
                    is_fresh = False; break
                if stype == "Short" and df['high'].iloc[j] > gap['top']:
                    is_fresh = False; break
            if is_fresh:
                gaps.append(gap)
    return gaps


def price_in_fvg(price_high, price_low, fvg):
    return price_low <= fvg['top'] and price_high >= fvg['bottom']


def body_breaks_fvg(candle, fvg, stype):
    body_top    = max(candle['open'], candle['close'])
    body_bottom = min(candle['open'], candle['close'])
    if stype == "Long":
        return body_bottom < fvg['bottom'] and body_top > fvg['bottom']
    else:
        return body_top > fvg['top'] and body_bottom < fvg['top']


def wick_only_touch(candle, fvg, stype):
    body_top    = max(candle['open'], candle['close'])
    body_bottom = min(candle['open'], candle['close'])
    if stype == "Long":
        return candle['low'] <= fvg['bottom'] and body_bottom >= fvg['bottom']
    else:
        return candle['high'] >= fvg['top'] and body_top <= fvg['top']


# ============================================================
# FUNGSI ORDER — FIX #6: round qty & price ke spec Bybit
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
# CEK TREN H1 BERUBAH — FIX #3: logic diperbaiki
# ============================================================

def h1_trend_broken(curr_h1, setup, sh_h1, sl_h1):
    """
    FIX #3: Setup batal jika harga melewati TP (swing terlampaui searah BOS).
    - Long  : harga tembus ATAS swing high → TP sudah kena, tidak ada pullback lagi
    - Short : harga tembus BAWAH swing low → TP sudah kena, tidak ada pullback lagi
    Sebelumnya logic terbalik: membatalkan setup valid, membiarkan setup gagal jalan.
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
# REPLAY H1
# ============================================================

def replay_h1(coin, df_h1):
    sh_h1, sl_h1 = find_swings(df_h1, left=8, right=8)
    if not sh_h1 or not sl_h1:
        return None

    closed_h1 = df_h1.iloc[-2]
    is_long  = closed_h1['close'] > sh_h1[-1]['val']
    is_short = closed_h1['close'] < sl_h1[-1]['val']
    if not (is_long or is_short):
        return None

    stype   = "Long" if is_long else "Short"
    ref_idx = sl_h1[-1]['idx'] if is_long else sh_h1[-1]['idx']

    df_snap = df_h1.copy()
    gaps    = get_internal_gaps(df_snap, stype, ref_idx)
    if not gaps:
        return None

    since_bos = df_snap.iloc[ref_idx:]
    tp_val    = since_bos['high'].max() if stype == "Long" else since_bos['low'].min()
    bos_ts    = df_snap['ts'].iloc[ref_idx]
    swing_ts  = sh_h1[-1]['ts'] if stype == "Long" else sl_h1[-1]['ts']

    state = {
        'type': stype, 'df_h1': df_snap,
        'fvg_list': gaps, 'fvg_idx': 0,
        'tp': tp_val, 'bos_ts': bos_ts,
        'swing_ts': swing_ts,
        'phase': "WAIT_FVG_TOUCH", 'fvg_touch_ts': 0,
        'm5_freeze_high': None, 'm5_freeze_low': None, 'm5_freeze_ts': None,
        'idm_list': [], 'idm_touched_val': None,
    }

    fvg_idx      = 0
    fvg_touch_ts = 0
    phase        = "WAIT_FVG_TOUCH"

    candles_after_bos = df_h1.iloc[ref_idx + 1 : -1]

    for _, candle in candles_after_bos.iterrows():
        if fvg_idx >= len(gaps):
            return None
        active_fvg = gaps[fvg_idx]

        if phase == "WAIT_FVG_TOUCH":
            if stype == "Long" and candle['close'] >= tp_val:
                return None
            if stype == "Short" and candle['close'] <= tp_val:
                return None
            if not price_in_fvg(candle['high'], candle['low'], active_fvg):
                continue
            if body_breaks_fvg(candle, active_fvg, stype):
                fvg_idx += 1
                continue
            if wick_only_touch(candle, active_fvg, stype):
                phase        = "WAIT_IDM_TOUCH"
                fvg_touch_ts = candle['ts']
                continue

        elif phase in ("WAIT_IDM_TOUCH", "WAIT_BOS_BREAK", "WAIT_MSS"):
            if stype == "Long" and candle['close'] >= tp_val:
                return None
            if stype == "Short" and candle['close'] <= tp_val:
                return None
            continue

    state['fvg_idx']      = fvg_idx
    state['phase']        = phase
    state['fvg_touch_ts'] = fvg_touch_ts

    print(f"\n📊 {coin} : BOS {stype}  | H:{sh_h1[-1]['val']}  L:{sl_h1[-1]['val']}")
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
# CORE LOOP — FIX #4: WAIT_MSS kini tercapai dengan benar
# ============================================================

def run_bot():
    print("🚀 SNIPER V4 | SMC FULL LOGIC | FIXED")
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

                sh_h1, sl_h1 = find_swings(df_h1_live, left=8, right=8)
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

                    # ── PHASE 1: TUNGGU FVG H1 DIWICK ────────────────
                    if setup['phase'] == "WAIT_FVG_TOUCH":
                        if not price_in_fvg(closed_h1['high'], closed_h1['low'], active_fvg):
                            if stype == "Long" and curr_h1['close'] >= setup['tp']:
                                print(f"🗑️ {coin}: TP kena sebelum FVG."); del pending[coin]
                            elif stype == "Short" and curr_h1['close'] <= setup['tp']:
                                print(f"🗑️ {coin}: TP kena sebelum FVG."); del pending[coin]
                            continue

                        if body_breaks_fvg(closed_h1, active_fvg, stype):
                            print(f"❌ {coin}: FVG {fvg_idx+1} ditembus body → coba berikutnya.")
                            pending[coin]['fvg_idx'] += 1
                            continue

                        if wick_only_touch(closed_h1, active_fvg, stype):
                            print(f"✅ {coin}: FVG {fvg_idx+1} diwick. Masuk M5.")
                            pending[coin]['phase']        = "WAIT_IDM_TOUCH"
                            pending[coin]['fvg_touch_ts'] = closed_h1['ts']
                        continue

                    # ── AMBIL DATA M5 ─────────────────────────────────
                    time.sleep(1)
                    df_m5_live = get_data(coin, "5", limit=200)
                    if df_m5_live is None: continue

                    swing_ts = setup.get('swing_ts', setup['bos_ts'])
                    df_m5    = df_m5_live[df_m5_live['ts'] >= swing_ts].reset_index(drop=True)
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
                        print(f"   → Target BOS M5 : {freeze_low if stype=='Long' else freeze_high}")
                        print(f"   → Target MSS    : {freeze_high if stype=='Long' else freeze_low}")

                        pending[coin]['phase']           = "WAIT_BOS_BREAK"
                        pending[coin]['idm_touched_val'] = idm_level
                        pending[coin]['m5_freeze_high']  = freeze_high
                        pending[coin]['m5_freeze_low']   = freeze_low
                        pending[coin]['m5_freeze_ts']    = freeze_ts
                        continue

                    # ── PHASE 3: TUNGGU BOS BREAK ─────────────────────
                    # FIX #4: Setelah BOS M5 → masuk WAIT_MSS (bukan balik WAIT_IDM_TOUCH)
                    if setup['phase'] == "WAIT_BOS_BREAK":
                        freeze_low  = setup['m5_freeze_low']
                        freeze_high = setup['m5_freeze_high']
                        freeze_ts   = setup['m5_freeze_ts']

                        df_after = df_m5[df_m5['ts'] > freeze_ts]
                        if df_after.empty:
                            continue

                        bos_broken    = False
                        bos_candle_ts = None

                        for _, c in df_after.iterrows():
                            if stype == "Long" and c['close'] < freeze_low:
                                bos_broken    = True
                                bos_candle_ts = c['ts']
                                print(f"📉 {coin}: BOS Bearish M5 @ {c['close']}. Masuk WAIT_MSS.")
                                break
                            elif stype == "Short" and c['close'] > freeze_high:
                                bos_broken    = True
                                bos_candle_ts = c['ts']
                                print(f"📈 {coin}: BOS Bullish M5 @ {c['close']}. Masuk WAIT_MSS.")
                                break

                        if bos_broken:
                            # FIX #4: Set WAIT_MSS, update freeze range dari zona BOS baru
                            df_after_bos    = df_m5[df_m5['ts'] > freeze_ts]
                            new_freeze_high = df_after_bos['high'].max() if not df_after_bos.empty else freeze_high
                            new_freeze_low  = df_after_bos['low'].min()  if not df_after_bos.empty else freeze_low

                            pending[coin]['phase']           = "WAIT_MSS"
                            pending[coin]['swing_ts']        = bos_candle_ts
                            pending[coin]['m5_freeze_high']  = new_freeze_high
                            pending[coin]['m5_freeze_low']   = new_freeze_low
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
                        if df_after.empty:
                            continue

                        mss_candle   = None
                        reset_to_idm = False

                        for _, c in df_after.iterrows():
                            if stype == "Long":
                                if c['close'] > freeze_high:
                                    mss_candle = c; break
                                elif c['close'] < freeze_low:
                                    reset_to_idm = True
                                    print(f"🔄 {coin}: Break bawah lagi. Cari IDM baru.")
                                    pending[coin].update({
                                        'swing_ts': c['ts'], 'phase': "WAIT_IDM_TOUCH",
                                        'm5_freeze_high': None, 'm5_freeze_low': None, 'm5_freeze_ts': None
                                    }); break
                            else:
                                if c['close'] < freeze_low:
                                    mss_candle = c; break
                                elif c['close'] > freeze_high:
                                    reset_to_idm = True
                                    print(f"🔄 {coin}: Break atas lagi. Cari IDM baru.")
                                    pending[coin].update({
                                        'swing_ts': c['ts'], 'phase': "WAIT_IDM_TOUCH",
                                        'm5_freeze_high': None, 'm5_freeze_low': None, 'm5_freeze_ts': None
                                    }); break

                        if reset_to_idm or mss_candle is None:
                            if not reset_to_idm:
                                if stype == "Long" and curr_m5['close'] >= setup['tp']:
                                    print(f"🗑️ {coin}: TP kena tanpa MSS."); del pending[coin]
                                elif stype == "Short" and curr_m5['close'] <= setup['tp']:
                                    print(f"🗑️ {coin}: TP kena tanpa MSS."); del pending[coin]
                            continue

                        # MSS confirmed — cek zona FVG H1
                        entry_fvg   = None
                        entry_price = None
                        for fvg in fvg_list:
                            if price_in_fvg(mss_candle['high'], mss_candle['low'], fvg):
                                entry_fvg   = fvg
                                entry_price = fvg['top'] if stype == "Long" else fvg['bottom']
                                break

                        if entry_fvg is None:
                            print(f"⏳ {coin}: MSS di luar FVG H1. Cari IDM lagi.")
                            pending[coin].update({
                                'phase': "WAIT_IDM_TOUCH",
                                'm5_freeze_high': None, 'm5_freeze_low': None, 'm5_freeze_ts': None
                            })
                            continue

                        sl_price   = mss_candle['low'] if stype == "Long" else mss_candle['high']
                        side_order = "Buy" if stype == "Long" else "Sell"

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

                df_h1_snap = df_h1_live.copy()
                gaps       = get_internal_gaps(df_h1_snap, stype, ref_idx)
                if not gaps:
                    print(f"⚠️ {coin}: BOS {stype} tapi tidak ada FVG.")
                    continue

                since_bos = df_h1_snap.iloc[ref_idx:]
                tp_val    = since_bos['high'].max() if stype == "Long" else since_bos['low'].min()
                swing_ts  = sh_h1[-1]['ts'] if stype == "Long" else sl_h1[-1]['ts']

                pending[coin] = {
                    'type': stype, 'df_h1': df_h1_snap,
                    'fvg_list': gaps, 'fvg_idx': 0,
                    'tp': tp_val, 'bos_ts': df_h1_snap['ts'].iloc[ref_idx],
                    'swing_ts': swing_ts,
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
