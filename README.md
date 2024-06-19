Description:
A simple web app that converts images of text into PDF documents. Users can upload an image file (JPEG format), and the app will extract the text from the image,
create a PDF containing the extracted text, and provide a download link for the PDF.

link: https://img2txt2.azurewebsites.net/

Features:

    -Image Upload
    -Text Extraction using Azure's OCR service to extract text from the uploaded image.
    -Image Optimization: Automatically resize and adjust image quality if it exceeds size constraints.
    -PDF Creation.
    -File Download: Provide a link for users to download the generated PDF.

Technical Stack:

    Backend: Python, Flask
    Image Processing: PIL (Pillow)
    PDF Generation: FPDF
    OCR Service: Azure Cognitive Services
    Deployment: Azure App Services, GitHub
    CI/CD: GitHub Actions, GitHub Secrets
