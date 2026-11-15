"""
make_line_by_line_pdf.py
------------------------
Builds the LINE-BY-LINE code explanation PDF.

    python make_line_by_line_pdf.py

The difference between this and make_code_pdf.py:

  * make_code_pdf.py explains the project in SECTIONS. Good for reading
    through once to understand the shape of the project.
  * this file explains EVERY SINGLE LINE. Good for revision, and for the
    moment in a live evaluation when someone points at line 73 and says
    "what does that do?"

How it works, and why it cannot go out of date:

  * the CODE is read from the real .py files on disk,
  * the EXPLANATIONS are read from docs/line_notes/*.py, keyed by line number,
  * the two are matched up at build time.

Because the code is never copied into the explanation files, the PDF always
shows exactly what the project currently contains. If a line moves, the
coverage check below notices that a line has no note and tells you.
"""

import importlib
import os
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (BaseDocTemplate, Frame, KeepTogether,
                                NextPageTemplate, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle)

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(
    PROJECT_DIR, "docs", "Fish_Classification_Line_By_Line.pdf"
)

# The files to document, in the order a reader should meet them.
FILES_IN_ORDER = [
    "src/config.py",
    "src/data_loader.py",
    "src/models.py",
    "src/train.py",
    "src/evaluate.py",
    "src/visualize.py",
    "prepare_dataset.py",
    "validate_data.py",
    "train_all_models.py",
    "app.py",
]

# Colours used throughout
INK = colors.HexColor("#1a1a1a")
GREY = colors.HexColor("#6b7280")
CODE_BG = colors.HexColor("#f6f8fa")
COMMENT = colors.HexColor("#6a737d")
ACCENT = colors.HexColor("#0b5394")
NOTE = colors.HexColor("#1f4e5f")


def notes_module_name(path):
    """
    Turn "src/config.py" into "docs.line_notes.src_config".

    Each documented file has a matching notes file, so the explanations for
    one module all live in one place and stay easy to edit.
    """
    stem = path.replace("/", "_").replace(".py", "")
    return f"docs.line_notes.{stem}"


def load_notes(path):
    """
    Import the notes for one source file.

    Returns (purpose_text, {line_number: explanation}).
    If no notes file exists yet, returns empty values rather than crashing,
    so the PDF can still be built while the notes are being written.
    """
    try:
        module = importlib.import_module(notes_module_name(path))
    except ModuleNotFoundError:
        return "", {}

    return getattr(module, "PURPOSE", ""), getattr(module, "NOTES", {})


def read_source(path):
    """Read one source file as a list of lines, without the newlines."""
    full = os.path.join(PROJECT_DIR, path)
    with open(full, "r", encoding="utf-8") as f:
        return f.read().split("\n")


def classify_lines(lines):
    """
    Label every line as "code", "comment", "doc" or "blank".

    Why bother: a comment and a docstring are already explanations written in
    English. Printing a second explanation underneath them would pad the
    document without teaching anything. Only lines labelled "code" need a note,
    and the coverage check at the end counts only those.

    The docstring detection is a small state machine. When a line starts with
    triple quotes we are inside a docstring until the matching triple quotes
    appear, which may be many lines later.
    """
    labels = []
    inside_docstring = False
    closing_marker = None

    for line in lines:
        stripped = line.strip()

        # Already inside a multi-line docstring?
        if inside_docstring:
            labels.append("doc")
            if closing_marker in stripped:
                inside_docstring = False
            continue

        if stripped == "":
            labels.append("blank")
            continue

        if stripped.startswith("#"):
            labels.append("comment")
            continue

        # Does this line OPEN a docstring?
        opened = False
        for marker in ('"""', "'''"):
            if stripped.startswith(marker):
                labels.append("doc")
                opened = True
                # A one-line docstring opens and closes on the same line.
                rest = stripped[len(marker):]
                if not rest.endswith(marker) or rest == "":
                    inside_docstring = True
                    closing_marker = marker
                break

        if not opened:
            labels.append("code")

    return labels


