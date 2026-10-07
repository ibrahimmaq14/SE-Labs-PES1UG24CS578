"""Build the Lab 4 chat transcript PDF in the supplied example's style."""

import html
import json
from itertools import groupby
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import CondPageBreak, Paragraph, SimpleDocTemplate


ROOT = Path(__file__).parent
SOURCE = ROOT / "chat_history.json"
OUTPUT = ROOT / "Repo Link and Codex Chat History SE Lab 4.pdf"


def plain(value):
    return html.escape(value).replace("\n", "<br/>")


def footer(canvas, document):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#777777"))
    canvas.drawRightString(190 * mm, 12 * mm, str(document.page))
    canvas.restoreState()


def main():
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    base = getSampleStyleSheet()
    styles = {
        "repo": ParagraphStyle("Repo", parent=base["Normal"], fontSize=10.5, leading=15, spaceAfter=15),
        "title": ParagraphStyle("TitleCustom", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=19,
                                leading=23, alignment=TA_LEFT, spaceAfter=16),
        "section": ParagraphStyle("SectionCustom", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=12,
                                  leading=16, spaceBefore=14, spaceAfter=8),
        "speaker": ParagraphStyle("SpeakerCustom", parent=base["Normal"], fontName="Helvetica-Bold", fontSize=11,
                                  leading=14, spaceBefore=13, spaceAfter=8),
        "body": ParagraphStyle("BodyCustom", parent=base["Normal"], fontSize=10, leading=14,
                               spaceAfter=9, splitLongWords=True),
        "tool": ParagraphStyle("ToolCustom", parent=base["Normal"], fontSize=10.5, leading=15,
                               spaceBefore=7, spaceAfter=3),
        "path": ParagraphStyle("PathCustom", parent=base["Normal"], fontName="Courier", fontSize=8.5,
                               leading=12, textColor=colors.HexColor("#19823B"),
                               spaceAfter=6, splitLongWords=True),
        "note": ParagraphStyle("NoteCustom", parent=base["Normal"], fontSize=8.5, leading=12,
                               textColor=colors.HexColor("#555555"), spaceAfter=8),
    }
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=25 * mm, rightMargin=25 * mm,
        topMargin=22 * mm, bottomMargin=20 * mm, title="SE Lab 4 - Vibe Coding - Codex Chat History",
        author="Codex and user",
    )
    story = []
    repo = html.escape(data["repoUrl"], quote=True)
    story.append(Paragraph(f'Repo Link: <link href="{repo}" color="#1457B6"><u>{repo}</u></link>', styles["repo"]))
    story.append(Paragraph(plain(data["title"]), styles["title"]))
    story.append(Paragraph(
        "This transcript keeps the actual user and assistant messages. The task briefs below come from the assigned "
        "Dig Dug README; they are labeled separately from user messages. Tool entries summarize verified edits and checks.",
        styles["note"],
    ))

    story.append(Paragraph("Conversation", styles["section"]))
    for role, group in groupby(data["messages"], key=lambda message: message["role"]):
        story.append(CondPageBreak(22 * mm))
        story.append(Paragraph(html.escape(role), styles["speaker"]))
        for message in group:
            story.append(Paragraph(plain(message["text"]), styles["body"]))

    story.append(CondPageBreak(40 * mm))
    story.append(Paragraph("Task-by-task work record", styles["section"]))
    for task in data["taskRecords"]:
        story.append(CondPageBreak(52 * mm))
        story.append(Paragraph(plain(task["title"]), styles["speaker"]))
        story.append(Paragraph(f'<b>Assigned README:</b> {plain(task["brief"])}', styles["body"]))
        story.append(Paragraph("Assistant", styles["speaker"]))
        story.append(Paragraph(f'Tool: <font color="#19823B">{plain(task["tool"])}</font>', styles["tool"]))
        story.append(Paragraph(plain(task["file"]), styles["path"]))
        story.append(Paragraph(plain(task["change"]), styles["body"]))
        story.append(Paragraph(f'<b>Check:</b> {plain(task["check"])}', styles["body"]))
        story.append(Paragraph(f'<b>Commit:</b> {plain(task["commit"])}', styles["note"]))

    story.append(Paragraph("Initial delivery", styles["section"]))
    story.append(Paragraph('Tool: <font color="#19823B">record_demo.py</font>', styles["tool"]))
    story.append(Paragraph("LAB4/videos/before.mp4 and LAB4/videos/after.mp4", styles["path"]))
    story.append(Paragraph("Captured two ten-second deterministic gameplay demonstrations.", styles["body"]))
    story.append(Paragraph('Tool: <font color="#19823B">unittest</font>', styles["tool"]))
    story.append(Paragraph("LAB4/test_game.py", styles["path"]))
    story.append(Paragraph("All four focused checks passed.", styles["body"]))
    story.append(Paragraph('Tool: <font color="#19823B">git_push</font>', styles["tool"]))
    story.append(Paragraph("Pushed the first Lab 4 submission to main at commit a256a33.", styles["body"]))

    source = html.escape(data["sourceUrl"], quote=True)
    share = html.escape(data["shareUrl"], quote=True)
    story.append(CondPageBreak(28 * mm))
    story.append(Paragraph(f'Assigned source: <link href="{source}" color="#1457B6">{source}</link>', styles["note"]))
    story.append(Paragraph(f'Shared chat snapshot: <link href="{share}" color="#1457B6">{share}</link>', styles["note"]))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()
