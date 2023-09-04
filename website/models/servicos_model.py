from website import db
from ..services.site_functions import TextToImage, MediaManipulations, DocumentManipulations

category_functions = db.Table('category_functions',
                              db.Column('service_id', db.Integer, db.ForeignKey(
                                  'services.id')),  # Updated to 'services.id'
                              db.Column('category_id', db.Integer, db.ForeignKey('category.id')))


class Service(db.Model):
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    function_name = db.Column(db.String, nullable=False)
    name_on_site = db.Column(db.String, nullable=False)

    def __init__(self, function_name, name_on_site, id=None):
        self.id = id
        self.function_name = function_name
        self.name_on_site = name_on_site

    def add_service(self):  # Renamed for clarity
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_services():
        return Service.query.all()

    @staticmethod
    def get_service(id):
        return Service.query.get(id)


class Category(db.Model):  # Added inheritance
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    name_on_site = db.Column(db.String, nullable=False)
    functions = db.relationship(
        'Service', backref='category', secondary=category_functions)  # Updated backref

    def __init__(self, name, name_on_site, id=None):
        self.id = id
        self.name = name
        self.name_on_site = name_on_site

    def add_category(self):  # Renamed for clarity
        db.session.add(self)
        db.session.commit()

    def add_service_to_category(self, service):
        if isinstance(service, Service):
            self.functions.append(service)
            db.session.commit()

    @staticmethod
    def get_categories():
        return Category.query.all()

    @staticmethod
    def get_category(id):
        return Category.query.get(id)


def insert_function_names():
    # Lista das classes a serem checadas
    classes_to_check = [DocumentManipulations,
                        MediaManipulations, TextToImage]

    for cls in classes_to_check:
        category = Category.query.filter_by(name=cls.__name__).first()
        if not category:
            category = Category(name=cls.__name__,
                                name_on_site=cls.class_name)
            category.add_category()

        for func_name, value in vars(cls).items():
            if not Service.query.filter_by(function_name=func_name).first():
                if isinstance(value, classmethod) and not func_name.startswith("__"):
                    service = Service(
                        function_name=func_name, name_on_site=cls.method_names.get(func_name, func_name))
                    service.add_service()
                    category.add_service_to_category(service)
