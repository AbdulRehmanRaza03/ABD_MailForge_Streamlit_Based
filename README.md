# 🔥 ABD MailForge — Bulk Email Sender Bot

> Made by **Abdulll,s** | [Connect on LinkedIn](https://www.linkedin.com/in/abdul-rehman-raza-7a125b332)

---

## 📌 Project Overview

ABD MailForge ek powerful bulk email sender bot hai jo Streamlit pe bana hai.
- Gmail SMTP se emails bhejta hai
- CSV ya text paste se 400 emails tak support karta hai
- Random 15-45 sec interval (spam se bachao)
- 3-5 templates, random pick per email
- PDF attachment support
- Supabase mein permanent logs
- Mobile aur PC dono pe kaam karta hai

---

## 🗂️ File Structure

```
abd-mailforge/
├── app.py                  → Main Streamlit app (UI + logic)
├── mailer.py               → Gmail SMTP sending
├── db.py                   → Supabase database operations
├── requirements.txt        → Python libraries
├── supabase_setup.sql      → DB tables banane ka SQL
├── .streamlit/
│   ├── config.toml         → Theme settings (maroon + black)
│   └── secrets.toml        → Supabase credentials (local only)
└── README.md               → Yeh file
```

---

## ✅ STEP 1 — Gmail App Password Banao

1. **Google Account** kholo → **Security**
2. **2-Step Verification** enable karo (agar nahi hai)
3. **App Passwords** dhundo (search box mein likho)
4. App: **Mail**, Device: **Other** → **Generate**
5. 16-character code milega → **save kar lo**

> ⚠️ Yeh apna real Gmail password NAHI hai — App Password alag hota hai

---

## ✅ STEP 2 — Supabase Setup

1. **[supabase.com](https://supabase.com)** pe free account banao
2. **New Project** create karo
3. Project ready hone ke baad:
   - Left menu → **SQL Editor**
   - `supabase_setup.sql` file kholo (is project mein)
   - Saara SQL copy karo → SQL Editor mein paste karo → **Run**
4. Left menu → **Settings** → **API**
   - **Project URL** copy karo
   - **anon / public key** copy karo

---

## ✅ STEP 3 — Local Test

### secrets.toml banao:
`.streamlit/secrets.toml` file kholo aur fill karo:
```toml
[supabase]
url = "https://xxxxx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIs..."
```

### Install libraries:
```bash
pip install -r requirements.txt
```

### Run karo:
```bash
streamlit run app.py
```

Browser mein khulega: `http://localhost:8501`

---

## ✅ STEP 4 — GitHub Pe Push Karo

```bash
# GitHub pe new repo banao: "abd-mailforge"
git init
git add .
git commit -m "ABD MailForge v1.0"
git remote add origin https://github.com/YOUR_USERNAME/abd-mailforge.git
git push -u origin main
```

> ⚠️ `.streamlit/secrets.toml` GitHub pe mat daalo!
> `.gitignore` mein add karo:
```
.streamlit/secrets.toml
__pycache__/
*.pyc
.env
```

---

## ✅ STEP 5 — Streamlit Cloud Deploy

1. **[share.streamlit.io](https://share.streamlit.io)** pe jao
2. **New app** → GitHub repo select karo
3. **Main file:** `app.py`
4. **Advanced settings** → **Secrets** mein yeh daalo:
```toml
[supabase]
url = "https://xxxxx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIs..."
```
5. **Deploy** dabao
6. Link milega: `https://abd-mailforge.streamlit.app`

---

## ✅ STEP 6 — UptimeRobot Setup (App Jaaga Rahe)

1. **[uptimerobot.com](https://uptimerobot.com)** pe free account
2. **Add Monitor** → **HTTP(s)**
3. URL: `https://abd-mailforge.streamlit.app`
4. Interval: **5 minutes**
5. **Create Monitor** → Done ✓

App 24/7 active rahegi — so nahi jaegi.

---

## 📱 Mobile Use

- Streamlit link mobile browser mein kholo
- Sab kuch mobile pe kaam karta hai
- **Sending ke waqt tab khula rakho** — band kiya toh sending ruk jayegi
- Chrome ya Safari dono pe kaam karta hai

---

## 🔐 Security

| Feature | Detail |
|---------|--------|
| Login | Gmail + 16-char App Password |
| Wrong attempts | 5 ke baad block |
| Password store | Nahi hota (session only) |
| Data | Supabase mein encrypted |

---

## 📊 Features Summary

| Feature | Status |
|---------|--------|
| CSV upload | ✅ |
| Text paste (max 400) | ✅ |
| PDF attachment | ✅ |
| 3-5 templates | ✅ |
| Random template pick | ✅ |
| Random 15-45s interval | ✅ |
| Live progress bar | ✅ |
| Send logs (Supabase) | ✅ |
| Dashboard + stats | ✅ |
| Mobile friendly | ✅ |
| Stop sending button | ✅ |
| 5-attempt block | ✅ |

---

## ❓ Troubleshooting

**Login fail ho raha hai?**
→ App Password check karo — 16 chars hone chahiye, spaces hata ke try karo

**Emails nahi ja rahi?**
→ Gmail mein "Less secure app access" OFF hai? → App Password use karo, woh sahi hai
→ Gmail ka daily limit: ~500 emails/day

**Supabase error?**
→ URL aur Key dobara check karo secrets.toml mein

**App slow hai?**
→ UptimeRobot laga hai? Laga lo — app instant open hogi

---

## 📬 Contact

**Made by Abdulll,s**
🔗 [LinkedIn — Abdul Rehman Raza](https://www.linkedin.com/in/abdul-rehman-raza-7a125b332)
