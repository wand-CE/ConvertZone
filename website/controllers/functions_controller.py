import os
from flask import Blueprint, render_template, request, jsonify, session
from website.services.site_functions import *

http_requests = Blueprint('http_requests', __name__)


def download_files(request_function, function_name, accept_extension):
    files = []

    if request_function.method == 'POST':
        uploaded_files = request_function.files.getlist('files')
        for file in uploaded_files:
            extension = os.path.splitext(file.filename)[1]
            if extension in accept_extension and file.filename:
                path = os.path.join(
                    session['user_path_media'], function_name, 'result')
                if not os.path.exists(path):
                    os.makedirs(path)
                filepath = os.path.join(
                    session['user_path_media'], function_name, file.filename)
                file.save(filepath)
                files.append(filepath)
    return files


@http_requests.route('/word_equal_pdf', methods=['GET', 'POST'])
def word_equal_pdf():
    function_name = DocumentManipulations.word_equal_pdf.__name__
    pdf_word = download_files(request, function_name, ['.pdf', '.docx'])
    if len(pdf_word) == 1:
        path = os.path.join(
            session['user_path_media'], function_name, 'result')

        extension = os.path.splitext(pdf_word[0])[1]
        if extension == '.docx':
            DocumentManipulations.word_equal_pdf(
                pdf_word[0], 'word_to_pdf', path)
        elif extension == '.pdf':
            DocumentManipulations.word_equal_pdf(
                pdf_word[0], 'pdf_to_word', path)

    return render_template('home.html')


@http_requests.route('/merge_pdf', methods=['GET', 'POST'])
def merge_pdf():
    function_name = DocumentManipulations.merge_pdf.__name__
    pdfs = download_files(request, function_name, ['.pdf'])
    if pdfs:
        path = os.path.join(
            session['user_path_media'], function_name, 'result')
        DocumentManipulations.merge_pdf(pdfs, path)

    return render_template('home.html')


@http_requests.route('/extract_img_pdf', methods=['GET', 'POST'])
def extract_img_pdf():
    function_name = DocumentManipulations.extract_img_pdf.__name__
    pdf = download_files(request, function_name, ['.pdf'])
    if len(pdf) == 1:
        path = os.path.join(
            session['user_path_media'], function_name, 'result')
        DocumentManipulations.extract_img_pdf(pdf[0], path)

    return render_template('home.html')


@http_requests.route('/remove_background_photo', methods=['GET', 'POST'])
def remove_background_photo():
    function_name = MediaManipulations.remove_background_photo.__name__
    photo = download_files(request, function_name, ['.png', '.jpeg', '.gif'])
    if len(photo) == 1:
        path = os.path.join(
            session['user_path_media'], function_name, 'result')
        DocumentManipulations.merge_pdf(photo[0], path)

    return render_template('home.html')


@http_requests.route('/convert_to_png', methods=['GET', 'POST'])
def convert_to_png():
    function_name = DocumentManipulations.merge_pdf.__name__
    pdfs = download_files(request, function_name, '.pdf')
    if pdfs:
        path = os.path.join(
            session['user_path_media'], function_name, 'result')
        DocumentManipulations.merge_pdf(pdfs, path)

    return render_template('home.html')


@http_requests.route('/video_to_audio', methods=['GET', 'POST'])
def video_to_audio():
    function_name = DocumentManipulations.merge_pdf.__name__
    pdfs = download_files(request, function_name, '.pdf')
    if pdfs:
        path = os.path.join(
            session['user_path_media'], function_name, 'result')
        DocumentManipulations.merge_pdf(pdfs, path)

    return render_template('home.html')


@http_requests.route('/join_audios', methods=['GET', 'POST'])
def join_audios():
    function_name = DocumentManipulations.merge_pdf.__name__
    pdfs = download_files(request, function_name, '.pdf')
    if pdfs:
        path = os.path.join(
            session['user_path_media'], function_name, 'result')
        DocumentManipulations.merge_pdf(pdfs, path)

    return render_template('home.html')


@http_requests.route('/text_to_qrcode', methods=['GET', 'POST'])
def text_to_qrcode():
    function_name = TextToImage.text_to_qrcode.__name__
    if request.method == 'POST':
        text = request.form.get('text')
        path = os.path.join(
            session['user_path_media'], function_name, 'result')
        TextToImage.text_to_qrcode(text, path)

    return render_template('home.html')


@http_requests.route('/wordcloud', methods=['GET', 'POST'])
def wordcloud():
    function_name = TextToImage.wordcloud.__name__
    if request.method == 'POST':
        text = request.form.get('text')
        path = os.path.join(
            session['user_path_media'], function_name, 'result')
        TextToImage.wordcloud(text, path)

    return render_template('home.html')
