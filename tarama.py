import datetime
import numpy as np
import pandas as pd
import requests
import yfinance as yf

# --- TELEGRAM BİLGİLERİNİZ ---
TELEGRAM_TOKEN = "8917483658:AAFOboAEz8Pgz0fUdXRFZI0gNd5bOGdI1eY"
TELEGRAM_CHAT_ID = "304934692"


# --- 1. TÜM BIST HİSSE KODLARINI OTOMATİK ÇEKME ---
def tum_bist_hisselerini_getir():
    try:
        url = "https://www.isyatirim.com.tr/_layouts/15/IsYatirim.MarketData/Common.aspx/GetHisseList"
        res = requests.get(url, timeout=10).json()
        hisseler = [item["code"] + ".IS" for item in res["d"]]
        return list(set(hisseler))
    except Exception:
        print("İş Yatırım listesi çekilemedi.")
        return []


# --- 2. SAF ADX / DMI HESAPLAMA FONKSİYONU ---
def adx_hesapla(df, n=14):
    high = df["High"]
    low = df["Low"]
    close = df["Close"]

    up = high - high.shift(1)
    down = low.shift(1) - low

    plus_dm = np.where((up > down) & (up > 0), up, 0.0)
    minus_dm = np.where((down > up) & (down > 0), down, 0.0)

    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    # Wilder's Smoothing
    tr_s = pd.Series(tr).ewm(alpha=1 / n, adjust=False).mean()
    p_dm_s = pd.Series(plus_dm).ewm(alpha=1 / n, adjust=False).mean()
    m_dm_s = pd.Series(minus_dm).ewm(alpha=1 / n, adjust=False).mean()

    plus_di = 100 * (p_dm_s / tr_s)
    minus_di = 100 * (m_dm_s / tr_s)

    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    adx = dx.ewm(alpha=1 / n, adjust=False).mean()

    return adx, plus_di, minus_di


# --- 3. TELEGRAM MESAJ FONKSİYONU ---
def telegram_mesaj_gonder(mesaj):
    if (
        TELEGRAM_TOKEN == "BURAYA_TELEGRAM_TOKEN_YAZIN"
        or not TELEGRAM_TOKEN
    ):
        print("Telegram bilgisi eksik.")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mesaj, "parse_mode": "HTML"}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Telegram hatası: {e}")


# --- 4. TARAMA MOTORU ---
def adx_tarama_yap():
    bist_hisseleri = tum_bist_hisselerini_getir()

    if not bist_hisseleri:
        print("Hisse listesi alınamadı.")
        return

    print(f"Toplam {len(bist_hisseleri)} BIST hissesi taranıyor...")

    al_sinyali_verenler = []

    for ticker in bist_hisseleri:
        try:
            df = yf.download(ticker, period="60d", interval="1d", progress=False)
            if df.empty or len(df) < 30:
                continue

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Saf ADX hesaplamamız
            adx, plus_di, minus_di = adx_hesapla(df, n=14)

            adx_bugun = adx.iloc[-1]
            adx_dun = adx.iloc[-2]
            plus_di_bugun = plus_di.iloc[-1]
            minus_di_bugun = minus_di.iloc[-1]

            # --- SAF ADX ALIM ŞARTLARINIZ ---
            adx_keser_15 = (adx_dun < 15) and (adx_bugun >= 15)
            adx_kucuk_25 = adx_bugun < 25
            plus_buyuk_minus = plus_di_bugun > minus_di_bugun
            minus_kucuk_20 = minus_di_bugun < 20

            if (
                adx_keser_15
                and adx_kucuk_25
                and plus_buyuk_minus
                and minus_kucuk_20
            ):
                hisse_kodu = ticker.replace(".IS", "")
                al_sinyali_verenler.append(hisse_kodu)

        except Exception:
            continue

    # --- TELEGRAM RAPORU ---
    bugun = datetime.date.today().strftime("%d.%m.%Y")
    if al_sinyali_verenler:
        mesaj = f"🚀 <b>BIST ADX Erken Patlama Sinyali ({bugun})</b>\n\n"
        mesaj += f"Taranan Hisse Sayısı: {len(bist_hisseleri)}\n\n"
        mesaj += "<b>Şartları Sağlayan Hisseler:</b>\n"
        for h in sorted(al_sinyali_verenler):
            mesaj += f"• <b>{h}</b>\n"
    else:
        mesaj = f"ℹ️ <b>BIST ADX Tarama Raporu ({bugun})</b>\n\nTaranan {len(bist_hisseleri)} hisse içinden bugün şartı sağlayan çıkmadı."

    telegram_mesaj_gonder(mesaj)


if __name__ == "__main__":
    adx_tarama_yap()