def build_styles():
    """Every text style the document uses, defined once."""
    base = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle(
            "title", parent=base["Title"], fontSize=26, leading=31,
            textColor=INK, spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "subtitle", parent=base["Normal"], fontSize=12.5, leading=18,
            textColor=GREY, alignment=1, spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontSize=18, leading=23,
            textColor=ACCENT, spaceBefore=4, spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontSize=13, leading=17,
            textColor=INK, spaceBefore=12, spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"], fontSize=10.3, leading=15.2,
            textColor=INK, alignment=TA_JUSTIFY, spaceAfter=7,
        ),
        "lead": ParagraphStyle(
            "lead", parent=base["Normal"], fontSize=10.5, leading=15.5,
            textColor=INK, alignment=TA_JUSTIFY, spaceAfter=9,
            borderPadding=7, backColor=colors.HexColor("#eef4fb"),
            borderColor=colors.HexColor("#c7dbf0"), borderWidth=0.6,
        ),
        "code": ParagraphStyle(
            "code", parent=base["Normal"], fontName="Courier", fontSize=8.1,
            leading=10.4, textColor=INK,
        ),
        "codecomment": ParagraphStyle(
            "codecomment", parent=base["Normal"], fontName="Courier",
            fontSize=8.1, leading=10.4, textColor=COMMENT,
        ),
        "lineno": ParagraphStyle(
            "lineno", parent=base["Normal"], fontName="Helvetica",
            fontSize=6.6, leading=10.4, textColor=colors.HexColor("#9aa4b2"),
            alignment=2,
        ),
        "note": ParagraphStyle(
            "note", parent=base["Normal"], fontSize=9.3, leading=13.2,
            textColor=NOTE, leftIndent=30, spaceBefore=1.5, spaceAfter=5,
        ),
        "toc": ParagraphStyle(
            "toc", parent=base["Normal"], fontSize=10.6, leading=19,
            textColor=INK,
        ),
    }
    return styles


def code_line_flowable(number, text, label, styles):
    """
    Render ONE line of source code: a small grey line number on the left,
    the code itself on a pale background to the right.

    Using a one-row table per line (rather than one big table for the whole
    file) is deliberate: it lets reportlab break the page between any two
    lines instead of complaining that a block is too tall to fit.
    """
    safe = escape(text).replace(" ", "&nbsp;") or "&nbsp;"
    style = styles["codecomment"] if label in ("comment", "doc") else styles["code"]

    table = Table(
        [[Paragraph(str(number), styles["lineno"]), Paragraph(safe, style)]],
        colWidths=[1.0 * cm, 15.0 * cm],
    )
    table.setStyle(TableStyle([
        ("BACKGROUND", (1, 0), (1, 0), CODE_BG),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 4),
        ("LEFTPADDING", (1, 0), (1, 0), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 1.2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2),
    ]))
    return table


def build_file_section(path, styles, coverage):
    """
    Build every flowable for one source file, and record coverage numbers.
    """
    purpose, notes = load_notes(path)
    lines = read_source(path)
    labels = classify_lines(lines)

    story = [Paragraph(escape(path), styles["h1"])]

    if purpose:
        story.append(Paragraph(purpose, styles["lead"]))

    code_total = 0
    code_explained = 0

    for index, (text, label) in enumerate(zip(lines, labels), start=1):

        if label == "blank":
            story.append(Spacer(1, 3))
            continue

        if label == "code":
            code_total += 1

        note = notes.get(index)
        if note and label == "code":
            code_explained += 1

        pieces = [code_line_flowable(index, text, label, styles)]
        if note:
            pieces.append(Paragraph(escape(note), styles["note"]))

        # KeepTogether stops a line being separated from its explanation
        # by a page break, which would make the document painful to read.
        story.append(KeepTogether(pieces))

    coverage[path] = (code_explained, code_total)

    story.append(PageBreak())
    return story


