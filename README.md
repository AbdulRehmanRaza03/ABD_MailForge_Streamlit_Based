# ✉️ ABD MailForge v2.0 — Bulk Email Sender Bot

> **Made by Abdulll,s** · [Connect on LinkedIn](https://www.linkedin.com/in/abdul-rehman-raza-7a125b332)

---

## 🚀 What Is ABD MailForge?

ABD MailForge is a professional bulk email sender built with Streamlit and Python. It uses Gmail SMTP to send personalized emails to up to 400 recipients per session, with random delays and template rotation to reduce spam flagging. All send history is stored permanently in Supabase PostgreSQL.

---

## ✅ Features

| Feature | Detail |
|---------|--------|
| Gmail SMTP | Sends via your own Gmail securely |
| CSV or Paste | Upload CSV or paste emails directly |
| Max Recipients | 400 per session |
| Send Interval | Random 15–45 seconds per email |
| Templates | Up to 5 — randomly selected per email |
| PDF Attachment | Optional — same PDF per batch |
| Dashboard | Full send history and stats |
| Database | Supabase PostgreSQL — permanent storage |
| Mobile Friendly | Works on mobile browser |
| Security | App Password only — real password never stored |

---

## 🗂️ File Structure

```
abd-mailforge/
├── app.py                → Main Streamlit app (UI + routing)
├── mailer.py             → Gmail SMTP sending logic
├── db.py                 → Supabase database operations
├── requirements.txt      → Python dependencies
├── supabase_setup.sql    → SQL to create database tables
├── .streamlit/
│   ├── config.toml       → Theme and server settings
│   └── secrets.toml      → Your Supabase credentials (local only)
├── .gitignore            → Excludes secrets from GitHub
└── README.md             → This file
```

---

## 📋 Setup Guide

### Step 1 — Get Gmail App Password

1. Go to [myaccount.google.com](https://myaccount.google.com)
2. Click **Security** → **2-Step Verification** → **App Passwords**
3. Select App: **Mail**, Device: **Other** → Name it "MailForge"
4. Click **Generate** → Copy the 16-character code
5. This is your App Password — save it securely

> ⚠️ This is NOT your real Gmail password. It is a separate access key for sending emails only.

---

### Step 2 — Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Click **New Project** — give it a name and password
3. Once the project is ready, go to **SQL Editor** (left sidebar)
4. Open the `supabase_setup.sql` file from this project
5. Copy all the SQL → paste into SQL Editor → click **Run**
6. Go to **Settings** → **API**
7. Copy your **Project URL** and **anon/public key**

---

### Step 3 — Add Supabase Column for Password

In Supabase → Table Editor → **sessions** table:
1. Click the **+** button to add a new column
2. Name: `app_password`, Type: `text`, Default: empty
3. Save

---

### Step 4 — Configure Secrets (Local)

Open `.streamlit/secrets.toml` and fill in:

```toml
[supabase]
url = "https://your-project-id.supabase.co"
key = "your-anon-public-key-here"
```

---

### Step 5 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 6 — Run Locally

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501` and test the app.

---

### Step 7 — Push to GitHub

```bash
git init
git add .
git commit -m "ABD MailForge v2.0"
git remote add origin https://github.com/YOUR_USERNAME/abd-mailforge.git
git push -u origin main
```

> ⚠️ Never push your `secrets.toml` to GitHub. It is listed in `.gitignore` automatically.

---

### Step 8 — Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **New app**
3. Select your GitHub repository
4. Main file path: `app.py`
5. Click **Advanced settings** → **Secrets**
6. Paste your secrets:

```toml
[supabase]
url = "https://your-project-id.supabase.co"
key = "your-anon-public-key-here"
```

7. Click **Deploy**
8. Your live link will be: `https://abd-mailforge.streamlit.app`

---

### Step 9 — Set Up UptimeRobot (Keep App Alive)

Streamlit Cloud sleeps inactive apps after 15 minutes.

1. Go to [uptimerobot.com](https://uptimerobot.com) and create a free account
2. Click **Add New Monitor**
3. Type: **HTTP(s)**
4. URL: your Streamlit app link
5. Interval: **5 minutes**
6. Click **Create Monitor**

Your app will now stay awake 24/7 for free.

---

## 🔒 Security Guide

### App Password Safety
- Your real Gmail password is never entered or stored
- App Password only allows sending emails — no other Gmail access
- If compromised: Google Account → Security → App Passwords → Delete "MailForge"
- Generate a new one and update it in Settings

### Supabase Data Privacy
- Only you can access your Supabase dashboard
- Send logs are stored privately under your account
- No third party can read your data

### Keep 2-Step Verification ON
- App Passwords require 2-Step Verification to be enabled
- This also protects your Google Account from unauthorized access

---

## ⚠️ Important Usage Warnings

**Keep Browser Tab Open**
Sending stops if you close the tab, switch apps, or lock your screen. Keep the tab visible and active throughout the entire sending session.

**Mobile Users**
Keep your screen on during sending. Plug your phone in if possible. Do not switch to another app.

**PC / Laptop Users**
Move your mouse occasionally to prevent sleep mode. Adjust power settings to disable screen sleep during sending.

**Internet Connection**
Any disconnect will cause that email attempt to fail. Use a mobile hotspot for the most stable connection.

**Gmail Daily Limits**
- New Gmail accounts: 50–100 emails/day
- Regular accounts: 100–200 emails/day
- Older active accounts: up to 400 emails/day
- Gmail official limit: 500/day — stay well below it

---

## 🛠️ Troubleshooting

**Login fails?**
→ Make sure App Password is exactly 16 characters with no spaces, or remove spaces and try again.

**Emails not going through?**
→ Check that 2-Step Verification is ON in your Google Account.
→ Try revoking the App Password and generating a new one.

**Dashboard shows no data?**
→ Go to Supabase → Authentication → Policies → Disable RLS on all three tables (send_logs, sessions, templates).

**App is slow to open?**
→ Set up UptimeRobot as described in Step 9.

**Streamlit secrets error?**
→ Double-check that your URL and key in secrets match exactly what Supabase shows.

---

## 🔗 My Other Projects

- **ABD Screen Recorder** → [abd-screen-recorder-web-app.streamlit.app](https://abd-screen-recorder-web-app.streamlit.app/)
- **ABD Cursor Mover & Game Site** → [abdulrehmanraza03.github.io/ABD_Cursor_Mover_Site](https://abdulrehmanraza03.github.io/ABD_Cursor_Mover_Site/)

---

## 👤 About

**Made by Abdulll,s (Abdul Rehman Raza)**
B.S. Artificial Intelligence — The Superior University, Lahore

🔗 [LinkedIn Profile](https://www.linkedin.com/in/abdul-rehman-raza-7a125b332)
💻 [GitHub](https://github.com/AbdulRehmanRaza03)
