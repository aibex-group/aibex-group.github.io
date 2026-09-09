# AIBEX Group

Preliminary website for the AIBEX group at UniFR.

## Previewing your website edits locally

Run `hugo server` in the root path.

## Updating publications

All publication data lives in `publications.bib` at the repository root. To add
a publication, append a normal BibTeX entry with a unique citation key and a
`year` field. If an author copy is available, put the PDF in
`static/research/papers/` and add a field such as:

```bibtex
file = {/research/papers/MyKey2026.pdf}
```

Then regenerate the page:

```sh
python3 scripts/generate_publications.py
```

The generator uses only Python's standard library. It groups publications by
year (newest first), then by type (books, journal articles, conference papers,
and patents/miscellaneous), and alphabetically by title. It preserves the
existing publication styling and generates `content/publications.md`, which
should be committed together with `publications.bib`.

To verify that the generated page is current without changing files, run:

```sh
python3 scripts/generate_publications.py --check
```
