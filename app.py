import streamlit as st
import pandas as pd
import numpy as np
import datetime as dt
import pyotp
from SmartApi.smartConnect import SmartConnect
import plotly.graph_objects as go

# Config
st.set_page_config(page_title="📈 TRIYAM", layout="wide")
st.title("📊 Advanced Stock Dashboard – Volume | Price | Money Flow")

# Angel One Login
api_key = st.secrets["API_KEY"]
client_id = st.secrets["CLIENT_ID"]
password = st.secrets["PASSWORD"]
totp_secret = st.secrets["TOTP_SECRET"]

try:
    totp = pyotp.TOTP(totp_secret).now()
    obj = SmartConnect(api_key=api_key)
    session_data = obj.generateSession(client_id, password, totp)
    st.success("✅ Angel One Login Successful")
except Exception as e:
    st.error(f"❌ Login Failed: {e}")
    st.stop()

# ------------------- STOCK LIST -------------------
stock_list = {
    "RELIANCE": "2885",
    "POLYCAB": "9590",
    "TCS": "11536",
    "INFY": "1594",
    "COCHINSHIP": "21508",
    "MAZDOCK": "509",
    "irfc":"1100234",
    "indigo":"11195",
    "keyfinsev": "4157",
    "NACL":"20425",
    "suzlon":"12018",
    "dixcon":"21690",
    "ofss":"10738",
    "forcemotors":"11573","20MICRONS": "16921", "21STCENMGM": "4", "3IINFOTECH": "11774", "3MINDIA": "474", "3PLAND": "2595",
    "5PAISA": "445", "63MOONS": "11868", "A2ZINFRA": "20906", "AAKASH": "235", "AARON": "1030",
    "AARTIDRUGS": "4481", "AARTIIND": "7", "AARVEEDEN": "13771", "AARVI": "19073", "AAVAS": "5385",
    "ABAN": "10", "ABB": "13", "ABBOTINDIA": "17903", "ABCAPITAL": "21614", "ABFRL": "30108",
    "ABSLBANETF": "13987", "ABSLNN50ET": "7339", "ACC": "22", "ACCELYA": "14018", "ACE": "560",
    "ADANIENT": "25", "ADANIGREEN": "9123", "ADANIPORTS": "15083", "ADANIPOWER": "3456", "ADANITRANS": "16338",
    "ADORWELD": "336", "ADROITINFO": "14339", "ADVANIHOTR": "281", "ADVENZYMES": "17233", "AEGISCHEM": "522",
    "AFFLE": "23633", "AGARIND": "19490", "AGCNET": "19993", "AGRITECH": "1434", "AHLADA": "35118",
    "AHLEAST": "14023", "AHLUCONT": "1343", "AIAENG": "179", "AIRAN": "18263", "AJANTPHARM": "13089",
    "AJMERA": "911", "AKASH": "14289", "AKZOINDIA": "163", "ALANKIT": "17057", "ALBERTDAVD": "889",
    "ALEMBICLTD": "390", "ALICON": "14904", "ALKALI": "678", "ALKEM": "21808", "ALKYLAMINE": "231",
    "ALLCARGO": "694", "ALLSEC": "15843", "ALMONDZ": "12608", "ALOKINDS": "907", "ALPA": "247",
    "ALPHAGEO": "938", "AMARAJABAT": "509", "AMBER": "22280", "AMBICAAGAR": "267", "AMBICAFIN": "20914",
    "AMBITECH": "18308", "AMBUJACEM": "24", "AMDIND": "17391", "AMJLAND": "1985", "AMRUTANJAN": "1321",
    "ANANTRAJ": "3139", "ANDHRACEMT": "1243", "ANDHRAPAP": "13814", "ANDHRSUGAR": "713", "ANDREWYU": "657",
    "ANGELBRKG": "23673", "ANIKINDS": "1094", "ANKITMETAL": "14379", "ANSALAPI": "1114", "ANSALHSG": "1046",
    "ANTGRAPHIC": "1864", "ANUP": "28039", "ANURAS": "30188", "APARINDS": "835", "APCL": "13769",
    "APCOTEXIND": "784", "APEX": "14511", "APLAPOLLO": "15836", "APLLTD": "15764", "APOLLO": "1185",
    "APOLLOHOSP": "157", "APOLLOPIPE": "28846", "APOLLOTYRE": "26", "APTECHT": "515", "APTUS": "28883",
    "ARCHIDPLY": "2364", "ARCHIES": "1241", "ARE&M": "1044", "AREMIND": "1572", "ARIES": "23765",
    "ARIHANTCAP": "14384", "ARIHANTSUP": "17298", "ARMANFIN": "17464", "AROGRANITE": "1830", "ARROWGREEN": "29278","RITES":"3761", "ARSHIYA": "10498", "ARSSINFRA": "13334", "ARVIND": "1232", "ARVINDFASN": "30394", "ASAHIINDIA": "1260",
    "ASAHISONG": "353", "ASAL": "1172", "ASALCBR": "17823", "ASHAPURMIN": "1096", "ASHIANA": "1003",
    "ASHIMASYN": "1270", "ASHOKA": "13441", "ASHOKLEY": "27", "ASIANENE": "340", "ASIANPAINT": "31",
    "ASIANTILES": "14053", "ASPINWALL": "1088", "ASTEC": "13755", "ASTERDM": "24557", "ASTRAL": "17967",
    "ASTRAMICRO": "273", "ASTRAZEN": "175", "ASTRON": "13944", "ATFL": "1204", "ATGL": "29025",
    "ATLANTA": "1006", "ATUL": "274", "ATULAUTO": "14363", "AUBANK": "21621", "AURIONPRO": "1016",
    "AUROPHARMA": "275", "AURUM": "4226", "AURUMPP": "4227", "AUSOMENT": "1724", "AUTOAXLES": "1472",
    "AUTOIND": "12517", "AUTOLITIND": "1069", "AVADHSUGAR": "27503", "AVANTIFEED": "15564", "AVTNPL": "1007",
    "AWHCL": "29284", "AXISBANK": "14", "AXISCADES": "17810", "AYMSYNTEX": "998", "AZAD": "4241",
    "BAGFILMS": "688", "BAJAJ-AUTO": "25", "BAJAJCON": "22904", "BAJAJELEC": "1029", "BAJAJFINSV": "11373",
    "BAJAJHCARE": "23182", "BAJAJHIND": "865", "BAJAJHLDNG": "1196", "BAJFINANCE": "317", "BALAJITELE": "1074",
    "BALAMINES": "1198", "BALAXI": "26398", "BALKRISHNA": "359", "BALKRISIND": "11240", "BALLARPUR": "9116",
    "BALMLAWRIE": "436", "BALPHARMA": "1570", "BALRAMCHIN": "770", "BANARBEADS": "1262", "BANARISUG": "1333",
    "BANCOINDIA": "1317", "BANDHANBNK": "18245", "BANG": "2010", "BANKA": "10129", "BANKBARODA": "466",
    "BANKINDIA": "459", "BANSWRAS": "1511", "BARBEQUE": "29763", "BASF": "392", "BASML": "1531",
    "BATAINDIA": "35", "BAYERCROP": "98", "BBL": "14024", "BBTC": "3170", "BCG": "5045",
    "BCLIND": "15369", "BCONCEPTS": "27649", "BCP": "2026", "BDL": "2144", "BDR": "21653",
    "BEARDSELL": "1341", "BECTORFOOD": "30129", "BEDMUTHA": "14348", "BEL": "5224", "BEML": "150",
    "BEPL": "12720", "BERGEPAINT": "519", "BESTAGRO": "27918", "BFINVEST": "19595", "BFUTILITIE": "12731",
    "BGRENERGY": "1829", "BHAGERIA": "15497", "BHAGCHEM": "23441", "BHAGYANGR": "1205", "BHANDARI": "13094",
    "BHARATFORG": "1223", "BHARATRAS": "156", "BHARATWIRE": "27971", "BHARTIARTL": "10604", "BHEL": "438",
    "BIGBLOC": "27647", "BIL": "1906", "BILENERGY": "15059", "BINANIIND": "1111", "BIOCON": "14413", "BIRLACABLE": "12385", "BIRLACORPN": "349", "BIRLAMONEY": "572", "BIRLATYRE": "3194", "BKMINDST": "13159",
    "BLBLIMITED": "24294", "BLISSGVS": "16125", "BLKASHYAP": "11047", "BLS": "17279", "BLUEDART": "1782",
    "BLUESTARCO": "161", "BODALCHEM": "15862", "BOMDYEING": "187", "BOROLTD": "2743", "BORORENEW": "4134",
    "BOSCHLTD": "177", "BPCL": "471", "BPL": "211", "BRFL": "1220", "BRIGADE": "1135",
    "BRITANNIA": "547", "BROOKS": "2933", "BSE": "20858", "BSHSL": "27567", "BSL": "1902",
    "BSOFT": "5258", "BURNPUR": "1923", "BUTTERFLY": "16528", "BVCL": "12828", "BYKE": "13551",
    "CADILAHC": "202", "CALSOFT": "1513", "CAMLINFINE": "15490", "CANBK": "482", "CANDC": "11434",
    "CANFINHOME": "1815", "CANTABIL": "14299", "CAPACITE": "27812", "CAPLIPOINT": "17891", "CAPTRUST": "20863",
    "CARBORUNIV": "193", "CAREERP": "23683", "CARERATING": "17094", "CASTROLIND": "1771", "CCCL": "12595",
    "CCHHL": "14431", "CCL": "13412", "CDSL": "20621", "CEATLTD": "2371", "CELEBRITY": "22752",
    "CENTENKA": "371", "CENTEXT": "1332", "CENTRALBK": "4719", "CENTRUM": "14271", "CENTUM": "13421",
    "CENTURYPLY": "13228", "CENTURYTEX": "269", "CERA": "1153", "CEREBRAINT": "10117", "CESC": "1720",
    "CGCL": "29341", "CGPOWER": "11723", "CHALET": "29428", "CHAMBLFERT": "1049", "CHEMBOND": "1040",
    "CHEMCON": "29706", "CHEMFAB": "28793", "CHEMPLASTS": "30268", "CHENNPETRO": "404", "CHEVIOT": "1331",
    "CHOLAFIN": "705", "CHOLAHLDNG": "18573", "CIGNITITEC": "11185", "CINELINE": "15346", "CINEVISTA": "1853",
    "CIPLA": "434", "CLEAN": "28575", "CLEDUCATE": "20648", "CLNINDIA": "4743", "CMSINFO": "30236",
    "COALINDIA": "20374", "COASTCORP": "14157", "COFFEEDAY": "21776", "COLPAL": "151",
    "COMPINFO": "14925", "COMPUSOFT": "12828", "CONCOR": "1660", "CONFIPET": "10093", "CONTROLPR": "1306",
    "CORALFINAC": "1837", "CORDSCABLE": "12106", "COROMANDEL": "488", "COSMOFILMS": "933", "COUNCODOS": "12218",
    "COX&KINGS": "11684", "CRAFTSMAN": "29282", "CREATIVEYE": "1454", "CREDITACC": "27509", "CREST": "12194",
    "CRISIL": "1601", "CROMPTON": "22901", "CSBBANK": "22265", "CUB": "542", "CUBEXTUB": "1903",
    "CUMMINSIND": "1104", "CUPID": "18520", "CYBERMEDIA": "15915", "CYBERTECH": "10241", "CYIENT": "12541","VTL":"2073","ZENTEC":"7508","saregamA":"4892","SHAKTIPUMP":"25574",
     "SWANENERGY-EQ":"27095","Nifty50":"99926046"
}

