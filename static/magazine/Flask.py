from flask import Flask, render_template, jsonify
import fitz
import os
from flask import Flask, render_template, send_from_directory



BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# PDF PATH
PDF_FILE = os.path.join(BASE_DIR, "it_magazine.pdf")

# OUTPUT FOLDERS
OUTPUT_DIR = os.path.join(BASE_DIR, "static", "pages")
THUMB_DIR = os.path.join(BASE_DIR, "static", "thumbs")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(THUMB_DIR, exist_ok=True)

# Default A4 size
PAGE_WIDTH = 595
PAGE_HEIGHT = 842


def clear_old_images():
    """
    Remove old cached images
    """

    for folder in [OUTPUT_DIR, THUMB_DIR]:

        for file in os.listdir(folder):

            if file.endswith(".jpg"):

                os.remove(os.path.join(folder, file))


def convert_pdf():

    global PAGE_WIDTH, PAGE_HEIGHT

    if not os.path.exists(PDF_FILE):

        print(f"ERROR: PDF not found -> {PDF_FILE}")

        return 0

    print("Loading PDF...")
    print(PDF_FILE)

    doc = fitz.open(PDF_FILE)

    total = len(doc)

    if total == 0:

        print("PDF contains no pages")

        return 0

    # Detect actual page size
    rect = doc[0].rect

    PAGE_WIDTH = rect.width
    PAGE_HEIGHT = rect.height

    print(
        f"Detected PDF size: "
        f"{PAGE_WIDTH:.2f} x {PAGE_HEIGHT:.2f}"
    )

    # Clear previous rendered pages
    clear_old_images()

    # Render all pages
    for i, page in enumerate(doc):

        print(f"Rendering page {i+1}/{total}")

        page_path = os.path.join(
            OUTPUT_DIR,
            f"page_{i:04d}.jpg"
        )

        thumb_path = os.path.join(
            THUMB_DIR,
            f"thumb_{i:04d}.jpg"
        )

        # Full page render
        mat = fitz.Matrix(2.5, 2.5)

        pix = page.get_pixmap(
            matrix=mat,
            alpha=False
        )

        pix.save(page_path)

        # Thumbnail render
        thumb_mat = fitz.Matrix(0.45, 0.45)

        thumb_pix = page.get_pixmap(
            matrix=thumb_mat,
            alpha=False
        )

        thumb_pix.save(thumb_path)

    doc.close()

    print(f"Successfully rendered {total} pages")

    return total


# IMPORTANT
# Convert PDF when app starts
total_pages = convert_pdf()


@app.route("/")
def index():

    pages = sorted([
        f for f in os.listdir(OUTPUT_DIR)
        if f.endswith(".jpg")
    ])

    thumbs = sorted([
        f for f in os.listdir(THUMB_DIR)
        if f.endswith(".jpg")
    ])

    aspect = round(PAGE_WIDTH / PAGE_HEIGHT, 4)

    return render_template(
        "index.html",
        pages=pages,
        thumbs=thumbs,
        total=len(pages),
        page_width=int(PAGE_WIDTH),
        page_height=int(PAGE_HEIGHT),
        aspect=aspect
    )


@app.route("/api/pages")
def api_pages():

    pages = sorted([
        f for f in os.listdir(OUTPUT_DIR)
        if f.endswith(".jpg")
    ])

    return jsonify(pages)
@app.route("/pdf")
def open_pdf():

    return send_from_directory(
        "static/magazine",
        "it_magazine.pdf"
    )
app = Flask(__name__)

if __name__ == "__main__":

    app.run(debug=True)