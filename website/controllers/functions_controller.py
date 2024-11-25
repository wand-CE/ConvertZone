import os
# url_for e redirect temporarios
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from website.services.site_functions import *
from PIL import Image

img_extensions = set(Image.registered_extensions().keys())

http_requests = Blueprint('http_requests', __name__)


def return_full_path(function_name):
    return os.path.join(session['user_path_media'], function_name, 'result')


def download_files(request_function, function_name, accept_extension):
    files = []

    if request_function.method == 'POST':
        uploaded_files = request_function.files.getlist('files')
        for file in uploaded_files:
            extension = os.path.splitext(file.filename)[1]
            if extension.lower() in accept_extension and file.filename:
                full_path = return_full_path(function_name)
                os.makedirs(full_path, exist_ok=True)

                filepath = os.path.join(session['user_path_media'], function_name, file.filename)
                file.save(filepath)
                files.append(filepath)
    return files


@http_requests.route('/download/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_from_directory(session['user_path_media'], filename, as_attachment=True)


@http_requests.route('/word_equal_pdf', methods=['GET', 'POST'])
def word_equal_pdf():
    function_name = DocumentManipulations.word_equal_pdf.__name__
    extension_list = ['.pdf', '.docx']
    pdf_word = download_files(request, function_name, extension_list)
    if len(pdf_word) == 1:
        output_path = return_full_path(function_name)

        extension = os.path.splitext(pdf_word[0])[1]
        if extension not in extension_list:
            return f'Tipo de extensão não suportada: {extension}', 500

        convert_to = 'word_to_pdf' if extension == '.docx' else 'pdf_to_word'

        file = DocumentManipulations.word_equal_pdf(pdf_word[0], convert_to, output_path)

        return jsonify({
            'path_file': f'word_equal_pdf/result/{file}',
            'file_name': file,
        })


@http_requests.route('/merge_pdf', methods=['GET', 'POST'])
def merge_pdf():
    function_name = DocumentManipulations.merge_pdf.__name__
    pdfs = download_files(request, function_name, ['.pdf'])
    if pdfs:
        output_path = return_full_path(function_name)
        file = DocumentManipulations.merge_pdf(pdfs, output_path)

        return jsonify({
            'path_file': f'merge_pdf/result/{file}',
            'file_name': file,
        })


@http_requests.route('/extract_img_pdf', methods=['GET', 'POST'])
def extract_img_pdf():
    function_name = DocumentManipulations.extract_img_pdf.__name__
    pdf = download_files(request, function_name, ['.pdf'])
    if len(pdf) == 1:
        output_path = return_full_path(function_name)
        file = DocumentManipulations.extract_img_pdf(pdf[0], output_path)
        return jsonify({
            'path_file': f'extract_img_pdf/result/{file}',
            'file_name': file,
        })

    return '', 500


@http_requests.route('/remove_background_photo', methods=['GET', 'POST'])
def remove_background_photo():
    function_name = MediaManipulations.remove_background_photo.__name__
    photo = download_files(request, function_name, img_extensions)

    if len(photo) == 1:
        output_path = return_full_path(function_name)
        file = MediaManipulations.remove_background_photo(photo[0], output_path)

        return jsonify({
            'path_file': f'remove_background_photo/result/{file}',
            'file_name': file,
        })

    return {'error': 'Arquivo inválido ou formato de extensão não suportado.'}


@http_requests.route('/convert_to_png', methods=['GET', 'POST'])
def convert_to_png():
    function_name = MediaManipulations.convert_to_png.__name__
    img = download_files(request, function_name, img_extensions)
    if len(img) == 1:
        output_path = return_full_path(function_name)
        file = MediaManipulations.convert_to_png(img[0], output_path)
        return jsonify({
            'path_file': f'convert_to_png/result/{file}',
            'file_name': file,
        })

    return '', 500


@http_requests.route('/video_to_audio', methods=['GET', 'POST'])
def video_to_audio():
    function_name = MediaManipulations.video_to_audio.__name__
    video = download_files(request, function_name, '.mp4')
    if len(video) == 1:
        output_path = return_full_path(function_name)
        file = MediaManipulations.video_to_audio(video[0], output_path)

        return jsonify({
            'path_file': f'video_to_audio/result/{file}',
            'file_name': file,
        })

    return '', 500


@http_requests.route('/join_audios', methods=['GET', 'POST'])
def join_audios():
    function_name = MediaManipulations.join_audios.__name__
    audios = download_files(request, function_name, '.mp3')
    if audios:
        output_path = return_full_path(function_name)
        file = MediaManipulations.join_audios(audios, output_path)
        return jsonify({
            'path_file': f'join_audios/result/{file}',
            'file_name': file,
        })

    return '', 500


@http_requests.route('/text_to_qrcode', methods=['GET', 'POST'])
def text_to_qrcode():
    function_name = TextToImage.text_to_qrcode.__name__
    if request.method == 'POST':
        text = request.form.get('text')
        output_path = return_full_path(function_name)
        file = TextToImage.text_to_qrcode(text, output_path)

        return jsonify({
            'path_file': f'text_to_qrcode/result/{file}',
            'file_name': file,
        })

    return '', 500


@http_requests.route('/wordcloud', methods=['GET', 'POST'])
def wordcloud():
    function_name = TextToImage.wordcloud.__name__
    if request.method == 'POST':
        text = request.form.get('text')
        output_path = return_full_path(function_name)
        file = TextToImage.wordcloud(text, output_path)

        return jsonify({
            'path_file': f'wordcloud/result/{file}',
            'file_name': file,
        })

    return '', 500
