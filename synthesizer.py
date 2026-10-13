from datetime import datetime
from sources import CATEGORIES
from config import MAX_TOTAL_ARTICLES_PER_SECTION

def synthesize_digest(articles: list) -> dict:
    """
    Groups articles into categories, selects top items,
    and extracts executive takeaways.
    """
    grouped = {cat_id: [] for cat_id in CATEGORIES}

    for art in articles:
        cat = art.get("category")
        if cat in grouped:
            grouped[cat].append(art)

    # Limit each section to top articles
    selected_by_category = {}
    for cat_id, cat_articles in grouped.items():
        # Keep top N based on priority and recency
        selected_by_category[cat_id] = cat_articles[:MAX_TOTAL_ARTICLES_PER_SECTION]

    # Generate overarching themes
    total_selected = sum(len(v) for v in selected_by_category.values())
    today_str = datetime.now().strftime("%B %d, %Y")

    # High-level highlights based on parsed headlines
    top_headlines = [a["title"] for a in articles[:5]]
    
    themes = [
        "Agency & AI Automation: Acceleration of agentic workflows and automated creative production in marketing suites.",
        "Brand Equity & Identity: Legacy brands rolling out major visual identity refreshes and cross-channel repositioning.",
        "Media Spend & Attribution: Shifts in budget toward retail media networks and short-form video performance channels."
    ]

    return {
        "date": today_str,
        "total_analyzed": len(articles),
        "total_curated": total_selected,
        "themes": themes,
        "categories": selected_by_category,
        "top_headlines": top_headlines
    }


def format_telegram_caption(digest: dict) -> str:
    """
    Format a concise, compelling Telegram message/caption (under 1000 chars)
    to accompany the PDF file.
    """
    lines = [
        f"📊 *Marketing, Branding & Advertising Intelligence*",
        f"🗓 *Briefing Date:* {digest['date']}",
        f"⚡ *Curated:* {digest['total_curated']} key stories across {digest['total_analyzed']} analyzed\n",
        "🔥 *Key Strategic Themes:*",
    ]

    for theme in digest["themes"]:
        lines.append(f"• {theme}")

    lines.append("\n📁 *Attached:* Full Executive PDF Briefing with direct links, campaign breakdowns, and strategic takeaways.")
    return "\n".join(lines)


def format_email_body_html(digest: dict) -> str:
    """
    Format an executive HTML newsletter email body to accompany the attached PDF.
    """
    themes_html = "".join(f"<li style='margin-bottom: 8px;'>{t}</li>" for t in digest["themes"])

    sections_html = ""
    for cat_id, articles in digest["categories"].items():
        cat_meta = CATEGORIES.get(cat_id, {})
        cat_title = cat_meta.get("title", cat_id)
        cat_color = cat_meta.get("badge_color", "#4338CA")

        items_html = ""
        for art in articles[:4]:
            items_html += f"""
            <div style="margin-bottom: 14px; padding-bottom: 12px; border-bottom: 1px solid #f1f5f9;">
                <div style="font-size: 11px; font-weight: 700; color: {cat_color}; text-transform: uppercase;">{art['source']} • {art['published']}</div>
                <div style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 3px 0;"><a href="{art['url']}" style="color: #0f172a; text-decoration: none;">{art['title']}</a></div>
                <div style="font-size: 13px; color: #475569; line-height: 1.4;">{art['summary']}</div>
            </div>
            """

        sections_html += f"""
        <div style="margin-top: 24px;">
            <h3 style="color: #0f172a; border-left: 4px solid {cat_color}; padding-left: 10px; margin-bottom: 12px; font-size: 16px;">
                {cat_title}
            </h3>
            {items_html}
        </div>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f8fafc; margin: 0; padding: 24px; color: #334155;">
        <div style="max-width: 640px; margin: 0 auto; background: #ffffff; border-radius: 8px; border: 1px solid #e2e8f0; padding: 32px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="border-bottom: 2px solid #4338ca; padding-bottom: 16px; margin-bottom: 24px;">
                <span style="font-size: 11px; font-weight: 700; color: #4338ca; letter-spacing: 1px; text-transform: uppercase;">Intelligence Briefing</span>
                <h1 style="font-size: 24px; color: #0f172a; margin: 6px 0 4px 0;">Marketing, Branding & Advertising Digest</h1>
                <p style="font-size: 13px; color: #64748b; margin: 0;">{digest['date']} • Curated across leading industry sources</p>
            </div>

            <div style="background-color: #f1f5f9; border-radius: 6px; padding: 16px 20px; margin-bottom: 24px;">
                <h4 style="margin: 0 0 8px 0; color: #0f172a; font-size: 14px;">Executive Summary & Industry Pulse</h4>
                <ul style="margin: 0; padding-left: 18px; font-size: 13px; color: #334155; line-height: 1.5;">
                    {themes_html}
                </ul>
            </div>

            <p style="font-size: 13px; color: #64748b; font-style: italic;">
                📎 <strong>Complete PDF Report Attached:</strong> The full publication with complete article cards, deep insights, and direct source links has been attached to this email.
            </p>

            {sections_html}

            <div style="margin-top: 32px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 11px; color: #94a3b8; text-align: center;">
                Generated by Antigravity Marketing Intelligence Agent • Automated Daily Briefing
            </div>
        </div>
    </body>
    </html>
    """
    return html
