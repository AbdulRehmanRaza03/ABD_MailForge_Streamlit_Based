import streamlit as st
import pandas as pd
import time
from datetime import datetime
from mailer import verify_gmail, send_email, get_random_interval, pick_random_template, parse_emails_from_text
from db import (save_session, check_blocked, increment_failed, reset_failed,
                save_templates, load_templates, log_send, get_logs, get_stats)

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ABD MailForge",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    background: #1a1a2e !important;
}

#MainMenu, footer, header {visibility: hidden;}
.block-container {padding-top: 1rem !important; padding-bottom: 1rem !important;}

/* ── Scrollbar ── */
::-webkit-scrollbar {width: 4px; height: 4px;}
::-webkit-scrollbar-track {background: transparent;}
::-webkit-scrollbar-thumb {background: #4a5568; border-radius: 4px;}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #16213e !important;
    border-right: 1px solid #2d3748 !important;
    min-width: 240px !important;
    max-width: 240px !important;
}
section[data-testid="stSidebar"] * {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #5b21b6) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 9px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 10px 20px !important;
    transition: all 0.2s !important;
    box-shadow: 0 3px 12px rgba(124, 58, 237, 0.3) !important;
}
.stButton > button:hover {
    box-shadow: 0 5px 20px rgba(124, 58, 237, 0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0f2040 !important;
    border: 1px solid #2d3748 !important;
    border-radius: 9px !important;
    color: #e2e8f0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 13px !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 2px rgba(124,58,237,0.2) !important;
}

/* ── Select ── */
.stSelectbox > div > div {
    background: #0f2040 !important;
    border: 1px solid #2d3748 !important;
    border-radius: 9px !important;
    color: #e2e8f0 !important;
}

/* ── File uploader ── */
.stFileUploader > div {
    background: #0f2040 !important;
    border: 1px dashed #4a5568 !important;
    border-radius: 9px !important;
}

/* ── Radio ── */
.stRadio > div {
    background: #16213e !important;
    border-radius: 9px !important;
    padding: 8px !important;
}

/* ── Progress ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #5b21b6, #7c3aed, #a78bfa) !important;
    border-radius: 99px !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #16213e !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid #2d3748 !important;
}
.stTabs [data-baseweb="tab"] {
    color: #94a3b8 !important;
    font-weight: 600 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    border-radius: 7px !important;
    padding: 8px 16px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #7c3aed, #5b21b6) !important;
    color: white !important;
}

/* ── Alerts ── */
.stSuccess {
    background: rgba(16,185,129,0.08) !important;
    border: 1px solid rgba(16,185,129,0.25) !important;
    border-radius: 9px !important;
    color: #e2e8f0 !important;
}
.stError {
    background: rgba(239,68,68,0.08) !important;
    border: 1px solid rgba(239,68,68,0.25) !important;
    border-radius: 9px !important;
}
.stWarning {
    background: rgba(245,158,11,0.08) !important;
    border: 1px solid rgba(245,158,11,0.25) !important;
    border-radius: 9px !important;
}
.stInfo {
    background: rgba(124,58,237,0.08) !important;
    border: 1px solid rgba(124,58,237,0.25) !important;
    border-radius: 9px !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #16213e !important;
    border: 1px solid #2d3748 !important;
    border-radius: 9px !important;
    color: #e2e8f0 !important;
    font-weight: 600 !important;
}

/* ── Divider ── */
hr {border-color: #2d3748 !important; margin: 12px 0 !important;}

/* ── Cards ── */
.abd-card {
    background: #16213e;
    border: 1px solid #2d3748;
    border-radius: 13px;
    padding: 20px;
    margin-bottom: 16px;
}
.abd-card-accent {
    background: linear-gradient(135deg, #1a2444, #16213e);
    border: 1px solid #7c3aed;
    border-radius: 13px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 24px rgba(124,58,237,0.12);
}
.abd-card-purple {
    background: linear-gradient(135deg, rgba(124,58,237,0.1), rgba(91,33,182,0.05));
    border: 1px solid rgba(124,58,237,0.25);
    border-radius: 13px;
    padding: 20px;
    margin-bottom: 16px;
}

/* ── Stat cards ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 16px;
}
.stat-box {
    background: #1a2444;
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 16px;
    position: relative;
    overflow: hidden;
}
.stat-box::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 2px 2px 0 0;
}
.stat-box.purple::before {background: #a78bfa;}
.stat-box.green::before  {background: #10b981;}
.stat-box.amber::before  {background: #f59e0b;}
.stat-box.red::before    {background: #ef4444;}
.stat-num {
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1.1;
}
.stat-num.purple {color: #a78bfa;}
.stat-num.green  {color: #10b981;}
.stat-num.amber  {color: #f59e0b;}
.stat-num.red    {color: #ef4444;}
.stat-label {
    font-size: 10px;
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 5px;
}
.stat-sub {font-size: 9px; color: #4a5568; margin-top: 3px; font-family: 'JetBrains Mono', monospace;}

/* ── Logo ── */
.abd-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding-bottom: 16px;
    border-bottom: 1px solid #2d3748;
    margin-bottom: 8px;
}
.abd-logo-icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #7c3aed, #5b21b6);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px;
    box-shadow: 0 4px 12px rgba(124,58,237,0.4);
    flex-shrink: 0;
}
.abd-logo-text {font-size: 16px; font-weight: 800; letter-spacing: -0.3px; color: #e2e8f0;}
.abd-logo-text em {color: #a78bfa; font-style: normal;}
.abd-logo-ver {font-size: 9px; color: #4a5568; font-family: 'JetBrains Mono', monospace; margin-top: 1px;}

/* ── User pill ── */
.user-pill {
    background: rgba(124,58,237,0.08);
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 10px;
    padding: 10px 12px;
    margin-bottom: 16px;
    display: flex; align-items: center; gap: 9px;
}
.user-avatar {
    width: 30px; height: 30px;
    background: linear-gradient(135deg, #7c3aed, #5b21b6);
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 12px; font-weight: 800; color: #fff;
    flex-shrink: 0;
}
.user-email {font-size: 11px; font-weight: 700; color: #a78bfa; word-break: break-all;}
.user-status {font-size: 9px; color: #4a5568; font-family: 'JetBrains Mono', monospace; margin-top: 2px;}

/* ── Nav ── */
.nav-section {
    font-size: 9px; color: #4a5568;
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase; letter-spacing: 1.5px;
    padding: 12px 4px 5px;
}

/* ── Feed ── */
.feed-item {
    display: flex; align-items: center; gap: 8px;
    padding: 8px 10px; border-radius: 8px;
    font-size: 11px; margin-bottom: 4px;
    border: 1px solid transparent;
}
.feed-item.sent {background: rgba(16,185,129,0.06); border-color: rgba(16,185,129,0.15);}
.feed-item.failed {background: rgba(239,68,68,0.06); border-color: rgba(239,68,68,0.15);}
.feed-dot {width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0;}
.feed-email {font-family: 'JetBrains Mono', monospace; font-size: 10px; flex: 1; color: #e2e8f0;}
.feed-badge {font-size: 9px; padding: 2px 7px; border-radius: 99px; font-family: 'JetBrains Mono', monospace; font-weight: 600;}
.feed-badge.sent {background: rgba(16,185,129,0.12); color: #10b981;}
.feed-badge.failed {background: rgba(239,68,68,0.12); color: #ef4444;}
.feed-time {font-size: 9px; color: #4a5568; font-family: 'JetBrains Mono', monospace;}

/* ── Config field ── */
.cfg-field {margin-bottom: 10px;}
.cfg-label {font-size: 9px; color: #4a5568; text-transform: uppercase; letter-spacing: 1px; font-family: 'JetBrains Mono', monospace; margin-bottom: 4px;}
.cfg-value {
    background: rgba(255,255,255,0.03);
    border: 1px solid #2d3748;
    border-radius: 7px; padding: 8px 11px;
    font-size: 11px; font-family: 'JetBrains Mono', monospace;
    color: #e2e8f0; display: flex; align-items: center; justify-content: space-between;
}
.cfg-badge {font-size: 9px; padding: 2px 8px; border-radius: 99px; font-family: 'JetBrains Mono', monospace;}
.cfg-badge.purple {background: rgba(124,58,237,0.15); color: #a78bfa; border: 1px solid rgba(124,58,237,0.3);}
.cfg-badge.green  {background: rgba(16,185,129,0.1);  color: #10b981; border: 1px solid rgba(16,185,129,0.25);}

/* ── Project cards ── */
.project-card {
    background: #1a2444;
    border: 1px solid #2d3748;
    border-radius: 11px;
    padding: 14px 16px;
    margin-bottom: 10px;
    display: flex; align-items: center; justify-content: space-between; gap: 12px;
    transition: all 0.2s;
}
.project-card:hover {border-color: #7c3aed; box-shadow: 0 4px 16px rgba(124,58,237,0.15);}
.project-name {font-size: 12px; font-weight: 700; color: #e2e8f0;}
.project-desc {font-size: 10px; color: #94a3b8; margin-top: 3px;}
.project-link {
    font-size: 10px; font-weight: 700; color: #a78bfa;
    background: rgba(124,58,237,0.12); border: 1px solid rgba(124,58,237,0.25);
    border-radius: 7px; padding: 5px 12px; white-space: nowrap;
    text-decoration: none; font-family: 'JetBrains Mono', monospace;
}

/* ── Guide section ── */
.guide-step {
    background: #1a2444;
    border: 1px solid #2d3748;
    border-left: 3px solid #7c3aed;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin-bottom: 10px;
}
.guide-step-title {font-size: 12px; font-weight: 700; color: #a78bfa; margin-bottom: 5px;}
.guide-step-body {font-size: 11.5px; color: #94a3b8; line-height: 1.7;}
.guide-warn {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 9px; padding: 10px 14px; margin-bottom: 10px;
    font-size: 11.5px; color: #fbbf24; line-height: 1.7;
}
.guide-tip {
    background: rgba(16,185,129,0.08);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 9px; padding: 10px 14px; margin-bottom: 10px;
    font-size: 11.5px; color: #34d399; line-height: 1.7;
}

/* ── Footer ── */
.abd-footer {
    text-align: center; padding: 24px 0 8px;
    border-top: 1px solid #2d3748; margin-top: 24px;
}
.abd-footer a {color: #a78bfa; text-decoration: none;}
.abd-footer a:hover {color: #c4b5fd;}

/* ── Welcome banner ── */
.welcome-banner {
    background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(91,33,182,0.06));
    border: 1px solid rgba(124,58,237,0.2);
    border-radius: 13px; padding: 18px 22px; margin-bottom: 20px;
}
.welcome-title {font-size: 20px; font-weight: 800; letter-spacing: -0.4px; color: #e2e8f0;}
.welcome-title em {color: #a78bfa; font-style: normal;}
.welcome-sub {font-size: 11px; color: #94a3b8; font-family: 'JetBrains Mono', monospace; margin-top: 4px;}
.live-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: rgba(16,185,129,0.1); color: #10b981;
    border: 1px solid rgba(16,185,129,0.25);
    border-radius: 99px; padding: 3px 10px;
    font-size: 10px; font-family: 'JetBrains Mono', monospace;
    margin-top: 8px;
}

/* ── Mono text ── */
.mono {font-family: 'JetBrains Mono', monospace;}

/* ── Email preview ── */
.email-preview {
    background: #0f2040; border: 1px solid #2d3748;
    border-radius: 10px; overflow: hidden;
}
.email-preview-head {
    padding: 12px 16px; border-bottom: 1px solid #2d3748;
    background: rgba(124,58,237,0.05);
}
.email-meta {font-family: 'JetBrains Mono', monospace; font-size: 10.5px; color: #94a3b8; margin-bottom: 2px; line-height: 1.6;}
.email-meta span {color: #e2e8f0;}
.email-var {color: #a78bfa; font-weight: 600;}
.email-body-preview {padding: 14px 16px; font-size: 12px; line-height: 1.85; color: #94a3b8;}
</style>
""", unsafe_allow_html=True)

# ── Session State ──────────────────────────────────────────────────────────────
for key, val in {
    "logged_in": False, "gmail": "", "app_password": "",
    "templates": [], "stop_sending": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = val


# ── Helpers ───────────────────────────────────────────────────────────────────
def footer():
    st.markdown("""
    <div class="abd-footer">
        <div style="margin-bottom:14px;">
            <div style="font-size:11px; color:#4a5568; font-family:'JetBrains Mono',monospace; margin-bottom:10px;">MY PROJECTS</div>
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
        <div style="margin-bottom:10px;">
            <a href="https://www.linkedin.com/in/abdul-rehman-raza-7a125b332" target="_blank"
               style="display:inline-flex;align-items:center;gap:7px;background:rgba(124,58,237,0.12);
               border:1px solid rgba(124,58,237,0.25);border-radius:9px;padding:8px 18px;
               font-size:12px;font-weight:700;color:#a78bfa;text-decoration:none;">
                🔗 Connect with Abdul Rehman Raza on LinkedIn
            </a>
        </div>
        <div style="font-size:10px;color:#4a5568;font-family:'JetBrains Mono',monospace;">
            Made with ❤️ by <span style="color:#a78bfa;font-weight:700;">Abdulll,s</span> · ABD MailForge v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)


def card(content_fn, accent=False, purple=False):
    cls = "abd-card-accent" if accent else ("abd-card-purple" if purple else "abd-card")
    st.markdown(f'<div class="{cls}">', unsafe_allow_html=True)
    content_fn()
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def login_page():
    col_l, col_m, col_r = st.columns([1, 2, 1])
    with col_m:

        # Logo
        st.markdown("""
        <div style="text-align:center; padding: 32px 0 24px;">
            <div style="display:inline-flex;align-items:center;gap:12px;margin-bottom:8px;">
                <div style="width:46px;height:46px;background:linear-gradient(135deg,#7c3aed,#5b21b6);
                    border-radius:12px;display:flex;align-items:center;justify-content:center;
                    font-size:22px;box-shadow:0 6px 20px rgba(124,58,237,0.4);">✉️</div>
                <div style="text-align:left;">
                    <div style="font-size:22px;font-weight:800;letter-spacing:-0.5px;color:#e2e8f0;">
                        ABD <span style="color:#a78bfa;">Mail</span>Forge</div>
                    <div style="font-size:10px;color:#4a5568;font-family:'JetBrains Mono',monospace;">
                        BULK EMAIL SENDER BOT · V2.0</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Quick guide before login
        with st.expander("📖 How It Works — Read Before Using", expanded=False):
            st.markdown("""
            <div style="font-size:12px;line-height:1.8;color:#94a3b8;">

            <div class="guide-step">
                <div class="guide-step-title">Step 1 — Login with Gmail App Password</div>
                <div class="guide-step-body">Use your Gmail address and a 16-character App Password (not your real Gmail password).
                Generate it from: Google Account → Security → 2-Step Verification → App Passwords</div>
            </div>

            <div class="guide-step">
                <div class="guide-step-title">Step 2 — Add Recipients</div>
                <div class="guide-step-body">Upload a CSV file (with Email column) or paste emails directly — one per line.
                Maximum 400 emails per session. Recommended: 100–150 per day to stay safe.</div>
            </div>

            <div class="guide-step">
                <div class="guide-step-title">Step 3 — Set Up Templates</div>
                <div class="guide-step-body">Create 3 different email templates (Professional, Friendly, Short).
                The app will randomly pick one per email — this reduces spam flagging.</div>
            </div>

            <div class="guide-step">
                <div class="guide-step-title">Step 4 — Send!</div>
                <div class="guide-step-body">Click Send Now. Emails go out with a random 15–45 second gap between each one.
                Keep the browser tab open until sending is complete.</div>
            </div>

            <div class="guide-warn">
            ⚠️ <strong>Important:</strong> Keep your browser tab open while sending.
            If you close the tab or your screen locks, sending will stop.
            On mobile, keep the screen on. Use a stable internet connection — preferably mobile hotspot.
            </div>

            </div>
            """, unsafe_allow_html=True)

        # Login form
        st.markdown('<div class="abd-card-accent">', unsafe_allow_html=True)
        st.markdown("#### 🔐 Login to ABD MailForge")
        st.caption("Enter your Gmail and 16-character App Password to continue")

        gmail_input = st.text_input(
            "📧 Gmail Address",
            placeholder="yourname@gmail.com",
            key="login_gmail"
        )
        pass_input = st.text_input(
            "🔑 App Password",
            type="password",
            placeholder="xxxx xxxx xxxx xxxx (16 characters)",
            key="login_pass"
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
        <div style="background:#0f2040;border:1px solid #2d3748;border-radius:9px;
             padding:10px 14px;margin-bottom:12px;font-size:11px;color:#94a3b8;
             font-family:'JetBrains Mono',monospace;line-height:1.7;">
        ℹ️ How to get App Password:<br>
        Google Account → Security → 2-Step Verification → App Passwords<br>
        Select: Mail → Generate → Copy the 16-character code
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Login & Verify Gmail", use_container_width=True):
            if not gmail_input or not pass_input:
                st.error("Please enter both Gmail and App Password.")
                return

            if check_blocked(gmail_input):
                st.error("⛔ This account is blocked after 5 failed attempts. Please use a different Gmail.")
                return

            with st.spinner("Verifying Gmail credentials..."):
                ok, msg = verify_gmail(gmail_input, pass_input)

            if ok:
                reset_failed(gmail_input)
                save_session(gmail_input, pass_input.replace(" ", ""))
                st.session_state.logged_in = True
                st.session_state.gmail = gmail_input
                st.session_state.app_password = pass_input.replace(" ", "")
                saved = load_templates(gmail_input)
                if saved:
                    st.session_state.templates = saved
                st.success("✅ Gmail verified! Logging you in...")
                time.sleep(1)
                st.rerun()
            else:
                attempts, blocked = increment_failed(gmail_input)
                remaining = 5 - attempts
                if blocked:
                    st.error("⛔ Account blocked — 5 failed attempts reached. Use a different Gmail.")
                else:
                    st.error(f"❌ {msg} — {remaining} attempt(s) remaining before block.")

        footer()


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
def render_sidebar():
    with st.sidebar:
        initials = st.session_state.gmail[:2].upper() if st.session_state.gmail else "AB"

        st.markdown(f"""
        <div class="abd-logo">
            <div class="abd-logo-icon">✉️</div>
            <div>
                <div class="abd-logo-text">ABD <em>Mail</em>Forge</div>
                <div class="abd-logo-ver">BULK EMAIL BOT · V2.0</div>
            </div>
        </div>
        <div class="user-pill">
            <div class="user-avatar">{initials}</div>
            <div>
                <div class="user-email">{st.session_state.gmail}</div>
                <div class="user-status">● SESSION ACTIVE</div>
            </div>
        </div>
        <div class="nav-section">Main</div>
        """, unsafe_allow_html=True)

        nav = st.radio(
            "nav",
            ["📊 Dashboard", "📤 Send Emails", "📋 Templates", "📖 Guide & Docs", "⚙️ Settings"],
            label_visibility="collapsed"
        )

        st.markdown('<div class="nav-section">Account</div>', unsafe_allow_html=True)

        if st.button("🚪 Logout", use_container_width=True):
            for k in ["logged_in", "gmail", "app_password", "templates", "stop_sending"]:
                st.session_state[k] = False if k == "logged_in" else ([] if k == "templates" else "")
            st.rerun()

        st.markdown("---")
        st.markdown("""
        <div style="font-size:10px;color:#4a5568;font-family:'JetBrains Mono',monospace;text-align:center;padding:4px 0;">
            <a href="https://www.linkedin.com/in/abdul-rehman-raza-7a125b332"
               target="_blank" style="color:#a78bfa;text-decoration:none;">
                🔗 LinkedIn — Abdulll,s
            </a><br>
            <span style="color:#2d3748;margin-top:4px;display:block;">ABD MailForge v2.0</span>
        </div>
        """, unsafe_allow_html=True)

    return nav


# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
def dashboard_page():
    st.markdown("""
    <div class="welcome-banner">
        <div class="welcome-title">Welcome to <em>ABD MailForge</em> ✉️</div>
        <div class="welcome-sub">YOUR SESSION · GMAIL SMTP ACTIVE · SUPABASE CONNECTED</div>
        <div class="live-badge">● LIVE SESSION</div>
    </div>
    """, unsafe_allow_html=True)

    # Refresh
    col_r1, col_r2 = st.columns([4, 1])
    with col_r2:
        if st.button("🔄 Refresh Stats"):
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
            <div class="stat-sub">across all sessions</div>
        </div>
        <div class="stat-box red">
            <div class="stat-num red">{stats['failed']}</div>
            <div class="stat-label">Total Failed</div>
            <div class="stat-sub">check logs below</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Tabs
    tab1, tab2 = st.tabs(["📜 Send History", "📊 Summary"])

    with tab1:
        logs = get_logs(st.session_state.gmail, limit=50)
        if logs:
            log_html = ""
            for log in logs:
                icon = "✓" if log["status"] == "sent" else "✗"
                cls = "sent" if log["status"] == "sent" else "failed"
                t = str(log.get("sent_at", ""))[:16].replace("T", " ")
                tmpl = log.get("template_used", "—")
                err = f" · {log.get('error','')}" if log.get("error") else ""
                log_html += f"""
                <div class="feed-item {cls}">
                    <div class="feed-dot" style="background:{'#10b981' if cls=='sent' else '#ef4444'}"></div>
                    <div class="feed-email">{log['recipient']}</div>
                    <div class="feed-badge {cls}">{icon} {cls.upper()}</div>
                    <div class="feed-time">{t} · {tmpl}{err}</div>
                </div>"""
            st.markdown(f"""
            <div style="background:#0f2040;border:1px solid #2d3748;border-radius:12px;
                 padding:14px;max-height:400px;overflow-y:auto;">
                {log_html}
            </div>""", unsafe_allow_html=True)
        else:
            st.info("No send history yet. Go to **Send Emails** to start sending.")

    with tab2:
        if stats['total'] > 0:
            rate = round((stats['sent'] / stats['total']) * 100, 1)
            st.markdown(f"""
            <div class="abd-card">
                <div style="font-size:13px;font-weight:700;margin-bottom:14px;">Session Summary</div>
                <div style="display:flex;gap:24px;flex-wrap:wrap;">
                    <div><div style="font-size:28px;font-weight:800;color:#a78bfa;">{rate}%</div>
                         <div style="font-size:10px;color:#94a3b8;font-family:'JetBrains Mono',monospace;">SUCCESS RATE</div></div>
                    <div><div style="font-size:28px;font-weight:800;color:#10b981;">{stats['sent']}</div>
                         <div style="font-size:10px;color:#94a3b8;font-family:'JetBrains Mono',monospace;">DELIVERED</div></div>
                    <div><div style="font-size:28px;font-weight:800;color:#ef4444;">{stats['failed']}</div>
                         <div style="font-size:10px;color:#94a3b8;font-family:'JetBrains Mono',monospace;">FAILED</div></div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.info("No data yet. Send some emails first!")

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# SEND PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def send_page():
    st.markdown("## 📤 Send Emails")
    st.caption("Upload a CSV or paste email addresses, write your message, and hit Send.")

    col1, col2 = st.columns([1, 1], gap="large")

    # ── Recipients ──
    with col1:
        st.markdown('<div class="abd-card">', unsafe_allow_html=True)
        st.markdown("#### 📧 Recipients")
        st.caption("Choose how to add email addresses")

        method = st.radio("Input method", ["📎 Upload CSV", "✏️ Paste Emails"], horizontal=True, label_visibility="collapsed")

        emails_list = []

        if method == "📎 Upload CSV":
            st.caption("CSV must have an **Email** column. Name column is optional.")
            csv_file = st.file_uploader("Choose CSV file", type=["csv"], label_visibility="collapsed")
            if csv_file:
                try:
                    df = pd.read_csv(csv_file)
                    email_col = next((c for c in df.columns if "email" in c.lower() or "mail" in c.lower()), df.columns[0])
                    emails_list = [str(e).strip().lower() for e in df[email_col].dropna() if "@" in str(e)][:400]
                    st.success(f"✅ {len(emails_list)} emails loaded from CSV")
                    with st.expander(f"Preview ({min(5, len(emails_list))} shown)"):
                        for e in emails_list[:5]:
                            st.code(e, language=None)
                except Exception as ex:
                    st.error(f"CSV error: {ex}")
        else:
            st.caption("Paste one email per line. Maximum 400 emails.")
            pasted = st.text_area("Email addresses", placeholder="ahmed@gmail.com\nsara@yahoo.com\nbilal@hotmail.com", height=160, label_visibility="collapsed")
            if pasted:
                emails_list = parse_emails_from_text(pasted)
                if emails_list:
                    st.success(f"✅ {len(emails_list)} valid emails found")
                else:
                    st.warning("No valid emails found. Check format.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Message ──
    with col2:
        st.markdown('<div class="abd-card">', unsafe_allow_html=True)
        st.markdown("#### ✉️ Message")
        st.caption("Write your message or choose a saved template")

        subject = st.text_input("Subject line", placeholder="Your Daily Update — June 2026")

        template_opts = ["✍️ Write custom message"] + [t["name"] for t in st.session_state.templates]
        if len(st.session_state.templates) >= 2:
            template_opts.append("🎲 Random template (recommended)")

        chosen = st.selectbox("Template", template_opts, label_visibility="collapsed")

        use_random = False
        body = ""

        if chosen == "✍️ Write custom message":
            body = st.text_area("Message body", placeholder="Write your email message here...", height=130, label_visibility="collapsed")
        elif chosen == "🎲 Random template (recommended)":
            use_random = True
            st.info("✓ A random template will be selected for each email — reduces spam flagging.")
        else:
            t = next((t for t in st.session_state.templates if t["name"] == chosen), None)
            if t:
                body = t["body"]
                st.text_area("Preview", value=body, height=130, disabled=True, label_visibility="collapsed")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── PDF ──
    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### 📎 PDF Attachment")
    st.caption("Optional — same PDF will be attached to every email in this batch")
    pdf_file = st.file_uploader("Upload PDF", type=["pdf"], label_visibility="collapsed")
    if pdf_file:
        st.success(f"✅ {pdf_file.name} ready ({round(len(pdf_file.read())/1024, 1)} KB)")
        pdf_file.seek(0)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    if not emails_list:
        st.warning("⚠️ Add recipients first (CSV or paste)")
        footer()
        return
    if not subject:
        st.warning("⚠️ Write a subject line")
        footer()
        return
    if not use_random and not body:
        st.warning("⚠️ Write a message or select a template")
        footer()
        return

    # Summary
    est_mins = (len(emails_list) * 30) // 60
    st.markdown(f"""
    <div class="abd-card-purple">
        <div style="font-size:12px;color:#94a3b8;font-family:'JetBrains Mono',monospace;
             margin-bottom:12px;text-transform:uppercase;letter-spacing:1px;">Send Summary</div>
        <div style="display:flex;gap:28px;flex-wrap:wrap;">
            <div><div style="font-size:26px;font-weight:800;color:#a78bfa;">{len(emails_list)}</div>
                 <div style="font-size:10px;color:#94a3b8;font-family:'JetBrains Mono',monospace;">RECIPIENTS</div></div>
            <div><div style="font-size:26px;font-weight:800;color:#10b981;">~{est_mins}m</div>
                 <div style="font-size:10px;color:#94a3b8;font-family:'JetBrains Mono',monospace;">EST. TIME</div></div>
            <div><div style="font-size:26px;font-weight:800;color:#f59e0b;">15–45s</div>
                 <div style="font-size:10px;color:#94a3b8;font-family:'JetBrains Mono',monospace;">RANDOM GAP</div></div>
            <div><div style="font-size:26px;font-weight:800;color:#a78bfa;">{"🎲 RND" if use_random else "FIXED"}</div>
                 <div style="font-size:10px;color:#94a3b8;font-family:'JetBrains Mono',monospace;">TEMPLATE</div></div>
        </div>
        <div style="margin-top:12px;font-size:11px;color:#f59e0b;">
        ⚠️ Keep this browser tab open while sending. Closing it will stop the process.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1:
        start = st.button("🚀 Start Sending", use_container_width=True)
    with c2:
        if st.button("⏹ Stop", use_container_width=True):
            st.session_state.stop_sending = True

    if start:
        st.session_state.stop_sending = False
        pdf_bytes = pdf_file.read() if pdf_file else None
        pdf_name = pdf_file.name if pdf_file else None

        st.markdown("---")
        st.markdown("### 📡 Live Sending Progress")

        prog = st.progress(0)
        status = st.empty()
        log_box = st.empty()

        sent_count = failed_count = 0
        logs_html = ""
        total = len(emails_list)

        for i, email in enumerate(emails_list):
            if st.session_state.stop_sending:
                st.warning(f"⏹ Stopped — {sent_count} sent, {failed_count} failed")
                break

            if use_random and st.session_state.templates:
                tname, tbody = pick_random_template(st.session_state.templates)
                cur_body = tbody
                cur_tname = tname
            else:
                cur_body = body
                cur_tname = chosen

            status.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#94a3b8;
                 background:#0f2040;border:1px solid #2d3748;border-radius:8px;padding:10px 14px;">
            Sending {i+1} / {total} → <span style="color:#e2e8f0;">{email}</span>
            </div>""", unsafe_allow_html=True)

            ok, msg = send_email(
                st.session_state.gmail, st.session_state.app_password,
                email, subject, cur_body, pdf_bytes, pdf_name
            )

            if ok:
                sent_count += 1
                logs_html = f'<div class="feed-item sent"><div class="feed-dot" style="background:#10b981"></div><div class="feed-email">{email}</div><div class="feed-badge sent">✓ SENT</div><div class="feed-time">[{i+1}/{total}] · {cur_tname}</div></div>' + logs_html
                log_send(st.session_state.gmail, email, subject, cur_tname, "sent")
            else:
                failed_count += 1
                logs_html = f'<div class="feed-item failed"><div class="feed-dot" style="background:#ef4444"></div><div class="feed-email">{email}</div><div class="feed-badge failed">✗ FAILED</div><div class="feed-time">[{i+1}/{total}] · {msg}</div></div>' + logs_html
                log_send(st.session_state.gmail, email, subject, cur_tname, "failed", msg)

            prog.progress((i + 1) / total)
            log_box.markdown(f"""
            <div style="background:#0f2040;border:1px solid #2d3748;border-radius:11px;
                 padding:12px;max-height:280px;overflow-y:auto;">
                {logs_html}
            </div>""", unsafe_allow_html=True)

            if i < total - 1 and not st.session_state.stop_sending:
                delay = get_random_interval()
                for r in range(delay, 0, -1):
                    status.markdown(f"""
                    <div style="font-family:'JetBrains Mono',monospace;font-size:12px;color:#94a3b8;
                         background:#0f2040;border:1px solid #2d3748;border-radius:8px;padding:10px 14px;">
                    ⏳ Next email in <span style="color:#a78bfa;">{r}s</span> · {sent_count} sent · {failed_count} failed
                    </div>""", unsafe_allow_html=True)
                    time.sleep(1)
                    if st.session_state.stop_sending:
                        break

        status.empty()
        if not st.session_state.stop_sending:
            if failed_count == 0:
                st.success(f"🎉 All done! {sent_count} emails sent successfully.")
            else:
                st.warning(f"✅ Completed — {sent_count} sent, {failed_count} failed.")

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATES PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def templates_page():
    st.markdown("## 📋 Email Templates")
    st.caption("Create up to 5 templates. The app randomly picks one per email to avoid spam filters.")

    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### ➕ Create New Template")
    st.caption("Give it a name and write the body. Use natural, human-like language.")

    t_name = st.text_input("Template name", placeholder="e.g. Professional, Friendly, Short Update")
    t_body = st.text_area("Template body", placeholder="Write your email message here...", height=140)

    if st.button("💾 Save Template"):
        if not t_name or not t_body:
            st.error("Both name and body are required.")
        elif len(st.session_state.templates) >= 5:
            st.error("Maximum 5 templates allowed.")
        elif any(t["name"] == t_name for t in st.session_state.templates):
            st.error(f"A template named '{t_name}' already exists.")
        else:
            st.session_state.templates.append({"name": t_name, "body": t_body})
            save_templates(st.session_state.gmail, st.session_state.templates)
            st.success(f"✅ Template '{t_name}' saved!")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.templates:
        st.markdown(f"### 📚 Saved Templates ({len(st.session_state.templates)} / 5)")
        st.caption("Tip: Having 3 different templates (Professional + Friendly + Short) gives the best results.")

        for i, t in enumerate(st.session_state.templates):
            with st.expander(f"📄 {t['name']}"):
                st.text_area("Content", value=t["body"], height=100, disabled=True, key=f"tview_{i}")
                if st.button(f"🗑️ Delete '{t['name']}'", key=f"tdel_{i}"):
                    st.session_state.templates.pop(i)
                    save_templates(st.session_state.gmail, st.session_state.templates)
                    st.rerun()
    else:
        st.info("No templates yet. Create your first template above.")

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# GUIDE PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def guide_page():
    st.markdown("## 📖 Guide & Documentation")
    st.caption("Everything you need to use ABD MailForge safely and effectively.")

    tab1, tab2, tab3, tab4 = st.tabs(["🚀 Getting Started", "📧 Sending Tips", "🔒 Security", "⚠️ Important Warnings"])

    with tab1:
        st.markdown("""
        <div class="guide-step">
            <div class="guide-step-title">1 — Get a Gmail App Password</div>
            <div class="guide-step-body">
            Go to your Google Account → Security → 2-Step Verification → App Passwords.<br>
            Select "Mail" and "Other (custom name)", name it "MailForge", then click Generate.<br>
            You will get a 16-character code — copy it. This is your App Password.<br>
            <strong style="color:#a78bfa;">Note: This is NOT your real Gmail password. It is a separate access key for apps.</strong>
            </div>
        </div>
        <div class="guide-step">
            <div class="guide-step-title">2 — Prepare Your Email List</div>
            <div class="guide-step-body">
            Option A — CSV File: Create a spreadsheet with a column named "Email". Save as CSV and upload.<br>
            Option B — Paste: Type or paste emails directly, one per line. Maximum 400 per session.<br>
            <strong style="color:#a78bfa;">Recommended: 100–150 emails per day to avoid Gmail sending limits.</strong>
            </div>
        </div>
        <div class="guide-step">
            <div class="guide-step-title">3 — Create 3 Templates</div>
            <div class="guide-step-body">
            Go to the Templates page and create 3 different versions of your message:<br>
            • Template A — Professional tone (formal language)<br>
            • Template B — Friendly tone (casual, warm)<br>
            • Template C — Short and direct (brief, to the point)<br>
            When sending, select "Random Template" — the app picks a different one for each email.
            </div>
        </div>
        <div class="guide-step">
            <div class="guide-step-title">4 — Send Your Emails</div>
            <div class="guide-step-body">
            Go to Send Emails, upload your list or paste emails, write your subject, attach a PDF if needed, then click Start Sending.<br>
            The app will send one email every 15–45 seconds (random) to mimic human behavior.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        st.markdown("""
        <div class="guide-step">
            <div class="guide-step-title">How Many Emails Per Day?</div>
            <div class="guide-step-body">
            • Beginner (new Gmail): 50–100 per day<br>
            • Regular Gmail: 100–200 per day<br>
            • Old active Gmail (2+ years): up to 400 per day<br>
            <strong style="color:#a78bfa;">Gmail's official limit is 500 per day. Stay well below to avoid suspension.</strong>
            </div>
        </div>
        <div class="guide-step">
            <div class="guide-step-title">Why Random 15–45 Second Gaps?</div>
            <div class="guide-step-body">
            Sending emails too fast looks like spam to Gmail's filters. The random delay makes your sending pattern look like a real human typing and sending emails manually. This significantly reduces the chance of your emails being flagged as spam.
            </div>
        </div>
        <div class="guide-step">
            <div class="guide-step-title">Why Use 3 Different Templates?</div>
            <div class="guide-step-body">
            Spam filters detect when the exact same email is sent to hundreds of people. By rotating 3 different versions of your message, each email looks unique — reducing spam detection. Keep the message natural and avoid too many links or ALL CAPS text.
            </div>
        </div>
        <div class="guide-tip">
        💡 <strong>Pro Tips:</strong><br>
        • Use a Gmail account that has been active for some time (older accounts have better reputation)<br>
        • Avoid sending to invalid or old email addresses — bounces hurt your reputation<br>
        • Always include a clear subject line — avoid spam trigger words like "FREE!!!" or "URGENT!!!"<br>
        • Use a mobile hotspot for a stable internet connection
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        st.markdown("""
        <div class="guide-step">
            <div class="guide-step-title">App Password vs Real Password</div>
            <div class="guide-step-body">
            Your real Gmail password never enters this app. An App Password is a separate 16-character code that only allows sending emails — nothing else. If you ever feel it is compromised, you can revoke it from Google Account settings without changing your real password.
            </div>
        </div>
        <div class="guide-step">
            <div class="guide-step-title">How to Revoke App Password</div>
            <div class="guide-step-body">
            Google Account → Security → 2-Step Verification → App Passwords → Find "MailForge" → Delete.<br>
            This immediately stops anyone from using that password. Generate a new one to continue using the app.
            </div>
        </div>
        <div class="guide-step">
            <div class="guide-step-title">Always Keep 2-Step Verification ON</div>
            <div class="guide-step-body">
            App Passwords only work when 2-Step Verification is enabled on your Google Account. This also adds an extra layer of security to your Gmail. Never turn it off.
            </div>
        </div>
        <div class="guide-step">
            <div class="guide-step-title">Your Data in Supabase</div>
            <div class="guide-step-body">
            Your send logs (who you sent to, when, which template) are stored in your private Supabase database. Only you can access this via your Supabase dashboard. No third party can read your data.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab4:
        st.markdown("""
        <div class="guide-warn">
        ⚠️ <strong>Keep Browser Tab Open While Sending</strong><br>
        ABD MailForge sends emails from your browser session. If you close the tab, switch apps, or lock your screen, the sending process will stop immediately. You will need to restart and re-upload your email list.
        </div>
        <div class="guide-warn">
        ⚠️ <strong>Keep Your Screen On — Mobile Users</strong><br>
        On mobile, if the screen turns off or the browser goes to background, sending stops. Keep your screen active the entire time. Consider keeping your phone plugged in and screen brightness low but on.
        </div>
        <div class="guide-warn">
        ⚠️ <strong>Move Your Mouse — PC/Laptop Users</strong><br>
        If your computer goes to sleep or the screen saver activates, the browser may suspend the tab. Move your mouse occasionally or adjust your power settings to prevent sleep during sending.
        </div>
        <div class="guide-warn">
        ⚠️ <strong>Use Stable Internet — Hotspot Recommended</strong><br>
        If your internet disconnects even for a moment during sending, that email attempt may fail. Mobile hotspot is more stable than Wi-Fi in most cases. Do not switch networks while sending.
        </div>
        <div class="guide-tip">
        💡 <strong>Best Practice Checklist Before Sending:</strong><br>
        ✓ Browser tab is open and visible<br>
        ✓ Internet connection is stable (hotspot preferred)<br>
        ✓ Screen will not lock or sleep<br>
        ✓ Email list is verified and clean<br>
        ✓ Subject line is written and natural<br>
        ✓ Templates are ready (at least 2–3)<br>
        ✓ PDF is attached if needed<br>
        ✓ You have checked Gmail daily limits
        </div>
        """, unsafe_allow_html=True)

    footer()


# ═══════════════════════════════════════════════════════════════════════════════
# SETTINGS PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def settings_page():
    st.markdown("## ⚙️ Settings")

    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### 📧 Current Account")
    st.markdown(f"""
    <div style="font-family:'JetBrains Mono',monospace;font-size:12px;line-height:2;color:#94a3b8;">
    Gmail: <span style="color:#a78bfa;font-weight:700;">{st.session_state.gmail}</span><br>
    Status: <span style="color:#10b981;">● Active Session</span><br>
    Templates saved: <span style="color:#e2e8f0;">{len(st.session_state.templates)}</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### 🔑 Update App Password")
    st.caption("If your App Password has changed or been revoked, update it here.")
    new_pass = st.text_input("New App Password", type="password", placeholder="xxxx xxxx xxxx xxxx")
    if st.button("🔄 Update Password"):
        if new_pass:
            ok, msg = verify_gmail(st.session_state.gmail, new_pass)
            if ok:
                st.session_state.app_password = new_pass.replace(" ", "")
                save_session(st.session_state.gmail, new_pass.replace(" ", ""))
                st.success("✅ App Password updated successfully.")
            else:
                st.error(f"❌ Verification failed: {msg}")
        else:
            st.error("Please enter a new App Password.")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### ℹ️ App Information")
    st.markdown("""
    <div style="font-family:'JetBrains Mono',monospace;font-size:11px;color:#94a3b8;line-height:2.2;">
    App Name: ABD MailForge<br>
    Version: 2.0<br>
    Made by: Abdulll,s<br>
    Email Engine: Gmail SMTP (SSL Port 465)<br>
    Database: Supabase PostgreSQL<br>
    Send Interval: Random 15–45 seconds<br>
    Max Emails per Session: 400<br>
    Max Templates: 5<br>
    Deployment: Streamlit Cloud
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
    nav = render_sidebar()
    if nav == "📊 Dashboard":
        dashboard_page()
    elif nav == "📤 Send Emails":
        send_page()
    elif nav == "📋 Templates":
        templates_page()
    elif nav == "📖 Guide & Docs":
        guide_page()
    elif nav == "⚙️ Settings":
        settings_page()
