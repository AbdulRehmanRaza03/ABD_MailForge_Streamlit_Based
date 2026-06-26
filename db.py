import streamlit as st
from supabase import create_client, Client
from datetime import datetime
import json

def get_client() -> Client:
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

def init_db():
    """Create tables if not exist via Supabase SQL"""
    # Tables are created manually in Supabase dashboard
    # See README.md for SQL commands
    pass

def save_session(gmail: str, password: str):
    """Save gmail session to supabase"""
    try:
        db = get_client()
        existing = db.table("sessions").select("*").eq("gmail", gmail).execute()
        if existing.data:
            db.table("sessions").update({
                "last_login": datetime.utcnow().isoformat(),
                "login_count": existing.data[0]["login_count"] + 1
            }).eq("gmail", gmail).execute()
        else:
            db.table("sessions").insert({
                "gmail": gmail,
                "last_login": datetime.utcnow().isoformat(),
                "login_count": 1,
                "failed_attempts": 0,
                "is_blocked": False
            }).execute()
    except Exception as e:
        st.error(f"DB Error: {e}")

def check_blocked(gmail: str) -> bool:
    try:
        db = get_client()
        res = db.table("sessions").select("*").eq("gmail", gmail).execute()
        if res.data:
            return res.data[0].get("is_blocked", False)
        return False
    except:
        return False

def increment_failed(gmail: str):
    try:
        db = get_client()
        res = db.table("sessions").select("*").eq("gmail", gmail).execute()
        if res.data:
            attempts = res.data[0].get("failed_attempts", 0) + 1
            is_blocked = attempts >= 5
            db.table("sessions").update({
                "failed_attempts": attempts,
                "is_blocked": is_blocked
            }).eq("gmail", gmail).execute()
            return attempts, is_blocked
        else:
            db.table("sessions").insert({
                "gmail": gmail,
                "last_login": None,
                "login_count": 0,
                "failed_attempts": 1,
                "is_blocked": False
            }).execute()
            return 1, False
    except:
        return 0, False

def reset_failed(gmail: str):
    try:
        db = get_client()
        db.table("sessions").update({
            "failed_attempts": 0,
            "is_blocked": False
        }).eq("gmail", gmail).execute()
    except:
        pass

def save_templates(gmail: str, templates: list):
    try:
        db = get_client()
        existing = db.table("templates").select("*").eq("gmail", gmail).execute()
        data = {"gmail": gmail, "templates": json.dumps(templates), "updated_at": datetime.utcnow().isoformat()}
        if existing.data:
            db.table("templates").update(data).eq("gmail", gmail).execute()
        else:
            db.table("templates").insert(data).execute()
    except Exception as e:
        st.error(f"Template save error: {e}")

def load_templates(gmail: str) -> list:
    try:
        db = get_client()
        res = db.table("templates").select("*").eq("gmail", gmail).execute()
        if res.data:
            return json.loads(res.data[0]["templates"])
        return []
    except:
        return []

def log_send(gmail: str, recipient: str, subject: str, template_used: str, status: str, error: str = None):
    try:
        db = get_client()
        db.table("send_logs").insert({
            "sender_gmail": gmail,
            "recipient": recipient,
            "subject": subject,
            "template_used": template_used,
            "status": status,
            "error": error,
            "sent_at": datetime.utcnow().isoformat()
        }).execute()
    except:
        pass

def get_logs(gmail: str, limit: int = 100) -> list:
    try:
        db = get_client()
        res = db.table("send_logs").select("*").eq("sender_gmail", gmail).order("sent_at", desc=True).limit(limit).execute()
        return res.data or []
    except:
        return []

def get_stats(gmail: str) -> dict:
    try:
        db = get_client()
        logs = db.table("send_logs").select("*").eq("sender_gmail", gmail).execute()
        data = logs.data or []
        total = len(data)
        sent = len([x for x in data if x["status"] == "sent"])
        failed = len([x for x in data if x["status"] == "failed"])
        today = datetime.utcnow().date().isoformat()
        today_sent = len([x for x in data if x["status"] == "sent" and x["sent_at"][:10] == today])
        return {"total": total, "sent": sent, "failed": failed, "today_sent": today_sent}
    except:
        return {"total": 0, "sent": 0, "failed": 0, "today_sent": 0}
