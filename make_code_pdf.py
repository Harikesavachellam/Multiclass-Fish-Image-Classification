"""
make_code_pdf.py
----------------
Builds the documentation PDF: every file of this project, every block of
code, with an explanation of what each line does.

Run it with:

    python make_code_pdf.py

It writes:  docs/Multiclass_Fish_Image_Classification_Code_Explained.pdf

How it works:
  - the WORDS (purpose of each file, explanation of each line) live in
    docs/walkthrough_content.py
  - the CODE is read straight out of the real .py files, so the PDF can
    never go out of date with the code
  - reportlab turns the two together into a PDF
"""

import html
import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)

from docs import walkthrough_content as content

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(
    PROJECT_DIR, "docs", "Multiclass_Fish_Image_Classification_Code_Explained.pdf"
)

# Colours used through the document
DARK_BLUE = colors.HexColor("#102A43")
MID_BLUE = colors.HexColor("#1C5D99")
CODE_BACKGROUND = colors.HexColor("#F4F6F8")
CODE_BORDER = colors.HexColor("#CBD2D9")
GREY_TEXT = colors.HexColor("#52606D")


# ----------------------------------------------------------------------
# STYLES
# ----------------------------------------------------------------------


def build_styles():
    """Create every text style the document uses, in one place."""
    base = getSampleStyleSheet()

    styles = {
        "title": ParagraphStyle(
            "title", parent=base["Title"], fontSize=26, leading=32,
            textColor=DARK_BLUE, spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "subtitle", parent=base["Normal"], fontSize=13, leading=18,
            textColor=GREY_TEXT, alignment=1, spaceAfter=6,
        ),
        "h1": ParagraphStyle(
            "h1", parent=base["Heading1"], fontSize=18, leading=23,
            textColor=DARK_BLUE, spaceBefore=4, spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"], fontSize=13, leading=17,
            textColor=MID_BLUE, spaceBefore=12, spaceAfter=5,
        ),
        "body": ParagraphStyle(
            "body", parent=base["BodyText"], fontSize=10, leading=14.5,
            alignment=TA_JUSTIFY, spaceAfter=6,
        ),
        "bullet": ParagraphStyle(
            "bullet", parent=base["BodyText"], fontSize=9.5, leading=13.5,
            leftIndent=12, bulletIndent=3, spaceAfter=3,
        ),
        "code": ParagraphStyle(
            "code", parent=base["Code"], fontName="Courier", fontSize=7.4,
            leading=9.4, textColor=colors.HexColor("#1F2933"),
        ),
        "caption": ParagraphStyle(
            "caption", parent=base["Normal"], fontSize=8.5, leading=11,
            textColor=GREY_TEXT, spaceAfter=3,
        ),
        "toc": ParagraphStyle(
            "toc", parent=base["Normal"], fontSize=10.5, leading=17,
        ),
    }
    return styles


STYLES = build_styles()


# ----------------------------------------------------------------------
# SMALL HELPERS
# ----------------------------------------------------------------------


def safe(text):
    """Escape <, > and & so reportlab does not read them as markup."""
    return html.escape(str(text))


def read_source_lines(relative_path):
    """Read a project file and return its lines, without the newline characters."""
    full_path = os.path.join(PROJECT_DIR, relative_path)
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read().splitlines()


def split_into_blocks(source_lines, block_definitions, relative_path):
    """
    Cut the file into the blocks described in walkthrough_content.py.

    Each block definition has a "start" value: the exact code line that
    begins that block. We find each one in order; a block runs until the
    line where the next block starts.

    Returns a list of (start_line_number, list_of_code_lines, definition).
    """
    stripped = [line.strip() for line in source_lines]

    # Find the line index where each block starts
    start_indexes = []
    search_from = 0

    for definition in block_definitions:
        anchor = definition["start"].strip()
        found = -1

        for index in range(search_from, len(stripped)):
            if stripped[index] == anchor:
                found = index
                break

        if found == -1:
            raise SystemExit(
                f"\nERROR in {relative_path}: could not find this line:\n"
                f"  {anchor}\n"
                f"Fix the 'start' value in docs/walkthrough_content.py."
            )

        start_indexes.append(found)
        search_from = found + 1

    # Turn the start positions into blocks
    blocks = []
    for position, start_index in enumerate(start_indexes):
        if position + 1 < len(start_indexes):
            end_index = start_indexes[position + 1]
        else:
            end_index = len(source_lines)

        blocks.append(
            (start_index + 1, source_lines[start_index:end_index], block_definitions[position])
        )

    return blocks


