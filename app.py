import streamlit as st
import pandas as pd
import time
from datetime import datetime
from mailer import verify_gmail, send_email, get_random_interval, pick_random_template, parse_emails_from_text
from db import (save_session, check_blocked, increment_failed, reset_failed,
                save_templates, load_templates, log_send, get_logs, get_stats)

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ABD MailForge",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
}

/* Background */
.stApp {
    background: linear-gradient(135deg, #0a0000 0%, #0f0000 40%, #1a0505 100%);
    min-height: 100vh;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0000 0%, #1a0000 100%) !important;
    border-right: 1px solid #4a0a0a !important;
}

/* Cards */
.abd-card {
    background: linear-gradient(135deg, #1a0505, #200808);
    border: 1px solid #4a0a0a;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 4px 24px rgba(192,57,43,0.08);
}

.abd-card-accent {
    background: linear-gradient(135deg, #1a0505, #200808);
    border: 1px solid #C0392B;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 16px;
    box-shadow: 0 4px 32px rgba(192,57,43,0.2);
}

/* Stat cards */
.stat-row { display: flex; gap: 12px; margin-bottom: 20px; flex-wrap: wrap; }
.stat-box {
    flex: 1; min-width: 120px;
    background: linear-gradient(135deg, #1a0505, #250a0a);
    border: 1px solid #4a0a0a;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}
.stat-num { font-size: 32px; font-weight: 800; color: #C0392B; line-height: 1; }
.stat-label { font-size: 11px; color: #8a4a4a; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }

/* Logo */
.logo-main {
    font-size: 28px; font-weight: 800;
    color: #f0e6e6;
    letter-spacing: -0.5px;
    line-height: 1;
}
.logo-main span { color: #C0392B; }
.logo-sub { font-size: 11px; color: #6a3a3a; font-family: 'IBM Plex Mono', monospace; margin-top: 4px; }

/* Status badge */
.badge-online {
    display: inline-block;
    background: rgba(192,57,43,0.15);
    color: #C0392B;
    border: 1px solid rgba(192,57,43,0.4);
    border-radius: 99px;
    padding: 3px 12px;
    font-size: 11px;
    font-family: 'IBM Plex Mono', monospace;
}

/* Log items */
.log-sent { color: #00e5a0; font-family: 'IBM Plex Mono', monospace; font-size: 12px; }
.log-failed { color: #ef4444; font-family: 'IBM Plex Mono', monospace; font-size: 12px; }
.log-info { color: #8a6a4a; font-family: 'IBM Plex Mono', monospace; font-size: 12px; }

/* Footer */
.abd-footer {
    text-align: center;
    padding: 24px 0 8px;
    color: #4a2a2a;
    font-size: 12px;
    border-top: 1px solid #2a0808;
    margin-top: 32px;
}
.abd-footer a { color: #C0392B; text-decoration: none; }
.abd-footer a:hover { color: #e74c3c; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #C0392B, #96281b) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    padding: 10px 24px !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #e74c3c, #C0392B) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(192,57,43,0.4) !important;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: #150303 !important;
    border: 1px solid #4a0a0a !important;
    border-radius: 8px !important;
    color: #f0e6e6 !important;
}

/* Progress */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #96281b, #C0392B, #e74c3c) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #0f0000 !important;
    border-radius: 10px !important;
    padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    color: #6a3a3a !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: #C0392B !important;
    color: white !important;
    border-radius: 8px !important;
}

/* Divider */
hr { border-color: #2a0808 !important; }

/* Success/Error */
.stSuccess { background: rgba(0,229,160,0.08) !important; border: 1px solid rgba(0,229,160,0.2) !important; }
.stError { background: rgba(239,68,68,0.08) !important; border: 1px solid rgba(239,68,68,0.2) !important; }
.stWarning { background: rgba(255,209,102,0.08) !important; border: 1px solid rgba(255,209,102,0.2) !important; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ──────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "gmail" not in st.session_state:
    st.session_state.gmail = ""
if "app_password" not in st.session_state:
    st.session_state.app_password = ""
if "templates" not in st.session_state:
    st.session_state.templates = []
if "sending" not in st.session_state:
    st.session_state.sending = False
if "stop_sending" not in st.session_state:
    st.session_state.stop_sending = False

# ─── Helper ────────────────────────────────────────────────────────────────────
def footer():
    st.markdown("""
    <div class="abd-footer">
        Made with ❤️ by <strong style="color:#C0392B">Abdulll,s</strong> &nbsp;|&nbsp;
        <a href="https://www.linkedin.com/in/abdul-rehman-raza-7a125b332" target="_blank">
            🔗 Connect on LinkedIn
        </a>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align:center; padding: 40px 0 32px;">
            <div class="logo-main">ABD <span>Mail</span>Forge</div>
            <div class="logo-sub">BULK EMAIL SENDER BOT · v1.0</div>
            <br>
            <span class="badge-online">🔴 POWERED BY GMAIL SMTP</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="abd-card-accent">', unsafe_allow_html=True)
        st.markdown("#### 🔐 Login with Gmail")
        st.caption("Use your Gmail + 16-character App Password")

        gmail_input = st.text_input("📧 Gmail Address", placeholder="yourname@gmail.com", key="login_gmail")
        pass_input = st.text_input("🔑 App Password (16 chars)", type="password",
                                   placeholder="xxxx xxxx xxxx xxxx", key="login_pass")

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button("🚀 Login & Verify", use_container_width=True):
            if not gmail_input or not pass_input:
                st.error("Gmail aur App Password dono daalo")
                return

            # Check if blocked
            if check_blocked(gmail_input):
                st.error("⛔ Yeh account 5 galat attempts ki wajah se block hai. Naye Gmail se try karo.")
                return

            with st.spinner("Gmail verify ho raha hai..."):
                ok, msg = verify_gmail(gmail_input, pass_input)

            if ok:
                reset_failed(gmail_input)
                save_session(gmail_input, pass_input)
                st.session_state.logged_in = True
                st.session_state.gmail = gmail_input
                st.session_state.app_password = pass_input.replace(" ", "")
                # Load saved templates
                saved = load_templates(gmail_input)
                if saved:
                    st.session_state.templates = saved
                st.success("✅ Login successful!")
                time.sleep(1)
                st.rerun()
            else:
                attempts, blocked = increment_failed(gmail_input)
                remaining = 5 - attempts
                if blocked:
                    st.error(f"⛔ Account block ho gaya — 5 galat attempts. Naye Gmail se try karo.")
                else:
                    st.error(f"❌ {msg} — {remaining} attempts baaki hain")

        st.markdown("""
        <div style="margin-top:16px; padding:12px; background:#150303; border-radius:10px; border:1px solid #2a0808;">
            <div style="font-size:12px; color:#6a3a3a; font-family:'IBM Plex Mono',monospace;">
            ℹ️ App Password kaise banayein:<br>
            Google Account → Security → 2-Step Verification → App Passwords<br>
            "Mail" select karo → Generate → 16-char code milega
            </div>
        </div>
        """, unsafe_allow_html=True)

        footer()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════
def main_app():
    # ── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.markdown("""
        <div style="padding: 8px 0 20px;">
            <div class="logo-main">ABD <span>Mail</span>Forge</div>
            <div class="logo-sub">v1.0 · BULK EMAIL BOT</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:#150303; border:1px solid #4a0a0a; border-radius:10px; padding:12px; margin-bottom:16px;">
            <div style="font-size:11px; color:#6a3a3a; font-family:'IBM Plex Mono',monospace;">LOGGED IN AS</div>
            <div style="font-size:13px; color:#C0392B; font-weight:700; margin-top:4px; word-break:break-all;">{st.session_state.gmail}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        nav = st.radio("Navigation", ["📤 Send Emails", "📋 Templates", "📊 Dashboard", "⚙️ Settings"],
                       label_visibility="collapsed")
        st.markdown("---")

        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.gmail = ""
            st.session_state.app_password = ""
            st.session_state.templates = []
            st.rerun()

        st.markdown("""
        <div style="position:fixed; bottom:16px; left:0; width:240px; text-align:center; font-size:10px; color:#3a1a1a; padding:0 16px;">
            Made by <span style="color:#C0392B">Abdulll,s</span><br>
            <a href="https://www.linkedin.com/in/abdul-rehman-raza-7a125b332" target="_blank" style="color:#C0392B;">LinkedIn ↗</a>
        </div>
        """, unsafe_allow_html=True)

    # ── Pages ─────────────────────────────────────────────────────────────────
    if nav == "📤 Send Emails":
        send_page()
    elif nav == "📋 Templates":
        templates_page()
    elif nav == "📊 Dashboard":
        dashboard_page()
    elif nav == "⚙️ Settings":
        settings_page()

# ═══════════════════════════════════════════════════════════════════════════════
# SEND PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def send_page():
    st.markdown("## 📤 Send Emails")
    st.caption("CSV upload karo ya emails paste karo — phir Send dabao")

    col1, col2 = st.columns([1, 1], gap="large")

    # ── Left: Email Input ──
    with col1:
        st.markdown('<div class="abd-card">', unsafe_allow_html=True)
        st.markdown("#### 📧 Recipients")

        input_method = st.radio("Input Method", ["📎 CSV Upload", "✏️ Paste Emails"],
                                horizontal=True, label_visibility="collapsed")

        emails_list = []

        if input_method == "📎 CSV Upload":
            csv_file = st.file_uploader("CSV file upload karo (Name, Email columns)", type=["csv"])
            if csv_file:
                try:
                    df = pd.read_csv(csv_file)
                    # Try to find email column
                    email_col = None
                    for col in df.columns:
                        if "email" in col.lower() or "mail" in col.lower():
                            email_col = col
                            break
                    if not email_col:
                        email_col = df.columns[0]

                    emails_list = df[email_col].dropna().tolist()
                    emails_list = [str(e).strip().lower() for e in emails_list if "@" in str(e)][:400]
                    st.success(f"✅ {len(emails_list)} emails load ho gayin")
                    with st.expander("Preview emails"):
                        st.write(emails_list[:10])
                        if len(emails_list) > 10:
                            st.caption(f"... aur {len(emails_list)-10} emails")
                except Exception as e:
                    st.error(f"CSV error: {e}")

        else:
            pasted = st.text_area(
                "Emails paste karo (ek line mein ek email, max 400)",
                placeholder="ahmed@gmail.com\nsara@yahoo.com\nbilal@hotmail.com",
                height=180
            )
            if pasted:
                emails_list = parse_emails_from_text(pasted)
                if emails_list:
                    st.success(f"✅ {len(emails_list)} valid emails mili hain")
                else:
                    st.warning("Koi valid email nahi mili")

        st.markdown("</div>", unsafe_allow_html=True)

    # ── Right: Message Setup ──
    with col2:
        st.markdown('<div class="abd-card">', unsafe_allow_html=True)
        st.markdown("#### ✉️ Message Setup")

        subject = st.text_input("📌 Subject", placeholder="Aapka daily update")

        # Template selector
        template_options = ["✍️ Khud likho"] + [t["name"] for t in st.session_state.templates]
        chosen_template = st.selectbox("📋 Template choose karo", template_options)

        if chosen_template == "✍️ Khud likho":
            body = st.text_area("Message body", placeholder="Apna message yahan likho...", height=150)
            use_random_template = False
        elif chosen_template == "🎲 Random (auto-pick)":
            body = ""
            use_random_template = True
            st.info("Har email ke liye random template choose hoga")
        else:
            selected_t = next((t for t in st.session_state.templates if t["name"] == chosen_template), None)
            body = selected_t["body"] if selected_t else ""
            st.text_area("Preview", value=body, height=150, disabled=True)
            use_random_template = False

        # Random template option
        if len(st.session_state.templates) >= 2:
            use_random = st.checkbox("🎲 Random template use karo (har email pe alag)")
            if use_random:
                use_random_template = True
                body = ""

        st.markdown("</div>", unsafe_allow_html=True)

    # ── PDF Attachment ──
    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### 📎 PDF Attachment (Optional)")
    pdf_file = st.file_uploader("PDF attach karo (har email ke saath jayegi)", type=["pdf"])
    if pdf_file:
        st.success(f"✅ {pdf_file.name} ready hai")
    st.markdown("</div>", unsafe_allow_html=True)

    # ── Send Button ──
    st.markdown("---")

    if not emails_list:
        st.warning("⚠️ Pehle emails add karo")
        footer()
        return

    if not subject:
        st.warning("⚠️ Subject likho")
        footer()
        return

    if not use_random_template and not body:
        st.warning("⚠️ Message body likho ya template choose karo")
        footer()
        return

    # Summary
    st.markdown(f"""
    <div class="abd-card-accent">
        <div style="display:flex; gap:32px; flex-wrap:wrap;">
            <div><div style="color:#6a3a3a;font-size:11px;text-transform:uppercase;">Recipients</div>
                 <div style="color:#C0392B;font-size:24px;font-weight:800;">{len(emails_list)}</div></div>
            <div><div style="color:#6a3a3a;font-size:11px;text-transform:uppercase;">Est. Time</div>
                 <div style="color:#C0392B;font-size:24px;font-weight:800;">~{len(emails_list)*30//60} min</div></div>
            <div><div style="color:#6a3a3a;font-size:11px;text-transform:uppercase;">Interval</div>
                 <div style="color:#C0392B;font-size:24px;font-weight:800;">15-45s</div></div>
            <div><div style="color:#6a3a3a;font-size:11px;text-transform:uppercase;">Template</div>
                 <div style="color:#C0392B;font-size:24px;font-weight:800;">{"🎲 Random" if use_random_template else "Fixed"}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns([3, 1])
    with col_btn1:
        start_btn = st.button("🚀 Start Sending", use_container_width=True)
    with col_btn2:
        stop_btn = st.button("⏹ Stop", use_container_width=True)

    if stop_btn:
        st.session_state.stop_sending = True

    if start_btn:
        st.session_state.stop_sending = False
        pdf_bytes = pdf_file.read() if pdf_file else None
        pdf_name = pdf_file.name if pdf_file else None

        st.markdown("---")
        st.markdown("### 📡 Live Progress")

        progress_bar = st.progress(0)
        status_text = st.empty()
        log_container = st.empty()

        sent_count = 0
        failed_count = 0
        logs = []
        total = len(emails_list)

        for i, email in enumerate(emails_list):
            if st.session_state.stop_sending:
                st.warning(f"⏹ Sending rok diya gaya — {sent_count} sent, {failed_count} failed")
                break

            # Pick template
            if use_random_template and st.session_state.templates:
                tname, tbody = pick_random_template(st.session_state.templates)
                current_body = tbody
                current_tname = tname
            else:
                current_body = body
                current_tname = chosen_template

            # Send
            status_text.markdown(f"""
            <div style="font-family:'IBM Plex Mono',monospace; font-size:13px; color:#8a4a4a;">
            Sending {i+1}/{total} → <span style="color:#f0e6e6">{email}</span>
            </div>
            """, unsafe_allow_html=True)

            ok, msg = send_email(
                st.session_state.gmail,
                st.session_state.app_password,
                email, subject, current_body,
                pdf_bytes, pdf_name
            )

            if ok:
                sent_count += 1
                logs.insert(0, f'<div class="log-sent">✓ [{i+1}/{total}] {email} — SENT ({current_tname})</div>')
                log_send(st.session_state.gmail, email, subject, current_tname, "sent")
            else:
                failed_count += 1
                logs.insert(0, f'<div class="log-failed">✗ [{i+1}/{total}] {email} — FAILED: {msg}</div>')
                log_send(st.session_state.gmail, email, subject, current_tname, "failed", msg)

            # Update UI
            progress_bar.progress((i + 1) / total)
            log_html = "".join(logs[:15])
            log_container.markdown(f"""
            <div style="background:#0f0000; border:1px solid #2a0808; border-radius:10px;
                        padding:14px; max-height:300px; overflow-y:auto; font-size:12px;">
                {log_html}
            </div>
            """, unsafe_allow_html=True)

            # Wait between emails (not after last)
            if i < total - 1 and not st.session_state.stop_sending:
                delay = get_random_interval()
                for remaining in range(delay, 0, -1):
                    status_text.markdown(f"""
                    <div style="font-family:'IBM Plex Mono',monospace; font-size:13px; color:#6a3a3a;">
                    ⏳ Next email in {remaining}s...
                    </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
                    if st.session_state.stop_sending:
                        break

        # Done
        if not st.session_state.stop_sending:
            status_text.empty()
            if failed_count == 0:
                st.success(f"🎉 Done! Sab {sent_count} emails bhej di gayin!")
            else:
                st.warning(f"✅ Done! {sent_count} sent, {failed_count} failed")

    footer()

# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATES PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def templates_page():
    st.markdown("## 📋 Email Templates")
    st.caption("3 templates banao — sending ke waqt randomly choose hongi")

    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### ➕ Naya Template Banao")

    t_name = st.text_input("Template Name", placeholder="e.g. Professional, Friendly, Short")
    t_body = st.text_area("Template Body", placeholder="Apna email message yahan likho...", height=150)

    if st.button("💾 Template Save Karo"):
        if not t_name or not t_body:
            st.error("Naam aur body dono chahiye")
        elif len(st.session_state.templates) >= 5:
            st.error("Max 5 templates allowed")
        elif any(t["name"] == t_name for t in st.session_state.templates):
            st.error("Is naam ka template pehle se hai")
        else:
            st.session_state.templates.append({"name": t_name, "body": t_body})
            save_templates(st.session_state.gmail, st.session_state.templates)
            st.success(f"✅ '{t_name}' save ho gaya!")
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Saved templates
    if st.session_state.templates:
        st.markdown(f"### 📚 Saved Templates ({len(st.session_state.templates)})")
        for i, t in enumerate(st.session_state.templates):
            with st.expander(f"📄 {t['name']}"):
                st.text_area("Body", value=t["body"], height=100, disabled=True, key=f"view_{i}")
                if st.button(f"🗑️ Delete '{t['name']}'", key=f"del_{i}"):
                    st.session_state.templates.pop(i)
                    save_templates(st.session_state.gmail, st.session_state.templates)
                    st.rerun()
    else:
        st.info("Abhi koi template nahi — upar banao")

    footer()

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def dashboard_page():
    st.markdown("## 📊 Dashboard")
    st.caption("Tumhari sending history aur stats")

    stats = get_stats(st.session_state.gmail)

    st.markdown(f"""
    <div class="stat-row">
        <div class="stat-box">
            <div class="stat-num">{stats['today_sent']}</div>
            <div class="stat-label">Aaj Bhaiji</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">{stats['sent']}</div>
            <div class="stat-label">Total Sent</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">{stats['failed']}</div>
            <div class="stat-label">Failed</div>
        </div>
        <div class="stat-box">
            <div class="stat-num">{stats['total']}</div>
            <div class="stat-label">Total Attempts</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📜 Recent Send Logs")
    logs = get_logs(st.session_state.gmail, limit=50)

    if logs:
        log_html = ""
        for log in logs:
            icon = "✓" if log["status"] == "sent" else "✗"
            cls = "log-sent" if log["status"] == "sent" else "log-failed"
            t = log.get("sent_at", "")[:16].replace("T", " ")
            log_html += f'<div class="{cls}">{icon} {t} → {log["recipient"]} [{log.get("template_used","?")}]</div>'

        st.markdown(f"""
        <div style="background:#0f0000; border:1px solid #2a0808; border-radius:12px;
                    padding:16px; max-height:400px; overflow-y:auto;">
            {log_html}
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Abhi koi logs nahi — pehle emails bhejo")

    footer()

# ═══════════════════════════════════════════════════════════════════════════════
# SETTINGS PAGE
# ═══════════════════════════════════════════════════════════════════════════════
def settings_page():
    st.markdown("## ⚙️ Settings")

    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### 📧 Current Account")
    st.markdown(f"""
    <div style="font-family:'IBM Plex Mono',monospace;">
        <span style="color:#6a3a3a;">Gmail:</span>
        <span style="color:#C0392B;"> {st.session_state.gmail}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🔑 App Password Update")
    new_pass = st.text_input("Naya App Password", type="password", placeholder="xxxx xxxx xxxx xxxx")
    if st.button("🔄 Password Update Karo"):
        if new_pass:
            ok, msg = verify_gmail(st.session_state.gmail, new_pass)
            if ok:
                st.session_state.app_password = new_pass.replace(" ", "")
                st.success("✅ Password update ho gaya!")
            else:
                st.error(f"❌ {msg}")
        else:
            st.error("Password daalo")

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="abd-card">', unsafe_allow_html=True)
    st.markdown("#### ℹ️ App Info")
    st.markdown("""
    <div style="font-family:'IBM Plex Mono',monospace; font-size:12px; color:#6a3a3a; line-height:2;">
        App Name: ABD MailForge v1.0<br>
        Made by: Abdulll,s<br>
        Email Engine: Gmail SMTP<br>
        Database: Supabase PostgreSQL<br>
        Sending Interval: Random 15-45 sec<br>
        Max Emails per Session: 400<br>
        Max Templates: 5
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
    main_app()
