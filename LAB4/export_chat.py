"""Create the submission PDF from the saved user/assistant message snapshot."""

import html
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer


ROOT = Path(__file__).parent
SOURCE = ROOT / "chat_history.json"
OUTPUT = ROOT / "chat_history.pdf"


def footer(canvas, document):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CAD5E2"))
    canvas.line(18 * mm, 17 * mm, 192 * mm, 17 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#617185"))
    canvas.drawString(18 * mm, 12 * mm, "Lab 4 Vibe Coding - Codex chat transcript")
    canvas.drawRightString(192 * mm, 12 * mm, f"Page {document.page}")
    canvas.restoreState()


def main():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=16, leading=19, textColor=colors.HexColor("#18324B"),
        alignment=TA_LEFT, spaceAfter=7,
    )
    note = ParagraphStyle(
        "NoteCustom", parent=styles["BodyText"], fontSize=8, leading=11,
        textColor=colors.HexColor("#526579"), spaceAfter=7,
    )
    speaker = ParagraphStyle(
        "SpeakerCustom", parent=styles["BodyText"], fontName="Helvetica-Bold",
        fontSize=9, leading=11, textColor=colors.HexColor("#176B91"),
        spaceBefore=5, spaceAfter=2,
    )
    body = ParagraphStyle(
        "BodyCustom", parent=styles["BodyText"], fontSize=8.2, leading=11,
        textColor=colors.HexColor("#203140"), spaceAfter=3,
        splitLongWords=True,
    )
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=15 * mm, bottomMargin=21 * mm,
        title=data["title"], author="Codex and user",
    )
    story = [Paragraph(html.escape(data["title"]), title)]
    story.append(Paragraph(
        "User and assistant messages captured during the Lab 4 work. "
        "The shared chat link below remains the complete, current conversation.", note
    ))
    url = html.escape(data["shareUrl"], quote=True)
    story.append(Paragraph(f'<link href="{url}" color="#176B91">{url}</link>', note))
    story.append(HRFlowable(width="100%", thickness=0.6, color=colors.HexColor("#CAD5E2")))
    for index, message in enumerate(data["messages"], 1):
        story.append(Paragraph(f'{index}. {html.escape(message["role"])}', speaker))
        content = html.escape(message["text"]).replace("\n", "<br/>")
        story.append(Paragraph(content, body))
        story.append(Spacer(1, 1 * mm))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()