def code_box(start_line_number, code_lines):
    """
    Build the grey, bordered box that shows numbered code.

    A Table with one cell is used because it is the easiest way to get a
    background colour, a border and padding around a block of text.
    """
    # One table ROW per code line. A table can only be split between rows,
    # so building it this way lets a long block flow onto the next page
    # instead of crashing with "flowable too large".
    rows = []
    for offset, line in enumerate(code_lines):
        line_number = start_line_number + offset
        # Tabs would break the alignment, so turn them into spaces
        clean_line = line.replace("\t", "    ")
        rows.append([Preformatted(f"{line_number:>4} | {clean_line}", STYLES["code"])])

    table = Table(rows, colWidths=[165 * mm], splitByRow=True)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), CODE_BACKGROUND),
                ("BOX", (0, 0), (-1, -1), 0.6, CODE_BORDER),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                # no padding between lines, so the code reads as one block
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                # a little breathing room at the very top and very bottom
                ("TOPPADDING", (0, 0), (0, 0), 5),
                ("BOTTOMPADDING", (0, -1), (0, -1), 5),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def bullets(explanation_lines):
    """Turn a list of strings into bullet points."""
    items = []
    for text in explanation_lines:
        items.append(Paragraph(safe(text), STYLES["bullet"], bulletText="•"))
    return items


# ----------------------------------------------------------------------
# PAGE DECORATION (the little header and the page number)
# ----------------------------------------------------------------------


def draw_page_furniture(canvas, document):
    """Called by reportlab for every page. Draws the header and footer."""
    canvas.saveState()

    page_width, page_height = A4

    # Header line (not on the cover page)
    if document.page > 1:
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GREY_TEXT)
        canvas.drawString(20 * mm, page_height - 12 * mm,
                          "Multiclass Fish Image Classification - Code Explained")
        canvas.setStrokeColor(CODE_BORDER)
        canvas.setLineWidth(0.5)
        canvas.line(20 * mm, page_height - 14 * mm, page_width - 20 * mm, page_height - 14 * mm)

    # Page number on every page except the cover
    if document.page > 1:
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(GREY_TEXT)
        canvas.drawCentredString(page_width / 2, 10 * mm, f"Page {document.page}")

    canvas.restoreState()


# ----------------------------------------------------------------------
# BUILDING THE STORY (the list of things to put on the pages)
# ----------------------------------------------------------------------


def build_cover():
    """The first page."""
    story = [
        Spacer(1, 55 * mm),
        Paragraph(safe(content.DOCUMENT_TITLE), STYLES["title"]),
        Paragraph(safe(content.DOCUMENT_SUBTITLE), STYLES["subtitle"]),
        Spacer(1, 8 * mm),
    ]

    rows = [[key, value] for key, value in content.COVER_FACTS]
    table = Table(rows, colWidths=[45 * mm, 110 * mm])
    table.setStyle(
        TableStyle(
            [
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9.5),
                ("TEXTCOLOR", (0, 0), (0, -1), DARK_BLUE),
                ("TEXTCOLOR", (1, 0), (1, -1), GREY_TEXT),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("LINEBELOW", (0, 0), (-1, -2), 0.4, CODE_BORDER),
            ]
        )
    )
    story.append(table)
    story.append(PageBreak())
    return story


