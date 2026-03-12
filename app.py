from flask import Flask, render_template, request, send_file
from pypdf import PdfReader, PdfWriter
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/merge", methods=["POST"])
def merge():

    pdf1 = request.files["pdf1"]
    pdf2 = request.files["pdf2"]

    reader1 = PdfReader(pdf1)
    reader2 = PdfReader(pdf2)

    writer = PdfWriter()

    max_pages = max(len(reader1.pages), len(reader2.pages))

    for i in range(max_pages):

        if i < len(reader1.pages):
            writer.add_page(reader1.pages[i])

        if i < len(reader2.pages):
            writer.add_page(reader2.pages[i])

    filename = f"{uuid.uuid4()}.pdf"
    output_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(output_path, "wb") as f:
        writer.write(f)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)