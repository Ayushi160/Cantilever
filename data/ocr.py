from flask import Flask, request, render_template
from PIL import Image
import pytesseract
import os

app = Flask('MyFlaskApp')

FOLDER = 'Images'
os.makedirs(FOLDER, exist_ok=True)
app.config['FOLDER'] = FOLDER

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\Tesseract.exe'  # Modify this line as per your installation


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    if file.filename == '':
        return "No selected file"

    filepath = os.path.join(app.config['FOLDER'], file.filename)
    file.save(filepath)

    text = pytesseract.image_to_string(Image.open(filepath))

    os.remove(filepath)

    return f"<h1>Extracted Text:</h1><p>{text}</p>"


if __name__ == '__main__':
    app.run(debug=True)