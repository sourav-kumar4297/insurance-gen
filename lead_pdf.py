import random
from datetime import datetime, timedelta
from pathlib import Path

import fitz

from config import (
    FONT_BOLD_PATH,
    FONT_REGULAR_PATH,
    FORM_NAME,
    SITE_NAME,
    SITE_URL,
)

PAGE_WIDTH = 841.92
PAGE_HEIGHT = 594.96
MARGIN_LEFT = 39.75
MARGIN_RIGHT = 39.75
HEADER_TOP = 39.75
HEADER_BOTTOM = 96.75
TABLE_HEADER_Y = 127.5
TABLE_HEADER_HEIGHT = 22.5
FIRST_ROW_Y = 171.0
ROW_HEIGHT = 21.0
ROW_STRIDE = 21.0
FOOTER_GAP = 18.0
PAGE_NUMBER_Y = PAGE_HEIGHT - 24

COL_BOUNDS = [40.5, 74.25, 276.0, 423.75, 505.5, 591.75, 801.75]
COLUMNS = ["#", "FORM NAME", "SUBMITTED ON", "FIRST NAME", "LAST NAME", "EMAIL"]

COLOR_HEADER_BG = (0.110, 0.090, 0.078)
COLOR_TITLE = (0.980, 0.976, 0.969)
COLOR_SUBTITLE = (0.788, 0.753, 0.710)
COLOR_META = (0.110, 0.090, 0.078)
COLOR_HEADER_TEXT = (1.0, 1.0, 1.0)
COLOR_ROW_NUM = (0.533, 0.533, 0.533)
COLOR_CELL_TEXT = (0.102, 0.102, 0.102)
COLOR_ROW_ALT = (0.980, 0.980, 0.973)
COLOR_ROW_BASE = (1.0, 1.0, 1.0)
COLOR_BORDER = (0.910, 0.894, 0.875)
COLOR_FOOTER = (0.557, 0.557, 0.557)
COLOR_PAGE_NUM = (0.557, 0.557, 0.557)

FONT_REGULAR = "SegoeUI"
FONT_BOLD = "SegoeUIBold"
FONT_SEMIBOLD = "SegoeUISemibold"


def format_submitted_on(dt):
    hour = dt.strftime("%I").lstrip("0") or "12"
    return dt.strftime(f"%B %d, %Y {hour}:%M:%S %p")


def format_generated_on(day):
    return day.strftime("%-d %B %Y") if False else day.strftime("%d %B %Y").lstrip("0")


def random_submission_times(count, start_date, end_date):
    days = []
    current = start_date
    while current <= end_date:
        days.append(current)
        current += timedelta(days=1)

    day_picks = []
    if count <= len(days):
        if count == 1:
            day_picks = [start_date]
        else:
            for i in range(count):
                idx = round(i * (len(days) - 1) / (count - 1))
                day_picks.append(days[idx])
    else:
        base, extra = divmod(count, len(days))
        for i, day in enumerate(days):
            day_picks.extend([day] * (base + (1 if i < extra else 0)))

    times = []
    used = set()
    for day in day_picks:
        day_start = datetime.combine(day, datetime.min.time()).replace(hour=9, minute=0, second=0)
        day_end = datetime.combine(day, datetime.min.time()).replace(hour=17, minute=30, second=0)
        total_seconds = int((day_end - day_start).total_seconds())
        for _ in range(40):
            offset = random.randint(0, total_seconds)
            candidate = day_start + timedelta(seconds=offset)
            key = candidate.strftime("%Y%m%d%H%M%S")
            if key not in used:
                used.add(key)
                times.append(candidate)
                break
        else:
            times.append(day_start + timedelta(minutes=len(times) * 7))

    return sorted(times)


def paginate_rows(rows, first_page_capacity=19, next_page_capacity=24):
    pages = []
    remaining = rows[:]
    if remaining:
        pages.append(remaining[:first_page_capacity])
        remaining = remaining[first_page_capacity:]
    while remaining:
        pages.append(remaining[:next_page_capacity])
        remaining = remaining[next_page_capacity:]
    return pages


def register_fonts(page):
    page.insert_font(fontname=FONT_REGULAR, fontfile=FONT_REGULAR_PATH)
    page.insert_font(fontname=FONT_BOLD, fontfile=FONT_BOLD_PATH)
    page.insert_font(fontname=FONT_SEMIBOLD, fontfile=FONT_BOLD_PATH)


def draw_header_banner(page, generated_on):
    page.draw_rect(
        fitz.Rect(MARGIN_LEFT, HEADER_TOP, PAGE_WIDTH - MARGIN_RIGHT, HEADER_BOTTOM),
        color=None,
        fill=COLOR_HEADER_BG,
    )
    page.insert_text(
        fitz.Point(52, 62),
        "Website Visit — Consultation Request",
        fontname=FONT_SEMIBOLD,
        fontsize=14,
        color=COLOR_TITLE,
    )
    page.insert_text(
        fitz.Point(52, 82),
        f"{SITE_NAME} form submissions export · Generated {generated_on}",
        fontname=FONT_REGULAR,
        fontsize=8.5,
        color=COLOR_SUBTITLE,
    )