# ------------------- UI SELECTION -------------------
stock_name = st.selectbox("📌 Select Stock", list(stock_list.keys()))
interval = st.selectbox("🕒 Select Interval", [
    "ONE_MINUTE", "FIVE_MINUTE", "FIFTEEN_MINUTE", "THIRTY_MINUTE", "ONE_HOUR", "ONE_DAY"
])
from_date = st.date_input("📆 From Date", dt.date.today() - dt.timedelta(days=5))
to_date = st.date_input("📆 To Date", dt.date.today())

if from_date > to_date:
    st.warning("⚠️ 'From Date' cannot be after 'To Date'")
    st.stop()

# ------------------- FETCH OHLC DATA -------------------
def fetch_ohlc_data(symbol, interval, from_date, to_date):
    try:
        params = {
            "exchange": "NSE",
            "symboltoken": stock_list[symbol],
            "interval": interval,
            "fromdate": from_date.strftime('%Y-%m-%d %H:%M'),
            "todate": to_date.strftime('%Y-%m-%d %H:%M')
        }
        response = obj.getCandleData(params)
        if response['status'] != True or 'data' not in response:
            return None
        data = pd.DataFrame(response['data'], columns=["timestamp", "open", "high", "low", "close", "volume"])
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        data[['open', 'high', 'low', 'close', 'volume']] = data[['open', 'high', 'low', 'close', 'volume']].astype(float)
        return data
    except Exception as e:
        st.error(f"Data fetch failed: {e}")
        return None

