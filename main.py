from flask import Flask, request, render_template, send_file
import os
from werkzeug.utils import secure_filename
import requests
from PIL import Image
from fpdf import FPDF

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Replace with your Azure endpoint and subscription key
endpoint = "https://nameocr1.cognitiveservices.azure.com/"
subscription_key = "17265e11e5ec4f4695c4f2fafa42182e"

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
    if file and file.filename.endswith('.jpg'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return process_file(filepath)
    return "Invalid file type"

def extract_text_from_image(image_path):
    with open(image_path, 'rb') as image_data:
        headers = {
            'Ocp-Apim-Subscription-Key': subscription_key,
            'Content-Type': 'application/octet-stream'
        }
        params = {
            'language': 'unk',
            'detectOrientation': 'true'
        }
        ocr_url = endpoint + "vision/v3.1/ocr"
        response = requests.post(ocr_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()
        analysis = response.json()

        # Extract the text from the response
        text = []
        for region in analysis['regions']:
            for line in region['lines']:
                line_text = ' '.join([word['text'] for word in line['words']])
                text.append(line_text)
        return '\n'.join(text)

def create_pdf(text, output_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)
    # Encode text as UTF-8
    text = text.encode('latin1', 'replace').decode('latin1')

    pdf.multi_cell(0, 10, text)
    pdf.output(output_path)

def process_file(filepath):
    # Extract text using OCR
    text = extract_text_from_image(filepath)

    # Create PDF from extracted text
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{os.path.splitext(os.path.basename(filepath))[0]}.pdf")
    create_pdf(text, pdf_path)

    # Send the PDF file as a response
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
