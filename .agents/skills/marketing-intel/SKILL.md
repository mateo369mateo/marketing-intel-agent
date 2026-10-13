---
name: marketing-intel
description: Reads latest news across marketing, branding, and advertising sources (Adweek, Campaign, Marketing Dive, Digiday, Brand New), synthesizes key campaign and branding moves, compiles an executive PDF briefing, and delivers it to Telegram and Email.
metadata:
  icon: newspaper
---

# Marketing, Branding & Advertising Intelligence Agent

This skill operates the automated intelligence agent located at `/Users/mac/.gemini/antigravity/scratch/marketing-intel-agent`.

## What This Agent Does

1. **Monitors Top Sources**:
   - **Advertising**: Adweek, Campaign Live, global agency developments.
   - **Branding**: Brand New (UnderConsideration), Retail Dive, rebrands & visual identity moves.
   - **Marketing & AdTech**: Marketing Dive, Digiday, Social Media Today.
2. **Synthesizes & Curates**:
   - Extracts key strategic themes (AI automation, brand repositions, retail media, consumer sentiment).
   - Groups top stories into clean categories with takeaways.
3. **Generates an Executive PDF Report**:
   - Formats a multi-page executive briefing complete with source badges, headlines, takeaways, and direct links.
4. **Multi-Channel Dispatch**:
   - Sends the PDF document and summary caption to Telegram via the Bot API.
   - Sends the PDF attachment and styled HTML newsletter via SMTP Email.

---

## How to Run

Virtualenv Python path:
`/Users/mac/.gemini/antigravity/scratch/marketing-intel-agent/.venv/bin/python`

### 1. Generate PDF Report (Dry Run / Test)
```bash
cd /Users/mac/.gemini/antigravity/scratch/marketing-intel-agent
.venv/bin/python agent.py --dry-run
```

### 2. Full Run (Generate and Dispatch to Telegram & Email)
```bash
cd /Users/mac/.gemini/antigravity/scratch/marketing-intel-agent
.venv/bin/python agent.py
```

### 3. Test Telegram & Email Credentials
```bash
cd /Users/mac/.gemini/antigravity/scratch/marketing-intel-agent
.venv/bin/python agent.py --test-delivery
```

### 4. Filter by Category
```bash
# Only Branding & Rebrands
.venv/bin/python agent.py --dry-run --category BRANDING

# Only Advertising Campaigns
.venv/bin/python agent.py --dry-run --category ADVERTISING

# Only Marketing & AdTech
.venv/bin/python agent.py --dry-run --category MARKETING_TECH
```

---

## Configuration (`.env`)

The agent reads credentials from:
`/Users/mac/.gemini/antigravity/scratch/marketing-intel-agent/.env`

Required for Telegram:
- `TELEGRAM_BOT_TOKEN`: Token obtained from Telegram's `@BotFather`.
- `TELEGRAM_CHAT_ID`: Your numerical user or group Chat ID (from `@userinfobot`).

Required for Email:
- `SMTP_HOST`: e.g. `smtp.gmail.com`
- `SMTP_PORT`: `587` (STARTTLS) or `465` (SSL)
- `SMTP_USER`: Sender email address
- `SMTP_PASSWORD`: App password (e.g., Google App Password)
- `EMAIL_TO`: Recipient email address
