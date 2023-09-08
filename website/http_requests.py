import os
from flask import Blueprint, render_template, request, current_app, session
from website.services.site_functions import *

http_requests = Blueprint('http_requests', __name__)


@http_requests.route('/', methods=['GET', 'POST'])
def merge_pdf():
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        pdfs = []
        function_name = DocumentManipulations.merge_pdf.__name__

        for file in uploaded_files:
            extension = os.path.splitext(file.filename)[1]
            if extension == '.pdf':
                if file.filename:
                    path = os.path.join(
                        session['user_path_media'], function_name)
                    if not os.path.exists(path):
                        os.mkdir(path)
                    filepath = os.path.join(
                        session['user_path_media'], function_name, file.filename)
                    file.save(filepath)
                    pdfs.append(filepath)
        if pdfs:
            path = os.path.join(
                session['user_path_media'], function_name, 'result')
            DocumentManipulations.merge_pdf(pdfs, path)

    return render_template('home.html')  # Nome do seu template HTML


@http_requests.route('/word_equal_pdf', methods=['GET', 'POST'])
def word_equal_pdf():
    return 'TRAVA'
    if request.method == 'POST':
        DocumentManipulations.word_equal_pdf()
    return 'oi'
