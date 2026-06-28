<div align="center">

<!-- HEADER BANNER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=200&section=header&text=ABD%20MailForge%20v2.0&fontSize=60&fontColor=fff&animation=twinkling&fontAlignY=35&desc=Professional%20Bulk%20Email%20Sender%20Bot&descAlignY=55&descSize=20" width="100%"/>

<!-- BADGES ROW -->
<p align="center">
  <img src="https://img.shields.io/badge/Version-2.0-blue?style=for-the-badge&logo=git&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gmail%20SMTP-EA4335?style=for-the-badge&logo=gmail&logoColor=white"/>
  <img src="https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Deployment-Streamlit%20Cloud-FF4B4B?style=for-the-badge&logo=streamlit"/>
  <img src="https://img.shields.io/badge/Made%20by-Abdulll%2Cs-blueviolet?style=for-the-badge"/>
</p>

<br/>

> **Send up to 400 personalized emails per session** — with smart delays, rotating templates, PDF attachments, and a full analytics dashboard. Built for professionals. Deployed in the cloud. Powered by Gmail SMTP + Supabase.

<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Abdul%20Rehman%20Raza-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/abdul-rehman-raza-7a125b332)
[![GitHub](https://img.shields.io/badge/GitHub-AbdulRehmanRaza03-181717?style=flat-square&logo=github)](https://github.com/AbdulRehmanRaza03)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-orange?style=flat-square&logo=firefox)](https://abdulrehmanraza03.github.io/My-Portfolio/)

</div>

---

## 📋 Table of Contents

- [What Is ABD MailForge?](#-what-is-abd-mailforge)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [How It Works — Flow Diagram](#-how-it-works--flow-diagram)
- [Setup Guide](#-setup-guide)
- [Deployment](#-deployment-streamlit-cloud)
- [Security Model](#-security-model)
- [Usage Limits & Best Practices](#-usage-limits--best-practices)
- [Troubleshooting](#-troubleshooting)
- [My Projects](#-other-projects-by-abdullls)
- [About the Developer](#-about-the-developer)

---

## 📬 What Is ABD MailForge?

**ABD MailForge v2.0** is a cloud-deployable bulk email automation tool built with **Python** and **Streamlit**. It sends personalized emails at human-like random intervals to bypass spam filters, supports multiple email templates with auto-rotation, optional PDF attachments, and stores every send event permanently in **Supabase PostgreSQL**.

Designed for marketers, freelancers, and businesses who need reliable, trackable bulk outreach — without expensive third-party email services.

### 🎯 Use Cases

| Use Case | How MailForge Helps |
|----------|---------------------|
| Cold outreach campaigns | Send personalized pitches to hundreds of leads |
| Newsletter distribution | Rotate templates, track all sends in dashboard |
| Client follow-ups | Attach PDF proposals/invoices per batch |
| Product promotions | Schedule campaign via CSV upload |
| Internal announcements | Reach team/community at scale |

---

## ✅ Key Features

<table>
<tr>
<td width="50%">

### 📧 Email Engine
- ✅ Gmail SMTP — secure, no third-party relay
- ✅ Up to **400 recipients** per session
- ✅ Random **15–45 second delays** (human-like pacing)
- ✅ Up to **5 rotating templates** per campaign
- ✅ Optional **PDF attachment** per batch

</td>
<td width="50%">

### 📊 Data & Dashboard
- ✅ Full **send history** with status per email
- ✅ **Supabase PostgreSQL** — permanent cloud storage
- ✅ **CSV upload** or paste emails manually
- ✅ Real-time **progress tracking** during send
- ✅ Mobile-friendly responsive UI

</td>
</tr>
<tr>
<td>

### 🔐 Security
- ✅ App Password only — real password **never stored**
- ✅ Supabase secrets in **`.streamlit/secrets.toml`**
- ✅ `.gitignore` protects credentials from GitHub
- ✅ RLS-compatible schema design

</td>
<td>

### ☁️ Deployment
- ✅ One-click deploy on **Streamlit Cloud**
- ✅ UptimeRobot integration — **stays alive 24/7**
- ✅ No server management required
- ✅ Free tier compatible (Streamlit + Supabase)

</td>
</tr>
</table>

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                              │
│                   (Streamlit Web Interface)                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │  HTTP
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT CLOUD SERVER                         │
│  ┌─────────────┐   ┌──────────────┐   ┌────────────────────┐   │
│  │   app.py    │──▶│  mailer.py   │──▶│  Gmail SMTP Server │   │
│  │  (UI/Router)│   │(Send Engine) │   │  smtp.gmail.com    │   │
│  └──────┬──────┘   └──────────────┘   │  Port 587 (TLS)    │   │
│         │                              └────────────────────┘   │
│         ▼                                                        │
│  ┌──────────────┐                                                │
│  │    db.py     │                                                │
│  │(DB Operations│                                                │
│  └──────┬───────┘                                                │
└─────────┼───────────────────────────────────────────────────────┘
          │  HTTPS / REST API
          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     SUPABASE (PostgreSQL)                         │
│  ┌──────────────┐  ┌────────────────┐  ┌───────────────────┐   │
│  │   sessions   │  │   send_logs    │  │     templates     │   │
│  │  (auth data) │  │ (email history)│  │  (email content)  │   │
│  └──────────────┘  └────────────────┘  └───────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit (Python) | Web UI, real-time progress, dashboard |
| **Email Engine** | Python `smtplib` + `ssl` | Gmail SMTP over TLS port 587 |
| **Database** | Supabase (PostgreSQL) | Permanent storage of all send events |
| **DB Client** | `supabase-py` | Python SDK for Supabase REST API |
| **File Handling** | `csv`, `io`, `base64` | CSV parsing, PDF attachment encoding |
| **Deployment** | Streamlit Community Cloud | Free cloud hosting |
| **Uptime** | UptimeRobot | Keeps app awake 24/7 with HTTP pings |
| **Security** | Google App Passwords | 2FA-gated send-only credential |

---

## 🗂️ Project Structure

```
abd-mailforge/
│
├── 📄 app.py                   → Main Streamlit app (UI + routing + session mgmt)
├── 📧 mailer.py                → Gmail SMTP engine (send loop + delay logic)
├── 🗄️ db.py                    → Supabase CRUD operations (logs, sessions, templates)
├── 📦 requirements.txt         → All Python dependencies
├── 🐘 supabase_setup.sql       → SQL schema — run this once in Supabase
│
├── 📁 .streamlit/
│   ├── config.toml             → Theme, server settings (port, headless)
│   └── secrets.toml            → 🔒 LOCAL ONLY — Supabase URL + anon key
│
├── 🚫 .gitignore               → Excludes secrets.toml, __pycache__, .env
└── 📖 README.md                → This file
```

### File Responsibilities

```
app.py
  ├── render_login()        → Gmail + App Password input UI
  ├── render_compose()      → Recipient list, templates, PDF upload
  ├── render_send()         → Progress bar, send loop caller
  └── render_dashboard()    → Send history stats from Supabase

mailer.py
  ├── send_email()          → Single email dispatch via SMTP
  ├── random_delay()        → 15–45s random sleep between sends
  └── rotate_template()     → Picks random template from pool

db.py
  ├── save_session()        → Store session on login
  ├── log_send()            → Record each email result (success/fail)
  └── get_history()         → Fetch send logs for dashboard
```

---

## 🔄 How It Works — Flow Diagram

```
                         ┌──────────────────┐
                         │   User Visits App │
                         └────────┬─────────┘
                                  │
                         ┌────────▼─────────┐
                         │  Enter Gmail +    │
                         │  App Password     │
                         └────────┬─────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │  Authenticate via SMTP test │
                    └──────┬──────────────────────┘
                           │
              ┌────────────▼──────────────┐
              │  Upload CSV OR Paste Emails│
              └────────────┬──────────────┘
                           │
              ┌────────────▼──────────────┐
              │  Add up to 5 Templates    │
              │  + Optional PDF Attachment│
              └────────────┬──────────────┘
                           │
              ┌────────────▼──────────────┐
              │     Click SEND            │
              └────────────┬──────────────┘
                           │
              ┌────────────▼──────────────┐
              │  For each recipient:       │
              │  1. Pick random template  │
              │  2. Build MIME email      │
              │  3. Attach PDF (if any)   │
              │  4. Send via SMTP/TLS     │
              │  5. Log result → Supabase │
              │  6. Sleep 15–45 seconds   │
              └────────────┬──────────────┘
                           │
              ┌────────────▼──────────────┐
              │  Dashboard: Full History   │
              │  Success Rate, Stats       │
              └───────────────────────────┘
```

---

## 📋 Setup Guide

### Step 1 — Get Gmail App Password

> ⚠️ **This is NOT your real Gmail password.** It's a separate 16-character send-only key.

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. **Security** → **2-Step Verification** → scroll down → **App Passwords**
3. App: `Mail` · Device: `Other` → Name: `MailForge`
4. Click **Generate** → copy the 16-character code
5. Save it — you'll enter it in the app's login screen

---

### Step 2 — Set Up Supabase Database

1. Go to [supabase.com](https://supabase.com) → create free account
2. **New Project** → name it + set a DB password → wait ~2 min
3. Left sidebar → **SQL Editor**
4. Open `supabase_setup.sql` from this repo → paste all SQL → click **Run**
5. Go to **Settings** → **API** → copy:
   - **Project URL** (looks like `https://xyz.supabase.co`)
   - **anon/public key** (long JWT string)

---

### Step 3 — Add App Password Column

In Supabase → **Table Editor** → `sessions` table:
1. Click **+** to add column
2. Name: `app_password` | Type: `text` | Default: *(leave empty)*
3. **Save**

---

### Step 4 — Configure Secrets (Local Only)

Create or edit `.streamlit/secrets.toml`:

```toml
[supabase]
url = "https://your-project-id.supabase.co"
key = "your-anon-public-key-here"
```

> 🔒 This file is in `.gitignore`. It will **never** be pushed to GitHub.

---

### Step 5 — Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` includes:**
```
streamlit
supabase
secure-smtplib
```

---

### Step 6 — Run Locally

```bash
streamlit run app.py
```

Open → `http://localhost:8501`

---

### Step 7 — Push to GitHub

```bash
git init
git add .
git commit -m "ABD MailForge v2.0 — initial commit"
git remote add origin https://github.com/YOUR_USERNAME/abd-mailforge.git
git push -u origin main
```

> ⚠️ Verify `.gitignore` contains `secrets.toml` before pushing.

---

## ☁️ Deployment: Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. **New app** → select your GitHub repo
3. Main file path: `app.py`
4. **Advanced settings** → **Secrets** → paste:

```toml
[supabase]
url = "https://your-project-id.supabase.co"
key = "your-anon-public-key-here"
```

5. Click **Deploy** → live link: `https://abd-mailforge.streamlit.app`

---

### ⏰ Keep App Alive with UptimeRobot

Streamlit Cloud sleeps apps after 15 minutes of inactivity.

1. Go to [uptimerobot.com](https://uptimerobot.com) → free account
2. **Add New Monitor** → Type: `HTTP(s)`
3. URL: your Streamlit live link
4. Interval: **5 minutes**
5. **Create Monitor** ✅

App now stays active 24/7 — zero cost.

---

## 🔐 Security Model

```
┌──────────────────────────────────────────────────────────┐
│                    CREDENTIAL FLOW                        │
│                                                          │
│  User enters App Password → stored in session (RAM only) │
│  Real Gmail password → NEVER entered or stored           │
│  Supabase keys → secrets.toml (local) / Cloud secrets    │
│  GitHub repo → credentials excluded via .gitignore       │
└──────────────────────────────────────────────────────────┘
```

| Threat | Protection |
|--------|-----------|
| Real password exposure | App Password used — scoped to send-only |
| Credential leak to GitHub | `.gitignore` excludes `secrets.toml` |
| Unauthorized DB access | Supabase anon key + RLS policies |
| App Password compromise | Revoke via Google Account → generate new |
| Data privacy | All logs private under your Supabase account |

**If App Password is compromised:**
Google Account → Security → App Passwords → Delete "MailForge" → Generate new → Update in app settings.

---

## 📊 Usage Limits & Best Practices

### Gmail Daily Send Limits

| Account Type | Safe Daily Limit |
|--------------|----------------|
| New Gmail account | 50–100 emails/day |
| Regular account (< 1 year) | 100–200 emails/day |
| Older, active account | Up to 400 emails/day |
| Gmail official ceiling | 500/day — stay 20% below |

### Best Practices for High Deliverability

- ✅ Keep 15–45s random delays (already built-in)
- ✅ Rotate between 3–5 templates (avoids content fingerprinting)
- ✅ Keep subject lines varied across templates
- ✅ Never send to invalid/purchased lists — high bounces = spam flag
- ✅ Warm up new accounts: start at 50/day, scale up weekly
- ✅ Keep browser tab open and screen active throughout sending

### Device Tips During Sending

| Device | Action |
|--------|--------|
| PC/Laptop | Disable sleep mode, move mouse occasionally |
| Mobile | Keep screen on, plug in charger, don't switch apps |
| Network | Use stable WiFi or mobile hotspot |

---

## 🛠️ Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Login fails | Spaces in App Password | Remove all spaces → 16 chars, no gaps |
| Emails not sending | 2-Step Verification off | Enable it in Google Account → Security |
| Dashboard empty | RLS blocking reads | Supabase → Authentication → Policies → Disable RLS on `send_logs`, `sessions`, `templates` |
| Secrets error | Wrong URL/key format | Re-copy from Supabase Settings → API exactly |
| App slow to open | App was sleeping | Wait 30s for cold start, or set up UptimeRobot |
| SMTP timeout | Network instability | Switch to mobile hotspot |
| PDF not attaching | File too large | Keep PDF under 5MB for reliable SMTP delivery |

---

## 🚀 Other Projects by Abdulll,s

<table>
<tr>
<td width="50%">

**🤖 AI & Machine Learning**

| Project | Link |
|---------|------|
| TalentIQ — AI Prediction App | [🔗 Visit](https://talentiq-ai-prediction.streamlit.app/) |
| Customer Churn Prediction | [🔗 Visit](https://customer-churn-prediction-analytics-5syak8uuar5rp4f8ihphvs.streamlit.app/) |
| ABD MailForge (this project) | [🔗 Visit](https://abd-mailforge.streamlit.app) |
| ABD Screen Recorder Web App | [🔗 Visit](https://abd-screen-recorder-web-app.streamlit.app/) |

</td>
<td width="50%">

**🌐 Web & E-commerce**

| Project | Link |
|---------|------|
| My Portfolio | [🔗 Visit](https://abdulrehmanraza03.github.io/My-Portfolio/) |
| ABD Wears — Fashion Store | [🔗 Visit](https://abdulrehmanraza03.github.io/ABD-Wears-Weabsite/#/) |
| FFC Pizza Restaurant | [🔗 Visit](https://abdulrehmanraza03.github.io/FFC_Pizza_Restaurent/) |
| The ABD Service (Website) | [🔗 Visit](https://replit-tool--theabdulservice.replit.app/#collections) |
| Cursor Mover & Game Site | [🔗 Visit](https://abdulrehmanraza03.github.io/ABD_Cursor_Mover_Site/) |

</td>
</tr>
</table>

---

## 👤 About the Developer

<div align="center">

### Abdul Rehman Raza
**B.S. Artificial Intelligence — The Superior University, Lahore**

*Full-Stack Developer · AI Engineer · E-commerce Entrepreneur*

<br/>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/abdul-rehman-raza-7a125b332)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github)](https://github.com/AbdulRehmanRaza03)
[![Portfolio](https://img.shields.io/badge/Portfolio-Explore-FF6B35?style=for-the-badge&logo=firefox)](https://abdulrehmanraza03.github.io/My-Portfolio/)

<br/>

**Skills Used in This Project**

`Python` · `Streamlit` · `Gmail SMTP` · `Supabase` · `PostgreSQL` · `REST APIs` · `Cloud Deployment` · `Security Engineering` · `UX/UI Design` · `Email Deliverability`

</div>

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&customColorList=6,11,20&height=100&section=footer" width="100%"/>

**⭐ If this project helped you — drop a star on GitHub!**

*Made with ❤️ by Abdulll,s — Lahore, Pakistan*

</div>
