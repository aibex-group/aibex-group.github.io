import re
import bibtexparser


def parse_conference_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    entries = []

    # Split by \bibitem
    raw_entries = re.split(r'\\bibitem\{([^}]*)\}', text)
    for i in range(1, len(raw_entries), 2):
        bib_id = raw_entries[i].strip()
        content = raw_entries[i + 1].strip()

        parts = re.split(r'\\newblock', content)
        authors = parts[0].replace("\\", "").replace("~", " ").strip().rstrip(".")
        title = parts[1].replace("\\", "").strip().rstrip(".")

        venue_block = parts[2]
        booktitle_match = re.search(r'In \{\\em (.*?)\}', venue_block)
        booktitle = booktitle_match.group(1) if booktitle_match else ""
        pages_match = re.search(r'pages ([0-9]+--[0-9]+)', venue_block)
        pages = pages_match.group(1) if pages_match else ""
        year_match = re.search(r'(19|20|21|22|23|24|25)[0-9]{2}', venue_block)
        year = year_match.group(0) if year_match else ""

        note = parts[3].replace("\\", "").strip() if len(parts) > 3 else ""

        entries.append({
            'ENTRYTYPE': 'inproceedings',
            "ID": bib_id,
            "author": authors,
            "title": title,
            "booktitle": booktitle,
            "pages": pages,
            "year": year,
            "note": note
        })

    return entries

import re

def parse_journal_file(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    entries = []
    raw_entries = re.split(r'\\bibitem\{([^}]*)\}', text)

    for i in range(1, len(raw_entries), 2):
        print(i)
        bib_id = raw_entries[i].strip()
        content = raw_entries[i + 1].strip()

        parts = re.split(r'\\\\newblock', content)
        authors = parts[0].replace("\\", "").replace("~", " ").strip().rstrip(".")
        title = parts[1].replace("\\", "").strip().rstrip(".")

        # Extract journal info
        journal_block = parts[2].replace("\n", " ").strip()
        # Match either \em or \emph
        journal_match = re.match(
            r'(?:\\em|\\emph)\{(.+?)\}\s*,\s*'          # Journal name
            r'(\d+)'                                     # volume
            r'(?:\((\d+)\))?'                            # optional number
            r'\s*:\s*([0-9\-]+)'                         # pages
            r'\s*,\s*(\d{4})',                           # year
            journal_block
        )

               # Extract journal info
        journal_block = parts[2].replace("\n", " ").strip()
        journal_match = re.match(
            r'(?:\\em|\\emph)\{(.+?)\}\s*,\s*'          # Journal name
            r'(\d+)'                                     # volume
            r'(?:\((\d+)\))?'                            # optional number
            r'\s*:\s*([0-9\-]+)'                         # pages
            r'\s*,\s*(\d{4})',                           # year
            journal_block
        )

        if journal_match:
            journal, volume, number, pages, year = journal_match.groups()
        else:
            journal, volume, number, pages, year = "", "", "", "", ""

        # Ensure all fields are strings
        entry = {
            'ENTRYTYPE': 'article',
            'ID': str(bib_id),
            'author': str(authors),
            'title': str(title),
            'journal': str(journal.strip()),
            'volume': str(volume),
            'number': str(number) if number else "",
            'pages': str(pages),
            'year': str(year)
        }

        entries.append(entry)
    return entries


def write_bibtex(entries, output_file):
    bib_db = bibtexparser.bibdatabase.BibDatabase()
    bib_db.entries = entries

    writer = bibtexparser.bwriter.BibTexWriter()
    writer.indent = '  '     # pretty print
    writer.comma_first = False
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(writer.write(bib_db))


# Example usage
if __name__ == "__main__":
    file_path = 'scripts/data/conferences.txt'
    entries = parse_conference_file(file_path)
    write_bibtex(entries, 'scripts/conferences.bib')

    # file_path = 'scripts/data/journals.txt'
    # entries = parse_journal_file(file_path)
    # print(entries)
    # write_bibtex(entries, 'scripts/journals.bib')
