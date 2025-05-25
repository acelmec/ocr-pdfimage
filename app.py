from flask import Flask, request, jsonify
import pytesseract
from pdf2image import convert_from_bytes, convert_from_path
from PIL import Image
import requests
from io import BytesIO
import os

app = Flask(__name__)

API_KEY = os.environ.get('API_KEY', 'XwJKCzj9vvMFe86FzpL9luiaQwfIvLon')

# Middleware simples para checar a API Key
@app.before_request
def check_api_key():
    if request.headers.get('X-API-Key') != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 401

# 📄 Endpoint para upload de arquivo local
@app.route('/extract-text', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']

    try:
        images = convert_from_bytes(file.read())
        text = ""
        for img in images:
            text += pytesseract.image_to_string(img, lang='por')
        return jsonify({'text': text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 🌐 Endpoint para envio de URL de imagem ou PDF
@app.route('/extract-text-from-url', methods=['POST'])
def extract_text_from_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing URL'}), 400

    try:
        response = requests.get(data['url'])
        if response.status_code != 200:
            return jsonify({'error': 'Failed to download file'}), 400

        content_type = response.headers.get('Content-Type', '')

        if 'application/pdf' in content_type:
            images = convert_from_bytes(response.content)
        elif 'image/' in content_type:
            image = Image.open(BytesIO(response.content))
            images = [image]
        else:
            return jsonify({'error': 'Unsupported file type'}), 400

        text = ""
        for img in images:
            text += pytesseract.image_to_string(img, lang='por')
        return jsonify({'text': text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
