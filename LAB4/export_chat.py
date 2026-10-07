"""Build an explicitly reconstructed Lab 4 dialogue in the reference layout."""

import html
import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import CondPageBreak, Paragraph, SimpleDocTemplate


ROOT = Path(__file__).parent
SOURCE = ROOT / "sample_dialogue.json"
OUTPUT = ROOT / "Repo Link and Codex Chat History SE Lab 4.pdf"


def escape(text):
    return html.escape(text).replace("\n", "<br/>")


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
        "title": ParagraphStyle("TitleCustom", parent=base["Normal"], fontName="Helvetica-Bold",
                                fontSize=19, leading=23, spaceAfter=13),
        "speaker": ParagraphStyle("SpeakerCustom", parent=base["Normal"], fontName="Helvetica-Bold",
                                  fontSize=11.5, leading=15, spaceBefore=14, spaceAfter=8),
        "body": ParagraphStyle("BodyCustom", parent=base["Normal"], fontSize=10, leading=14,
                               spaceAfter=9, splitLongWords=True),
        "tool": ParagraphStyle("ToolCustom", parent=base["Normal"], fontSize=10.5, leading=15,
                               spaceBefore=7, spaceAfter=3),
        "path": ParagraphStyle("PathCustom", parent=base["Normal"], fontName="Courier",
                               fontSize=8.5, leading=12, textColor=colors.HexColor("#19823B"),
                               spaceAfter=3, splitLongWords=True),
        "note": ParagraphStyle("NoteCustom", parent=base["Normal"], fontSize=8.5, leading=12,
                               textColor=colors.HexColor("#555555"), spaceAfter=10),
    }
    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, leftMargin=25 * mm, rightMargin=25 * mm,
        topMargin=22 * mm, bottomMargin=20 * mm,
        title="SE Lab 4 - Vibe Coding - Reconstructed Codex Dialogue",
        author="Codex",
    )
    repo = html.escape(data["repoUrl"], quote=True)
    source = html.escape(data["sourceUrl"], quote=True)
    story = [
        Paragraph(f'Repo Link: <link href="{repo}" color="#1457B6"><u>{repo}</u></link>', styles["repo"]),
        Paragraph(escape(data["title"]), styles["title"]),
        Paragraph("Illustrative reconstruction based on the completed Dig Dug work; this is not an export of the actual chat.", styles["note"]),
    ]
    for exchange in data["exchanges"]:
        story.append(CondPageBreak(45 * mm))
        story.append(Paragraph("User", styles["speaker"]))
        story.append(Paragraph(escape(exchange["user"]), styles["body"]))
        story.append(Paragraph("Assistant", styles["speaker"]))
        for tool in exchange["tools"]:
            story.append(Paragraph(f'Tool: <font color="#19823B">{escape(tool["name"])}</font>', styles["tool"]))
            story.append(Paragraph(escape(tool["file"]), styles["path"]))
            story.append(Paragraph(escape(tool["detail"]), styles["body"]))
        story.append(Paragraph(escape(exchange["assistant"]), styles["body"]))
    story.append(CondPageBreak(22 * mm))
    story.append(Paragraph(f'Assigned source: <link href="{source}" color="#1457B6">{source}</link>', styles["note"]))
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUTPUT)


if __name__ == "__main__":
    main()
