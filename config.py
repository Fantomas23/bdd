import os

basedir = os.path.abspath(os.path.dirname(__file__)) or os.environ.get('DATABASE_URL')


class Config(object):
    if os.environ.get('DATABASE_URL') is None:
        basedir = os.path.abspath(os.path.dirname(__file__))
        SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(basedir, 'app.db')
    else:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

    SQLALCHEMY_TRACK_MODIFICATIONS=False

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clef très très secrète'
    UPLOAD_FOLDER = r'.\appstagesn\uploads'
    MAX_CONTENT_PATH = 1024
    ALLOWED_EXTENSIONS = set(['csv'])
