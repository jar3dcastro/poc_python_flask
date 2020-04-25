from config import db

class Producto (db.Model) :
    __table_args__ = {'schema':'public'}
    __tablename__ = 'tabla_producto'
    id_producto = db.Column(db.Integer, primary_key=True)
    descripcion_producto = db.Column(db.String(50))