def build_contents_page():
    """A simple numbered list of the chapters."""
    story = [Paragraph("Contents", STYLES["h1"]), Spacer(1, 3 * mm)]

    number = 1
    for heading, _paragraphs in content.INTRO_SECTIONS:
        story.append(Paragraph(f"{number}. &nbsp;{safe(heading)}", STYLES["toc"]))
        number += 1

    for file_entry in content.FILES:
        story.append(
            Paragraph(f"{number}. &nbsp;{safe(file_entry['path'])}", STYLES["toc"])
        )
        number += 1

    for heading, _paragraphs in content.CLOSING_SECTIONS:
        story.append(Paragraph(f"{number}. &nbsp;{safe(heading)}", STYLES["toc"]))
        number += 1

    story.append(PageBreak())
    return story


def build_text_sections(sections, start_number):
    """Build the plain-text chapters (introduction, checklist, and so on)."""
    story = []
    number = start_number

    for heading, paragraphs in sections:
        story.append(Paragraph(f"{number}. {safe(heading)}", STYLES["h1"]))

        for paragraph in paragraphs:
            if isinstance(paragraph, list):
                # a list inside the chapter becomes bullet points
                story.extend(bullets(paragraph))
            elif isinstance(paragraph, tuple):
                # a tuple becomes a sub-heading
                story.append(Paragraph(safe(paragraph[0]), STYLES["h2"]))
            else:
                story.append(Paragraph(safe(paragraph), STYLES["body"]))

        story.append(PageBreak())
        number += 1

    return story, number


def build_file_chapter(file_entry, chapter_number):
    """Build one chapter: one source file, block by block."""
    relative_path = file_entry["path"]
    source_lines = read_source_lines(relative_path)

    story = [
        Paragraph(f"{chapter_number}. {safe(relative_path)}", STYLES["h1"]),
        Paragraph(
            f"{len(source_lines)} lines &nbsp;|&nbsp; {safe(file_entry['role'])}",
            STYLES["caption"],
        ),
        Paragraph(safe(file_entry["purpose"]), STYLES["body"]),
    ]

    blocks = split_into_blocks(source_lines, file_entry["blocks"], relative_path)

    for start_line_number, code_lines, definition in blocks:
        last_line_number = start_line_number + len(code_lines) - 1

        story.append(
            Paragraph(
                f"{safe(definition['title'])} "
                f"<font color='#7B8794' size='9'>"
                f"(lines {start_line_number}-{last_line_number})</font>",
                STYLES["h2"],
            )
        )
        story.append(code_box(start_line_number, code_lines))
        story.append(Spacer(1, 3 * mm))
        story.append(Paragraph("<b>Line by line</b>", STYLES["caption"]))
        story.extend(bullets(definition["explain"]))
        story.append(Spacer(1, 3 * mm))

    story.append(PageBreak())
    return story


def build_story():
    """Put the whole document together, in order."""
    story = []
    story.extend(build_cover())
    story.extend(build_contents_page())

    intro_story, next_number = build_text_sections(content.INTRO_SECTIONS, 1)
    story.extend(intro_story)

    for file_entry in content.FILES:
        story.extend(build_file_chapter(file_entry, next_number))
        next_number += 1

    closing_story, _ = build_text_sections(content.CLOSING_SECTIONS, next_number)
    story.extend(closing_story)

    return story


def main():
    os.makedirs(os.path.join(PROJECT_DIR, "docs"), exist_ok=True)

    document = BaseDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        title=content.DOCUMENT_TITLE,
        author=content.DOCUMENT_AUTHOR,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=20 * mm,
        bottomMargin=18 * mm,
    )

    # A frame is the rectangle on the page that the text flows into
    frame = Frame(
        document.leftMargin,
        document.bottomMargin,
        document.width,
        document.height,
        id="main",
    )

    document.addPageTemplates(
        [PageTemplate(id="all", frames=[frame], onPage=draw_page_furniture)]
    )

    document.build(build_story())

    size_kb = os.path.getsize(OUTPUT_PATH) / 1024
    print(f"PDF written: {OUTPUT_PATH}")
    print(f"Size: {size_kb:.0f} KB")


if __name__ == "__main__":
    # Make sure we can import the docs package no matter where we run from
    sys.path.insert(0, PROJECT_DIR)
    main()
