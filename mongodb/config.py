from flask import Flask
from flask_pymongo import PyMongo

# general config
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://admin:x2DEvf6UTp3R3CF09Ue1-b3nchm4rk.$@35.236.64.17:27017/nosql-benchmarkdb?authSource=admin'
db = PyMongo(app)
