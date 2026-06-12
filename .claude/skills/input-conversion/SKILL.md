---
name: input-conversion
description: How to convert document inputs (PDF/Word/PowerPoint/Excel/HTML) to text/Markdown for term and relation extraction, with markitdown first and pypdf/python-docx/pandas as proven fallbacks. Used by the input-agent and the document adapter.
---

# Input conversion (documents → text/Markdown)

Documents are **conceptual signal for design**, not data to load. Convert them to clean text/Markdown so
the scenario-and-cq and modeling agents can extract terms and relations. Used inside the
`input/adapters/` document adapter.

## Order of attempts (lightweight first)
1. **markitdown** — the baseline converter for PDF / Word / PowerPoint / Excel / HTML → Markdown.
   ```python
   from markitdown import MarkItDown
   text = MarkItDown().convert(path).text_content
   ```
2. **Proven fallbacks** when markitdown is absent or fails on a format:
   - **PDF** → `pypdf` (`PdfReader(path)`, join `page.extract_text()`).
   - **Word** → `python-docx` (`Document(path)`, join paragraph text).
   - **Excel / CSV** → `pandas` (`read_excel` / `read_csv`, then `to_markdown()`).
   - **HTML** → markitdown, or a simple tag strip.
3. **Heavy, layout-aware converters** (e.g. docling) are a **per-project** library-scout pick, not
   baseline — propose them at `/scout-libs` only when the corpus needs layout fidelity.

## Honesty
If no converter is available for a format, **say so plainly** and record the file as
`designed-not-exercised` rather than silently producing empty text (Limitation 5). Never fabricate
content a converter could not extract.

## Output
Hand back normalised text + a one-line note per file. The document adapter wraps this into an
`InputItem(type="document", text=...)` for the typed input pack.
