import datetime
import numpy as np
import pandas as pd
import requests
import yfinance as yf

# --- TELEGRAM BİLGİLERİNİZ ---
TELEGRAM_TOKEN = "8917483658:AAFOboAEz8Pgz0fUdXRFZI0gNd5bOGdI1eY"
TELEGRAM_CHAT_ID = "304934692"

# --- TÜM BIST HİSSE LİSTESİ (SABİT YEDEK LİSTE) ---
TUM_BIST_HISSELERI = [
    "AAVTUR.IS",
    "ADEL.IS",
    "ADESE.IS",
    "AEFES.IS",
    "AFYON.IS",
    "AGESA.IS",
    "AGHOL.IS",
    "AGROT.IS",
    "AHGAZ.IS",
    "AKBNK.IS",
    "AKCNS.IS",
    "AKFGY.IS",
    "AKFYE.IS",
    "AKGRT.IS",
    "MGROS.IS",
    "AKMGY.IS",
    "AKSA.IS",
    "AKSEN.IS",
    "AKSGY.IS",
    "ALARK.IS",
    "ALBRK.IS",
    "ALCAR.IS",
    "ALCTL.IS",
    "ALFAS.IS",
    "ALGYO.IS",
    "ALKA.IS",
    "ALKIM.IS",
    "ALMAD.IS",
    "ALTNY.IS",
    "ALVES.IS",
    "ANGEN.IS",
    "ANHYT.IS",
    "ANSGR.IS",
    "ARASE.IS",
    "ARCLK.IS",
    "ARDYZ.IS",
    "ARENA.IS",
    "ARSAN.IS",
    "ARTMS.IS",
    "ASELS.IS",
    "ASGYO.IS",
    "ASTOR.IS",
    "ATAGY.IS",
    "ATATP.IS",
    "ATEKS.IS",
    "ATAKP.IS",
    "AUPUR.IS",
    "AVPGY.IS",
    "AVTUR.IS",
    "AYCES.IS",
    "AYDEM.IS",
    "AYGAZ.IS",
    "AZTEK.IS",
    "BAGFS.IS",
    "BAKAB.IS",
    "BALAT.IS",
    "BANVT.IS",
    "BARMA.IS",
    "BASGZ.IS",
    "BAYRK.IS",
    "BEGYO.IS",
    "BERA.IS",
    "BEYAZ.IS",
    "BFREN.IS",
    "BIENY.IS",
    "BIGCHEFS.IS",
    "BIMAS.IS",
    "BINHO.IS",
    "BIOEN.IS",
    "BIZIM.IS",
    "BJKAS.IS",
    "BLCYT.IS",
    "BNTAS.IS",
    "BOBET.IS",
    "BOSSA.IS",
    "BRISA.IS",
    "BRKO.IS",
    "BRKSN.IS",
    "BRKVY.IS",
    "BRLSM.IS",
    "BRMEN.IS",
    "BRSAN.IS",
    "BRYAT.IS",
    "BSOKE.IS",
    "BTCIM.IS",
    "BUCIM.IS",
    "BURCE.IS",
    "BURVA.IS",
    "BVSAN.IS",
    "BYDNR.IS",
    "CANTE.IS",
    "CASA.IS",
    "CATES.IS",
    "CCOLA.IS",
    "CELHA.IS",
    "CEMAS.IS",
    "CEMTS.IS",
    "CMBTN.IS",
    "CMENT.IS",
    "CONSE.IS",
    "COSMO.IS",
    "CRDFA.IS",
    "CRFSA.IS",
    "CUSAN.IS",
    "CVKMD.IS",
    "CWENE.IS",
    "DAGI.IS",
    "DAPGM.IS",
    "DARDL.IS",
    "DENGE.IS",
    "DERHL.IS",
    "DERIM.IS",
    "DESA.IS",
    "DESPC.IS",
    "DEVA.IS",
    "DGGYO.IS",
    "DITAS.IS",
    "DMRGD.IS",
    "DMSAS.IS",
    "DOAS.IS",
    "DOBUR.IS",
    "DOCO.IS",
    "DOGUB.IS",
    "DOHOL.IS",
    "DOKTA.IS",
    "DURDO.IS",
    "DYOBY.IS",
    "DZGYO.IS",
    "EBEBK.IS",
    "ECILC.IS",
    "ECZYT.IS",
    "EDATA.IS",
    "EDIP.IS",
    "EGEEN.IS",
    "EGGUB.IS",
    "EGPRO.IS",
    "EGSER.IS",
    "EKGYO.IS",
    "EKIZ.IS",
    "EKSUN.IS",
    "ELITE.IS",
    "EMKEL.IS",
    "ENKAI.IS",
    "ENJSA.IS",
    "ENSRI.IS",
    "EPLAS.IS",
    "ERCB.IS",
    "EREGL.IS",
    "ERIM.IS",
    "ESCAR.IS",
    "ESCOM.IS",
    "ESEN.IS",
    "ETILR.IS",
    "ETYAT.IS",
    "EUHOL.IS",
    "EUKYO.IS",
    "EUPWR.IS",
    "EUREK.IS",
    "EYGYO.IS",
    "FADE.IS",
    "FENER.IS",
    "FLAP.IS",
    "FMIZP.IS",
    "FORMT.IS",
    "FORTE.IS",
    "FRIGO.IS",
    "FROTO.IS",
    "FZLGY.IS",
    "GARAN.IS",
    "GARFA.IS",
    "GEDIK.IS",
    "GEDZA.IS",
    "GENIL.IS",
    "GENTS.IS",
    "GEREL.IS",
    "GESAN.IS",
    "GIPTA.IS",
    "GLBMD.IS",
    "GLCVY.IS",
    "GLYHO.IS",
    "GMTAS.IS",
    "GOKNR.IS",
    "GOLTS.IS",
    "GOODY.IS",
    "GOZDE.IS",
    "GRNYO.IS",
    "GRSEL.IS",
    "GSDHO.IS",
    "GSRAY.IS",
    "GUBRF.IS",
    "GWIND.IS",
    "GZNMI.IS",
    "HALKB.IS",
    "HATEK.IS",
    "HATSN.IS",
    "HEDEF.IS",
    "HEKTS.IS",
    "HKTM.IS",
    "HOLDR.IS",
    "HUBVC.IS",
    "HUNER.IS",
    "HURGZ.IS",
    "ICBCT.IS",
    "IDEAS.IS",
    "IDGYO.IS",
    "IEYHO.IS",
    "IHAAS.IS",
    "IHEVA.IS",
    "IHGZT.IS",
    "IHLGM.IS",
    "IHLAS.IS",
    "INGRM.IS",
    "INTEM.IS",
    "INVEO.IS",
    "INVES.IS",
    "ISATR.IS",
    "ISBTR.IS",
    "ISCTR.IS",
    "ISDMR.IS",
    "ISFIN.IS",
    "ISGSY.IS",
    "ISGYO.IS",
    "ISMEN.IS",
    "ISSEN.IS",
    "IZENR.IS",
    "IZFAS.IS",
    "IZINV.IS",
    "IZMDC.IS",
    "JANTS.IS",
    "KFEIN.IS",
    "KAPLM.IS",
    "KAREL.IS",
    "KARSN.IS",
    "KARTN.IS",
    "KATMR.IS",
    "KAYSE.IS",
    "KBORU.IS",
    "KCAER.IS",
    "KCHOL.IS",
    "KENT.IS",
    "KRVGD.IS",
    "KLGYO.IS",
    "KLMSN.IS",
    "KLNMA.IS",
    "KLRHO.IS",
    "KLSER.IS",
    "KLYSN.IS",
    "KMPUR.IS",
    "KONTR.IS",
    "KONYA.IS",
    "KORDS.IS",
    "KOZAL.IS",
    "KOZAA.IS",
    "KRDMD.IS",
    "KRONT.IS",
    "KTLEV.IS",
    "KUTPO.IS",
    "KSTUR.IS",
    "KUPDA.IS",
    "LIDER.IS",
    "LKMNH.IS",
    "LMKDC.IS",
    "LOGO.IS",
    "LRVHO.IS",
    "LUKSK.IS",
    "MAALT.IS",
    "MACKO.IS",
    "MAKIM.IS",
    "MAKTK.IS",
    "MANAS.IS",
    "MARKA.IS",
    "MAVI.IS",
    "MEDTR.IS",
    "MEGAP.IS",
    "MEPET.IS",
    "MERCN.IS",
    "MERIT.IS",
    "MERKO.IS",
    "METRO.IS",
    "MIATK.IS",
    "MHMTR.IS",
    "MIPAZ.IS",
    "MMCAS.IS",
    "MNTZE.IS",
    "MOBTL.IS",
    "MTRKS.IS",
    "MTRYO.IS",
    "MZHLD.IS",
    "NATEN.IS",
    "NETAS.IS",
    "NIBAS.IS",
    "NTHOL.IS",
    "NUGYO.IS",
    "NUHCM.IS",
    "OBAMS.IS",
    "OBASE.IS",
    "ODAS.IS",
    "OFSYM.IS",
    "ONCSM.IS",
    "ORCA.IS",
    "ORGE.IS",
    "ORMA.IS",
    "OSTIM.IS",
    "OTKAR.IS",
    "OYAKC.IS",
    "OYYAT.IS",
    "OZKGY.IS",
    "OZRDN.IS",
    "PAGYO.IS",
    "PAMEL.IS",
    "PARSN.IS",
    "PASEU.IS",
    "PENGD.IS",
    "PENTA.IS",
    "PETKM.IS",
    "PETUN.IS",
    "PGSUS.IS",
    "PINSU.IS",
    "PKENT.IS",
    "PLTUR.IS",
    "PNLSN.IS",
    "PNSUT.IS",
    "POLHO.IS",
    "POLTK.IS",
    "PRKAB.IS",
    "PRKME.IS",
    "PRDGS.IS",
    "PSGYO.IS",
    "QNBFK.IS",
    "QNBFL.IS",
    "QUAGR.IS",
    "RALYH.IS",
    "RAYSG.IS",
    "REEDR.IS",
    "RGYAS.IS",
    "RNPOL.IS",
    "RODRG.IS",
    "ROYAL.IS",
    "RTALB.IS",
    "RUBNS.IS",
    "RYGYO.IS",
    "RYSAS.IS",
    "SAHOL.IS",
    "SAMAT.IS",
    "SANEL.IS",
    "SANFM.IS",
    "SANKO.IS",
    "SARKY.IS",
    "SASA.IS",
    "SAYAS.IS",
    "SDTTR.IS",
    "SEGMN.IS",
    "SEKFK.IS",
    "SEKUR.IS",
    "SELEC.IS",
    "SELVA.IS",
    "SEYKM.IS",
    "SILVR.IS",
    "SISE.IS",
    "SKBNK.IS",
    "SMART.IS",
    "SMRTG.IS",
    "SNAAM.IS",
    "SOKE.IS",
    "SONME.IS",
    "SRVGY.IS",
    "SUNTK.IS",
    "SURGY.IS",
    "SUWEN.IS",
    "TABGD.IS",
    "TARKM.IS",
    "TATEN.IS",
    "TATGD.IS",
    "TAVHL.IS",
    "TCELL.IS",
    "TDGYO.IS",
    "TEKTN.IS",
    "TETMT.IS",
    "TGPKY.IS",
    "THYAO.IS",
    "TKFEN.IS",
    "TKNSA.IS",
    "TLMAN.IS",
    "TMPOL.IS",
    "TMSN.IS",
    "TNZTP.IS",
    "TOASO.IS",
    "TRCAS.IS",
    "TRGYO.IS",
    "TRILC.IS",
    "TSKB.IS",
    "TSPOR.IS",
    "TTKOM.IS",
    "TTRAK.IS",
    "TUCLK.IS",
    "TUPRS.IS",
    "TURGG.IS",
    "TURSG.IS",
    "UFUK.IS",
    "ULAS.IS",
    "ULKER.IS",
    "UNLU.IS",
    "USAK.IS",
    "VAKBN.IS",
    "VAKFN.IS",
    "VAKKO.IS",
    "VBTYZ.IS",
    "VERTU.IS",
    "VERUS.IS",
    "VESBE.IS",
    "VESTL.IS",
    "VKGYO.IS",
    "YAPRK.IS",
    "YATAS.IS",
    "YAYLA.IS",
    "YEOTK.IS",
    "YGGYO.IS",
    "YGYO.IS",
    "YKBNK.IS",
    "YYLGD.IS",
    "ZOREN.IS",
]


