#!/usr/bin/env python3
"""Generate the publications page from the canonical BibTeX file.

Only Python's standard library is used, so maintaining the publication list
does not require a project-specific Python environment.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BIB = ROOT / "publications.bib"
DEFAULT_OUTPUT = ROOT / "content" / "publications.md"

TYPE_ORDER = {
    "book": 0,
    "incollection": 0,
    "article": 1,
    "inproceedings": 2,
    "patent": 3,
    "misc": 3,
}

COLOR_SQUARE = {
    "book": "<span class='publication-marker' style='color:rgb(255, 213, 0)' aria-hidden='true'>&#9724;</span>",
    "incollection": "<span class='publication-marker' style='color:rgb(255, 213, 0)' aria-hidden='true'>&#9724;</span>",
    "article": "<span class='publication-marker' style='color:rgb(195, 43, 114)' aria-hidden='true'>&#9724;</span>",
    "inproceedings": "<span class='publication-marker' style='color:rgb(25, 108, 163)' aria-hidden='true'>&#9724;</span>",
    "patent": "<span class='publication-marker' style='color:rgb(136, 85, 34)' aria-hidden='true'>&#9724;</span>",
    "misc": "<span class='publication-marker' style='color:rgb(136, 85, 34)' aria-hidden='true'>&#9724;</span>",
}

PUBLICATION_TYPES = {
    "article": ("journal", "Journal articles"),
    "inproceedings": ("conference", "Conference papers"),
    "book": ("book", "Books and chapters"),
    "incollection": ("book", "Books and chapters"),
    "patent": ("patent", "Patents"),
    "misc": ("other", "Other"),
}

PUBLICATION_TYPE_ORDER = ("journal", "conference", "book", "patent", "other")

ACCENTS = {
    '"': "\u0308",
    "'": "\u0301",
    "`": "\u0300",
    "^": "\u0302",
    "~": "\u0303",
    "=": "\u0304",
    ".": "\u0307",
    "c": "\u0327",
    "v": "\u030c",
    "u": "\u0306",
    "H": "\u030b",
}


@dataclass(frozen=True)
class Entry:
    entry_type: str
    key: str
    fields: dict[str, str]
    raw: str
    position: int


def find_closing(text: str, start: int, opening: str, closing: str) -> int:
    depth = 0
    quoted = False
    escaped = False
    for index in range(start, len(text)):
        char = text[index]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            quoted = not quoted
            continue
        if quoted:
            continue
        if char == opening:
            depth += 1
        elif char == closing:
            depth -= 1
            if depth == 0:
                return index
    raise ValueError(f"Unclosed BibTeX entry starting at character {start}")


def split_entry_body(body: str) -> tuple[str, str]:
    depth = 0
    quoted = False
    escaped = False
    for index, char in enumerate(body):
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == '"':
            quoted = not quoted
        elif not quoted and char == "{":
            depth += 1
        elif not quoted and char == "}":
            depth -= 1
        elif not quoted and depth == 0 and char == ",":
            return body[:index].strip(), body[index + 1 :]
    raise ValueError("A BibTeX entry is missing the comma after its citation key")


def parse_fields(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    index = 0
    while index < len(text):
        while index < len(text) and (text[index].isspace() or text[index] == ","):
            index += 1
        if index >= len(text):
            break

        name_match = re.match(r"[A-Za-z][A-Za-z0-9_-]*", text[index:])
        if not name_match:
            raise ValueError(f"Invalid field near: {text[index:index + 30]!r}")
        name = name_match.group(0).lower()
        index += len(name_match.group(0))
        while index < len(text) and text[index].isspace():
            index += 1
        if index >= len(text) or text[index] != "=":
            raise ValueError(f"Field {name!r} is missing '='")
        index += 1
        while index < len(text) and text[index].isspace():
            index += 1
        if index >= len(text):
            raise ValueError(f"Field {name!r} has no value")

        if text[index] == "{":
            end = find_closing(text, index, "{", "}")
            value = text[index + 1 : end]
            index = end + 1
        elif text[index] == '"':
            end = index + 1
            escaped = False
            while end < len(text):
                if text[end] == '"' and not escaped:
                    break
                escaped = text[end] == "\\" and not escaped
                if text[end] != "\\":
                    escaped = False
                end += 1
            if end >= len(text):
                raise ValueError(f"Unclosed quoted value for field {name!r}")
            value = text[index + 1 : end]
            index = end + 1
        else:
            end = text.find(",", index)
            if end == -1:
                end = len(text)
            value = text[index:end].strip()
            index = end
        fields[name] = value.strip()
    return fields


def parse_bibtex(text: str) -> list[Entry]:
    entries: list[Entry] = []
    index = 0
    while True:
        start = text.find("@", index)
        if start == -1:
            break
        type_match = re.match(r"@([A-Za-z]+)\s*([({])", text[start:])
        if not type_match:
            raise ValueError(f"Invalid BibTeX entry near character {start}")
        entry_type = type_match.group(1).lower()
        opening = type_match.group(2)
        closing = "}" if opening == "{" else ")"
        open_index = start + type_match.end() - 1
        end = find_closing(text, open_index, opening, closing)
        raw = text[start : end + 1].strip()
        index = end + 1
        if entry_type in {"comment", "preamble", "string"}:
            continue
        key, field_text = split_entry_body(text[open_index + 1 : end])
        if not key:
            raise ValueError(f"Entry near character {start} has no citation key")
        entries.append(Entry(entry_type, key, parse_fields(field_text), raw, len(entries)))

    if not entries:
        raise ValueError("No publication entries were found")
    seen: set[str] = set()
    duplicates: set[str] = set()
    for entry in entries:
        if entry.key in seen:
            duplicates.add(entry.key)
        seen.add(entry.key)
    if duplicates:
        raise ValueError(f"Duplicate citation keys: {', '.join(sorted(duplicates))}")
    return entries


def plain_text(value: str) -> str:
    value = value.strip()
    while len(value) >= 2 and value[0] == "{" and value[-1] == "}":
        value = value[1:-1].strip()
    value = value.replace("~", " ").replace(r"\&", "&")
    accent_pattern = re.compile(r"\\([\"'`^~=\.cvuH])\s*\{?([A-Za-z])\}?")

    def replace_accent(match: re.Match[str]) -> str:
        return unicodedata.normalize("NFC", match.group(2) + ACCENTS[match.group(1)])

    value = accent_pattern.sub(replace_accent, value)
    value = re.sub(r"\\(?:textit|emph|textbf)\s*\{([^{}]*)\}", r"\1", value)
    value = value.replace(r"\ss", "ß").replace(r"\ae", "æ").replace(r"\AE", "Æ")
    value = value.replace(r"\o", "ø").replace(r"\O", "Ø").replace(r"\l", "ł").replace(r"\L", "Ł")
    return value.replace("{", "").replace("}", "")


def format_author(name: str) -> str:
    parts = name.replace("~", " ").split(",")
    if len(parts) == 2:
        last, first = parts
    else:
        words = parts[0].split()
        if not words:
            return ""
        last = words[-1]
        first = " ".join(words[:-1])
    initials = "&nbsp;".join(f"{word[0]}." for word in first.split() if word)
    return f"{initials}{'&nbsp;' if initials else ''}{plain_text(last.strip())}"


def format_authors(raw: str) -> str:
    names = re.split(r"\s+and\s+", raw.replace("\n", " "))
    authors = [format_author(name.strip()) for name in names]
    return ", ".join(author for author in authors if author).replace("†", "<sup>&dagger;</sup>").replace("‡", "<sup>&Dagger;</sup>")


def author_names(raw: str) -> list[str]:
    names: list[str] = []
    for name in re.split(r"\s+and\s+", raw.replace("\n", " ")):
        display_name = html.unescape(format_author(name.strip()).replace("&nbsp;", " "))
        display_name = display_name.replace("†", "").replace("‡", "").strip()
        if display_name:
            names.append(display_name)
    return names


def publication_type(entry_type: str) -> tuple[str, str]:
    return PUBLICATION_TYPES.get(entry_type, ("other", "Other"))


def publication_info(entry: Entry) -> str:
    fields = entry.fields
    info = html.escape(plain_text(fields.get("journal", "") or fields.get("booktitle", "")))
    if fields.get("volume"):
        info += f", Volume {html.escape(plain_text(fields['volume']))}"
    if fields.get("number"):
        info += (", " if info else "") + f"Number {html.escape(plain_text(fields['number']))}"
    if fields.get("pages"):
        info += f", pp. {html.escape(plain_text(fields['pages']))}"
    if not info:
        info = "Preprint"
    year = plain_text(fields.get("year", ""))
    if year and year not in info:
        info += f", {year}"
    note = plain_text(fields.get("note", ""))
    if note:
        info += f"<br /><strong>{html.escape(note)}</strong>"
    return info


def title_markup(entry: Entry) -> str:
    title = html.escape(plain_text(entry.fields.get("title", "Untitled")))
    return f"<cite>{title}</cite>"


def links_markup(entry: Entry) -> str:
    fields = entry.fields
    links: list[str] = []
    eprint = plain_text(fields.get("eprint", ""))
    doi = plain_text(fields.get("doi", ""))
    file_path = plain_text(fields.get("file", ""))
    if eprint and "arxiv" in plain_text(fields.get("eprinttype", "arxiv")).lower():
        links.append(f'<a href="https://arxiv.org/abs/{html.escape(eprint, quote=True)}">Preprint</a>')
    if doi:
        target = doi if doi.startswith(("http://", "https://")) else f"https://doi.org/{doi}"
        links.append(f'<small><a href="{html.escape(target, quote=True)}">DOI</a></small>')
    if file_path:
        links.append(
            f'<a href="{html.escape(file_path, quote=True)}" target="_blank" rel="noopener" title="Author\'s copy">'
            '<img src="/icons/pdf.svg" alt="PDF" width="22" height="22" />'
            "</a>"
        )
    # insert whitespace before and after the bullet to avoid it being too close to the links
    link_separator = ' <small>&bull;</small> '

    inline_links = f'<span class="publication-links">{link_separator.join(links)}</span>' if links else ""
    safe_id = re.sub(r"[^A-Za-z0-9_:.]", "_", entry.key)
    bibtex = html.escape(entry.raw)
    bibtex_control = f'''<img src="/icons/bibtex.svg" alt="BibTeX"
        style="width:48px; vertical-align:middle; cursor:pointer;"
        onclick="var x=document.getElementById('{safe_id}');
                if(x.style.display==='none'){{x.style.display='block';}}
                else{{x.style.display='none';}}"
        title="Show BibTeX" />'''
    bibtex_panel = f'''<pre id="{safe_id}" style="display:none; padding:2px; border:1px solid #ccc;
        background:#f9f9f9; white-space:pre-wrap; overflow-x:auto; margin-top:4px;">{bibtex}</pre>'''
    separator = link_separator if links else ""
    return f'<div class="publication-actions">{inline_links}{separator}{bibtex_control}</div>{bibtex_panel}'


def render(entries: list[Entry]) -> str:
    def year(entry: Entry) -> int:
        match = re.search(r"\d{4}", plain_text(entry.fields.get("year", "")))
        return int(match.group(0)) if match else -1

    ordered = sorted(
        entries,
        key=lambda entry: (
            -year(entry),
            TYPE_ORDER.get(entry.entry_type, 4),
            plain_text(entry.fields.get("title", "")).casefold(),
            entry.position,
        ),
    )
    years = sorted({year(entry) for entry in ordered}, reverse=True)
    available_types = {publication_type(entry.entry_type)[0] for entry in ordered}
    type_labels = {key: label for key, label in PUBLICATION_TYPES.values()}

    year_buttons = "".join(
        f'<button type="button" data-filter-year="{entry_year}" aria-pressed="false">{entry_year if entry_year >= 0 else "Unknown"}</button>'
        for entry_year in years
    )
    type_buttons = "".join(
        f'<button type="button" data-filter-type="{type_key}" aria-pressed="false">{type_labels[type_key]}</button>'
        for type_key in PUBLICATION_TYPE_ORDER
        if type_key in available_types
    )
    lines: list[str] = [
        "---",
        'title: "Publications"',
        'description: "Publications by the AIBEX research group in artificial intelligence, pattern recognition, document analysis, and related fields."',
        "---",
        "",
        "# Publications",
        "",
        '<div class="publication-explorer">',
        '  <form class="publication-filters" role="search">',
        '    <label class="publication-search">Search<input type="search" name="query" placeholder="Title, author, or venue" autocomplete="off"></label>',
        '    <fieldset class="publication-filter-group"><legend>Year</legend>',
        f'      <div class="publication-filter-buttons"><button type="button" data-filter-year="" aria-pressed="true">All years</button>{year_buttons}</div>',
        '    </fieldset>',
        '    <fieldset class="publication-filter-group"><legend>Publication type</legend>',
        f'      <div class="publication-filter-buttons"><button type="button" data-filter-type="" aria-pressed="true">All types</button>{type_buttons}</div>',
        '    </fieldset>',
        '    <button class="publication-clear" type="button">Clear filters</button>',
        "  </form>",
        f'  <p class="publication-count" aria-live="polite">{len(ordered)} publications</p>',
        '  <div class="publication-list">',
    ]
    current_year: int | None = None
    for entry in ordered:
        entry_year = year(entry)
        if entry_year != current_year:
            if current_year is not None:
                lines.append("  </section>")
            year_label = entry_year if entry_year >= 0 else "Unknown"
            lines.extend(
                (
                    f'  <section class="publication-year" data-year="{entry_year}">',
                    f"    <h2>{year_label}</h2>",
                )
            )
            current_year = entry_year
        color = COLOR_SQUARE.get(entry.entry_type, COLOR_SQUARE["misc"])
        type_key, _ = publication_type(entry.entry_type)
        names = author_names(entry.fields.get("author", ""))
        data_authors = html.escape("||".join(names), quote=True)
        search_text = " ".join(
            (
                plain_text(entry.fields.get("title", "")),
                " ".join(names),
                plain_text(entry.fields.get("journal", "") or entry.fields.get("booktitle", "")),
            )
        )
        data_search = html.escape(" ".join(search_text.split()), quote=True)
        lines.extend(
            (
                f'    <article class="publication-entry" data-year="{entry_year}" data-type="{type_key}" data-authors="{data_authors}" data-search="{data_search}">',
                f'      <div class="publication-title-row">{color}{title_markup(entry)}</div>',
                f'      <div class="publication-authors">{format_authors(entry.fields.get("author", ""))}</div>',
                f'      <div class="publication-venue">{publication_info(entry)}</div>',
                f"      {links_markup(entry)}",
                "    </article>",
            )
        )
    if current_year is not None:
        lines.append("  </section>")
    lines.extend(
        (
            "  </div>",
            "</div>",
            '<script src="/js/publications.js" defer></script>',
        )
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the Hugo publication list from one BibTeX file.")
    parser.add_argument("--bib", type=Path, default=DEFAULT_BIB, help="canonical BibTeX file")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="generated Markdown file")
    parser.add_argument("--check", action="store_true", help="fail if generated Markdown is out of date")
    args = parser.parse_args()
    try:
        entries = parse_bibtex(args.bib.read_text(encoding="utf-8"))
        generated = render(entries)
    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if args.check:
        try:
            current = args.output.read_text(encoding="utf-8")
        except FileNotFoundError:
            current = ""
        if current != generated:
            print(f"{args.output} is out of date. Run: python3 scripts/generate_publications.py", file=sys.stderr)
            return 1
        print(f"Publication page is up to date ({len(entries)} entries).")
        return 0

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(generated, encoding="utf-8")
    print(f"Wrote {len(entries)} publications to {args.output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
