from flask import Flask
from flask_pymongo import PyMongo

# general config
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://admin:x2DEvf6UTp3R3CF09Ue1-b3nchm4rk.$@34.94.202.184:27017/nosql-benchmarkdb?authSource=admin'
db = PyMongo(app)
