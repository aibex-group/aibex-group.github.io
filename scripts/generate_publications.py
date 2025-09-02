import os
import bibtexparser
from collections import defaultdict
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode


def format_author(name):
    parts = name.replace("~", " ").split(",")
    if len(parts) == 2:
        last, first = parts
    else:
        first_last = parts[0].split()
        last = first_last[-1]
        first = " ".join(first_last[:-1])
    initials = "&nbsp;".join([f[0] + "." if len(f) > 0 else "" for f in first.split()])
    return f"{initials}&nbsp;{last.strip()}"


def format_authors(authors_raw):
    authors = [format_author(name.strip()) for name in authors_raw.replace("\n", " ").split(" and ")]
    formatted = ", ".join(authors)
    formatted = formatted.replace("†", "<sup>&dagger;</sup>").replace("‡", "<sup>&Dagger;</sup>")
    return formatted


def entry_link(title, url):
    return f"[*{title}*]({url})"


def get_publication_info(entry):
    if entry.get("journal"):
        info = f"{entry['journal']}"
        if "volume" in entry:
            info += f", Volume {entry['volume']}"
        if "number" in entry:
            info += f", Number {entry['number']}"
        if "pages" in entry:
            info += f", pp. {entry['pages']}"
    elif entry.get("booktitle"):
        info = f"{entry['booktitle']}"
    else:
        info = "Preprint"
    year = entry.get("year", "")
    return f"{info}, {year}" if year not in info else info


def get_links(entry, filename):
    links = []
    if "eprint" in entry and "arxiv" in entry.get("eprinttype", "arxiv").lower():
        links.append(f'[\[Preprint\]](https://arxiv.org/abs/{entry["eprint"]})')
    if "doi" in entry:
        links.append(f'[\[DOI\]](https://dx.doi.org/{entry["doi"]})')
    if "url" in entry:
        links.append(f'[\[Author\'s copy\]]({entry["url"]})')
    links.append(f'[\[BibTeX\]]({filename})')
    return " &bull; ".join(links)


def process_bib_file(filepath):
    with open(filepath, "r", encoding="utf-8") as bibfile:
        parser = BibTexParser(common_strings=True)
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibfile, parser=parser)

    entries_by_year = defaultdict(list)
    for entry in bib_database.entries:
        title = entry.get("title", "").strip("{}")
        authors = format_authors(entry.get("author", ""))
        pub_info = get_publication_info(entry)
        bib_filename = os.path.basename(filepath)
        links = get_links(entry, bib_filename)

        # Title with possible link
        if "doi" in entry:
            title_line = entry_link(title, f"https://dx.doi.org/{entry['doi']}")
        elif "url" in entry:
            title_line = entry_link(title, entry["url"])
        elif "eprint" in entry:
            title_line = entry_link(title, f"https://arxiv.org/abs/{entry['eprint']}")
        else:
            title_line = f"*{title}*"

        md_entry = f"- {title_line}<br />\n" \
                   f"{authors}<br />\n" \
                   f"{pub_info}<br />\n" \
                   f"        <small>{links}</small>"

        year = entry.get("year", "Unknown")
        # if entry.get("publisher", None):
        #     year = entry.get("publisher").split(" ")[-1]
        # else:
        #     year = entry.get("address").split("-")[0]
        # # print(year)
        # year = [i for i in entry.get("ID") if i.isdigit()]
        # year = int("".join(year))
        entries_by_year[year].append(md_entry)

    return entries_by_year


def generate_markdown_list(directory):
    all_entries_by_year = defaultdict(list)

    for filename in sorted(os.listdir(directory)):
        if filename.endswith(".bib"):
            filepath = os.path.join(directory, filename)
            yearly_entries = process_bib_file(filepath)
            for year, entries in yearly_entries.items():
                all_entries_by_year[year].extend(entries)

    # Sort years descending
    sorted_years = sorted(all_entries_by_year.keys(), reverse=True)

    output_lines = []
    for year in sorted_years:
        output_lines.append(f"### {year}\n")
        output_lines.extend(all_entries_by_year[year])
        output_lines.append("")  # Add blank line after each year

    return "\n".join(output_lines)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Markdown list from BibTeX files, grouped by year.")
    parser.add_argument("directory", help="Path to directory containing .bib files")
    parser.add_argument("output", help="Path to output file")

    args = parser.parse_args()

    output_md = generate_markdown_list(args.directory)
    # print(output_md)s

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(output_md)