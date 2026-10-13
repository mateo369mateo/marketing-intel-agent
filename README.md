# 🎯 Marketing, Branding & Advertising Intelligence Agent

An automated intelligence agent that tracks breaking news across the marketing, branding, and advertising landscape, synthesizes executive insights, compiles a styled PDF briefing, and delivers it directly to **Telegram** and **Email**.

---

## ⚡ What it Does

- 📡 **Monitors Leading Industry Sources**:
  - **Advertising & Campaigns**: *Adweek*, *Campaign Live*, Agency and Commercial moves.
  - **Branding & Visual Identity**: *Brand New (UnderConsideration)*, *Retail Dive*, major rebrands and packaging redesigns.
  - **Marketing Strategy & Media**: *Marketing Dive*, *Digiday*, *Social Media Today*.
- 🧠 **Synthesizes & Curates**:
  - Automatically deduplicates and filters stories by priority.
  - Extracts key strategic themes (e.g., AI agentic marketing, retail media networks, consumer sentiment shifts).
  - Organizes articles into categorized digests with source badges, dates, summaries, and direct source links.
- 📄 **Compiles Executive PDF Briefing**:
  - Built with ReportLab using a modern executive editorial layout.
  - Dynamic page numbering ("Page X of Y"), callout boxes, and clickable links.
- 🚀 **Multi-Channel Dispatch**:
  - **Telegram**: Uploads the PDF document directly to your Telegram chat with a summary caption.
  - **Email**: Sends an HTML newsletter with the PDF attached via SMTP (Gmail, Outlook, etc.).

---

## 📂 Project Structure

```
marketing-intel-agent/
├── agent.py               # Main CLI orchestrator (run, dry-run, test)
├── config.py              # Configuration & environment variable loader
├── sources.py             # Curated list of RSS/Atom feeds and category metadata
├── fetcher.py             # Parallel feed fetcher, parser & deduplicator
├── synthesizer.py         # Digest categorization, strategic themes & message formatting
├── pdf_generator.py       # Two-pass ReportLab executive PDF builder
├── dispatcher.py          # Telegram Bot API and SMTP Email dispatchers
├── .env.example           # Credential template
├── .env                   # Your local secrets (Telegram & Email)
├── reports/               # Output directory where generated PDFs are stored
└── .agents/skills/        # Antigravity skill definition
```

---

## 🛠 Setup & Credentials Guide

### 1. Telegram Setup (Takes 2 minutes)
1. Open Telegram and search for [@BotFather](https://t.me/BotFather).
2. Send `/newbot`, choose a name and username. Copy the **HTTP API token**.
3. Set in `.env`:
   ```env
   TELEGRAM_BOT_TOKEN="your_token_from_botfather"
   ```
4. Start a conversation with your new bot (press **Start**).
5. Search for [@userinfobot](https://t.me/userinfobot) on Telegram and send `/start` to see your personal **Chat ID** (a number like `123456789`).
6. Set in `.env`:
   ```env
   TELEGRAM_CHAT_ID="123456789"
   ```

### 2. Email Setup (Using Gmail or custom SMTP)
1. **Gmail with App Password**:
   - Go to your [Google Account Security](https://myaccount.google.com/security).
   - Ensure 2-Step Verification is ON.
   - Go to [App Passwords](https://myaccount.google.com/apppasswords).
   - Create a new App Password (name it "Marketing Agent") and copy the 16-character code.
2. In `.env`, set:
   ```env
   SMTP_HOST="smtp.gmail.com"
   SMTP_PORT=587
   SMTP_USER="your_email@gmail.com"
   SMTP_PASSWORD="your-16-char-app-password"
   EMAIL_FROM="your_email@gmail.com"
   EMAIL_TO="recipient_email@example.com"
   ```

---

## 🚀 Running the Agent

The project includes an isolated virtual environment at `.venv/`.

### Generate PDF without sending (Dry Run)
```bash
.venv/bin/python agent.py --dry-run
```

### Full Run (Fetch, Generate PDF & Deliver to Telegram + Email)
```bash
.venv/bin/python agent.py
```

### Verify Connections to Telegram and Email
```bash
.venv/bin/python agent.py --test-delivery
```

### Filter for a Specific Section
```bash
# Branding only
.venv/bin/python agent.py --dry-run --category BRANDING

# Advertising campaigns only
.venv/bin/python agent.py --dry-run --category ADVERTISING

# Marketing & Tech only
.venv/bin/python agent.py --dry-run --category MARKETING_TECH
```

---

## ⏰ Automated Scheduling (Cron / Background)

To have this run automatically every weekday morning (e.g. at 8:00 AM), you can set a cron job:

```bash
# Edit crontab
crontab -e

# Add this entry for 8:00 AM Monday–Friday:
0 8 * * 1-5 cd /Users/mac/.gemini/antigravity/scratch/marketing-intel-agent && .venv/bin/python agent.py >> reports/cron.log 2>&1
```
