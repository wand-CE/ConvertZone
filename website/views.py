from flask import Blueprint, render_template
from website.models.servicos_model import Service, Category

views = Blueprint('views', __name__)


@views.route('/')
def main():
    categories = Category.get_categories()
    return render_template('home.html', categories=categories)
