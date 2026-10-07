
import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
from pathlib import Path
import random
import math

# ============================================================
# MARPOL-SAFE | Intelligent Compliance Management System
# Major Project Prototype
# ============================================================

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "marpol_safe.db"

st.set_page_config(
    page_title="MARPOL-SAFE | Compliance Management",
    page_icon="⚓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown("""
<style>

    /* =========================================================
       MARPOL-SAFE - FIXED UI STYLING
       ========================================================= */

    /* Main application background */
    .stApp {
        background: #f5f8fc !important;
        color: #1f2937 !important;
    }

    /* =========================================================
       FIX INVISIBLE HEADINGS / TEXT
       ========================================================= */

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6 {
        color: #0b2c5c !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4,
    [data-testid="stMarkdownContainer"] h5,
    [data-testid="stMarkdownContainer"] h6 {
        color: #0b2c5c !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    [data-testid="stMarkdownContainer"] p {
        color: #1f2937 !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    [data-testid="stWidgetLabel"] p {
        color: #1f2937 !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    label {
        color: #1f2937 !important;
        visibility: visible !important;
    }

    /* =========================================================
       SIDEBAR
       ========================================================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #071b3a 0%,
            #0b2c5c 100%
        ) !important;
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    /* =========================================================
       BRAND
       ========================================================= */

    .brand {
        font-size: 24px;
        font-weight: 800;
        letter-spacing: .5px;
        color: #0b2c5c !important;
        margin-bottom: 0;
        visibility: visible !important;
    }

    .subtitle {
        color: #64748b !important;
        margin-top: 0;
    }

    /* =========================================================
       METRIC CARDS
       ========================================================= */

    .metric-card {
        background: white !important;
        border: 1px solid #e4eaf2 !important;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 2px 10px rgba(15,23,42,.04);
        min-height: 105px;
        visibility: visible !important;
    }

    .metric-title {
        color: #64748b !important;
        font-size: 13px;
        font-weight: 600;
        visibility: visible !important;
    }

    .metric-value {
        color: #0b2c5c !important;
        font-size: 28px;
        font-weight: 800;
        margin-top: 5px;
        visibility: visible !important;
    }

    .metric-note {
        font-size: 12px;
        color: #64748b !important;
        visibility: visible !important;
    }

    div[data-testid="stMetric"] {
        background: white !important;
        border: 1px solid #e4eaf2 !important;
        padding: 10px;
        border-radius: 10px;
    }

    /* =========================================================
       STATUS
       ========================================================= */

    .status-approved {
        color: #138a45 !important;
        font-weight: 700;
    }

    .status-pending {
        color: #b77900 !important;
        font-weight: 700;
    }

    .status-alert {
        color: #c0392b !important;
        font-weight: 700;
    }

    /* =========================================================
       INFORMATION BOX
       ========================================================= */

    .info-box {
        background: #eef6ff !important;
        border-left: 4px solid #1769aa !important;
        padding: 12px 16px !important;
        border-radius: 8px !important;
        margin: 8px 0 16px 0 !important;

        color: #1f2937 !important;
        font-size: 14px !important;
        line-height: 1.6 !important;

        visibility: visible !important;
        opacity: 1 !important;
    }

    .info-box b {
        color: #0b2c5c !important;
        font-weight: 800 !important;
        visibility: visible !important;
    }

    /* =========================================================
       OFFLINE / ONLINE BOX
       ========================================================= */

    .offline-box {
        background: #fff7df !important;
        border: 1px solid #f2cf63 !important;
        color: #765800 !important;
        padding: 10px 14px;
        border-radius: 8px;
        font-weight: 600;
    }

    .online-box {
        background: #eaf8ef !important;
        border: 1px solid #9dd8b1 !important;
        color: #146b34 !important;
        padding: 10px 14px;
        border-radius: 8px;
        font-weight: 600;
    }

    /* =========================================================
       SMALL TEXT
       ========================================================= */

    .small {
        font-size: 12px;
        color: #64748b !important;
        visibility: visible !important;
    }

    /* =========================================================
       MARPOL-SAFE V2 UI/UX
       ========================================================= */

    .stApp {
        background: linear-gradient(
            135deg,
            #f4f8fc 0%,
            #eef5fb 100%
        ) !important;
    }

    /* =========================================================
       LOGIN
       ========================================================= */

    .login-shell {
        min-height: 82vh;
        display: grid;
        grid-template-columns: 1.1fr .9fr;
        border-radius: 24px;
        overflow: hidden;
        background: #fff;
        box-shadow: 0 20px 60px rgba(7,27,58,.16);
        border: 1px solid #dce7f2;
    }

    .login-visual {
        position: relative;
        min-height: 650px;
        background: #062b52 url('/app/static/ship.svg')
                    center/cover no-repeat;
        overflow: hidden;
    }

    .login-visual:after {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(
            125deg,
            rgba(3,25,51,.94),
            rgba(3,95,126,.48)
        );
    }

    .login-copy {
        position: absolute;
        z-index: 2;
        left: 9%;
        right: 8%;
        top: 16%;
        color: #fff !important;
    }

    .login-copy h1 {
        font-size: 64px;
        letter-spacing: -3px;
        margin: 14px 0 8px;
        font-weight: 900;
        color: #ffffff !important;
    }

    .login-copy h1 span {
        color: #43d7e8 !important;
    }

    .login-copy p {
        font-size: 18px;
        line-height: 1.6;
        color: #d9eef5 !important;
        max-width: 560px;
    }

    .login-tag {
        display: inline-block;
        padding: 9px 14px;
        border: 1px solid rgba(255,255,255,.28);
        border-radius: 24px;
        background: rgba(255,255,255,.08);
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.2px;
        color: #ffffff !important;
    }

    .login-card {
        padding: 55px 10%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        background: #fff !important;
    }

    .login-card h2 {
        font-size: 34px;
        color: #09284b !important;
        margin: 28px 0 4px;
    }

    .login-muted {
        color: #718096 !important;
        margin: 0 0 24px;
    }

    .login-info {
        margin-top: 18px;
        padding: 12px 14px;
        border-radius: 10px;
        background: #eef8fb !important;
        color: #31546b !important;
        font-size: 12px;
        border: 1px solid #d3edf2;
    }

    .login-security {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 18px;
    }

    .security-chip {
        padding: 7px 10px;
        border-radius: 20px;
        background: #f4f7fb !important;
        color: #526579 !important;
        font-size: 10px;
        font-weight: 800;
    }

    /* =========================================================
       VESSEL BANNER
       ========================================================= */

    .vessel-banner {
        background: linear-gradient(
            100deg,
            #062b52,
            #0a7898
        ) !important;
        color: #ffffff !important;
        padding: 16px 20px;
        border-radius: 14px;
        margin: 10px 0 18px;
        box-shadow: 0 8px 24px rgba(6,43,82,.14);
    }

    .vessel-banner b {
        font-size: 18px;
        color: #ffffff !important;
    }

    .vessel-banner span {
        color: #ffffff !important;
    }

    /* =========================================================
       LIVE CLOCK
       ========================================================= */

    .live-clock {
        text-align: right;
        font-weight: 800;
        color: #0b2c5c !important;
        font-size: 13px;
        visibility: visible !important;
    }

    /* =========================================================
       GPS CARD
       ========================================================= */

    .gps-card {
        background: #fff !important;
        border: 1px solid #dce7f2;
        border-radius: 13px;
        padding: 15px;
        box-shadow: 0 3px 14px rgba(15,23,42,.04);
    }

    .gps-value {
        color: #0a7898 !important;
        font-size: 18px;
        font-weight: 900;
    }

    .gps-note {
        font-size: 11px;
        color: #718096 !important;
    }

    /* =========================================================
       PROFILE
       ========================================================= */

    .profile-box {
        background: rgba(255,255,255,.08);
        border: 1px solid rgba(255,255,255,.14);
        border-radius: 12px;
        padding: 12px;
        margin-top: 10px;
    }

    .logout-btn {
        background: #b52f3a !important;
        color: #fff !important;
        border: 0 !important;
    }

    /* =========================================================
       TABS
       ========================================================= */

    button[data-baseweb="tab"] {
        color: #0b2c5c !important;
        visibility: visible !important;
    }

    button[data-baseweb="tab"] p {
        color: #0b2c5c !important;
        visibility: visible !important;
    }

    /* =========================================================
       STREAMLIT EXPANDERS / TEXT
       ========================================================= */

    [data-testid="stExpander"] {
        visibility: visible !important;
    }

    [data-testid="stExpander"] * {
        visibility: visible !important;
    }

    /* =========================================================
       DATAFRAME
       ========================================================= */

    [data-testid="stDataFrame"] {
        visibility: visible !important;
    }

    /* =========================================================
       RESPONSIVE LOGIN
       ========================================================= */

    @media(max-width:900px) {
        .login-shell {
            grid-template-columns: 1fr;
        }

        .login-visual {
            min-height: 390px;
        }

        .login-copy h1 {
            font-size: 45px;
        }

        .login-card {
            padding: 35px 8%;
        }
    }

</style>
""", unsafe_allow_html=True)

ANNEXES = {
    "Annex I - Oil": "Oil",
    "Annex II - NLS": "NLS",
    "Annex III - Packaged": "Packaged",
    "Annex IV - Sewage": "Sewage",
    "Annex V - Garbage": "Garbage",
    "Annex VI - Air": "Air",
}

OPERATIONS = {
    "Annex I - Oil": ["Sludge Discharge", "Bilge/Oily Water Discharge", "Oil Transfer"],
    "Annex II - NLS": ["Cargo Tank Cleaning", "NLS Discharge", "Tank Residue Operation"],
    "Annex III - Packaged": ["Disposal to Port", "Package Transfer", "Cargo Inspection"],
    "Annex IV - Sewage": ["Sewage Discharge", "Sewage Treatment"],
    "Annex V - Garbage": ["Incineration", "Food Waste Disposal", "Garbage Discharge"],
    "Annex VI - Air": ["Fuel Changeover", "Bunker Operation", "Emission Record"],
}

LOCATIONS = ["Arabian Sea", "Mangalore Anchorage", "Mangalore Port", "Singapore", "Bay of Bengal"]


# -----------------------------
# Authentication + vessel state
# -----------------------------
USERS = {
    "chief": {"password":"marpol123", "name":"Chief Engineer", "role":"Chief Engineer"},
    "second": {"password":"marpol123", "name":"Second Engineer", "role":"Second Engineer"},
    "officer": {"password":"marpol123", "name":"Third Officer", "role":"Third Officer"},
    "cadet": {"password":"marpol123", "name":"Deck Cadet", "role":"Deck Cadet"},
}
VESSEL = {
    "name":"MV OCEAN PIONEER", "imo":"9876543", "flag":"India",
    "type":"Oil Tanker", "gt":"45,678 GT", "voyage":"V-2026-001",
    "route":"Mangalore → Singapore", "base_lat":12.5933, "base_lon":74.8718
}


# -----------------------------
# Database
# -----------------------------
def db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    cur = conn.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        record_id TEXT UNIQUE,
        annex TEXT NOT NULL,
        operation TEXT NOT NULL,
        record_date TEXT NOT NULL,
        location TEXT NOT NULL,
        position TEXT,
        quantity REAL DEFAULT 0,
        unit TEXT DEFAULT 'm³',
        equipment TEXT,
        remarks TEXT,
        evidence TEXT DEFAULT 'Pending',
        status TEXT DEFAULT 'Pending',
        created_by TEXT DEFAULT 'Second Engineer',
        submitted_on TEXT,
        reviewed_by TEXT,
        approved_on TEXT,
        synced INTEGER DEFAULT 1,
        created_at TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alert_id TEXT UNIQUE,
        alert_type TEXT,
        message TEXT,
        related_record TEXT,
        alert_date TEXT,
        severity TEXT,
        resolved INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS audit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_time TEXT,
        user_name TEXT,
        role TEXT,
        action TEXT,
        record_id TEXT,
        details TEXT
    );
    """)
    conn.commit()
    conn.close()
    seed_data()

def seed_data():
    conn = db()
    count = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
    if count > 0:
        conn.close()
        return

    base = date(2026, 8, 1)
    samples = [
        ("ORB-I-000087","Annex I - Oil","Sludge Discharge",date(2026,8,9),"Arabian Sea","12°35.6' N, 74°52.3' E",25.0,"m³","OWS-01","Discharged through OWS as per regulation","Uploaded","Approved","Second Engineer","09 Aug 2026 10:20","Chief Engineer","09 Aug 2026 11:05",1),
        ("SRB-IV-0032","Annex IV - Sewage","Sewage Discharge",date(2026,8,9),"Arabian Sea","12°20.1' N, 74°40.2' E",18.0,"m³","Sewage Plant","Treatment completed before discharge","Uploaded","Approved","Second Engineer","09 Aug 2026 10:15","Chief Engineer","09 Aug 2026 10:45",1),
        ("GRB-V-0082","Annex V - Garbage","Food Waste Disposal",date(2026,8,8),"Mangalore Anchorage","12°10.0' N, 74°30.0' E",12.0,"kg","Incinerator","Food waste processed","Uploaded","Approved","Second Engineer","08 Aug 2026 18:42","Chief Engineer","08 Aug 2026 19:05",1),
        ("ORB-I-0056","Annex II - NLS","Cargo Tank Cleaning",date(2026,8,8),"Mangalore Anchorage","12°10.0' N, 74°30.0' E",30.0,"m³","Cargo Pump","Tank cleaning record submitted","Uploaded","Pending","Second Engineer","08 Aug 2026 09:05","","",1),
        ("PRB-III-0021","Annex III - Packaged","Disposal to Port",date(2026,8,7),"Mangalore Port","Mangalore Port",8.0,"kg","Cargo Handling","Transferred to approved reception facility","Uploaded","Approved","Third Officer","07 Aug 2026 16:30","Chief Engineer","07 Aug 2026 17:10",1),
        ("AIR-VI-0044","Annex VI - Air","Fuel Changeover",date(2026,8,6),"Arabian Sea","12°01.2' N, 74°20.0' E",4.0,"m³","Main Engine","Fuel changeover completed","Uploaded","Approved","Second Engineer","06 Aug 2026 13:10","Chief Engineer","06 Aug 2026 14:00",1),
        ("ORB-I-0091","Annex I - Oil","Bilge/Oily Water Discharge",date(2026,8,5),"Arabian Sea","11°50.2' N, 74°10.0' E",20.0,"m³","OWS-01","OWS operation recorded","Pending","Pending","Second Engineer","05 Aug 2026 12:00","","",1),
        ("GRB-V-0089","Annex V - Garbage","Incineration",date(2026,8,4),"Singapore","01°15.2' N, 103°49.0' E",15.0,"kg","Incinerator","Incineration completed","Uploaded","Approved","Third Officer","04 Aug 2026 17:20","Chief Engineer","04 Aug 2026 18:00",1),
    ]

    for s in samples:
        conn.execute("""
            INSERT INTO records
            (record_id,annex,operation,record_date,location,position,quantity,unit,
             equipment,remarks,evidence,status,created_by,submitted_on,reviewed_by,
             approved_on,synced,created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (*s, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    alerts = [
        ("ALT-0003","Error","Oil discharge recorded inside prohibited area","ORB-I-0080","09 Aug 2026 14:28","Error"),
        ("ALT-0002","Warning","Missing evidence for record","SRB-IV-0028","09 Aug 2026 10:15","Warning"),
        ("ALT-0001","Warning","Garbage record not submitted for last 24 hours","GRB-V-0079","08 Aug 2026 19:05","Warning"),
    ]
    for a in alerts:
        conn.execute("""INSERT INTO alerts
            (alert_id,alert_type,message,related_record,alert_date,severity)
            VALUES (?,?,?,?,?,?)""", a)

    audit_rows = [
        ("09 Aug 2026 11:05","Chief Engineer","Chief Engineer","Approved","ORB-I-000087","Record approved after validation"),
        ("09 Aug 2026 10:20","Second Engineer","Second Engineer","Submitted","ORB-I-000087","Record submitted for approval"),
        ("08 Aug 2026 18:42","Third Officer","Third Officer","Created","GRB-V-0082","Garbage operation recorded"),
        ("08 Aug 2026 09:05","Second Engineer","Second Engineer","Submitted","ORB-I-0056","Awaiting review"),
    ]
    for a in audit_rows:
        conn.execute("""INSERT INTO audit
            (event_time,user_name,role,action,record_id,details)
            VALUES (?,?,?,?,?,?)""", a)

    conn.commit()
    conn.close()

def query_df(sql, params=()):
    conn = db()
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df

def execute(sql, params=()):
    conn = db()
    cur = conn.execute(sql, params)
    conn.commit()
    last = cur.lastrowid
    conn.close()
    return last

def add_audit(action, record_id="", details="", user="Chief Engineer", role="Chief Engineer"):
    execute("""INSERT INTO audit(event_time,user_name,role,action,record_id,details)
               VALUES (?,?,?,?,?,?)""",
            (datetime.now().strftime("%d %b %Y %H:%M"), user, role, action, record_id, details))


def live_vessel_position():
    "Realistic prototype GPS feed. Replace with actual onboard GPS/NMEA feed in production."
    # Small deterministic movement around Mangalore/Arabian Sea; does not pretend to be a real GPS sensor.
    t = int(datetime.now().timestamp() // 30)
    lat = VESSEL["base_lat"] + 0.00008 * math.sin(t / 7)
    lon = VESSEL["base_lon"] + 0.00012 * math.cos(t / 9)
    return lat, lon

def dms(lat, lon):
    def one(v, pos, neg):
        a=abs(v); deg=int(a); minutes=(a-deg)*60
        return f"{deg:02d}°{minutes:05.2f}' {pos if v>=0 else neg}"
    return one(lat,'N','S'), one(lon,'E','W')

def login_screen():
    st.markdown('<div class="login-shell">', unsafe_allow_html=True)
    left,right=st.columns([1.1,.9], gap="small")
    with left:
        st.markdown('''<div class="login-visual"><div class="login-copy">
        <div class="login-tag">SHIPBOARD ENVIRONMENTAL COMPLIANCE</div>
        <h1>MARPOL<span>-SAFE</span></h1>
        <p>Intelligent digital compliance management for modern vessels — records, approvals, alerts, analytics and offline synchronization in one shipboard console.</p>
        <div class="login-tag">⚓ ANNEX I — VI &nbsp; • &nbsp; OFFLINE-FIRST &nbsp; • &nbsp; AUDIT READY</div>
        </div></div>''', unsafe_allow_html=True)
    with right:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.markdown('<div class="brand">⚓ MARPOL-SAFE <small>V2.0</small></div>', unsafe_allow_html=True)
        st.markdown('<h2>Welcome aboard</h2><p class="login-muted">Sign in to the shipboard compliance console.</p>', unsafe_allow_html=True)
        with st.form("login_form"):
            username=st.text_input("Username", placeholder="chief / second / officer / cadet")
            password=st.text_input("Password", type="password", placeholder="Enter password")
            submitted=st.form_submit_button("SIGN IN  →", type="primary", use_container_width=True)
        if submitted:
            u=USERS.get(username.strip().lower())
            if u and password==u["password"]:
                st.session_state.authenticated=True
                st.session_state.user=u["name"]
                st.session_state.role=u["role"]
                add_audit("Login","",f"Successful login from {u['role']}",u["name"],u["role"])
                st.rerun()
            else:
                st.error("Invalid credentials. Please try again.")
        st.markdown('<div class="login-info"><b>Demo access</b><br>chief / marpol123 &nbsp; • &nbsp; second / marpol123<br>officer / marpol123 &nbsp; • &nbsp; cadet / marpol123</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-security"><span class="security-chip">🔐 ROLE BASED</span><span class="security-chip">🗃 LOCAL DATABASE</span><span class="security-chip">📡 OFFLINE READY</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------
# Helpers
# -----------------------------
def compliance_score(df):
    if df.empty:
        return 100
    approved = (df["status"] == "Approved").sum()
    pending = (df["status"] == "Pending").sum()
    # Prototype scoring model: approved = full compliance, pending = small deduction.
    return max(0, round(100 - (pending / len(df) * 10)))

def card(title, value, note="", icon=""):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">{icon} {title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)

def status_badge(status):
    cls = "status-approved" if status == "Approved" else "status-pending" if status == "Pending" else "status-alert"
    return f'<span class="{cls}">{status}</span>'

def generate_id(annex):
    prefix = {"Annex I - Oil":"ORB-I","Annex II - NLS":"CRB-II","Annex III - Packaged":"PRB-III",
              "Annex IV - Sewage":"SRB-IV","Annex V - Garbage":"GRB-V","Annex VI - Air":"AIR-VI"}[annex]
    n = random.randint(1000,9999)
    return f"{prefix}-{n:04d}"

# -----------------------------
# Session state
# -----------------------------
if "offline" not in st.session_state:
    st.session_state.offline = False
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user" not in st.session_state:
    st.session_state.user = ""
if "role" not in st.session_state:
    st.session_state.role = ""

init_db()

# Live UI refresh every 30 seconds while logged in.
if st.session_state.authenticated:
    try:
        from streamlit_autorefresh import st_autorefresh
        st_autorefresh(interval=30000, key="marpol_live_refresh")
    except Exception:
        pass

if not st.session_state.authenticated:
    login_screen()
    st.stop()

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.markdown("## ⚓ MARPOL-SAFE")
    st.caption("Intelligent Compliance Management System")
    st.divider()

    pages = [
        "Dashboard",
        "Record an Operation",
        "MARPOL Records",
        "Compliance Alerts",
        "Approval Queue",
        "Reports & Analytics",
        "Audit Trail",
        "MARPOL Library",
        "System Settings",
    ]
    page = st.radio("MAIN MENU", pages, label_visibility="visible")

    st.divider()
    st.markdown("### Vessel")
    st.write(f"🚢 **{VESSEL['name']}**")
    st.caption(f"IMO: {VESSEL['imo']} • {VESSEL['flag']}")
    st.caption(f"{VESSEL['type']} • {VESSEL['gt']}")
    st.caption(f"Voyage: {VESSEL['voyage']}")

    st.divider()
    st.markdown(f"### 👤 {st.session_state.user}")
    st.caption(f"Role: {st.session_state.role}")
    if st.button("↪ Logout", use_container_width=True):
        add_audit("Logout","", "User signed out", st.session_state.user, st.session_state.role)
        st.session_state.authenticated = False
        st.session_state.user = ""
        st.session_state.role = ""
        st.rerun()

    st.divider()
    mode = "OFFLINE" if st.session_state.offline else "ONLINE"
    st.markdown(f"**Connection:** {mode}")
    if st.button("Toggle Online / Offline", use_container_width=True):
        st.session_state.offline = not st.session_state.offline
        st.rerun()

# -----------------------------
# Header
# -----------------------------
c1, c2, c3 = st.columns([5,2.4,2.6])
with c1:
    st.markdown('<div class="brand">MARPOL-SAFE</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Digital MARPOL Compliance Management • Shipboard Prototype</div>', unsafe_allow_html=True)
with c2:
    lat,lon=live_vessel_position()
    lat_s,lon_s=dms(lat,lon)
    st.markdown(f'<div class="gps-card"><div class="small">📍 LIVE VESSEL POSITION</div><div class="gps-value">{lat_s}</div><div class="gps-value">{lon_s}</div><div class="gps-note">Prototype GPS feed • Accuracy target ±0.01 NM</div></div>', unsafe_allow_html=True)
with c3:
    now_live=datetime.now().strftime("%d %b %Y • %H:%M:%S")
    st.markdown(f'<div class="live-clock">🟢 SYSTEM ONLINE<br>{now_live}<br><span class="small">{VESSEL["name"]} • IMO {VESSEL["imo"]}</span></div>', unsafe_allow_html=True)

if st.session_state.offline:
    st.markdown('<div class="offline-box">⚠ Offline Mode — records are stored locally and marked for synchronization when connectivity returns.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="online-box">● Online — local data can be synchronized with shore office.</div>', unsafe_allow_html=True)

lat,lon=live_vessel_position()
lat_s,lon_s=dms(lat,lon)
st.markdown(f'<div class="vessel-banner"><b>🚢 {VESSEL["name"]}</b> &nbsp; • &nbsp; IMO {VESSEL["imo"]} &nbsp; • &nbsp; {VESSEL["type"]}<br><span style="font-size:12px">Voyage {VESSEL["voyage"]} &nbsp; | &nbsp; Route {VESSEL["route"]} &nbsp; | &nbsp; GPS {lat_s}, {lon_s}</span></div>', unsafe_allow_html=True)

# ============================================================
# DASHBOARD
# ============================================================
if page == "Dashboard":
    ship_col, status_col = st.columns([2.2,1])
    with ship_col:
        st.image(str(APP_DIR / "assets" / "ship_dashboard.svg"), use_container_width=True)
    with status_col:
        st.markdown("### Vessel Operations")
        st.write("**Navigation:** Arabian Sea")
        st.write("**Next Port:** Singapore")
        st.write(f"**Latitude:** {lat_s}")
        st.write(f"**Longitude:** {lon_s}")
        st.success("GPS / Compliance feed active")
    df = query_df("SELECT * FROM records ORDER BY record_date DESC")
    alerts = query_df("SELECT * FROM alerts WHERE resolved=0")
    total = len(df)
    approved = int((df.status == "Approved").sum()) if total else 0
    pending = int((df.status == "Pending").sum()) if total else 0
    score = compliance_score(df)

    st.markdown("## Dashboard Overview")
    st.caption("Real-time operational view of vessel MARPOL compliance.")

    cols = st.columns(6)
    metrics = [
        ("Overall Compliance", f"{score}%", "Good • last 7 days", "✓"),
        ("MARPOL Records", total, "This voyage", "▣"),
        ("Open Alerts", len(alerts), "Requires attention", "⚠"),
        ("Pending Approvals", pending, "Awaiting review", "◷"),
        ("Documents", int((df.evidence == "Uploaded").sum()), "Uploaded evidence", "▤"),
        ("Sync Pending", int((df.synced == 0).sum()), "Local records", "↕"),
    ]
    for col, (t,v,n,i) in zip(cols, metrics):
        with col:
            card(t,v,n,i)

    st.write("")
    left, right = st.columns([1.05, 1])
    with left:
        st.markdown("### Vessel Status")
        vessel = pd.DataFrame({
            "Item":["IMO Number","Flag","Ship Type","Current Voyage","Route","Position","Weather","Speed"],
            "Value":["9876543","India","Oil Tanker","V-2026-001","Mangalore → Singapore",
                     "12°35.6' N, 74°52.3' E","28 °C • Light Rain","12.4 Knots"]
        })
        st.dataframe(vessel, hide_index=True, use_container_width=True)
    with right:
        st.markdown("### Annex-wise Compliance")
        annex_rows = []
        for annex in ANNEXES:
            sub = df[df.annex == annex]
            annex_rows.append({
                "Annex": annex,
                "Records": len(sub),
                "Compliance": f"{compliance_score(sub)}%"
            })
        st.dataframe(pd.DataFrame(annex_rows), hide_index=True, use_container_width=True)

    st.markdown("### Recent MARPOL Operations")
    recent = df.head(8)[["record_id","annex","operation","record_date","location","status"]].copy()
    recent.columns = ["Record ID","Annex","Operation","Date","Location","Status"]
    st.dataframe(recent, hide_index=True, use_container_width=True)

    a,b = st.columns(2)
    with a:
        st.markdown("### Monthly MARPOL Activity")
        activity = pd.DataFrame({
            "Category":["Oil operations","Garbage operations","Fuel changes","NLS operations","Sewage events","Other"],
            "Count":[42,31,8,14,9,80]
        }).set_index("Category")
        st.bar_chart(activity)
    with b:
        st.markdown("### Compliance Trend")
        trend = pd.DataFrame({"Compliance":[86,89,92,95,94,96]}, index=["Mar","Apr","May","Jun","Jul","Aug"])
        st.line_chart(trend)

# ============================================================
# RECORD OPERATION
# ============================================================
elif page == "Record an Operation":
    st.markdown("## Record an Operation")
    st.caption("Intelligent wizard: select the MARPOL annex → enter details → validate → submit.")

    steps = ["1. Select Operation","2. System Guidance","3. Enter Details","4. Validate","5. Evidence","6. Submit"]
    st.progress(0.17)
    st.info("Step 1 of 6 — The system automatically determines the applicable record book and required information.")

    annex = st.selectbox("Select Annex / Operation Category", list(ANNEXES.keys()))
    op = st.selectbox("Operation", OPERATIONS[annex])

    guidance = {
        "Annex I - Oil":"Applicable Oil Record Book • Part I / Part II depending on operation.",
        "Annex II - NLS":"Applicable Cargo Record Book and NLS category information.",
        "Annex III - Packaged":"Documentation and package/cargo transfer evidence.",
        "Annex IV - Sewage":"Sewage Record Book and treatment/discharge information.",
        "Annex V - Garbage":"Garbage Record Book and disposal/incineration details.",
        "Annex VI - Air":"Fuel, NOx/SOx and air pollution related records.",
    }
    st.markdown(f'<div class="info-box"><b>System Guidance:</b> {guidance[annex]}<br><br><b>Required:</b> Date & Time • Position • Tank/Space or location • Quantity • Method • Equipment • Supporting evidence where applicable.</div>', unsafe_allow_html=True)

    with st.form("operation_form"):
        c1,c2 = st.columns(2)
        with c1:
            record_date = st.date_input("Date", value=date.today())
            record_time = st.time_input("Time")
            position = st.text_input("Position (Latitude / Longitude)", f"{lat_s}, {lon_s}")
            location = st.selectbox("Location", LOCATIONS)
            quantity = st.number_input("Quantity", min_value=0.0, value=25.0, step=0.5)
        with c2:
            unit = st.selectbox("Unit", ["m³","kg","L","tonnes","hours"])
            equipment = st.text_input("Equipment Used", "OWS-01 / Applicable Equipment")
            discharge = st.selectbox("Method / Operation", OPERATIONS[annex])
            evidence = st.selectbox("Supporting Evidence", ["Uploaded","Pending","Not Applicable"])
            remarks = st.text_area("Remarks", "Operation completed in accordance with applicable MARPOL requirements.")

        st.markdown(f'<div class="info-box"><b>Live position pre-filled:</b> {lat_s}, {lon_s}. In production, connect this field to the vessel GPS/NMEA gateway.</div>', unsafe_allow_html=True)

        st.markdown("**Evidence file (prototype)**")
        uploaded = st.file_uploader("Upload supporting document", type=["pdf","jpg","jpeg","png"], accept_multiple_files=True)

        submitted = st.form_submit_button("Validate & Continue →", type="primary", use_container_width=True)

    if submitted:
        errors = []
        if not position.strip():
            errors.append("Position is required.")
        if quantity <= 0:
            errors.append("Quantity must be greater than zero.")
        if not equipment.strip():
            errors.append("Equipment is required.")
        if evidence == "Uploaded" and not uploaded:
            errors.append("Please upload at least one evidence file or choose Pending.")

        if errors:
            st.error("Validation failed: " + " ".join(errors))
        else:
            rid = generate_id(annex)
            while not query_df("SELECT record_id FROM records WHERE record_id=?", (rid,)).empty:
                rid = generate_id(annex)

            now = datetime.now().strftime("%d %b %Y %H:%M")
            sync_flag = 0 if st.session_state.offline else 1
            status = "Pending"
            execute("""
                INSERT INTO records
                (record_id,annex,operation,record_date,location,position,quantity,unit,
                 equipment,remarks,evidence,status,created_by,submitted_on,synced,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (rid,annex,op,record_date.isoformat(),location,position,quantity,unit,
                  equipment,remarks,evidence,status,st.session_state.user,now,sync_flag,
                  datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            add_audit("Submitted", rid, f"{annex} / {op}", st.session_state.user, st.session_state.user)
            st.session_state["last_record"] = rid
            st.success(f"Validation passed. Record {rid} has been submitted for approval.")
            st.info("Next workflow: Evidence → Chief Engineer approval → Final record.")
            st.rerun()

    if "last_record" in st.session_state:
        st.markdown(f"**Latest record:** `{st.session_state.last_record}`")

# ============================================================
# RECORDS
# ============================================================
elif page == "MARPOL Records":
    st.markdown("## MARPOL Records")
    st.caption("Search, filter and review all shipboard compliance records.")

    c1,c2,c3,c4 = st.columns(4)
    with c1: annex_filter = st.selectbox("Annex", ["All"] + list(ANNEXES.keys()))
    with c2: status_filter = st.selectbox("Status", ["All","Approved","Pending"])
    with c3: date_from = st.date_input("From", value=date(2026,8,1))
    with c4: date_to = st.date_input("To", value=date.today())

    df = query_df("SELECT * FROM records ORDER BY record_date DESC")
    if annex_filter != "All": df = df[df.annex == annex_filter]
    if status_filter != "All": df = df[df.status == status_filter]
    if not df.empty:
        df = df[(pd.to_datetime(df.record_date).dt.date >= date_from) & (pd.to_datetime(df.record_date).dt.date <= date_to)]

    st.write(f"Showing **{len(df)}** records")
    display = df[["record_id","annex","operation","record_date","location","status","evidence","created_by","synced"]].copy()
    display.columns = ["Record ID","Annex","Operation","Date","Location","Status","Evidence","Created By","Synced"]
    st.dataframe(display, hide_index=True, use_container_width=True)

    if not df.empty:
        st.markdown("### Record Details")
        selected = st.selectbox("Select Record", df.record_id.tolist())
        row = df[df.record_id == selected].iloc[0]
        c1,c2 = st.columns(2)
        with c1:
            st.write("**Record ID:**", row.record_id)
            st.write("**Annex:**", row.annex)
            st.write("**Operation:**", row.operation)
            st.write("**Date:**", row.record_date)
            st.write("**Position:**", row.position)
            st.write("**Quantity:**", f"{row.quantity} {row.unit}")
        with c2:
            st.write("**Location:**", row.location)
            st.write("**Equipment:**", row.equipment)
            st.write("**Evidence:**", row.evidence)
            st.write("**Created By:**", row.created_by)
            st.write("**Submitted:**", row.submitted_on)
            st.write("**Status:**", row.status)
        st.write("**Remarks:**", row.remarks)

        if row.status == "Pending":
            if st.button("Approve Selected Record", type="primary"):
                now = datetime.now().strftime("%d %b %Y %H:%M")
                execute("""UPDATE records SET status='Approved', reviewed_by=?, approved_on=? WHERE record_id=?""",
                        (st.session_state.user,now,row.record_id))
                add_audit("Approved", row.record_id, "Record approved after validation", st.session_state.user)
                st.success("Record approved and audit trail updated.")
                st.rerun()

# ============================================================
# ALERTS
# ============================================================
elif page == "Compliance Alerts":
    st.markdown("## Compliance Alerts")
    alerts = query_df("SELECT * FROM alerts WHERE resolved=0 ORDER BY id DESC")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("All Alerts", len(alerts))
    with c2: st.metric("Errors", int((alerts.severity=="Error").sum()))
    with c3: st.metric("Warnings", int((alerts.severity=="Warning").sum()))
    with c4: st.metric("Information", int((alerts.severity=="Information").sum()))

    if alerts.empty:
        st.success("No open compliance alerts.")
    else:
        st.dataframe(alerts[["alert_id","severity","message","related_record","alert_date"]],
                     hide_index=True, use_container_width=True)
        selected = st.selectbox("Resolve Alert", alerts.alert_id.tolist())
        if st.button("Mark as Resolved"):
            execute("UPDATE alerts SET resolved=1 WHERE alert_id=?", (selected,))
            add_audit("Resolved Alert", "", selected, st.session_state.user)
            st.success("Alert resolved.")
            st.rerun()

# ============================================================
# APPROVAL QUEUE
# ============================================================
elif page == "Approval Queue":
    st.markdown("## Approval Queue")
    st.caption("Chief Engineer review workflow for submitted MARPOL records.")

    pending = query_df("SELECT * FROM records WHERE status='Pending' ORDER BY submitted_on DESC")
    approved = query_df("SELECT * FROM records WHERE status='Approved' ORDER BY approved_on DESC")

    a,b,c = st.columns(3)
    with a: st.metric("Pending", len(pending))
    with b: st.metric("Approved", len(approved))
    with c: st.metric("Total Records", len(pending)+len(approved))

    st.markdown("### Pending Approval")
    if pending.empty:
        st.success("Approval queue is clear.")
    else:
        st.dataframe(pending[["record_id","annex","operation","created_by","submitted_on","evidence"]],
                     hide_index=True, use_container_width=True)
        selected = st.selectbox("Review Record", pending.record_id.tolist())
        row = pending[pending.record_id == selected].iloc[0]
        st.markdown(f"**{row.record_id}** • {row.annex} • {row.operation}")
        st.write(f"Quantity: **{row.quantity} {row.unit}** | Location: **{row.location}** | Evidence: **{row.evidence}**")
        c1,c2 = st.columns(2)
        with c1:
            if st.button("✓ Approve Record", type="primary", use_container_width=True):
                now = datetime.now().strftime("%d %b %Y %H:%M")
                execute("""UPDATE records SET status='Approved', reviewed_by=?, approved_on=? WHERE record_id=?""",
                        (st.session_state.user,now,selected))
                add_audit("Approved",selected,"Approved from Approval Queue",st.session_state.user)
                st.success("Approved successfully.")
                st.rerun()
        with c2:
            if st.button("Return for Evidence", use_container_width=True):
                execute("UPDATE records SET evidence='Pending' WHERE record_id=?", (selected,))
                add_audit("Returned",selected,"Returned for supporting evidence",st.session_state.user)
                st.warning("Record returned for evidence.")
                st.rerun()

# ============================================================
# REPORTS
# ============================================================
elif page == "Reports & Analytics":
    st.markdown("## Reports & Analytics")
    st.caption("Management-level compliance reporting for shipboard and shore-office review.")

    df = query_df("SELECT * FROM records")
    st.markdown("### MARPOL Summary Report")
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Total Records", len(df))
    with c2: st.metric("Approved", int((df.status=="Approved").sum()))
    with c3: st.metric("Pending", int((df.status=="Pending").sum()))
    with c4: st.metric("Compliance", f"{compliance_score(df)}%")

    st.markdown("### Monthly MARPOL Activity")
    activity = pd.DataFrame({
        "Category":["Oil operations","Garbage operations","Fuel changes","NLS operations","Sewage events","Other"],
        "Count":[42,31,8,14,9,80]
    })
    st.bar_chart(activity.set_index("Category"))

    st.markdown("### Error Analysis")
    errors = pd.DataFrame({
        "Error Type":["Missing field","Invalid quantity","Missing evidence","Location warning","Approval pending"],
        "Count":[4,2,3,1,5]
    })
    st.bar_chart(errors.set_index("Error Type"))

    st.markdown("### Compliance Trend")
    trend = pd.DataFrame({"Compliance %":[86,89,92,95,94,96]}, index=["Mar","Apr","May","Jun","Jul","Aug"])
    st.line_chart(trend)

    st.markdown("### Export")
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Records CSV", csv, "marpol_records.csv", "text/csv", type="primary")
    st.download_button("Download Report Data", errors.to_csv(index=False).encode(), "compliance_errors.csv", "text/csv")

# ============================================================
# AUDIT TRAIL
# ============================================================
elif page == "Audit Trail":
    st.markdown("## Audit Trail")
    st.caption("Traceability: who created, submitted, reviewed and approved each record.")

    audit = query_df("SELECT * FROM audit ORDER BY id DESC")
    st.dataframe(audit[["event_time","user_name","role","action","record_id","details"]],
                 hide_index=True, use_container_width=True)

    st.markdown("### Example Trace")
    st.code("""
Entry ID: ORB-I-000087

Created by: Second Engineer
Submitted: 09 Aug 2026 10:20
Reviewed by: Chief Engineer
Approved: 09 Aug 2026 11:05
Status: FINAL
""")

# ============================================================
# LIBRARY
# ============================================================
elif page == "MARPOL Library":
    st.markdown("## MARPOL Library")
    st.caption("Structured compliance knowledge base for quick shipboard reference.")

    tabs = st.tabs(list(ANNEXES.keys()))
    library = {
        "Annex I - Oil": ["Regulations","ORB Part I","ORB Part II","Forms","Rules"],
        "Annex II - NLS": ["Regulations","Cargo Record Book","Categories","Rules"],
        "Annex III - Packaged": ["Regulations","Documentation","Rules"],
        "Annex IV - Sewage": ["Regulations","Rules"],
        "Annex V - Garbage": ["Regulations","Garbage Record Book","Rules"],
        "Annex VI - Air": ["Regulations","ODS","Fuel","NOx","SOx","Rules"],
    }
    for tab, annex in zip(tabs, ANNEXES.keys()):
        with tab:
            for item in library[annex]:
                st.markdown(f"**▸ {item}**")
            st.info("Prototype library section. In the final deployment, approved company/IMO documents can be linked here.")

# ============================================================
# SETTINGS
# ============================================================
# ============================================================
# SETTINGS
# ============================================================
elif page == "System Settings":

    # Page heading
    st.markdown(
        """
        <h1 style="
            color:#0b2c5c !important;
            font-size:32px;
            font-weight:800;
            margin-bottom:5px;
        ">
            System Settings
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style="
            color:#475569 !important;
            font-size:15px;
            margin-top:0;
            margin-bottom:25px;
        ">
            Prototype configuration and offline synchronization simulation.
        </p>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # VESSEL PROFILE
    # ========================================================

    st.markdown(
        """
        <h3 style="
            color:#0b2c5c !important;
            font-size:22px;
            font-weight:800;
            margin-top:10px;
            margin-bottom:15px;
        ">
            Vessel Profile
        </h3>
        """,
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        st.text_input(
            "Vessel Name",
            "MV OCEAN PIONEER"
        )

        st.text_input(
            "IMO Number",
            "9876543"
        )

        st.text_input(
            "Flag",
            "India"
        )

        st.text_input(
            "Ship Type",
            "Oil Tanker"
        )

    with c2:

        st.text_input(
            "Gross Tonnage",
            "45,678"
        )

        st.text_input(
            "Current Voyage",
            "V-2026-001"
        )

        st.text_input(
            "Route",
            "Mangalore → Singapore"
        )

        st.text_input(
            "Current Position",
            f"{lat_s}, {lon_s}"
        )

    # ========================================================
    # OFFLINE SYNCHRONIZATION
    # ========================================================

    st.markdown(
        """
        <h3 style="
            color:#0b2c5c !important;
            font-size:22px;
            font-weight:800;
            margin-top:30px;
            margin-bottom:15px;
        ">
            Offline Sync Simulator
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="info-box">
            <b>Synchronization System</b><br>
            Records created while offline are stored locally and can
            be synchronized with the shore server when connectivity returns.
        </div>
        """,
        unsafe_allow_html=True
    )

    unsynced = query_df(
        "SELECT * FROM records WHERE synced=0"
    )

    st.markdown(
        f"""
        <div style="
            background:white;
            border:1px solid #dce7f2;
            border-radius:12px;
            padding:16px;
            margin:10px 0 15px 0;
        ">
            <div style="
                color:#64748b;
                font-size:13px;
                font-weight:600;
            ">
                RECORDS WAITING FOR SYNCHRONIZATION
            </div>

            <div style="
                color:#0b2c5c;
                font-size:30px;
                font-weight:800;
                margin-top:5px;
            ">
                {len(unsynced)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not unsynced.empty:

        st.markdown(
            """
            <h4 style="
                color:#0b2c5c !important;
                font-size:18px;
                font-weight:700;
                margin-top:15px;
            ">
                Records Awaiting Synchronization
            </h4>
            """,
            unsafe_allow_html=True
        )

        st.dataframe(
            unsynced[
                [
                    "record_id",
                    "annex",
                    "operation",
                    "record_date"
                ]
            ],
            hide_index=True,
            use_container_width=True
        )

    # Sync button
    if st.button(
        "🔄 Sync Local Records to Shore Server",
        type="primary",
        use_container_width=True
    ):

        if st.session_state.offline:

            st.warning(
                "⚠ Internet unavailable. Switch to Online mode first."
            )

        else:

            execute(
                "UPDATE records SET synced=1 WHERE synced=0"
            )

            add_audit(
                "Sync",
                "",
                "Local records synchronized to shore server",
                st.session_state.user,
                st.session_state.role
            )

            st.success(
                "✓ Synchronization completed successfully."
            )

            st.rerun()

    # ========================================================
    # SYSTEM INFORMATION
    # ========================================================

    st.markdown(
        """
        <h3 style="
            color:#0b2c5c !important;
            font-size:22px;
            font-weight:800;
            margin-top:35px;
            margin-bottom:15px;
        ">
            System Information
        </h3>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="
            background:white;
            border:1px solid #dce7f2;
            border-radius:12px;
            padding:20px;
            margin-bottom:15px;
        ">

            <div style="
                color:#64748b;
                font-size:12px;
                font-weight:700;
                margin-bottom:5px;
            ">
                ARCHITECTURE
            </div>

            <div style="
                color:#0b2c5c;
                font-size:15px;
                font-weight:600;
                margin-bottom:18px;
            ">
                Shipboard Browser → Local SQLite → Offline Queue
                → Sync Server → Shore Office
            </div>

            <div style="
                color:#64748b;
                font-size:12px;
                font-weight:700;
                margin-bottom:5px;
            ">
                PROTOTYPE STACK
            </div>

            <div style="
                color:#0b2c5c;
                font-size:15px;
                font-weight:600;
                margin-bottom:18px;
            ">
                Python + Streamlit + SQLite + Pandas
            </div>

            <div style="
                color:#64748b;
                font-size:12px;
                font-weight:700;
                margin-bottom:5px;
            ">
                SECURITY EXTENSION FOR FINAL DEPLOYMENT
            </div>

            <div style="
                color:#0b2c5c;
                font-size:15px;
                font-weight:600;
                line-height:1.6;
            ">
                Authentication, role-based access, encrypted sync,
                backups and server-side validation.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        color:#64748b !important;
        font-size:13px;
        padding:10px;
    ">
        ⚓ <b style="color:#0b2c5c;">MARPOL-SAFE</b>
        • Major Project Prototype
        • For academic demonstration
    </div>
    """,
    unsafe_allow_html=True
)