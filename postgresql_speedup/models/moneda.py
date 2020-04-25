from config import db

class Moneda (db.Model) :
    __table_args__ = {'schema':'public'}
    __tablename__ = 'tabla_moneda'
    id_moneda = db.Column(db.Integer, primary_key=True)
    iso_moneda = db.Column(db.String(3))
    descripcion_moneda = db.Column(db.String(50))
