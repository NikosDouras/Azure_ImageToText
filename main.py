#main.py
from flask import Flask, request, render_template, send_file
import os, logging
from werkzeug.utils import secure_filename
from PIL import Image
from utilities import optimize_image, create_pdf, extract_text_from_image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.error("No file part in request")
        return "No file part"

    file = request.files['file']
    if file.filename == '':
        logger.error("No selected file")
        return "No selected file"

    try:
        file_content = file.read()
        content_length = len(file_content)

        image = Image.open(file)
        width, height = image.size
    except IOError:
        logger.error("Invalid image file")
        return "Invalid image file"

    file.seek(0)

    if file and file.filename.lower().endswith('.jpg'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        if (content_length > 4 * 1024 * 1024) or width <= 50 or height <= 50 or width >= 4200 or height >= 4200:
            optimized_filepath = os.path.join(app.config['UPLOAD_FOLDER'], f"optimized_{filename}")
            optimize_image(filepath, optimized_filepath)
            return process_file(optimized_filepath)
        else:
            return process_file(filepath)

    logger.error("Invalid file type")
    return "Invalid file type"





def process_file(filepath):
    text = extract_text_from_image(filepath)

    # Create PDF from extracted text
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{os.path.splitext(os.path.basename(filepath))[0]}.pdf")
    create_pdf(text, pdf_path)

    return send_file(pdf_path, as_attachment=True)




if __name__ == '__main__':
    app.run(debug=True)
