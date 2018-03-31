import os
from flask_sqlalchemy import SQLAlchemy

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-wont-guess-secret'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://sql9224742:yUGUhbHBeC@sql9.freemysqlhosting.net/sql9224742'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ELASTICSEARCH_HOST = "127.0.0.1:9200"
