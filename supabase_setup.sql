-- Run these SQL commands in Supabase Dashboard → SQL Editor

-- 1. Sessions table (login tracking)
CREATE TABLE IF NOT EXISTS sessions (
    id SERIAL PRIMARY KEY,
    gmail TEXT UNIQUE NOT NULL,
    last_login TIMESTAMP,
    login_count INTEGER DEFAULT 0,
    failed_attempts INTEGER DEFAULT 0,
    is_blocked BOOLEAN DEFAULT FALSE
);

-- 2. Templates table
CREATE TABLE IF NOT EXISTS templates (
    id SERIAL PRIMARY KEY,
    gmail TEXT UNIQUE NOT NULL,
    templates TEXT NOT NULL,
    updated_at TIMESTAMP
);

-- 3. Send logs table
CREATE TABLE IF NOT EXISTS send_logs (
    id SERIAL PRIMARY KEY,
    sender_gmail TEXT NOT NULL,
    recipient TEXT NOT NULL,
    subject TEXT,
    template_used TEXT,
    status TEXT NOT NULL,
    error TEXT,
    sent_at TIMESTAMP DEFAULT NOW()
);

-- 4. Indexes for faster queries
CREATE INDEX IF NOT EXISTS idx_send_logs_gmail ON send_logs(sender_gmail);
CREATE INDEX IF NOT EXISTS idx_send_logs_sent_at ON send_logs(sent_at);
CREATE INDEX IF NOT EXISTS idx_sessions_gmail ON sessions(gmail);