def draw_meta_line(page, num_rows, start_date, end_date):
    y = 115
    segments = [
        (f"Total submissions: {num_rows}", 52),
        (
            f"Date range: {start_date.strftime('%B %d, %Y')} — {end_date.strftime('%B %d, %Y')}",
            170,
        ),
        (f"Source: {SITE_URL.replace('https://', '')}", 430),
    ]
    for text, x in segments:
        page.insert_text(
            fitz.Point(x, y),
            text,
            fontname=FONT_BOLD,
            fontsize=8.5,
            color=COLOR_META,
        )


def draw_table_header(page, y, height=TABLE_HEADER_HEIGHT):
    for idx in range(len(COLUMNS)):
        x0, x1 = COL_BOUNDS[idx], COL_BOUNDS[idx + 1]
        page.draw_rect(fitz.Rect(x0, y, x1, y + height), color=None, fill=COLOR_HEADER_BG)
        text = COLUMNS[idx]
        text_x = x0 + 6 if idx > 0 else x0 + 10
        page.insert_text(
            fitz.Point(text_x, y + height - 8),
            text,
            fontname=FONT_BOLD,
            fontsize=8,
            color=COLOR_HEADER_TEXT,
        )


def draw_cell_borders(page, x0, y0, x1, y1):
    border = COLOR_BORDER
    page.draw_line(fitz.Point(x0, y0), fitz.Point(x1, y0), color=border, width=0.6)
    page.draw_line(fitz.Point(x0, y1), fitz.Point(x1, y1), color=border, width=0.6)
    page.draw_line(fitz.Point(x0, y0), fitz.Point(x0, y1), color=border, width=0.6)
    page.draw_line(fitz.Point(x1, y0), fitz.Point(x1, y1), color=border, width=0.6)


def draw_row(page, y, row_index, row):
    bg = COLOR_ROW_ALT if row_index % 2 == 0 else COLOR_ROW_BASE
    values = [
        str(row["index"]),
        FORM_NAME,
        format_submitted_on(row["submitted_on"]),
        row["first_name"],
        row["last_name"],
        row["email"],
    ]
    for col_idx, value in enumerate(values):
        x0, x1 = COL_BOUNDS[col_idx], COL_BOUNDS[col_idx + 1]
        page.draw_rect(fitz.Rect(x0, y, x1, y + ROW_HEIGHT), color=None, fill=bg)
        draw_cell_borders(page, x0, y, x1, y + ROW_HEIGHT)
        color = COLOR_ROW_NUM if col_idx == 0 else COLOR_CELL_TEXT
        text_x = x0 + 10 if col_idx == 0 else x0 + 6
        page.insert_text(
            fitz.Point(text_x, y + 14),
            value,
            fontname=FONT_REGULAR,
            fontsize=8.5,
            color=color,
        )


def draw_page_number(page, current, total):
    text = f"-- {current} of {total} --"
    page.insert_text(
        fitz.Point(PAGE_WIDTH / 2 - 35, PAGE_NUMBER_Y),
        text,
        fontname=FONT_REGULAR,
        fontsize=8,
        color=COLOR_PAGE_NUM,
    )


def draw_footer(page, y, generated_on):
    left = f"{SITE_NAME} form submissions"
    right = f"Website visit export · {generated_on}"
    page.insert_text(
        fitz.Point(52, y),
        left,
        fontname=FONT_REGULAR,
        fontsize=8,
        color=COLOR_FOOTER,
    )
    page.insert_text(
        fitz.Point(620, y),
        right,
        fontname=FONT_REGULAR,
        fontsize=8,
        color=COLOR_FOOTER,
    )


def build_pdf(rows, output_path, start_date, end_date, generated_on):
    pages_of_rows = paginate_rows(rows)
    total_pages = len(pages_of_rows)
    doc = fitz.open()
    num_rows = len(rows)

    for page_num, page_rows in enumerate(pages_of_rows, start=1):
        page = doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        register_fonts(page)

        if page_num == 1:
            draw_header_banner(page, generated_on)
            draw_meta_line(page, num_rows, start_date, end_date)
            draw_table_header(page, TABLE_HEADER_Y)
            y = FIRST_ROW_Y
        else:
            continuation_header_y = 39.75
            draw_table_header(page, continuation_header_y)
            y = continuation_header_y + TABLE_HEADER_HEIGHT + 8

        for idx, row in enumerate(page_rows):
            draw_row(page, y, idx, row)
            y += ROW_STRIDE

        draw_page_number(page, page_num, total_pages)
        if page_num == total_pages:
            draw_footer(page, y + FOOTER_GAP, generated_on)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    doc.save(output_path)
    doc.close()
    return output_path
