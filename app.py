from flask import Flask, request, jsonify
import pytesseract
from pdf2image import convert_from_path
from io import BytesIO

app = Flask(__name__)

@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']

    # Converte PDF para imagens
    images = convert_from_path(file.stream)

    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang='por')

    return jsonify({'text': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)