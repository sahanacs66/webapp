from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from elasticsearch import Elasticsearch
from flask_pymongo import pymongo
from pymongo import MongoClient



app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

es = Elasticsearch([{'host':'localhost','port':9200}])
client = MongoClient('localhost',27017)

login = LoginManager(app)
login.login_view = 'login'

from app import routes,models
