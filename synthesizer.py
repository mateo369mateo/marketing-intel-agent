from datetime import datetime
from sources import CATEGORIES
from config import MAX_TOTAL_ARTICLES_PER_SECTION
from ai_analyst import analyze_with_ai

def synthesize_digest(articles: list) -> dict:
    """
    Groups articles into categories, selects top items,
    and runs cognitive AI analysis to generate executive takeaways.
    """
    grouped = {cat_id: [] for cat_id in CATEGORIES}

    for art in articles:
        cat = art.get("category")
        if cat in grouped:
            grouped[cat].append(art)

    # Limit each section to top articles
    selected_by_category = {}
    flat_selected = []
    for cat_id, cat_articles in grouped.items():
        top_articles = cat_articles[:MAX_TOTAL_ARTICLES_PER_SECTION]
        selected_by_category[cat_id] = top_articles
        flat_selected.extend(top_articles)

    today_str = datetime.now().strftime("%B %d, %Y")
    total_selected = len(flat_selected)

    # Default heuristic fallback themes
    themes = [
        "Agency & AI Automation: Acceleration of agentic workflows and automated creative production in marketing suites.",
        "Brand Equity & Identity: Legacy brands rolling out major visual identity refreshes and cross-channel repositioning.",
        "Media Spend & Attribution: Shifts in budget toward retail media networks and short-form video performance channels."
    ]
    executive_summary = (
        "Macro marketing shifts today emphasize aggressive adoption of generative workflows, "
        "heritage brand visual identity transformations, and consolidation across omnichannel retail media."
    )
    is_ai_powered = False

    # Run AI Analysis
    ai_insights = analyze_with_ai(flat_selected)
    if ai_insights:
        is_ai_powered = True
        if ai_insights.get("strategic_themes"):
            themes = ai_insights["strategic_themes"]
        if ai_insights.get("executive_summary"):
            executive_summary = ai_insights["executive_summary"]

        # Map article insights back to each article
        insights_list = ai_insights.get("article_insights", [])
        insight_map = {}
        for item in insights_list:
            if isinstance(item, dict) and "id" in item and "strategic_takeaway" in item:
                insight_map[item["id"]] = item["strategic_takeaway"]

        # Assign back to flat_selected
        for idx, art in enumerate(flat_selected):
            if idx in insight_map:
                art["ai_insight"] = insight_map[idx]
            else:
                art["ai_insight"] = ""

    return {
        "date": today_str,
        "total_analyzed": len(articles),
        "total_curated": total_selected,
        "executive_summary": executive_summary,
        "themes": themes,
        "categories": selected_by_category,
        "is_ai_powered": is_ai_powered
    }


def format_telegram_caption(digest: dict) -> str:
    """
    Format an executive AI-powered Telegram message/caption to accompany the PDF file.
    """
    ai_badge = "🧠 *AI-Synthesized CMO Briefing*" if digest.get("is_ai_powered") else "📊 *Executive Briefing*"
    
    lines = [
        f"{ai_badge}",
        f"🗓 *Date:* {digest['date']}",
        f"⚡ *Curated:* {digest['total_curated']} key stories across {digest['total_analyzed']} analyzed\n",
        f"💡 *Executive Pulse:*\n_{digest.get('executive_summary', '')}_\n",
        "🔥 *Key Strategic Themes:*",
    ]

    for theme in digest["themes"][:3]:
        lines.append(f"• {theme}")

    lines.append("\n📁 *Attached:* Full Executive PDF Briefing with deep strategic takeaways and source links.")
    return "\n".join(lines)


def format_email_body_html(digest: dict) -> str:
    """
    Format an executive HTML newsletter email body to accompany the attached PDF.
    """
    ai_label = "AI-Powered Executive Intelligence" if digest.get("is_ai_powered") else "Intelligence Briefing"
    themes_html = "".join(f"<li style='margin-bottom: 8px;'>{t}</li>" for t in digest["themes"])

    sections_html = ""
    for cat_id, articles in digest["categories"].items():
        cat_meta = CATEGORIES.get(cat_id, {})
        cat_title = cat_meta.get("title", cat_id)
        cat_color = cat_meta.get("badge_color", "#4338CA")

        items_html = ""
        for art in articles[:4]:
            ai_takeaway_html = ""
            if art.get("ai_insight"):
                ai_takeaway_html = f"""
                <div style="margin-top: 6px; padding: 6px 10px; background: #eef2ff; border-left: 3px solid #4f46e5; border-radius: 4px; font-size: 12px; color: #3730a3;">
                    <strong>💡 Strategic Takeaway:</strong> {art['ai_insight']}
                </div>
                """

            items_html += f"""
            <div style="margin-bottom: 16px; padding-bottom: 14px; border-bottom: 1px solid #f1f5f9;">
                <div style="font-size: 11px; font-weight: 700; color: {cat_color}; text-transform: uppercase;">{art['source']} • {art['published']}</div>
                <div style="font-size: 15px; font-weight: 600; color: #0f172a; margin: 3px 0;"><a href="{art['url']}" style="color: #0f172a; text-decoration: none;">{art['title']}</a></div>
                <div style="font-size: 13px; color: #475569; line-height: 1.4;">{art['summary']}</div>
                {ai_takeaway_html}
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
                <span style="font-size: 11px; font-weight: 700; color: #4338ca; letter-spacing: 1px; text-transform: uppercase;">{ai_label}</span>
                <h1 style="font-size: 24px; color: #0f172a; margin: 6px 0 4px 0;">Marketing, Branding & Advertising Digest</h1>
                <p style="font-size: 13px; color: #64748b; margin: 0;">{digest['date']} • Curated across leading industry sources</p>
            </div>

            <div style="background-color: #f1f5f9; border-radius: 6px; padding: 16px 20px; margin-bottom: 24px;">
                <h4 style="margin: 0 0 6px 0; color: #0f172a; font-size: 14px;">🧠 Executive Pulse & Macro Trends</h4>
                <p style="margin: 0 0 10px 0; font-size: 13px; color: #1e293b; line-height: 1.5; font-style: italic;">
                    "{digest.get('executive_summary', '')}"
                </p>
                <ul style="margin: 0; padding-left: 18px; font-size: 13px; color: #334155; line-height: 1.5;">
                    {themes_html}
                </ul>
            </div>

            <p style="font-size: 13px; color: #64748b; font-style: italic;">
                📎 <strong>Complete PDF Report Attached:</strong> The full publication with complete article cards, AI strategic takeaways, and direct source links has been attached to this email.
            </p>

            {sections_html}

            <div style="margin-top: 32px; padding-top: 16px; border-top: 1px solid #e2e8f0; font-size: 11px; color: #94a3b8; text-align: center;">
                Generated by Antigravity AI Marketing Intelligence Agent • Automated Daily Briefing
            </div>
        </div>
    </body>
    </html>
    """
    return html
