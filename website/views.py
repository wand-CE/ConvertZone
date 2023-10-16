import os
from flask import Blueprint, render_template
from website.models.servicos_model import Service, Category

views = Blueprint('views', __name__)


@views.route('/')
def main():
    categories = Category.get_categories()
    return render_template('home.html', categories=categories)


@views.route('/service/<categoryName>/<serviceName>', methods=['GET'])
def service(categoryName, serviceName):
    categories = Category.get_categories()
    category = Category.query.filter_by(name=categoryName).first()
    service = Service.query.filter_by(name=serviceName).first()

    return render_template('services.html',
                           category=category,
                           service=service,
                           categories=categories,)
