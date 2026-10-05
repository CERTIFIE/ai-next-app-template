"""Convert the client documents in .documents/ into Markdown for the agents.

The agents read Markdown far more reliably than binary Office files, so every
DOCX, XLSX, PDF (and PPTX/XLS) is extracted to docs/sources/<file>.md together
with an INDEX.md that records checksums. The originals stay authoritative: the
extract is a reading aid, and anything visual (images, layout, signatures) must
still be checked on the original.

Usage (inside the "documents" container):
    python convert.py [--input /documents] [--output /out] [--force]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

from markitdown import MarkItDown

CONVERTIBLE = {".pdf", ".docx", ".xlsx", ".xls", ".pptx"}
COPIED_AS_TEXT = {".md", ".txt", ".csv"}
# Below this many characters per page a PDF is probably scanned: the agents
# must look at the original pages instead of trusting an almost empty extract.
SCANNED_PDF_CHARS_PER_PAGE = 200
STATE_FILE = ".index.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pdf_page_count(path: Path) -> int:
    try:
        import pdfplumber

        with pdfplumber.open(path) as pdf:
            return len(pdf.pages)
    except Exception:  # an unreadable page count must not block the conversion
        return 0


def header(source: Path, checksum: str, note: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "<!--",
        f"  Estratto automatico di .documents/{source.name}",
        f"  sha256: {checksum}",
        f"  generato: {now}",
        "  Non modificare: rigenera con il servizio Docker 'documents'.",
        "  In caso di dubbio fa fede il documento originale.",
    ]
    if note:
        lines.append(f"  ATTENZIONE: {note}")
    lines.append("-->")
    return "\n".join(lines) + "\n\n"


def convert_one(converter: MarkItDown, source: Path) -> tuple[str, str]:
    suffix = source.suffix.lower()
    if suffix in COPIED_AS_TEXT:
        return source.read_text(encoding="utf-8", errors="replace"), ""
    text = converter.convert(str(source)).text_content or ""
    note = ""
    if suffix == ".pdf":
        pages = pdf_page_count(source)
        if pages and len(text.strip()) / pages < SCANNED_PDF_CHARS_PER_PAGE:
            note = (
                f"poco testo estratto ({len(text.strip())} caratteri su {pages} pagine): "
                "probabile PDF scansionato, leggi le pagine dell'originale come immagini"
            )
    if suffix in {".docx", ".pptx"}:
        note = note or "immagini e diagrammi non sono estratti: verificali sull'originale"
    return text, note


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="/documents")
    parser.add_argument("--output", default="/out")
    parser.add_argument("--force", action="store_true", help="riconverti anche i file invariati")
    args = parser.parse_args()

    source_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    state_path = output_dir / STATE_FILE
    state: dict[str, dict] = json.loads(state_path.read_text()) if state_path.exists() else {}

    converter = MarkItDown(enable_plugins=False)
    rows: list[dict] = []
    seen: set[str] = set()
    failures = 0

    for source in sorted(p for p in source_dir.iterdir() if p.is_file()):
        if source.name.startswith((".", "~$")):  # hidden files and Office lock files
            continue
        suffix = source.suffix.lower()
        target_name = f"{source.name}.md"
        seen.add(source.name)

        if suffix not in CONVERTIBLE | COPIED_AS_TEXT:
            rows.append({"source": source.name, "status": "non supportato", "note":
                         "formato non convertibile: converti in DOCX, XLSX o PDF", "target": ""})
            print(f"[documents] SALTATO   {source.name} (formato non supportato)")
            continue

        checksum = sha256(source)
        previous = state.get(source.name)
        target = output_dir / target_name
        if not args.force and previous and previous["sha256"] == checksum and target.exists():
            rows.append(previous | {"status": "invariato"})
            print(f"[documents] invariato {source.name}")
            continue

        try:
            text, note = convert_one(converter, source)
        except Exception as error:  # report every failure, keep converting the rest
            failures += 1
            rows.append({"source": source.name, "status": "errore", "note": str(error)[:200],
                         "target": "", "sha256": checksum})
            print(f"[documents] ERRORE    {source.name}: {error}", file=sys.stderr)
            continue

        target.write_text(header(source, checksum, note) + text.strip() + "\n", encoding="utf-8")
        status = "nuovo" if not previous else "aggiornato"
        entry = {"source": source.name, "target": target_name, "sha256": checksum,
                 "chars": len(text), "note": note,
                 "converted": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}
        state[source.name] = entry
        rows.append(entry | {"status": status})
        print(f"[documents] {status:<9} {source.name} -> docs/sources/{target_name}")

    # Extracts whose original was removed from .documents/ would mislead the agents.
    for name in sorted(set(state) - seen):
        stale = output_dir / state[name]["target"]
        if stale.exists():
            stale.unlink()
        rows.append({"source": name, "status": "rimosso", "target": "",
                     "note": "documento non più presente in .documents/"})
        print(f"[documents] rimosso   {name}")
        del state[name]

    state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    write_index(output_dir, rows)
    return 1 if failures else 0


def write_index(output_dir: Path, rows: list[dict]) -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Indice dei documenti del cliente",
        "",
        f"Generato il {now} dal servizio Docker `documents`. Non modificare a mano.",
        "",
        "Gli originali in `.documents/` fanno fede; questi estratti servono alla lettura.",
        "Stato: nuovo, aggiornato (l'originale è cambiato: rivedi i requisiti collegati),",
        "invariato, errore, non supportato, rimosso.",
        "",
        "| Documento originale | Estratto | Stato | sha256 | Note |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        target = f"[{row['target']}]({row['target']})" if row.get("target") else "—"
        short = (row.get("sha256") or "")[:12]
        note = (row.get("note") or "").replace("|", "/")
        lines.append(f"| `{row['source']}` | {target} | {row['status']} | `{short}` | {note} |")
    (output_dir / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
