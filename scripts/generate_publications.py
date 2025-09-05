import os
import bibtexparser
from collections import defaultdict
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode

color_square = {"book": "<span style='color:rgb(255, 213, 0)'>&#9724;</span>", 
              "incollection": "<span style='color:rgb(255, 213, 0)'>&#9724;</span>",
               "article": "<span style='color:rgb(195, 43, 114)'>&#9724;</span>", 
               "inproceedings": "<span style='color:rgb(25, 108, 163)'>&#9724;</span>", 
               "patent": "<span style='color:rgb(136, 85, 34)'>&#9724;</span>", 
               "misc": "<span style='color:rgb(136, 85, 34)'>&#9724;</span>"}

# --- Helper functions ---

def format_author(name):
    parts = name.replace("~", " ").split(",")
    print(name, parts)
    if len(parts) == 2:
        last, first = parts
    else:
        first_last = parts[0].split()
        last = first_last[-1]
        first = " ".join(first_last[:-1])
    initials = "&nbsp;".join([f[0] + "." if len(f) > 0 else "" for f in first.split()])
    return f"{initials}&nbsp;{last.strip()}"

def format_authors(authors_raw):
    authors_raw = authors_raw.replace(" and ", ", ")
    authors = [format_author(name.strip()) for name in authors_raw.replace("\n", " ").split(",") if name]
    formatted = ", ".join(authors)
    formatted = formatted.replace("†", "<sup>&dagger;</sup>").replace("‡", "<sup>&Dagger;</sup>")
    return formatted

def entry_link(title, url):
    return f"[*{title}*]({url})"

def get_publication_info(entry):
    info = ""
    if entry.get("journal"):
        info = f"{entry['journal']}"
    if entry.get("booktitle"):
        info = f"{entry['booktitle']}"

    if "volume" in entry:
        info += f", Volume {entry['volume']}"
    if "number" in entry:
        if info:
            info += ", "
        info += f"Number {entry['number']}"
    if "pages" in entry:
        info += f", pp. {entry['pages']}"

    if not info:
        info = "Preprint"
    year = entry.get("year", "")

    out = f"{info}, {year}" if year not in info else info
    if not entry.get("note", None):
        return out 
    else:
        return out + "<br />" + f"**{entry.get('note')}**"


bib_dir = "static/research"

def get_links(entry, filename):
    links = []
    if "eprint" in entry and "arxiv" in entry.get("eprinttype", "arxiv").lower():
        links.append(f'[\[Preprint\]](https://arxiv.org/abs/{entry["eprint"]})')
    if "doi" in entry:
        links.append(f'[\[DOI\]](https://dx.doi.org/{entry["doi"]})')
    if "file" in entry:
        # Use PDF SVG icon
        pdf_icon_path = "/icons/pdf.svg"  # relative path to your Hugo static folder
        links.append(
            f'<a href="{entry["file"]}" target="_blank" title="Author\'s copy">'
            f'<img src="{pdf_icon_path}" alt="PDF" style="width:16px; height:16px; vertical-align:middle;" />'
            f'</a>'
        )

    # Inline links (optional <small>)
    links_html = f'<small>{" &bull; ".join(links)}</small>' if links else ""

    # Read BibTeX file content
    bib_path = os.path.join(bib_dir, filename)
    if os.path.exists(bib_path):
        with open(bib_path, "r", encoding="utf-8") as f:
            bibtex_content = f.read().replace("<", "&lt;").replace(">", "&gt;")
    else:
        bibtex_content = "BibTeX not found"

    # Collapsible BibTeX
    sanitized_id = entry['ID'].replace(" ", "_").replace("-", "_")
    bibtex_icon_path = "/icons/bibtex.svg"  # relative path to your Hugo static folder
    bibtex_html = f'''<img src="{bibtex_icon_path}" alt="BibTeX"
        style="width:48px; vertical-align:middle; cursor:pointer;"
        onclick="var x=document.getElementById('{sanitized_id}');
                if(x.style.display==='none'){{x.style.display='block';}}
                else{{x.style.display='none';}}"
        title="Show BibTeX" />
    <pre id="{sanitized_id}" style="display:none; padding:2px; border:1px solid #ccc;
        background:#f9f9f9; white-space: pre-wrap; overflow-x:auto; margin-top:4px;">{bibtex_content}</pre>'''





    return f'{links_html} {bibtex_html}'


