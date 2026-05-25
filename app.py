from flask import Flask, render_template
import os
import fitz

app = Flask(__name__)

# PDF Flipbook configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_FILE = os.path.join(BASE_DIR, "static", "magazine", "it_magazine.pdf")  # Update this to your PDF filename
OUTPUT_DIR = os.path.join(BASE_DIR, "static", "pages")
THUMB_DIR = os.path.join(BASE_DIR, "static", "thumbs")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(THUMB_DIR, exist_ok=True)

def get_pdf_data():
    pages = []
    thumbs = []
    total = 0
    aspect = 0.7071  # Default A4 aspect ratio

    if not os.path.exists(PDF_FILE):
        print(f"Warning: {PDF_FILE} not found. Add your PDF file.")
        return pages, thumbs, total, aspect

    doc = fitz.open(PDF_FILE)
    total = len(doc)

    # Read actual dimensions from first page
    if total > 0:
        rect = doc[0].rect
        aspect = rect.width / rect.height

    for i in range(total):
        page_path = f"page_{i:04d}.jpg"
        thumb_path = f"thumb_{i:04d}.jpg"
        pages.append(page_path)
        thumbs.append(thumb_path)

        # Generate images if not exist
        full_page_path = os.path.join(OUTPUT_DIR, page_path)
        full_thumb_path = os.path.join(THUMB_DIR, thumb_path)

        if not os.path.exists(full_page_path):
            page = doc[i]
            mat = fitz.Matrix(2.0, 2.0)
            pix = page.get_pixmap(matrix=mat)
            pix.save(full_page_path)

        if not os.path.exists(full_thumb_path):
            page = doc[i]
            mat = fitz.Matrix(0.3, 0.3)
            pix = page.get_pixmap(matrix=mat)
            pix.save(full_thumb_path)

    doc.close()
    return pages, thumbs, total, aspect

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/magazine/')
def magazine():
    pages, thumbs, total, aspect = get_pdf_data()
    return render_template('index1.html', pages=pages, thumbs=thumbs, total=total, aspect=aspect)

@app.route('/achievers/')
def achievers():
    return render_template('achievers.html')

@app.route('/faculty/')
def faculty():
    return render_template('faculty.html')
@app.route('/annual-magazine/')
def annual_magazine():
    magazines = [
        {
            "year": "2025",
            "cover": "magazine_covers/y.png",
            "pdf": "magazine/x.pdf"
        }
    ]

    return render_template(
        'annual_magazine.html',
        magazines=magazines
    )
if __name__ == '__main__':
    app.run(debug=True)