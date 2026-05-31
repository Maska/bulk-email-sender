"""Create personalized PDFs."""

import io
import logging
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from config import personalize

LOG = logging.getLogger(__name__)


def create_letters(entries: dict, config: dict) -> None:
    """Create letters and add the letter path to entries."""
    template = config["paths"]["template"]
    if not template:
        LOG.info("No template given, not creating letters")
        return
    LOG.debug(f"Creating letters from template {template}")
    for entry in entries:
        _create_letter(personalize(config, entry))
    LOG.info(f"Created {len(entries)} letters")


def _create_letter(config: dict) -> None:
    """Create a personal letter. Write it to the attachment path."""
    output_file = config["paths"]["attachment"]
    if output_file.is_dir():
        abs_path = output_file.absolute()
        msg = (
            f"Attachment path resolves to a directory ({abs_path}). "
            "Did you forget to set the attachment path?"
        )
        raise IsADirectoryError(msg)
    if not output_file.parent.is_dir():
        output_file.parent.mkdir(exist_ok=True, parents=True)

    personalization = _draw_personalization(config)
    _merge(config["paths"]["template"], personalization, output_file)
    LOG.debug(f"Created letter {output_file}")


def _draw_personalization(config: dict) -> io.BytesIO:
    """Create a PDF with personal texts and return it as an in-memory file."""
    memory_file = io.BytesIO()
    canvas = Canvas(memory_file, pagesize=A4)
    tables = config.get("line_of_text", [])
    for table in tables:
        font = table["font"]
        registerFont(TTFont(font, config["paths"]["font_folder"] / font))
        canvas.setFont(font, table["size"])
        canvas.drawString(
            table["x"],
            table["y"],
            table["text"],
        )
    canvas.showPage()
    canvas.save()
    memory_file.seek(0)
    return memory_file


def _merge(template: Path, personalization: io.BytesIO, output: Path) -> None:
    """Watermark template with given personalization. Write to output path."""
    stamp = PdfReader(personalization).pages[0]
    writer = PdfWriter()
    reader = PdfReader(template)
    writer.append(reader, pages=None)
    writer.pages[0].merge_page(stamp)
    writer.write(output)
