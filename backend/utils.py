from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

ASSETS_DIR = "assets"

def save_to_pdf(text, filename="output.pdf", images=None):
    """
    Convert text + optional images into a downloadable PDF buffer.
    text: str
    images: list of (caption, path)
    """
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50

    # Add text
    for line in text.split("\n"):
        c.drawString(50, y, line[:100])  # wrap long lines
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 50

    # Add images (if provided)
    if images:
        for caption, img_path in images:
            try:
                # Show caption
                if y < 100:
                    c.showPage()
                    y = height - 50
                c.drawString(50, y, caption)
                y -= 20

                # Insert image
                img = ImageReader(img_path)
                img_width, img_height = img.getSize()
                aspect = img_height / float(img_width)

                display_width = width - 100
                display_height = display_width * aspect

                if y - display_height < 50:  # new page if not enough space
                    c.showPage()
                    y = height - 50

                c.drawImage(img, 50, y - display_height, width=display_width, height=display_height)
                y -= display_height + 40
            except Exception as e:
                print("⚠️ Could not add image to PDF:", e)

    c.save()
    buffer.seek(0)
    return buffer


def save_image(image_bytes, filename):
    """Save generated image to assets folder"""
    if not os.path.exists(ASSETS_DIR):
        os.makedirs(ASSETS_DIR)
    path = os.path.join(ASSETS_DIR, filename.replace(" ", "_"))
    with open(path, "wb") as f:
        f.write(image_bytes)
    return path