df = fetch_ohlc_data(stock_name, interval, from_date, to_date)
if df is None or df.empty:
    st.warning("⚠️ No data available.")
    st.stop()

# ------------------- CMF CALCULATION -------------------
def calculate_cmf(df, period=20):
    mf = ((df['close'] - df['low']) - (df['high'] - df['close'])) / (df['high'] - df['low'])
    mf = mf.replace([np.inf, -np.inf], 0).fillna(0)
    mf_volume = mf * df['volume']
    df['cmf'] = mf_volume.rolling(window=period).sum() / df['volume'].rolling(window=period).sum()
    df = df.dropna()
    return df

df = calculate_cmf(df)

# ------------------- DIVERGENCE DETECTION -------------------
df['cmf_diff'] = df['cmf'].diff()
df['price_diff'] = df['close'].diff()
df['divergence'] = (df['cmf_diff'] * df['price_diff']) < 0

# ------------------- PLOT FUNCTIONS -------------------
def plot_3d_animated(df):
    fig = go.Figure()
    fig.add_trace(go.Scatter3d(
        x=df['volume'],
        y=df['close'],
        z=df['cmf'],
        mode='lines+markers',
        marker=dict(size=5, color=df['cmf'], colorscale='Viridis', opacity=0.9),
        line=dict(width=2, color='blue'),
        text=df['timestamp'].astype(str)
    ))
    fig.update_layout(scene=dict(
        xaxis_title="Volume",
        yaxis_title="Price",
        zaxis_title="Money Flow (CMF)"
    ), height=750, margin=dict(l=0, r=0, b=0, t=30))
    return fig

def plot_2d(df, x_col, y_col, highlight_div=False):
    color = np.where(df['divergence'], 'red', 'blue') if highlight_div else 'blue'
    fig = go.Figure(data=go.Scatter(x=df[x_col], y=df[y_col],
                                    mode='markers+lines',
                                    marker=dict(color=color)))
    fig.update_layout(xaxis_title=x_col.capitalize(), yaxis_title=y_col.capitalize())
    return fig

# ------------------- STREAMLIT TABS -------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 3D Chart", "📉 Price vs CMF", "📊 Volume vs CMF", "🚨 Divergence Alerts"
])

with tab1:
    st.plotly_chart(plot_3d_animated(df), use_container_width=True)

with tab2:
    st.plotly_chart(plot_2d(df, 'close', 'cmf'), use_container_width=True)

with tab3:
    st.plotly_chart(plot_2d(df, 'volume', 'cmf'), use_container_width=True)

with tab4:
    st.write("🔴 Red points show divergence (Price & CMF moving opposite).")
    st.plotly_chart(plot_2d(df, 'timestamp', 'close', highlight_div=True), use_container_width=True)