def main():
    styles = build_styles()

    doc = BaseDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        leftMargin=2.1 * cm, rightMargin=2.1 * cm,
        topMargin=2.0 * cm, bottomMargin=1.8 * cm,
        title="Multiclass Fish Image Classification - Line by Line",
        author="Code explanation",
    )

    frame = Frame(
        doc.leftMargin, doc.bottomMargin,
        doc.width, doc.height, id="main",
    )

    def footer(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.6)
        canvas.setFillColor(GREY)
        canvas.drawCentredString(
            A4[0] / 2.0, 1.05 * cm, str(document.page)
        )
        canvas.restoreState()

    doc.addPageTemplates([
        PageTemplate(id="plain", frames=[frame], onPage=footer),
    ])

    story = []

    # ---------------- cover ----------------
    story.append(Spacer(1, 4.6 * cm))
    story.append(Paragraph("Multiclass Fish<br/>Image Classification", styles["title"]))
    story.append(Paragraph(
        "Every line of code, explained", styles["subtitle"]))
    story.append(Spacer(1, 1.1 * cm))
    story.append(Paragraph(
        "This document prints the complete source of the project and attaches a "
        "plain-English note to every line of code. It is meant to be read with the "
        "project open beside it, and to be used for revision before a live "
        "evaluation.",
        styles["body"]))
    story.append(PageBreak())

    # ---------------- how to read ----------------
    story.append(Paragraph("How to read this document", styles["h1"]))
    story.append(Paragraph(
        "Each file gets its own chapter. Inside a chapter the file is printed in full, "
        "exactly as it is on disk, one line at a time. The small grey number on the left "
        "is the real line number, so you can open the file in an editor and jump straight "
        "to it.",
        styles["body"]))
    story.append(Paragraph(
        "Underneath a line of code, in blue, is the explanation of that line.",
        styles["body"]))
    story.append(Paragraph("Two conventions worth knowing:", styles["h2"]))
    story.append(Paragraph(
        "<b>Comment lines are shown in grey and usually carry no separate note.</b> "
        "A comment is already an explanation written in English, so repeating it "
        "underneath would only pad the page. The comments are still printed, because "
        "this document shows the file in full and hides nothing.",
        styles["body"]))
    story.append(Paragraph(
        "<b>Blank lines appear as blank space.</b> They separate ideas and do nothing "
        "when the program runs.",
        styles["body"]))
    story.append(Paragraph(
        "Everything that is actually code — every import, every assignment, every "
        "function call, every <font face='Courier' size='9'>if</font> and "
        "<font face='Courier' size='9'>for</font> — has its own note. The last page "
        "reports what percentage of code lines carry a note, so you can confirm that "
        "for yourself rather than taking this paragraph's word for it.",
        styles["body"]))
    story.append(PageBreak())

    # ---------------- contents ----------------
    story.append(Paragraph("Contents", styles["h1"]))
    for position, path in enumerate(FILES_IN_ORDER, start=1):
        story.append(Paragraph(
            f"{position}. &nbsp;<font face='Courier' size='9.5'>{escape(path)}</font>",
            styles["toc"]))
    story.append(PageBreak())

    # ---------------- the files ----------------
    coverage = {}
    for path in FILES_IN_ORDER:
        story.extend(build_file_section(path, styles, coverage))

    # ---------------- coverage page ----------------
    story.append(Paragraph("Coverage check", styles["h1"]))
    story.append(Paragraph(
        "This page is produced by the program that built this document, by counting "
        "the lines it actually annotated. It is not typed in by hand.",
        styles["body"]))

    rows = [["File", "Code lines", "Explained", "Coverage"]]
    total_code = 0
    total_done = 0
    for path in FILES_IN_ORDER:
        done, total = coverage.get(path, (0, 0))
        total_code += total
        total_done += done
        percent = (100.0 * done / total) if total else 0.0
        rows.append([path, str(total), str(done), f"{percent:.0f}%"])

    overall = (100.0 * total_done / total_code) if total_code else 0.0
    rows.append(["TOTAL", str(total_code), str(total_done), f"{overall:.0f}%"])

    table = Table(rows, colWidths=[7.6 * cm, 2.6 * cm, 2.6 * cm, 2.6 * cm])
    table.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTNAME", (0, 1), (0, -1), "Courier"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.6),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef6")),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#f2f5f9")),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#c9d3e0")),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(table)

    doc.build(story)

    # ---------------- report to the terminal ----------------
    print(f"PDF written: {OUTPUT_PATH}")
    print(f"Size: {os.path.getsize(OUTPUT_PATH) / 1024:.0f} KB\n")
    print(f"{'file':<26} {'code':>6} {'noted':>6} {'cover':>7}")
    for path in FILES_IN_ORDER:
        done, total = coverage.get(path, (0, 0))
        percent = (100.0 * done / total) if total else 0.0
        flag = "" if percent >= 100 else "   <-- incomplete"
        print(f"{path:<26} {total:>6} {done:>6} {percent:>6.0f}%{flag}")
    print(f"{'TOTAL':<26} {total_code:>6} {total_done:>6} {overall:>6.0f}%")


if __name__ == "__main__":
    main()
