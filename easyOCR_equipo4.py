### Autors:
### Sacnicté Cruz Arellano
### Ana Paula Guillen Maldonado
### Alejandro Harael García Sanchez
### Cesar Briones Martinez

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
import cv2
import easyocr
import fitz
from PIL import Image
import sys
import json
import datetime
import re
import spacy

app = Flask(__name__)

UPLOAD_FOLDER = '.'
ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
LOG_FILE = 'processed_files_log.json'
nlp = spacy.load("en_core_web_sm")  # Carga el modelo de spaCy

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def pdf2png(file_name):
    directory_path = "./Output_files/"
    base_name = os.path.splitext(os.path.basename(file_name))[0]
    generated_files = []

    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"Directory '{directory_path}' created successfully.")

    existing_files = [f for f in os.listdir(directory_path) if f.startswith(base_name) and f.endswith('.png')]
    if existing_files:
        generated_files = [os.path.join(directory_path, f) for f in existing_files]

    pdf_document = fitz.open(file_name)
    for page_number in range(pdf_document.page_count):
        page = pdf_document.load_page(page_number)
        img = page.get_pixmap(matrix=fitz.Matrix(600/300, 600/300))
        img_pillow = Image.frombytes("RGB", [img.width, img.height], img.samples)
        new_file_name = f"{directory_path}{base_name}_{page_number + 1}.png"
        if not os.path.exists(new_file_name):
            img_pillow.save(new_file_name, "PNG")
            generated_files.append(new_file_name)
            print(f"File '{new_file_name}' saved successfully.")
    pdf_document.close()
    return generated_files

class Reader():
    def __init__(self):
        languages = ['en', 'es', 'fr', 'de', 'it', 'pt']
        self.reader = easyocr.Reader(languages, model_storage_directory=os.path.join('models'), download_enabled=True)

    def read_img(self, img_path):
        img = cv2.imread(img_path)
        return img

    def extract_text(self, img):
        result = self.reader.readtext(img)
        extracted_text = []
        for text in filter(lambda x: x[-1] > .45, result):
            box, acc_text, confidence = text
            img = cv2.rectangle(img, [int(i) for i in box[0]], [int(i) for i in box[2]], (0, 255, 0), 2)
            extracted_text.append(acc_text)
        return extracted_text, img

def create_text(output_file_name, text):
    output_file_path = f"./Output_files/{output_file_name[:-4]}.txt"
    text_joined = ','.join(text)
    with open(output_file_path, 'w') as file2write:
        file2write.write(text_joined)
    print(f"Archivo txt para {output_file_name} generado con éxito")
    return text_joined

def log_processed_file(filename, extracted_text):
    log_entry = {
        'filename': filename,
        'timestamp': datetime.datetime.now().isoformat(),
        'extracted_text': extracted_text
    }
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as log_file:
            logs = json.load(log_file)
    else:
        logs = []

    logs.append(log_entry)
    with open(LOG_FILE, 'w') as log_file:
        json.dump(logs, log_file, indent=4)

def seccion_informacion(texto):
    secciones = {}
    current_section = None

    for linea in texto:
        doc = nlp(linea)
        if any([token.is_title for token in doc]):
            current_section = linea
            secciones[current_section] = []
        elif current_section:
            secciones[current_section].append(linea)
        else:
            secciones.setdefault('Uncategorized', []).append(linea)

    return secciones

@app.route('/archs', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No se ha proporcionado ningún archivo'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se ha seleccionado ningún archivo'})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        if filename.rsplit('.', 1)[1].lower() == 'pdf':
            generated_files = pdf2png(filepath)
        else:
            generated_files = [filepath]

        reader = Reader()
        extracted_text_all = []
        for generated_file in generated_files:
            img = reader.read_img(generated_file)
            extracted_text, _ = reader.extract_text(img)
            extracted_text_all.extend(extracted_text)

        output_text = create_text(filename, extracted_text_all)
        secciones = seccion_informacion(extracted_text_all)
        log_processed_file(filename, secciones)

        for generated_file in generated_files:
            if generated_file != filepath:
                os.remove(generated_file)
        os.remove(filepath)

        return jsonify({'texto_extraído': secciones})
    else:
        return jsonify({'error': 'Extensión de archivo no permitida'})

def main():
    if len(sys.argv) < 2:
        print("Uso: python archivo.py <input.pdf> [output.txt]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.pdf', '.txt')

    if input_file.rsplit('.', 1)[1].lower() == 'pdf':
        generated_files = pdf2png(input_file)
    else:
        generated_files = [input_file]

    reader = Reader()
    extracted_text_all = []
    for generated_file in generated_files:
        img = reader.read_img(generated_file)
        extracted_text, _ = reader.extract_text(img)
        extracted_text_all.extend(extracted_text)

    output_text = create_text(output_file, extracted_text_all)
    secciones = seccion_informacion(extracted_text_all)
    log_processed_file(input_file, secciones)
    print(json.dumps(secciones, indent=4))

if __name__ == '__main__':
    if 'flask' in sys.argv:
        app.run(debug=True)
    else:
        main()
