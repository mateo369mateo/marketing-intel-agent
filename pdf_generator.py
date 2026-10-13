import os
from xml.sax.saxutils import escape as xml_escape
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas
from sources import CATEGORIES
from config import REPORTS_DIR

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page count"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Bottom Line
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 46, 612 - 54, 46)
        
        # Footer text
        left_footer = "Marketing & Branding Intelligence Briefing • Confidential Executive Report"
        right_footer = f"Page {self._pageNumber} of {page_count}"
        self.drawString(54, 34, left_footer)
        self.drawRightString(612 - 54, 34, right_footer)
        
        self.restoreState()


def safe_escape(text: str) -> str:
    """Escapes special characters for ReportLab XML parser."""
    if not text:
        return ""
    # Standard XML escaping
    escaped = xml_escape(str(text))
    return escaped


def generate_pdf_report(digest: dict, output_filename: str = None) -> str:
    """
    Builds an executive PDF briefing from synthesized digest data.
    """
    if not output_filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"marketing_briefing_{timestamp}.pdf"

    pdf_path = os.path.join(REPORTS_DIR, output_filename)

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=50,
        bottomMargin=60
    )

    styles = getSampleStyleSheet()

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0F172A")
    )
    date_style = ParagraphStyle(
        'DocDate',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#4338CA"),
        alignment=2 # Right aligned
    )
    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#64748B")
    )
    section_title_style = ParagraphStyle(
        'SectionTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=14,
        spaceAfter=4
    )
    section_desc_style = ParagraphStyle(
        'SectionDesc',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#64748B"),
        spaceAfter=10
    )
    card_source_style = ParagraphStyle(
        'CardSource',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#4338CA")
    )
    card_headline_style = ParagraphStyle(
        'CardHeadline',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0F172A")
    )
    card_body_style = ParagraphStyle(
        'CardBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#334155")
    )
    card_link_style = ParagraphStyle(
        'CardLink',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#2563EB")
    )
    box_heading_style = ParagraphStyle(
        'BoxHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0F172A")
    )
    box_body_style = ParagraphStyle(
        'BoxBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#334155")
    )

    story = []

    # 1. Header Table (Title on Left, Date & Edition on Right)
    left_header = [
        Paragraph("MARKETING & BRANDING INTELLIGENCE", title_style),
        Spacer(1, 2),
        Paragraph("Daily Executive Intelligence • Key Moves, Campaigns & Industry Trends", meta_style)
    ]
    right_header = [
        Paragraph(safe_escape(digest['date']), date_style),
        Spacer(1, 2),
        Paragraph(f"Analyzed {digest['total_analyzed']} stories • Curated {digest['total_curated']}", ParagraphStyle('RightMeta', parent=meta_style, alignment=2))
    ]
    
    header_table = Table([[left_header, right_header]], colWidths=[330, 174])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    # Colored Divider
    story.append(HRFlowable(width="100%", thickness=2.5, color=colors.HexColor("#4338CA"), spaceAfter=14))

    # 2. Executive Pulse / Strategic Overview Callout Box
    pulse_content = [
        Paragraph("<b>EXECUTIVE PULSE & STRATEGIC HIGHLIGHTS</b>", box_heading_style),
        Spacer(1, 5)
    ]
    for idx, theme in enumerate(digest.get("themes", []), 1):
        pulse_content.append(
            Paragraph(f"• <b>{safe_escape(theme.split(':')[0])}:</b> {safe_escape(theme.split(':', 1)[-1].strip())}", box_body_style)
        )
        pulse_content.append(Spacer(1, 3))

    pulse_table = Table([[pulse_content]], colWidths=[504])
    pulse_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
    ]))
    story.append(pulse_table)
    story.append(Spacer(1, 14))

    # 3. Categorized Content Sections
    for cat_id, articles in digest.get("categories", {}).items():
        if not articles:
            continue

        cat_meta = CATEGORIES.get(cat_id, {})
        cat_title = cat_meta.get("title", cat_id)
        cat_desc = cat_meta.get("description", "")
        badge_hex = cat_meta.get("badge_color", "#4338CA")
        badge_color = colors.HexColor(badge_hex)

        # Section Header with colored indicator
        sec_bar = HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0"), spaceAfter=6, spaceBefore=8)
        story.append(sec_bar)

        story.append(Paragraph(safe_escape(cat_title), section_title_style))
        if cat_desc:
            story.append(Paragraph(safe_escape(cat_desc), section_desc_style))

        # Render Articles as modern card flowables
        for art in articles:
            card_elements = []

            # Pill/Badge line
            source_tag = f"<font color='{badge_hex}'><b>{safe_escape(art['source'].upper())}</b></font>  |  {safe_escape(art['published'])}"
            card_elements.append(Paragraph(source_tag, card_source_style))
            card_elements.append(Spacer(1, 2))

            # Headline
            card_elements.append(Paragraph(safe_escape(art["title"]), card_headline_style))
            card_elements.append(Spacer(1, 3))

            # Summary
            card_elements.append(Paragraph(safe_escape(art["summary"]), card_body_style))
            card_elements.append(Spacer(1, 3))

            # Link
            if art.get("url"):
                link_text = f"<a href='{safe_escape(art['url'])}' color='#2563EB'><u>Read full article at {safe_escape(art['source'])} &rarr;</u></a>"
                card_elements.append(Paragraph(link_text, card_link_style))

            # Wrap into an article card table
            card_table = Table([[card_elements]], colWidths=[504])
            card_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#FFFFFF")),
                ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor("#E2E8F0")),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ]))

            # Keep individual card together to avoid splitting mid-card
            story.append(KeepTogether([card_table, Spacer(1, 7)]))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[PDF Generator] ✅ Successfully created PDF report at: {pdf_path}")
    return pdf_path
