import os
from uuid import uuid4
from flask import Blueprint, session, redirect, url_for, request, render_template, current_app
from website.services.site_functions import DocumentManipulations, MediaManipulations, TextToImage

auth = Blueprint('auth', __name__)


@auth.before_app_request
def ensure_user_id():
    if 'user_id' not in session:
        user_id = generate_unique_id()
        session['user_id'] = user_id

    path = os.path.join(
        current_app.config['MEDIA'], 'temp_users', session['user_id'])

    try:
        if not os.path.exists(path):
            os.mkdir(path)
            session['user_path_media'] = path
            create_functions_folders(path)
    except OSError as e:
        print(f"Erro ao criar diretório {path}: {e}")

    print(session['user_id'])


@auth.route('/set_session', methods=['GET', 'POST'])
def set_session():
    if request.method == 'POST':
        session['user_data'] = request.form['data']
        # Observe o prefixo '.' para rotas dentro deste Blueprint
        return redirect(url_for('.get_session'))
    return render_template('set_session.html')


@auth.route('/get_session')
def get_session():
    user_data = session.get('user_data', 'Not Set')
    return f'User Data: {user_data}'


def generate_unique_id():
    return str(uuid4())


def create_functions_folders(path):
    classes_to_check = [DocumentManipulations,
                        MediaManipulations, TextToImage]

    for cls in classes_to_check:
        for func_name, value in vars(cls).items():
            if isinstance(value, classmethod) and not func_name.startswith("__"):
                function_path = os.path.join(path, value.__name__, 'result')
                os.makedirs(function_path)
