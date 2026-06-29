import streamlit as st
import pandas as pd
import time
from datetime import datetime
from mailer import verify_gmail, send_email, get_random_interval, pick_random_template, parse_emails_from_text
from db import (save_session, check_blocked, increment_failed, reset_failed,
                save_templates, load_templates, log_send, get_logs, get_stats,
                save_send_progress, load_send_progress, clear_send_progress)

st.set_page_config(
    page_title="ABD MailForge",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: #1a1a2e !important;
    color: #e2e8f0 !important;
}
#MainMenu, footer, header {visibility: hidden;}
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 2rem !important;
    max-width: 1100px !important;
}

/* ── Hide sidebar completely ── */
section[data-testid="stSidebar"] {display: none !important;}
button[data-testid="collapsedControl"] {display: none !important;}

/* ── Top Nav Bar ── */
.topnav {
    background: #16213e;
    border-bottom: 1px solid #2d3748;
    padding: 0 24px;
    margin-bottom: 24px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 999;
    box-shadow: 0 2px 12px rgba(0,0,0,0.3);
}
.topnav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px 0;
    flex-shrink: 0;
}
.topnav-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg,#7c3aed,#5b21b6);
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 3px 10px rgba(124,58,237,0.4);
}
.topnav-name {
    font-size: 17px; font-weight: 800;
    letter-spacing: -0.3px; color: #e2e8f0;
}
.topnav-name em {color: #a78bfa; font-style: normal;}
.topnav-links {
    display: flex; align-items: center; gap: 4px;
    flex-wrap: nowrap; overflow-x: auto;
}
.topnav-links::-webkit-scrollbar {display: none;}
.tnl {
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 600;
    color: #94a3b8;
    cursor: pointer;
    white-space: nowrap;
    border: none;
    background: transparent;
    transition: all 0.15s;
    text-decoration: none;
    display: inline-block;
}
.tnl:hover {color: #e2e8f0; background: rgba(255,255,255,0.05);}
.tnl.active {
    color: #a78bfa;
    background: rgba(124,58,237,0.12);
    border: 1px solid rgba(124,58,237,0.25);
}
.topnav-user {
    display: flex; align-items: center; gap: 8px;
    flex-shrink: 0; padding: 6px 0;
}
.uavatar-sm {
    width: 30px; height: 30px;
    background: linear-gradient(135deg,#7c3aed,#5b21b6);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 800; color: #fff;
}
.uemail-sm {
    font-size: 12px; color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
    max-width: 160px; overflow: hidden;
    text-overflow: ellipsis; white-space: nowrap;
}

/* ── Scrollbar ── */
::-webkit-scrollbar {width: 4px; height: 4px;}
::-webkit-scrollbar-track {background: transparent;}
::-webkit-scrollbar-thumb {background: #4a5568; border-radius: 4px;}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg,#7c3aed,#5b21b6) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 12px 24px !important;
    transition: all 0.2s !important;
    box-shadow: 0 3px 12px rgba(124,58,237,0.3) !important;
    width: 100% !important;
}
.stButton > button:hover {
    box-shadow: 0 5px 20px rgba(124,58,237,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0f2040 !important;
    border: 1px solid #2d3748 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 16px !important;
    padding: 14px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.15) !important;
}
.stTextInput label, .stTextArea label,
.stSelectbox label, .stFileUploader label {
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
    margin-bottom: 6px !important;
}

/* ── Select ── */
.stSelectbox > div > div {
    background: #0f2040 !important;
    border: 1px solid #2d3748 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-size: 15px !important;
}

/* ── File uploader ── */
.stFileUploader > div {
    background: #0f2040 !important;
    border: 1px dashed #4a5568 !important;
    border-radius: 10px !important;
}

/* ── Radio ── */
.stRadio > div {background: #16213e !important; border-radius: 10px !important; padding: 10px !important;}
.stRadio label {font-size: 15px !important; color: #e2e8f0 !important; font-weight: 500 !important;}

/* ── Progress ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg,#5b21b6,#7c3aed,#a78bfa) !important;
    border-radius: 99px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #16213e !important;
    border-radius: 10px !important;
    padding: 4px !important; gap: 4px !important;
    border: 1px solid #2d3748 !important;
}
.stTabs [data-baseweb="tab"] {
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    border-radius: 7px !important;
    padding: 10px 18px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#7c3aed,#5b21b6) !important;
    color: white !important;
}

/* ── Alerts ── */
.stSuccess, .stError, .stWarning, .stInfo {
    border-radius: 10px !important;
    font-size: 15px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
.stSuccess {background: rgba(16,185,129,0.08) !important; border: 1px solid rgba(16,185,129,0.25) !important;}
.stError   {background: rgba(239,68,68,0.08)  !important; border: 1px solid rgba(239,68,68,0.25)  !important;}
.stWarning {background: rgba(245,158,11,0.08) !important; border: 1px solid rgba(245,158,11,0.25) !important;}
.stInfo    {background: rgba(124,58,237,0.08) !important; border: 1px solid rgba(124,58,237,0.25) !important;}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #16213e !important; border: 1px solid #2d3748 !important;
    border-radius: 10px !important; color: #e2e8f0 !important;
    font-weight: 600 !important; font-size: 15px !important;
}
hr {border-color: #2d3748 !important; margin: 18px 0 !important;}

/* ── Cards ── */
.abd-card {
    background: #16213e; border: 1px solid #2d3748;
    border-radius: 14px; padding: 24px; margin-bottom: 20px;
}
.abd-card-accent {
    background: linear-gradient(135deg,#1a2444,#16213e);
    border: 1px solid #7c3aed; border-radius: 14px;
    padding: 24px; margin-bottom: 20px;
    box-shadow: 0 4px 24px rgba(124,58,237,0.12);
}
.abd-card-purple {
    background: linear-gradient(135deg,rgba(124,58,237,0.1),rgba(91,33,182,0.05));
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 14px; padding: 24px; margin-bottom: 20px;
}

/* ── Stat cards ── */
.stat-grid {
    display: grid; grid-template-columns: repeat(4,1fr);
    gap: 14px; margin-bottom: 22px;
}
@media(max-width:640px){.stat-grid{grid-template-columns:repeat(2,1fr);}}
.stat-box {
    background: #1a2444; border: 1px solid #2d3748;
    border-radius: 14px; padding: 20px;
    position: relative; overflow: hidden;
}
.stat-box::before {
    content:''; position:absolute; top:0; left:0; right:0;
    height:3px; border-radius:3px 3px 0 0;
}
.stat-box.purple::before {background:#a78bfa;}
.stat-box.green::before  {background:#10b981;}
.stat-box.amber::before  {background:#f59e0b;}
.stat-box.red::before    {background:#ef4444;}
.stat-num {font-size:40px;font-weight:800;letter-spacing:-1px;line-height:1.1;}
.stat-num.purple {color:#a78bfa;}
.stat-num.green  {color:#10b981;}
.stat-num.amber  {color:#f59e0b;}
.stat-num.red    {color:#ef4444;}
.stat-label {font-size:12px;color:#94a3b8;font-family:'JetBrains Mono',monospace;text-transform:uppercase;letter-spacing:0.8px;margin-top:8px;}
.stat-sub   {font-size:11px;color:#4a5568;margin-top:4px;font-family:'JetBrains Mono',monospace;}

/* ── Feed ── */
.feed-item {
    display:flex;align-items:center;gap:10px;
    padding:12px 14px;border-radius:10px;
    font-size:14px;margin-bottom:6px;border:1px solid transparent;
}
.feed-item.sent   {background:rgba(16,185,129,0.06);border-color:rgba(16,185,129,0.15);}
.feed-item.failed {background:rgba(239,68,68,0.06);border-color:rgba(239,68,68,0.15);}
.feed-dot   {width:8px;height:8px;border-radius:50%;flex-shrink:0;}
.feed-email {font-family:'JetBrains Mono',monospace;font-size:13px;flex:1;color:#e2e8f0;}
.feed-badge {font-size:11px;padding:3px 10px;border-radius:99px;font-family:'JetBrains Mono',monospace;font-weight:600;}
.feed-badge.sent   {background:rgba(16,185,129,0.12);color:#10b981;}
.feed-badge.failed {background:rgba(239,68,68,0.12);color:#ef4444;}
.feed-time  {font-size:12px;color:#4a5568;font-family:'JetBrains Mono',monospace;}

/* ── Project cards ── */
.project-card {
    background:#1a2444;border:1px solid #2d3748;
    border-radius:13px;padding:18px 20px;margin-bottom:12px;
    display:flex;align-items:center;justify-content:space-between;gap:16px;
    transition:all 0.2s;
}
.project-card:hover {border-color:#7c3aed;box-shadow:0 4px 16px rgba(124,58,237,0.15);}
.project-name {font-size:15px;font-weight:700;color:#e2e8f0;}
.project-desc {font-size:13px;color:#94a3b8;margin-top:4px;}
.project-link {
    font-size:13px;font-weight:700;color:#a78bfa;
    background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.25);
    border-radius:8px;padding:7px 16px;white-space:nowrap;
    text-decoration:none;font-family:'JetBrains Mono',monospace;
}

/* ── Guide ── */
.guide-section {margin-bottom:32px;}
.guide-headline {
    font-size:22px;font-weight:800;color:#e2e8f0;
    letter-spacing:-0.3px;margin-bottom:14px;
    padding-bottom:12px;border-bottom:1px solid #2d3748;
}
.guide-body {font-size:16px;color:#94a3b8;line-height:2.0;}
.guide-body strong {color:#e2e8f0;}
.guide-body a {color:#7c3aed;font-weight:700;}

/* ── Welcome banner ── */
.welcome-banner {
    background:linear-gradient(135deg,rgba(124,58,237,0.12),rgba(91,33,182,0.06));
    border:1px solid rgba(124,58,237,0.2);
    border-radius:14px;padding:22px 26px;margin-bottom:24px;
}
.welcome-title {font-size:24px;font-weight:800;letter-spacing:-0.4px;color:#e2e8f0;}
.welcome-title em {color:#a78bfa;font-style:normal;}
.live-badge {
    display:inline-flex;align-items:center;gap:7px;
    background:rgba(16,185,129,0.1);color:#10b981;
    border:1px solid rgba(16,185,129,0.25);
    border-radius:99px;padding:5px 14px;
    font-size:13px;font-family:'JetBrains Mono',monospace;
    margin-top:12px;
}

/* ── Footer ── */
.abd-footer {
    text-align:center;padding:30px 0 12px;
    border-top:1px solid #2d3748;margin-top:32px;
}
.abd-footer a {color:#a78bfa;text-decoration:none;}
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────────────
defaults = {
    "logged_in": False, "gmail": "", "app_password": "",
    "templates": [], "stop_sending": False, "page": "dashboard",
    "emails_list": [], "send_subject": "", "send_body": "",
    "send_template_choice": "", "sent_emails": []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ── Helpers ───────────────────────────────────────────────────────────────────
def set_page(p):
    st.session_state.page = p
    st.rerun()


def footer():
    st.markdown("""
    <div class="abd-footer">
        <div style="margin-bottom:18px;">
            <div style="font-size:12px;color:#4a5568;font-family:'JetBrains Mono',monospace;
                 margin-bottom:14px;text-transform:uppercase;letter-spacing:1px;">My Projects</div>
            <div class="project-card">
                <div>
                    <div class="project-name">🎥 ABD Screen Recorder</div>
                    <div class="project-desc">Web-based screen recording app built with Streamlit</div>
                </div>
                <a class="project-link" href="https://abd-screen-recorder-web-app.streamlit.app/" target="_blank">Visit →</a>
            </div>
            <div class="project-card">
                <div>
                    <div class="project-name">🖱️ ABD Cursor Mover & Game Site</div>
                    <div class="project-desc">Interactive cursor mover and browser game experience</div>
                </div>
                <a class="project-link" href="https://abdulrehmanraza03.github.io/ABD_Cursor_Mover_Site/" target="_blank">Visit →</a>
            </div>
        </div>
        <div style="margin-bottom:14px;">
            <a href="https://www.linkedin.com/in/abdul-rehman-raza-7a125b332" target="_blank"
               style="display:inline-flex;align-items:center;gap:8px;
               background:rgba(124,58,237,0.12);border:1px solid rgba(124,58,237,0.25);
               border-radius:10px;padding:11px 22px;font-size:15px;font-weight:700;
               color:#a78bfa;text-decoration:none;">
                🔗 Connect with Abdul Rehman Raza on LinkedIn
            </a>
        </div>
        <div style="font-size:13px;color:#4a5568;font-family:'JetBrains Mono',monospace;">
            Made with ❤️ by <span style="color:#a78bfa;font-weight:700;">Abdulll,s</span> · ABD MailForge v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)


def top_nav():
    initials = st.session_state.gmail[:2].upper() if st.session_state.gmail else "AB"
    page = st.session_state.page

    def cls(p):
        return "tnl active" if page == p else "tnl"

    st.markdown(f"""
    <div class="topnav">
        <div class="topnav-brand">
            <div class="topnav-icon">✉️</div>
            <div class="topnav-name">ABD <em>Mail</em>Forge</div>
        </div>
        <div class="topnav-links" id="tnlinks">
        </div>
        <div class="topnav-user">
            <div class="uavatar-sm">{initials}</div>
            <div class="uemail-sm">{st.session_state.gmail}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Actual navigation using Streamlit buttons in columns
    nav_cols = st.columns([1,1,1,1,1,1])
    pages = [
        ("dashboard",  "📊 Dashboard"),
        ("send",       "📤 Send"),
        ("templates",  "📋 Templates"),
        ("guide",      "📖 Guide"),
        ("settings",   "⚙️ Settings"),
        ("logout",     "🚪 Logout"),
    ]
    for i, (pg, label) in enumerate(pages):
        with nav_cols[i]:
            if st.button(label, key=f"nav_{pg}", use_container_width=True):
                if pg == "logout":
                    for k in defaults:
                        st.session_state[k] = defaults[k]
                    st.rerun()
                else:
                    st.session_state.page = pg
                    st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ═══════════════════════════════════════════════════════════════════════════════
def login_page():
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:
        st.markdown("""
        <div style="text-align:center;padding:40px 0 28px;">
            <div style="display:inline-flex;align-items:center;gap:14px;margin-bottom:10px;">
                <div style="width:54px;height:54px;background:linear-gradient(135deg,#7c3aed,#5b21b6);
                    border-radius:14px;display:flex;align-items:center;justify-content:center;
                    font-size:26px;box-shadow:0 6px 20px rgba(124,58,237,0.4);">✉️</div>
                <div style="text-align:left;">
                    <div style="font-size:26px;font-weight:800;letter-spacing:-0.5px;color:#e2e8f0;">
                        ABD <span style="color:#a78bfa;">Mail</span>Forge</div>
                    <div style="font-size:11px;color:#4a5568;font-family:'JetBrains Mono',monospace;">
                        BULK EMAIL SENDER · V2.0</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("📖 Quick Guide — Read Before Using", expanded=False):
            st.markdown("""
            <div class="guide-section">
                <div class="guide-headline">Step 1 — Gmail App Password</div>
                <div class="guide-body">You need a 16-character App Password from Google — not your real Gmail password.<br>
                <strong>Go to:</strong> Google Account → Security → 2-Step Verification → App Passwords<br>
                Or click the direct link below the login form.</div>
            </div>
            <div class="guide-section">
                <div class="guide-headline">Step 2 — Add Recipients</div>
                <div class="guide-body">Upload a CSV (Email column) or paste emails one per line.<br>
                <strong>Maximum 400 per session.</strong> Recommended daily limit: 100–150.</div>
            </div>
            <div class="guide-section">
                <div class="guide-headline">Step 3 — Templates & Send</div>
                <div class="guide-body">Create 3 templates (Professional, Friendly, Short).<br>
                The app picks one randomly per email. Emails go out with a <strong>random 15–45 second gap.</strong><br>
                Keep the browser tab open until sending is complete.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="abd-card-accent">', unsafe_allow_html=True)
        st.markdown("#### 🔐 Login to ABD MailForge")
        st.caption("Enter your Gmail and 16-character App Password to continue.")

        gmail_input = st.text_input("📧 Gmail Address", placeholder="yourname@gmail.com", key="li_gmail")
        pass_input  = st.text_input("🔑 App Password", type="password",
                                     placeholder="xxxx xxxx xxxx xxxx", key="li_pass")

        st.markdown("""
        <div style="background:#0f2040;border:1px solid #2d3748;border-radius:10px;
             padding:14px 18px;margin:14px 0;font-size:14px;color:#94a3b8;line-height:1.9;">
            <strong style="color:#a78bfa;">Need an App Password?</strong><br>
            👉 <a href="https://myaccount.google.com/apppasswords" target="_blank"
               style="color:#7c3aed;font-weight:700;font-size:15px;">
               Click here → Generate Gmail App Password</a><br>
            <span style="font-size:13px;color:#4a5568;">
            Google Account → Security → 2-Step Verification → App Passwords → Generate</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🚀 Login & Verify Gmail", use_container_width=True):
            if not gmail_input or not pass_input:
                st.error("Please enter both your Gmail address and App Password.")
                return

            # Check blocked — silently
            try:
                if check_blocked(gmail_input):
                    st.error("⛔ This account is blocked after 5 failed attempts. Use a different Gmail.")
                    return
            except:
                pass

            # Spinner while verifying
            with st.spinner("🔄 Verifying your Gmail credentials — please wait..."):
                ok, msg = verify_gmail(gmail_input, pass_input)

            if ok:
                try:
                    reset_failed(gmail_input)
                    save_session(gmail_input, pass_input.replace(" ", ""))
                except:
                    pass

                st.session_state.logged_in    = True
                st.session_state.gmail        = gmail_input
                st.session_state.app_password = pass_input.replace(" ", "")
                st.session_state.page         = "dashboard"

                # Auto-load saved templates
                try:
                    saved = load_templates(gmail_input)
                    if saved:
                        st.session_state.templates = saved
                except:
                    pass

                st.success("✅ Gmail verified! Welcome to ABD MailForge.")
                time.sleep(0.8)
                st.rerun()
            else:
                try:
                    attempts, is_blocked = increment_failed(gmail_input)
                    remaining = 5 - attempts
                    if is_blocked:
                        st.error("⛔ Account blocked — 5 failed attempts. Please use a different Gmail.")
                    else:
                        st.error(f"❌ {msg} — {remaining} attempt(s) remaining before block.")
                except:
                    st.error(f"❌ {msg}")

        footer()


# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def dashboard_page():
    st.markdown("""
    <div class="welcome-banner">
        <div class="welcome-title">Welcome to <em>ABD MailForge</em> ✉️</div>
        <div class="live-badge">● Live Session Active</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([5,1])
    with c2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    stats = get_stats(st.session_state.gmail)

    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-box purple">
            <div class="stat-num purple">{stats['today_sent']}</div>
            <div class="stat-label">Sent Today</div>
            <div class="stat-sub">emails delivered</div>
        </div>
        <div class="stat-box green">
            <div class="stat-num green">{stats['sent']}</div>
            <div class="stat-label">Total Sent</div>
            <div class="stat-sub">all time</div>
        </div>
        <div class="stat-box amber">
            <div class="stat-num amber">{stats['total']}</div>
            <div class="stat-label">Total Attempts</div>
            <div class="stat-sub">all sessions</div>
        </div>
        <div class="stat-box red">
            <div class="stat-num red">{stats['failed']}</div>
            <div class="stat-label">Total Failed</div>
            <div class="stat-sub">check logs below</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📜 Send History", "📊 Summary"])

    with tab1:
        logs = get_logs(st.session_state.gmail, limit=50)
        if logs:
            log_html = ""
            for log in logs:
                icon = "✓" if log["status"] == "sent" else "✗"
                cls  = "sent" if log["status"] == "sent" else "failed"
                t    = str(log.get("sent_at",""))[:16].replace("T"," ")
                tmpl = log.get("template_used","—")
                log_html += f"""
                <div class="feed-item {cls}">
                    <div class="feed-dot" style="background:{'#10b981' if cls=='sent' else '#ef4444'}"></div>
                    <div class="feed-email">{log['recipient']}</div>
                    <div class="feed-badge {cls}">{icon} {cls.upper()}</div>
                    <div class="feed-time">{t} · {tmpl}</div>
                </div>"""
            st.markdown(f"""
            <div style="background:#0f2040;border:1px solid #2d3748;border-radius:13px;
                 padding:16px;max-height:420px;overflow-y:auto;">{log_html}</div>""",
            unsafe_allow_html=True)
        else:
            st.info("No send history yet. Go to **Send Emails** to get started.")

    with tab2:
        if stats['total'] > 0:
            rate = round((stats['sent'] / stats['total']) * 100, 1)
            st.markdown(f"""
            <div class="abd-card">
                <div style="font-size:17px;font-weight:700;margin-bottom:18px;color:#e2e8f0;">Session Summary</div>
                <div style="display:flex;gap:32px;flex-wrap:wrap;">
                    <div><div style="font-size:42px;font-weight:800;color:#a78bfa;">{rate}%</div>
                         <div style="font-size:13px;color:#94a3b8;font-family:'JetBrains Mono',monospace;text-transform:uppercase;">Success Rate</div></div>
                    <div><div style="font-size:42px;font-weight:800;color:#10b981;">{stats['sent']}</div>
                         <div style="font-size:13px;color:#94a3b8;font-family:'JetBrains Mono',monospace;text-transform:uppercase;">Delivered</div></div>
                    <div><div style="font-size:42px;font-weight:800;color:#ef4444;">{stats['failed']}</div>
                         <div style="font-size:13px;color:#94a3b8;font-family:'JetBrains Mono',monospace;text-transform:uppercase;">Failed</div></div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("No data yet. Send some emails first to see your summary.")

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# SEND PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def send_page():
    st.markdown("## 📤 Send Emails")
    st.caption("Upload a CSV or paste email addresses, set up your message, then hit Send.")

    # ── Resume banner ──
    if st.session_state.sent_emails:
        done = len(st.session_state.sent_emails)
        total_prev = len(st.session_state.emails_list)
        remaining = [e for e in st.session_state.emails_list if e not in st.session_state.sent_emails]
        st.markdown(f"""
        <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.25);
             border-radius:12px;padding:16px 20px;margin-bottom:18px;font-size:15px;color:#fbbf24;">
        ⚡ <strong>Previous session found:</strong> {done} of {total_prev} emails sent.
        {len(remaining)} emails remaining. You can resume below or start fresh.
        </div>
        """, unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("▶ Resume Sending", use_container_width=True):
                st.session_state.emails_list = remaining
                st.session_state.stop_sending = False
                st.rerun()
        with c2:
            if st.button("🔄 Start Fresh", use_container_width=True):
                st.session_state.sent_emails = []
                st.session_state.emails_list = []
                st.rerun()
        st.markdown("---")

    col1, col2 = st.columns([1,1], gap="large")

    with col1:
        st.markdown('<div class="abd-card">', unsafe_allow_html=True)
        st.markdown("#### 📧 Recipients")
        st.caption("Upload CSV (Email column required) or paste emails one per line. Max 400.")

        method = st.radio("Method", ["📎 Upload CSV","✏️ Paste Emails"],
                          horizontal=True, label_visibility="collapsed")
        emails_list = []

        if method == "📎 Upload CSV":
            csv_file = st.file_uploader("CSV File", type=["csv"], label_visibility="collapsed")
            if csv_file:
                try:
                    df = pd.read_csv(csv_file)
                    email_col = next((c for c in df.columns if "email" in c.lower() or "mail" in c.lower()), df.columns[0])
                    emails_list = [str(e).strip().lower() for e in df[email_col].dropna() if "@" in str(e)][:400]
                    st.success(f"✅ {len(emails_list)} emails loaded from CSV")
                    with st.expander("Preview first 5"):
                        for e in emails_list[:5]: st.code(e, language=None)
                except Exception as ex:
                    st.error(f"CSV error: {ex}")
        else:
            pasted = st.text_area("Paste emails here", height=180,
                                   placeholder="ahmed@gmail.com\nsara@yahoo.com\nbilal@hotmail.com",
                                   label_visibility="collapsed")
            if pasted:
                emails_list = parse_emails_from_text(pasted)
                if emails_list:
                    st.success(f"✅ {len(emails_list)} valid emails found")
                else:
                    st.warning("No valid emails found. Check format.")

        if emails_list:
            st.session_state.emails_list = emails_list

        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="abd-card">', unsafe_allow_html=True)
        st.markdown("#### ✉️ Message")
        st.caption("Select a saved template or write a custom message.")

        subject = st.text_input("Subject line", placeholder="Your Daily Update — June 2026",
                                 value=st.session_state.get("send_subject",""))
        if subject:
            st.session_state.send_subject = subject

        template_opts = ["✍️ Write custom message"] + [t["name"] for t in st.session_state.templates]
        if len(st.session_state.templates) >= 2:
            template_opts.append("🎲 Random template (recommended)")

        prev_choice = st.session_state.get("send_template_choice","")
        default_idx = template_opts.index(prev_choice) if prev_choice in template_opts else 0
        chosen = st.selectbox("Template", template_opts,
                               index=default_idx, label_visibility="collapsed")
        st.session_state.send_template_choice = chosen

        use_random = False
        body = ""

        if chosen == "✍️ Write custom message":
            body = st.text_area("Message body", height=150,
                                 value=st.session_state.get("send_body",""),
                                 placeholder="Write your email message here...",
                                 label_visibility="collapsed")
            if body:
                st.session_state.send_body = body
        elif chosen == "🎲 Random template (recommended)":
            use_random = True
            st.info("✓ A different template will be picked randomly for each email.")
        else:
            t = next((t for t in st.session_state.templates if t["name"]==chosen), None)
            if t:
                body = t["body"]
                st.text_area("Preview", value=body, height=150,
                              disabled=True, label_visibility="collapsed")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### 📎 PDF Attachment (Optional)")
    st.caption("Upload a PDF — it will be attached to every email in this batch.")
    pdf_file = st.file_uploader("PDF file", type=["pdf"], label_visibility="collapsed")
    if pdf_file:
        st.success(f"✅ {pdf_file.name} ready to attach")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    active_emails = st.session_state.emails_list
    if not active_emails:
        st.warning("⚠️ Add recipients first — upload CSV or paste emails above.")
        footer(); return
    if not subject and not st.session_state.get("send_subject"):
        st.warning("⚠️ Please write a subject line.")
        footer(); return
    if not use_random and not body and not st.session_state.get("send_body"):
        st.warning("⚠️ Write a message or select a template.")
        footer(); return

    final_subject = subject or st.session_state.get("send_subject","")
    final_body    = body or st.session_state.get("send_body","")
    est_mins = max(1, (len(active_emails)*30)//60)

    st.markdown(f"""
    <div class="abd-card-purple">
        <div style="font-size:13px;color:#94a3b8;font-family:'JetBrains Mono',monospace;
             margin-bottom:16px;text-transform:uppercase;letter-spacing:1px;">Send Summary</div>
        <div style="display:flex;gap:36px;flex-wrap:wrap;">
            <div><div style="font-size:36px;font-weight:800;color:#a78bfa;">{len(active_emails)}</div>
                 <div style="font-size:13px;color:#94a3b8;font-family:'JetBrains Mono',monospace;text-transform:uppercase;">Recipients</div></div>
            <div><div style="font-size:36px;font-weight:800;color:#10b981;">~{est_mins}m</div>
                 <div style="font-size:13px;color:#94a3b8;font-family:'JetBrains Mono',monospace;text-transform:uppercase;">Est. Time</div></div>
            <div><div style="font-size:36px;font-weight:800;color:#f59e0b;">15–45s</div>
                 <div style="font-size:13px;color:#94a3b8;font-family:'JetBrains Mono',monospace;text-transform:uppercase;">Gap Per Email</div></div>
            <div><div style="font-size:36px;font-weight:800;color:#a78bfa;">{"🎲 RND" if use_random else "FIXED"}</div>
                 <div style="font-size:13px;color:#94a3b8;font-family:'JetBrains Mono',monospace;text-transform:uppercase;">Template</div></div>
        </div>
        <div style="margin-top:16px;font-size:15px;color:#f59e0b;font-weight:600;">
        ⚠️ Keep this browser tab open while sending. Closing it will stop the process.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([3,1])
    with c1:
        start = st.button("🚀 Start Sending", use_container_width=True)
    with c2:
        if st.button("⏹ Stop", use_container_width=True):
            st.session_state.stop_sending = True

    if start:
        st.session_state.stop_sending = False
        pdf_bytes = pdf_file.read() if pdf_file else None
        pdf_name  = pdf_file.name  if pdf_file else None

        st.markdown("---")
        st.markdown("### 📡 Live Sending Progress")

        prog    = st.progress(0)
        status  = st.empty()
        log_box = st.empty()

        sent_count = failed_count = 0
        logs_html  = ""
        total = len(active_emails)
        sent_this_session = []

        for i, email in enumerate(active_emails):
            if st.session_state.stop_sending:
                st.warning(f"⏹ Stopped — {sent_count} sent, {failed_count} failed.")
                break

            if use_random and st.session_state.templates:
                tname, tbody = pick_random_template(st.session_state.templates)
                cur_body, cur_tname = tbody, tname
            else:
                cur_body  = final_body
                cur_tname = chosen

            status.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace;font-size:15px;color:#94a3b8;
                 background:#0f2040;border:1px solid #2d3748;border-radius:10px;padding:14px 18px;">
            Sending <strong style="color:#a78bfa;">{i+1} / {total}</strong> →
            <span style="color:#e2e8f0;">{email}</span>
            </div>""", unsafe_allow_html=True)

            # Retry logic — 3 attempts per email
            ok, msg = False, ""
            for attempt in range(3):
                ok, msg = send_email(
                    st.session_state.gmail, st.session_state.app_password,
                    email, final_subject, cur_body, pdf_bytes, pdf_name
                )
                if ok:
                    break
                if attempt < 2:
                    time.sleep(5)

            if ok:
                sent_count += 1
                sent_this_session.append(email)
                st.session_state.sent_emails.append(email)
                logs_html = f'<div class="feed-item sent"><div class="feed-dot" style="background:#10b981"></div><div class="feed-email">{email}</div><div class="feed-badge sent">✓ SENT</div><div class="feed-time">[{i+1}/{total}] · {cur_tname}</div></div>' + logs_html
                try: log_send(st.session_state.gmail, email, final_subject, cur_tname, "sent")
                except: pass
            else:
                failed_count += 1
                logs_html = f'<div class="feed-item failed"><div class="feed-dot" style="background:#ef4444"></div><div class="feed-email">{email}</div><div class="feed-badge failed">✗ FAILED</div><div class="feed-time">[{i+1}/{total}] · {msg}</div></div>' + logs_html
                try: log_send(st.session_state.gmail, email, final_subject, cur_tname, "failed", msg)
                except: pass

            prog.progress((i+1)/total)
            log_box.markdown(f"""
            <div style="background:#0f2040;border:1px solid #2d3748;border-radius:12px;
                 padding:16px;max-height:320px;overflow-y:auto;">{logs_html}</div>""",
            unsafe_allow_html=True)

            if i < total-1 and not st.session_state.stop_sending:
                delay = get_random_interval()
                for r in range(delay, 0, -1):
                    status.markdown(f"""
                    <div style="font-family:'JetBrains Mono',monospace;font-size:15px;color:#94a3b8;
                         background:#0f2040;border:1px solid #2d3748;border-radius:10px;padding:14px 18px;">
                    ⏳ Next email in <span style="color:#a78bfa;font-size:18px;font-weight:800;">{r}s</span>
                    &nbsp;&nbsp; ✓ {sent_count} sent &nbsp; ✗ {failed_count} failed
                    </div>""", unsafe_allow_html=True)
                    time.sleep(1)
                    if st.session_state.stop_sending: break

        status.empty()
        if not st.session_state.stop_sending:
            # Clear progress on full completion
            st.session_state.sent_emails = []
            st.session_state.emails_list = []
            try: clear_send_progress(st.session_state.gmail)
            except: pass
            if failed_count == 0:
                st.success(f"🎉 All done! {sent_count} emails sent successfully.")
            else:
                st.warning(f"✅ Completed — {sent_count} sent, {failed_count} failed.")

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATES
# ═══════════════════════════════════════════════════════════════════════════════
def templates_page():
    st.markdown("## 📋 Email Templates")
    st.caption("Create up to 5 templates. The app randomly picks one per email to reduce spam flagging.")

    if st.session_state.templates:
        st.success(f"✅ {len(st.session_state.templates)} template(s) saved and ready to use.")

    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### ➕ Create New Template")
    st.caption("Tip: Create Professional, Friendly, and Short versions for best results.")

    t_name = st.text_input("Template name", placeholder="e.g. Professional, Friendly, Short Update")
    t_body = st.text_area("Template body", placeholder="Write your email message here...", height=160)

    if st.button("💾 Save Template"):
        if not t_name or not t_body:
            st.error("Both name and body are required.")
        elif len(st.session_state.templates) >= 5:
            st.error("Maximum 5 templates allowed.")
        elif any(t["name"]==t_name for t in st.session_state.templates):
            st.error(f"A template named '{t_name}' already exists.")
        else:
            st.session_state.templates.append({"name": t_name, "body": t_body})
            try: save_templates(st.session_state.gmail, st.session_state.templates)
            except: pass
            st.success(f"✅ Template '{t_name}' saved!")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.templates:
        st.markdown(f"### 📚 Saved Templates ({len(st.session_state.templates)} / 5)")
        for i, t in enumerate(st.session_state.templates):
            with st.expander(f"📄 {t['name']}"):
                st.text_area("Content", value=t["body"], height=120, disabled=True, key=f"tv_{i}")
                if st.button(f"🗑️ Delete '{t['name']}'", key=f"td_{i}"):
                    st.session_state.templates.pop(i)
                    try: save_templates(st.session_state.gmail, st.session_state.templates)
                    except: pass
                    st.rerun()
    else:
        st.info("No templates yet. Create your first template above.")

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# GUIDE
# ═══════════════════════════════════════════════════════════════════════════════
def guide_page():
    st.markdown("## 📖 Guide & Documentation")
    st.caption("Complete guide to using ABD MailForge safely and effectively.")

    tab1, tab2, tab3, tab4 = st.tabs(["🚀 Getting Started","📧 Sending Tips","🔒 Security","⚠️ Warnings"])

    with tab1:
        st.markdown("""
        <div class="guide-section">
            <div class="guide-headline">Get a Gmail App Password</div>
            <div class="guide-body">
            Go to your <strong>Google Account → Security → 2-Step Verification → App Passwords</strong>.<br>
            Select Mail and Other, name it MailForge, then click Generate.<br>
            Copy the 16-character code. This is your App Password.<br><br>
            Direct link: <a href="https://myaccount.google.com/apppasswords" target="_blank">myaccount.google.com/apppasswords</a>
            </div>
        </div>
        <div class="guide-section">
            <div class="guide-headline">Prepare Your Email List</div>
            <div class="guide-body">
            <strong>Option A — CSV File:</strong> Create a spreadsheet with a column named Email. Save as CSV and upload.<br>
            <strong>Option B — Paste:</strong> Type or paste emails directly, one per line. Maximum 400 per session.<br><br>
            Recommended daily limit: 100–150 emails to stay within Gmail sending limits.
            </div>
        </div>
        <div class="guide-section">
            <div class="guide-headline">Create 3 Email Templates</div>
            <div class="guide-body">
            Go to Templates and create 3 different versions of your message.<br>
            <strong>Template A</strong> — Professional tone<br>
            <strong>Template B</strong> — Friendly tone<br>
            <strong>Template C</strong> — Short and direct<br><br>
            When sending, select Random Template so each email gets a different version automatically.
            </div>
        </div>
        <div class="guide-section">
            <div class="guide-headline">Send Your Emails</div>
            <div class="guide-body">
            Go to Send Emails, upload your list or paste emails, write your subject, attach a PDF if needed, then click Start Sending.<br>
            The app sends one email every 15 to 45 seconds randomly to mimic natural human sending behavior.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="guide-section">
            <div class="guide-headline">How Many Emails Per Day?</div>
            <div class="guide-body">
            New Gmail account: 50–100 emails per day<br>
            Regular Gmail: 100–200 emails per day<br>
            Older active Gmail (2+ years): up to 400 per day<br><br>
            Gmail's daily limit is 500. Stay well below it to avoid suspension.
            </div>
        </div>
        <div class="guide-section">
            <div class="guide-headline">Why Random Gaps Between Emails?</div>
            <div class="guide-body">
            Sending too fast triggers Gmail's spam filters.<br>
            A random 15–45 second delay makes your sending pattern look like a real human.<br>
            This significantly reduces spam flagging and account suspension risk.
            </div>
        </div>
        <div class="guide-section">
            <div class="guide-headline">Why Use 3 Different Templates?</div>
            <div class="guide-body">
            Spam filters detect when the exact same email is sent to many people.<br>
            Rotating 3 different versions makes each email look unique.<br>
            Keep messages natural. Avoid ALL CAPS and spam words like FREE!!! or URGENT!!!
            </div>
        </div>
        <div class="guide-section">
            <div class="guide-headline">Internet Connection Tips</div>
            <div class="guide-body">
            Use a stable internet connection throughout sending.<br>
            Mobile hotspot is more reliable than shared Wi-Fi in most cases.<br>
            Do not switch networks while sending is in progress.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="guide-section">
            <div class="guide-headline">App Password vs Real Password</div>
            <div class="guide-body">
            Your real Gmail password never enters this app.<br>
            An App Password is a separate 16-character code that only allows sending emails.<br>
            If compromised, revoke it from Google Account settings without changing your real password.
            </div>
        </div>
        <div class="guide-section">
            <div class="guide-headline">How to Revoke an App Password</div>
            <div class="guide-body">
            Google Account → Security → 2-Step Verification → App Passwords → Find MailForge → Delete.<br>
            This immediately blocks anyone from using that password.<br>
            Generate a new one and update it in Settings to continue.
            </div>
        </div>
        <div class="guide-section">
            <div class="guide-headline">Always Keep 2-Step Verification ON</div>
            <div class="guide-body">
            App Passwords require 2-Step Verification to be enabled on your Google Account.<br>
            This also adds a critical layer of security to your Gmail. Never turn it off.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        <div class="guide-section">
            <div class="guide-headline">Keep Browser Tab Open While Sending</div>
            <div class="guide-body">
            ABD MailForge sends emails from your active browser session.<br>
            Closing the tab, switching apps, or locking your screen will stop sending immediately.<br>
            If interrupted, go back to Send Emails — you will see a Resume option to continue from where you left off.
            </div>
        </div>
        <div class="guide-section">
            <div class="guide-headline">Mobile Users — Keep Screen Active</div>
            <div class="guide-body">
            On mobile, if the screen turns off or the browser goes to the background, sending stops.<br>
            Keep your screen on throughout. Keep your phone plugged in during sending.
            </div>
        </div>
        <div class="guide-section">
            <div class="guide-headline">PC and Laptop Users — Prevent Sleep</div>
            <div class="guide-body">
            Move your mouse occasionally to prevent your computer from going to sleep.<br>
            Adjust power settings to disable screen sleep during long sending sessions.
            </div>
        </div>
        <div class="guide-section">
            <div class="guide-headline">Before You Send — Checklist</div>
            <div class="guide-body">
            ✓ Browser tab is open and visible<br>
            ✓ Internet connection is stable<br>
            ✓ Screen will not lock or sleep<br>
            ✓ Email list is clean and verified<br>
            ✓ Subject line is written naturally<br>
            ✓ At least 2–3 templates are ready<br>
            ✓ PDF attached if needed<br>
            ✓ Daily sending limit is respected
            </div>
        </div>
        """, unsafe_allow_html=True)

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# SETTINGS
# ═══════════════════════════════════════════════════════════════════════════════
def settings_page():
    st.markdown("## ⚙️ Settings")

    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### 📧 Current Account")
    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace;font-size:15px;line-height:2.4;color:#94a3b8;">
    Gmail: <span style="color:#a78bfa;font-weight:700;">{st.session_state.gmail}</span><br>
    Status: <span style="color:#10b981;font-weight:600;">● Active Session</span><br>
    Templates Saved: <span style="color:#e2e8f0;font-weight:700;">{len(st.session_state.templates)}</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### 🔑 Update App Password")
    st.caption("Update your App Password here if it has changed or been revoked.")
    new_pass = st.text_input("New App Password", type="password", placeholder="xxxx xxxx xxxx xxxx")
    if st.button("🔄 Update & Verify Password"):
        if new_pass:
            with st.spinner("Verifying new App Password..."):
                ok, msg = verify_gmail(st.session_state.gmail, new_pass)
            if ok:
                st.session_state.app_password = new_pass.replace(" ","")
                try: save_session(st.session_state.gmail, new_pass.replace(" ",""))
                except: pass
                st.success("✅ App Password updated successfully.")
            else:
                st.error(f"❌ Verification failed: {msg}")
        else:
            st.error("Please enter a new App Password.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### 🔗 Generate App Password")
    st.markdown("""
    <div style="font-size:16px;color:#94a3b8;line-height:2.0;">
    Need a new App Password?<br>
    <a href="https://myaccount.google.com/apppasswords" target="_blank"
       style="color:#7c3aed;font-weight:700;font-size:16px;">
        👉 Click here — Google App Passwords Page
    </a><br>
    <span style="font-size:14px;color:#4a5568;">
    Google Account → Security → 2-Step Verification → App Passwords → Generate
    </span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    login_page()
else:
    top_nav()
    page = st.session_state.page
    if   page == "dashboard": dashboard_page()
    elif page == "send":      send_page()
    elif page == "templates": templates_page()
    elif page == "guide":     guide_page()
    elif page == "settings":  settings_page()
