import bibtexparser
import requests, os
from pathlib import Path
from bs4 import BeautifulSoup

# Path to your BibTeX file
bib_file = "fischer-bibtex.bib"
output_dir = Path("static/research/papers")
output_dir.mkdir(exist_ok=True)
bib_outdir = Path("static/research")
# Read BibTeX file
with open(bib_file, "r", encoding="utf-8") as f:
    bib_database = bibtexparser.load(f)

new_entries = []

for entry in bib_database.entries:
    # Extract first author
    authors = entry.get('author', '').split(' and ')
    if not authors:
        continue
    first_author = authors[0].split(',')[0].strip()

    # Extract year
    year = entry.get('year')

    if not year:
        # fallback: try to find a 4-digit number in publisher/journal/address
        for field in ['publisher', 'journal', 'address']:
            if field in entry:
                import re
                match = re.search(r'(\d{4})', entry[field])
                if match:
                    year = match.group(1)
                    break
    if not year:
        print(f"Skipping {entry.get('ID')} because year not found")
        continue

    # New BibTeX key
    new_key = f"{first_author}{year}"
    entry["year"] = year
    entry['ID'] = new_key
    for k in ["number", "recid", "publisher"]:
        if entry.get(k, None):
            del entry[k] 


    new_entries.append(entry)

    # Download PDF
    url = entry.get('url')
    pdf_path = output_dir / f"{new_key}.pdf"

    pdf_path = f"static/research/papers/{entry.get('ID')}.pdf"
    if os.path.exists(pdf_path):
        entry["url"] = f"/research/papers/{entry.get('ID')}.pdf" # Update URL to local path
    else:
        del entry["url"]  # Remove URL if download failed

    # Save individual .bib file
    single_bib = bibtexparser.bibdatabase.BibDatabase()
    single_bib.entries = [entry]
    bib_path = bib_outdir / f"{new_key}.bib"
    with open(bib_path, "w", encoding="utf-8") as f:
        bibtexparser.dump(single_bib, f)
    print(f"Saved {bib_path}")


    # if os.path.exists(pdf_path):
    #     print(f"{pdf_path} already exists, skipping download.")
    #     continue
    
    # # --- Get record URL ---
    # record_url = entry.get("url")
    # if not record_url:
    #     continue

    # try:
    #     # Fetch the HTML page
    #     page = requests.get(record_url)
    #     page.raise_for_status()
    #     soup = BeautifulSoup(page.text, "html.parser")

    #     # Find all links to PDFs
    #     pdf_links = [
    #         a["href"] for a in soup.find_all("a", href=True)
    #         if a["href"].lower().endswith(".pdf")
    #     ]

    #     if not pdf_links:
    #         print(f"No PDF found on {record_url}")
    #         continue

    #     # Download the first PDF (or loop if multiple)
    #     for i, pdf_link in enumerate(pdf_links, start=1):
    #         # Handle relative URLs
    #         if pdf_link.startswith("/"):
    #             base_url = re.match(r"^https?://[^/]+", record_url).group(0)
    #             pdf_link = base_url + pdf_link

    #         pdf_name = f"{new_key}.pdf" if len(pdf_links) == 1 else f"{new_key}_{i}.pdf"
    #         pdf_path = output_dir / pdf_name

    #         r = requests.get(pdf_link)
    #         if r.status_code == 200:
    #             with open(pdf_path, "wb") as pdf_file:
    #                 pdf_file.write(r.content)
    #             print(f"Downloaded {pdf_path}")
    #         else:
    #             print(f"Failed to download {pdf_link} (status {r.status_code})")

    # except Exception as e:
    #     print(f"Error scraping {record_url}: {e}")
    


    # if url:
    #     try:
    #         response = requests.get(url)
    #         if response.status_code == 200:
    #             with open(pdf_path, 'wb') as f:
    #                 f.write(response.content)
    #             print(f"Downloaded {pdf_path}")
    #         else:
    #             print(f"Failed to download {url} (status {response.status_code})")
    #     except Exception as e:
    #         print(f"Error downloading {url}: {e}")

# # Save updated BibTeX
# new_bib = bibtexparser.bibdatabase.BibDatabase()
# new_bib.entries = new_entries
# with open("references_updated.bib", "w", encoding="utf-8") as f:
#     bibtexparser.dump(new_bib, f)

# print("Updated BibTeX saved as references_updated.bib")
