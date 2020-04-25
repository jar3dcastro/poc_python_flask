from config import db
from models.producto import Producto
from models.moneda import Moneda

class Venta (db.Model) :
    __table_args__ = {'schema':'public'}
    __tablename__ = 'tabla_ventas'
    id_producto = db.Column(db.Integer, primary_key=True)
    id_moneda = db.Column(db.Integer, primary_key=True)
    monto = db.Column(db.Float, primary_key=True)
    fecha = db.Column(db.DateTime, primary_key=True)
