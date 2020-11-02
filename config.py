import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

    #SECRET_KEY
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A-VERY-LONG-SECRET-KEY'

    # PUBLIC_KEY
    RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY') or 'A-VERY-LONG-PRIVATE_KEY'
    # PRIVATE_KEY
    RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY') or 'A-VERY-LONG-PRIVATE_KEY'

    # Database configuration
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:123456789@localhost:3306/flask'
    SQLALCHEMY_TRACK_MODIFICATIONS = False