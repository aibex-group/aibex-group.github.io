import os
import bibtexparser
from collections import defaultdict

# --- Configuration ---
src = "scripts//bibs"
BIB_FILES = ["conferences.bib", "journals.bib", "books.bib", "patents.bib"]
OUTPUT_DIR = "static/research"
PDF_DIR = "static/research/papers"  # PDFs named as original BibTeX ID, e.g., cholleton22deep.pdf

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Load all entries ---
all_entries = []
for bib_file in BIB_FILES:
    bib_file = os.path.join(src, bib_file)
    with open(bib_file, 'r', encoding='utf-8') as f:
        bib_db = bibtexparser.load(f)
        all_entries.extend(bib_db.entries)

# --- Prepare ID mapping ---
author_year_count = defaultdict(int)
new_ids = {}

for entry in all_entries:
    # Use first author's last name and year
    first_author = entry['author'].replace(" and ", ",").split(",")[0].strip()
    last_name = first_author.split()[-1].capitalize()  # ensure capitalized
    year = entry.get('year', 'XXXX')
    
    base_id = f"{last_name}{year}"
    author_year_count[base_id] += 1
    count = author_year_count[base_id]
    pdf_path = os.path.join(PDF_DIR, f"{base_id}.pdf")

    if count == 1:
        new_id = base_id
    else:
        new_id = f"{base_id}{chr(ord('a') + count - 2)}"  # a, b, c...
    
    new_ids[entry['ID']] = new_id
    entry['ID'] = new_id

    # Append PDF if exists
    if os.path.exists(pdf_path):
        entry['file'] = f"/research/papers/{base_id}.pdf"

import re 
def sanitize_filename(s):
    # Keep only letters, numbers, dash, underscore
    return re.sub(r'[^A-Za-z0-9_\-]', '', s)

# --- Write each entry to a separate .bib file ---
writer = bibtexparser.bwriter.BibTexWriter()
writer.indent = '  '
writer.comma_first = False

for entry in all_entries:
    db = bibtexparser.bibdatabase.BibDatabase()
    db.entries = [entry]
    entry_bib_str = writer.write(db)

    safe_id = sanitize_filename(entry['ID'])
    output_path = os.path.join(OUTPUT_DIR, f"{safe_id}.bib")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(entry_bib_str)