# # --- Process a single bib file ---
# def process_bib_file(filepath):
#     with open(filepath, "r", encoding="utf-8") as bibfile:
#         parser = BibTexParser(common_strings=True)
#         parser.customization = convert_to_unicode
#         bib_database = bibtexparser.load(bibfile, parser=parser)

#     entries_by_year = defaultdict(list)
#     # Ordering: books -> journals -> conferences -> patents/misc
#     type_order = {"book": 0, "incollection": 0, "article": 1, "inproceedings": 2, "patent": 3, "misc": 4}

#     for entry in bib_database.entries:
#         title = entry.get("title", "").strip("{}")
#         authors = format_authors(entry.get("author", ""))
#         pub_info = get_publication_info(entry)
#         bib_filename = os.path.basename(filepath)
#         links = get_links(entry, bib_filename)

#         # Title with possible link
#         if "doi" in entry:
#             title_line = entry_link(title, f"https://dx.doi.org/{entry['doi']}")
#         elif "url" in entry:
#             title_line = entry_link(title, entry["url"])
#         elif "eprint" in entry:
#             title_line = entry_link(title, f"https://arxiv.org/abs/{entry['eprint']}")
#         else:
#             title_line = f"*{title}*"

#         md_entry = {
#             "md": f"- {entry.get('ENTRYTYPE')} {title_line}<br />\n{authors}<br />\n{pub_info}<br />\n        <small>{links}</small>",
#             "type_order": type_order.get(entry.get("ENTRYTYPE", "misc").lower(), 4)
#         }

#         year = entry.get("year", "Unknown")
#         entries_by_year[year].append(md_entry)

#     # Sort entries per year by type_order
#     for year in entries_by_year:
#         entries_by_year[year] = [e["md"] for e in sorted(entries_by_year[year], key=lambda x: x["type_order"])]

#     return entries_by_year

def generate_markdown_list(directory):
    all_entries_by_year = defaultdict(list)
    type_order = {"book": 0, "incollection": 0, "article": 1, "inproceedings": 2, "patent": 3, "misc": 3}

    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".bib"):
            filepath = os.path.join(directory, filename)
            with open(filepath, "r", encoding="utf-8") as bibfile:
                parser = BibTexParser(common_strings=True)
                parser.customization = convert_to_unicode
                bib_database = bibtexparser.load(bibfile, parser=parser)

            for entry in bib_database.entries:
                title = entry.get("title", "").strip("{}")
                authors = format_authors(entry.get("author", ""))
                pub_info = get_publication_info(entry)
                bib_filename = os.path.basename(filepath)
                links = get_links(entry, bib_filename)

                if "doi" in entry:
                    title_line = entry_link(title, f"https://dx.doi.org/{entry['doi']}")
                elif "url" in entry:
                    title_line = entry_link(title, entry["url"])
                elif "eprint" in entry:
                    title_line = entry_link(title, f"https://arxiv.org/abs/{entry['eprint']}")
                else:
                    title_line = f"*{title}*"

                e = entry.get("ENTRYTYPE", "misc")
                md_entry = {
                    "md": f"{color_square[e]}  {title_line}<br />\n{authors}<br />\n{pub_info}<br />\n {links}",
                    "type_order": type_order.get(entry.get("ENTRYTYPE", "misc").lower(), 4)
                }

                year = entry.get("year", "Unknown")
                all_entries_by_year[year].append(md_entry)

    # --- Sort entries per year by type_order ---
    for year in all_entries_by_year:
        all_entries_by_year[year] = [e["md"] + "\n" for e in sorted(all_entries_by_year[year], key=lambda x: x["type_order"])]

    # Sort years descending
    sorted_years = sorted(all_entries_by_year.keys(), reverse=True)

    output_lines = []
    for year in sorted_years:
        output_lines.append(f"### {year}\n")
        output_lines.extend(all_entries_by_year[year])
        output_lines.append("")  # Blank line after each year

    return "\n".join(output_lines)


# --- Main ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Markdown list from BibTeX files, grouped by year.")
    parser.add_argument("directory", help="Path to directory containing .bib files")
    parser.add_argument("output", help="Path to output Markdown file")

    args = parser.parse_args()

    output_md = generate_markdown_list(args.directory)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output_md)
