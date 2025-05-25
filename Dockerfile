FROM python:3.10-slim

# Instala dependências do sistema (tesseract + poppler-utils para pdf2image)
RUN apt-get update && apt-get install -y \
    python3-venv \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-por \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev \
    libwebp-dev \
  && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia arquivos do projeto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Define variável ambiente para tesseract (se precisar)
ENV TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata/

# Expõe porta
EXPOSE 5000

# Comando para rodar a API Flask (ajuste se usar outra framework)
CMD ["python", "app.py"]
