from textwrap import wrap

from PIL import Image


PAGE_WIDTH = 595
PAGE_HEIGHT = 842
LEFT_MARGIN = 50
TOP_MARGIN = 60
BOTTOM_MARGIN = 50
LINE_HEIGHT = 16
FONT_SIZE = 11
TITLE_SIZE = 18
MAX_TEXT_WIDTH = 82
SECTION_SPACING = 8


def _escape_pdf_text(value):
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace("(", "\\(")
        .replace(")", "\\)")
    )


def _wrap_line(label, value=""):
    text = f"{label}{value}" if value != "" else label
    if not text:
        return [""]
    wrapped = wrap(text, width=MAX_TEXT_WIDTH, break_long_words=True)
    return wrapped or [text]


def _load_pdf_image(image_path):
    if not image_path:
        return None

    try:
        with Image.open(image_path) as image:
            if image.mode != "RGB":
                image = image.convert("RGB")

            original_width, original_height = image.size
            if not original_width or not original_height:
                return None

            max_width = 220
            max_height = 180
            ratio = min(max_width / original_width, max_height / original_height, 1)
            display_width = round(original_width * ratio, 2)
            display_height = round(original_height * ratio, 2)

            from io import BytesIO

            buffer = BytesIO()
            image.save(buffer, format="JPEG", quality=85)
            return {
                "bytes": buffer.getvalue(),
                "width": original_width,
                "height": original_height,
                "display_width": display_width,
                "display_height": display_height,
            }
    except Exception:
        return None


def build_simple_pdf(title, sections, image_path=None):
    pages = []
    current_page = []
    y = PAGE_HEIGHT - TOP_MARGIN
    image_info = _load_pdf_image(image_path)

    def add_line(text, font_name="F1", font_size=FONT_SIZE):
        nonlocal y, current_page
        if y <= BOTTOM_MARGIN:
            pages.append(current_page)
            current_page = []
            y = PAGE_HEIGHT - TOP_MARGIN
        current_page.append((font_name, font_size, LEFT_MARGIN, y, text))
        y -= LINE_HEIGHT

    add_line(title, font_name="F2", font_size=TITLE_SIZE)
    add_line("Farmer-friendly ASF report for printing or vet sharing", font_name="F1", font_size=10)
    y -= 6

    if image_info:
        caption = "Pig Photo"
        add_line(caption, font_name="F2", font_size=13)
        image_bottom_y = y - image_info["display_height"]
        if image_bottom_y <= BOTTOM_MARGIN:
            pages.append(current_page)
            current_page = []
            y = PAGE_HEIGHT - TOP_MARGIN
            add_line(caption, font_name="F2", font_size=13)
            image_bottom_y = y - image_info["display_height"]
        current_page.append(
            (
                "IMAGE",
                LEFT_MARGIN,
                image_bottom_y,
                image_info["display_width"],
                image_info["display_height"],
            )
        )
        y = image_bottom_y - 24

    for heading, lines in sections:
        add_line(heading, font_name="F2", font_size=13)
        for line in lines:
            for wrapped_line in _wrap_line(line):
                add_line(wrapped_line)
        y -= SECTION_SPACING

    if current_page:
        pages.append(current_page)

    objects = []

    def add_object(content):
        objects.append(content)
        return len(objects)

    font_regular_id = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
    font_bold_id = add_object("<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
    image_id = None

    if image_info:
        image_stream = image_info["bytes"]
        image_id = add_object(
            (
                f"<< /Type /XObject /Subtype /Image /Width {image_info['width']} "
                f"/Height {image_info['height']} /ColorSpace /DeviceRGB /BitsPerComponent 8 "
                f"/Filter /DCTDecode /Length {len(image_stream)} >>\nstream\n".encode("latin-1")
                + image_stream
                + b"\nendstream"
            )
        )

    page_ids = []
    content_ids = []
    pages_id = None

    for page_lines in pages:
        stream_parts = ["BT"]
        has_image = False
        for entry in page_lines:
            if entry[0] == "IMAGE":
                has_image = True
                continue
            font_name, font_size, x, line_y, text = entry
            escaped = _escape_pdf_text(text)
            stream_parts.append(f"/{font_name} {font_size} Tf")
            stream_parts.append(f"1 0 0 1 {x} {line_y} Tm")
            stream_parts.append(f"({escaped}) Tj")
        stream_parts.append("ET")
        for entry in page_lines:
            if entry[0] != "IMAGE":
                continue
            _, x, image_y, image_width, image_height = entry
            stream_parts.append("q")
            stream_parts.append(f"{image_width} 0 0 {image_height} {x} {image_y} cm")
            stream_parts.append("/Im1 Do")
            stream_parts.append("Q")
        stream = "\n".join(stream_parts)
        content_id = add_object(
            f"<< /Length {len(stream.encode('latin-1', errors='replace'))} >>\nstream\n{stream}\nendstream"
        )
        content_ids.append(content_id)
        xobject_resources = ""
        if has_image and image_id is not None:
            xobject_resources = f" /XObject << /Im1 {image_id} 0 R >>"
        page_ids.append(
            add_object(
                "<< /Type /Page /Parent {pages_ref} 0 R "
                f"/MediaBox [0 0 {PAGE_WIDTH} {PAGE_HEIGHT}] "
                f"/Resources << /Font << /F1 {font_regular_id} 0 R /F2 {font_bold_id} 0 R >>{xobject_resources} >> "
                f"/Contents {content_id} 0 R >>"
            )
        )

    kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
    pages_id = add_object(f"<< /Type /Pages /Count {len(page_ids)} /Kids [{kids}] >>")
    catalog_id = add_object(f"<< /Type /Catalog /Pages {pages_id} 0 R >>")

    rendered_objects = []
    for index, content in enumerate(objects, start=1):
        if isinstance(content, bytes):
            content_bytes = content.replace(b"{pages_ref}", str(pages_id).encode("latin-1"))
        else:
            if "{pages_ref}" in content:
                content = content.replace("{pages_ref}", str(pages_id))
            content_bytes = content.encode("latin-1", errors="replace")
        rendered_objects.append((index, content_bytes))

    pdf_parts = [b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"]
    offsets = [0]
    current_offset = len(pdf_parts[0])

    for object_id, content_bytes in rendered_objects:
        obj_bytes = (
            f"{object_id} 0 obj\n".encode("latin-1")
            + content_bytes
            + b"\nendobj\n"
        )
        offsets.append(current_offset)
        pdf_parts.append(obj_bytes)
        current_offset += len(obj_bytes)

    xref_offset = current_offset
    xref_lines = [f"xref\n0 {len(rendered_objects) + 1}\n", "0000000000 65535 f \n"]
    for offset in offsets[1:]:
        xref_lines.append(f"{offset:010d} 00000 n \n")
    trailer = (
        "".join(xref_lines)
        + f"trailer\n<< /Size {len(rendered_objects) + 1} /Root {catalog_id} 0 R >>\n"
        + f"startxref\n{xref_offset}\n%%EOF"
    )
    pdf_parts.append(trailer.encode("latin-1"))
    return b"".join(pdf_parts)