# --- 1. SAF ADX / DMI HESAPLAMA FONKSİYONU ---
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

    tr_s = pd.Series(tr).ewm(alpha=1 / n, adjust=False).mean()
    p_dm_s = pd.Series(plus_dm).ewm(alpha=1 / n, adjust=False).mean()
    m_dm_s = pd.Series(minus_dm).ewm(alpha=1 / n, adjust=False).mean()

    plus_di = 100 * (p_dm_s / tr_s)
    minus_di = 100 * (m_dm_s / tr_s)

    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    adx = dx.ewm(alpha=1 / n, adjust=False).mean()

    return adx, plus_di, minus_di


# --- 2. TELEGRAM MESAJ FONKSİYONU ---
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


# --- 3. TARAMA MOTORU ---
def adx_tarama_yap():
    print(f"Toplam {len(TUM_BIST_HISSELERI)} BIST hissesi taranıyor...")

    al_sinyali_verenler = []

    for ticker in TUM_BIST_HISSELERI:
        try:
            df = yf.download(ticker, period="60d", interval="1d", progress=False)
            if df.empty or len(df) < 30:
                continue

            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            adx, plus_di, minus_di = adx_hesapla(df, n=14)

            adx_bugun = adx.iloc[-1]
            adx_dun = adx.iloc[-2]
            plus_di_bugun = plus_di.iloc[-1]
            minus_di_bugun = minus_di.iloc[-1]

            # --- ALIM KOŞULLARI ---
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
        mesaj += f"Taranan Hisse Sayısı: {len(TUM_BIST_HISSELERI)}\n\n"
        mesaj += "<b>Şartları Sağlayan Hisseler:</b>\n"
        for h in sorted(al_sinyali_verenler):
            mesaj += f"• <b>{h}</b>\n"
    else:
        mesaj = f"ℹ️ <b>BIST ADX Tarama Raporu ({bugun})</b>\n\nTaranan {len(TUM_BIST_HISSELERI)} hisse içinden bugün şartı sağlayan çıkmadı."

    telegram_mesaj_gonder(mesaj)


if __name__ == "__main__":
    adx_tarama_yap()
