from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# general config
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:4Hns7_1cf4z5eKJn9slArz.b3nchm4k1S.$@35.236.92.189:5432/sql-benchmarkdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
