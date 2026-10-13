#!/usr/bin/env python3
"""
Marketing, Branding & Advertising Intelligence Agent
Orchestrator CLI: Ingests news, synthesizes intelligence, generates executive PDF, and dispatches to Telegram & Email.
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path

from fetcher import fetch_all_marketing_news
from synthesizer import synthesize_digest, format_telegram_caption, format_email_body_html
from pdf_generator import generate_pdf_report
from dispatcher import send_to_telegram, send_to_email
import config

BANNER = """
========================================================================
  🎯 MARKETING, BRANDING & ADVERTISING INTELLIGENCE AGENT
  Automated Executive Briefing Generator & Dispatcher
========================================================================
"""

def test_delivery():
    """Test connections to Telegram and Email with a sample PDF."""
    print("\n--- 🧪 Testing Delivery Channels ---")
    
    # Create or use a dummy test PDF
    test_pdf = config.REPORTS_DIR / "test_delivery_sample.pdf"
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    
    doc = SimpleDocTemplate(str(test_pdf), pagesize=letter)
    styles = getSampleStyleSheet()
    doc.build([Paragraph("Marketing Intelligence Agent - Connection Test Successful!", styles['Normal'])])
    
    # Test Telegram
    print("\n1. Testing Telegram:")
    t_status = send_to_telegram(
        str(test_pdf),
        "🔔 *Marketing Intelligence Agent Test*\nYour Telegram delivery channel is connected successfully!"
    )
    
    # Test Email
    print("\n2. Testing Email:")
    e_status = send_to_email(
        str(test_pdf),
        "Test Briefing - Marketing Intelligence Agent",
        "<h3>Marketing Intelligence Agent Test</h3><p>Your email delivery channel is configured and functioning properly.</p>"
    )
    
    print("\n--- Test Results ---")
    print(f"Telegram: {'✅ Configured & Working' if t_status else '⚠️  Not Configured or Failed'}")
    print(f"Email:    {'✅ Configured & Working' if e_status else '⚠️  Not Configured or Failed'}")


def run_agent(dry_run: bool = False, output_file: str = None, category_filter: str = None):
    print(BANNER)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Mode: {'🔍 Dry Run (PDF only)' if dry_run else '🚀 Full Run (Generate & Dispatch)'}")
    print("------------------------------------------------------------------------\n")

    # Step 1: Fetch feeds
    articles = fetch_all_marketing_news()
    if not articles:
        print("[Agent] ❌ No articles could be retrieved. Check network connection.")
        return False

    if category_filter:
        cat_upper = category_filter.upper()
        articles = [a for a in articles if a.get("category") == cat_upper]
        print(f"[Agent] Filtered to {len(articles)} articles in category '{cat_upper}'")

    # Step 2: Synthesize
    print("\n[Synthesizer] Synthesizing executive briefing and identifying key themes...")
    digest = synthesize_digest(articles)
    print(f"[Synthesizer] ✅ Synthesized {digest['total_curated']} key stories across {len(digest['categories'])} sections.")

    # Step 3: Generate Executive PDF
    print("\n[PDF Generator] Compiling executive PDF report...")
    pdf_path = generate_pdf_report(digest, output_filename=output_file)
    print(f"[PDF Generator] 📄 Report generated: {pdf_path}")

    # Step 4: Dispatch
    if dry_run:
        print("\n[Agent] 💡 Dry run completed. Skipping dispatch to Telegram and Email.")
        print(f"[Agent] 📁 You can view your generated PDF at: {pdf_path}")
        return True

    print("\n[Dispatcher] Initiating multi-channel dispatch...")
    
    # Prepare message formats
    tg_caption = format_telegram_caption(digest)
    email_subject = f"Executive Intelligence Briefing: Marketing, Branding & Advertising ({digest['date']})"
    email_html = format_email_body_html(digest)

    # Send to Telegram
    tg_success = send_to_telegram(pdf_path, tg_caption)

    # Send to Email
    email_success = send_to_email(pdf_path, email_subject, email_html)

    print("\n========================================================================")
    print("  🏁 EXECUTION SUMMARY")
    print("========================================================================")
    print(f"  • Curated Articles: {digest['total_curated']}")
    print(f"  • PDF Generated:    {pdf_path}")
    print(f"  • Telegram Status:  {'✅ Delivered' if tg_success else '⚠️  Skipped / Failed (Check .env)'}")
    print(f"  • Email Status:     {'✅ Delivered' if email_success else '⚠️  Skipped / Failed (Check .env)'}")
    print("========================================================================\n")

    return True


def main():
    parser = argparse.ArgumentParser(description="Marketing, Branding & Advertising Intelligence Agent")
    parser.add_argument("--dry-run", action="store_true", help="Generate PDF report without sending to Telegram or Email")
    parser.add_argument("--test-delivery", action="store_true", help="Send a test document to verify Telegram and Email credentials")
    parser.add_argument("--output", type=str, default=None, help="Custom output filename for the generated PDF")
    parser.add_argument("--category", type=str, default=None, help="Filter for a specific category (BRANDING, ADVERTISING, MARKETING_TECH)")
    
    args = parser.parse_args()

    if args.test_delivery:
        test_delivery()
    else:
        run_agent(dry_run=args.dry_run, output_file=args.output, category_filter=args.category)

if __name__ == "__main__":
    main()
